import json
import os
import re
from datetime import datetime
from PROJECT.LOGS.error_hendal import error_handler

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_DIR = os.path.join(BASE_DIR, "DATABASE")
ORDER_FILE = os.path.join(DATABASE_DIR, "orders.json")
BILL_FILE = os.path.join(DATABASE_DIR, "bills.json")

TAX_RATE = 5
DISCOUNT_LIMIT = 1000
DISCOUNT_RATE = 10

def log_error(function_name, message, level="ERROR"):
    try:
        if level == "WARNING":
            error_handler.log_warning("Billing", function_name, message)
        else:
            error_handler.log_error("Billing", function_name, message)
    except Exception:
        pass

def load_data(file_name):
    if not os.path.exists(file_name):
        return []
    try:
        with open(file_name, "r") as file:
            data = json.load(file)
            return data if isinstance(data, list) else []
    except Exception as e:
        log_error("load_data", str(e))
        return []

def save_bills(bills):
    try:
        os.makedirs(DATABASE_DIR, exist_ok=True)
        with open(BILL_FILE, "w") as file:
            json.dump(bills, file, indent=4)
        return True
    except Exception as e:
        log_error("save_bills", str(e))
        print("Bill save karne me error aaya!")
        return False

def generate_bill_id(bills):
    numbers = [
        int(bill["bill_id"][1:])
        for bill in bills
        if re.fullmatch(r"B\d+", bill.get("bill_id", ""))
    ]
    return f"B{max(numbers, default=0) + 1:03d}"


def get_order_id():
    while True:
        order_id = input("Enter Order ID: ").strip().upper()
        if re.fullmatch(r"O\d{3}", order_id):
            return order_id
        print("Invalid Order ID! Example: O001")
        log_error("get_order_id", f"Invalid Order ID: {order_id}", "WARNING")


def get_customer_name():
    while True:
        name = input("Enter Customer Name: ").strip()
        if len(name) >= 3 and all(char.isalpha() or char == " " for char in name):
            return name.title()
        print("Name must contain at least 3 letters.")
        log_error("get_customer_name", f"Invalid name: {name}", "WARNING")


def get_mobile():
    while True:
        mobile = input("Enter Mobile Number: ").strip()
        if re.fullmatch(r"[6-9]\d{9}", mobile):
            return mobile
        print("Enter a valid 10-digit mobile number.")
        log_error("get_mobile", f"Invalid mobile: {mobile}", "WARNING")


def generate_bill():
    orders = load_data(ORDER_FILE)
    bills = load_data(BILL_FILE)

    if not orders:
        print("No orders found.")
        log_error("generate_bill", "No orders found.", "WARNING")
        return

    print("\n========== ORDERS ==========")
    for order in orders:
        print(
            f"{order.get('order_id', 'N/A')} | "
            f"Table: {order.get('table_no') or 'None'} | "
            f"Status: {order.get('status', 'N/A')}"
        )

    order_id = get_order_id()
    order = next((o for o in orders if o.get("order_id", "").upper() == order_id), None)

    if order is None:
        print("Order ID not found.")
        log_error("generate_bill", f"Order not found: {order_id}", "WARNING")
        return

    if order.get("status", "").lower() == "cancelled":
        print("Cancelled order cannot be billed.")
        log_error("generate_bill", f"Cancelled order: {order_id}", "WARNING")
        return

    if any(b.get("order_id", "").upper() == order_id for b in bills):
        print("Bill already generated for this order.")
        log_error("generate_bill", f"Duplicate bill: {order_id}", "WARNING")
        return

    items = order.get("items", [])
    if not items:
        print("Order has no items.")
        log_error("generate_bill", f"No items in order: {order_id}", "WARNING")
        return

    try:
        subtotal = sum(float(item["total"]) for item in items)
        if subtotal <= 0:
            raise ValueError("Subtotal must be greater than zero.")
    except (KeyError, TypeError, ValueError) as e:
        print("Invalid order item total.")
        log_error("generate_bill", str(e))
        return

    customer_name = get_customer_name()
    mobile = get_mobile()

    discount_rate = DISCOUNT_RATE if subtotal > DISCOUNT_LIMIT else 0
    discount = round(subtotal * discount_rate / 100, 2)
    after_discount = subtotal - discount
    tax = round(after_discount * TAX_RATE / 100, 2)
    grand_total = round(after_discount + tax, 2)
    now = datetime.now()

    bill = {
        "bill_id": generate_bill_id(bills),
        "order_id": order["order_id"],
        "customer_name": customer_name,
        "mobile": mobile,
        "table_no": order.get("table_no"),
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M:%S"),
        "items": items,
        "subtotal": round(subtotal, 2),
        "discount_rate": discount_rate,
        "discount": discount,
        "tax_rate": TAX_RATE,
        "tax": tax,
        "grand_total": grand_total,
        "payment_status": "Unpaid",
        "payment_method": "Not Selected",
        "payment_number": "Not Available",
    }

    bills.append(bill)
    if not save_bills(bills):
        return

    print("\n========== BILL ==========")
    print("Bill ID:", bill["bill_id"])
    print("Order ID:", bill["order_id"])
    print("Customer:", customer_name)
    print("Mobile:", mobile)
    print("Table:", bill["table_no"] or "None")
    print("Date:", bill["date"])
    print("Time:", bill["time"])
    print("\nItems:")
    print(f"{'Item':22} {'Qty':5} {'Price':10} {'Total':10}")
    print("-" * 50)

    for item in items:
        name = item.get("name", item.get("item_name", "Unknown"))
        quantity = int(item.get("quantity", item.get("qty", 1)))
        price = float(item.get("price", 0))
        total = float(item.get("total", price * quantity))
        print(f"{name:22} {quantity:<5} ₹{price:<9.2f} ₹{total:.2f}")

    print("-" * 50)
    print(f"Subtotal: ₹{subtotal:.2f}")
    print(f"Discount ({discount_rate}%): ₹{discount:.2f}")
    print(f"Tax ({TAX_RATE}%): ₹{tax:.2f}")
    print(f"Grand Total: ₹{grand_total:.2f}")
    print("Payment Status: Unpaid")
    print("Bill generated successfully!")


def view_bills():
    bills = load_data(BILL_FILE)
    if not bills:
        print("No bills found.")
        return

    print("\n========== ALL BILLS ==========")
    for bill in bills:
        print("\n------------------------------")
        print("Bill ID:", bill.get("bill_id", "N/A"))
        print("Order ID:", bill.get("order_id", "N/A"))
        print("Customer:", bill.get("customer_name", "N/A"))
        print("Mobile:", bill.get("mobile", "N/A"))
        print("Table:", bill.get("table_no") or "None")
        print("Date:", bill.get("date", "N/A"))
        print("Time:", bill.get("time", "N/A"))
        print("\nItems:")

        for item in bill.get("items", []):
            name = item.get("name", item.get("item_name", "Unknown"))
            qty = item.get("quantity", item.get("qty", 1))
            price = float(item.get("price", 0))
            total = float(item.get("total", price * int(qty)))
            print(f"{name} x {qty} | ₹{price:.2f} | ₹{total:.2f}")

        print(f"Subtotal: ₹{float(bill.get('subtotal', 0)):.2f}")
        print(f"Discount: ₹{float(bill.get('discount', 0)):.2f}")
        print(f"Tax: ₹{float(bill.get('tax', 0)):.2f}")
        print(f"Grand Total: ₹{float(bill.get('grand_total', 0)):.2f}")
        print("Payment Status:", bill.get("payment_status", "Unpaid"))
        print("Payment Method:", bill.get("payment_method", "Not Selected"))
        print("Payment Number:", bill.get("payment_number", "Not Available"))


def get_bill_id():
    while True:
        bill_id = input("Enter Bill ID: ").strip().upper()
        if re.fullmatch(r"B\d{3,}", bill_id):
            return bill_id
        print("Invalid Bill ID! Example: B001")
        log_error("get_bill_id", f"Invalid Bill ID: {bill_id}", "WARNING")


def validate_upi():
    while True:
        upi = input("Enter UPI ID: ").strip()
        if re.fullmatch(r"[A-Za-z0-9._-]+@[A-Za-z0-9.-]+", upi):
            return upi
        print("Invalid UPI ID! Example: name@upi")
        log_error("validate_upi", f"Invalid UPI: {upi}", "WARNING")


def validate_card():
    while True:
        card = input("Enter 16 digit Card Number: ").strip().replace(" ", "")
        if card.isdigit() and len(card) == 16:
            break
        print("Card number must contain exactly 16 digits.")
        log_error("validate_card", "Invalid card number.", "WARNING")

    while True:
        cvv = input("Enter CVV: ").strip()
        if cvv.isdigit() and len(cvv) in (3, 4):
            break
        print("CVV must contain 3 or 4 digits.")
        log_error("validate_card", "Invalid CVV.", "WARNING")

    return "**** **** **** " + card[-4:]


def update_payment():
    bills = load_data(BILL_FILE)
    if not bills:
        print("No bills found.")
        return

    print("\n========== BILLS ==========")
    for bill in bills:
        print(
            f"{bill.get('bill_id', 'N/A')} | "
            f"{bill.get('customer_name', 'N/A')} | "
            f"₹{float(bill.get('grand_total', 0)):.2f} | "
            f"{bill.get('payment_status', 'Unpaid')}"
        )

    bill_id = get_bill_id()
    bill = next((b for b in bills if b.get("bill_id", "").upper() == bill_id), None)

    if bill is None:
        print("Bill ID not found.")
        log_error("update_payment", f"Bill not found: {bill_id}", "WARNING")
        return

    if bill.get("payment_status") == "Paid":
        print("Bill is already paid.")
        return

    print("\n1. Paid")
    print("2. Unpaid")
    choice = input("Enter choice: ").strip()

    if choice == "1":
        print("\n1. Cash")
        print("2. UPI")
        print("3. Card")
        method = input("Enter payment method: ").strip()

        if method == "1":
            payment_method = "Cash"
            payment_number = "Not Required"
        elif method == "2":
            payment_method = "UPI"
            payment_number = validate_upi()
        elif method == "3":
            payment_method = "Card"
            payment_number = validate_card()
        else:
            print("Invalid payment method.")
            log_error("update_payment", f"Invalid method: {method}", "WARNING")
            return

        bill["payment_status"] = "Paid"
        bill["payment_method"] = payment_method
        bill["payment_number"] = payment_number

    elif choice == "2":
        bill["payment_status"] = "Unpaid"
        bill["payment_method"] = "Not Selected"
        bill["payment_number"] = "Not Available"
    else:
        print("Invalid choice.")
        log_error("update_payment", f"Invalid status choice: {choice}", "WARNING")
        return

    if save_bills(bills):
        print("Payment updated successfully!")
        print("Bill ID:", bill["bill_id"])
        print("Payment Status:", bill["payment_status"])
        print("Payment Method:", bill["payment_method"])


def billing_menu():
    while True:
        print("\n========== BILLING MANAGEMENT ==========")
        print("1. Generate Bill")
        print("2. View Bills")
        print("3. Update Payment")
        print("4. Exit")
        choice = input("Enter choice: ").strip()

        if choice == "1":
            generate_bill()
        elif choice == "2":
            view_bills()
        elif choice == "3":
            update_payment()
        elif choice == "4":
            print("Billing Management closed.")
            break
        else:
            print("Invalid choice.")
            log_error("billing_menu", f"Invalid choice: {choice}", "WARNING")