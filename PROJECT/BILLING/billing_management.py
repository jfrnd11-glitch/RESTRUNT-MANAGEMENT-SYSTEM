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


def log_error(function_name, message):
    try:
        error_handler.log_error("Billing", function_name, message)
    except Exception:
        pass


def log_warning(function_name, message):
    try:
        error_handler.log_warning("Billing", function_name, message)
    except Exception:
        pass


def log_exception(function_name, exception):
    try:
        error_handler.log_exception("Billing", function_name, exception)
    except Exception:
        pass


def load_orders():

    if not os.path.exists(ORDER_FILE):
        return []

    try:
        with open(ORDER_FILE, "r") as file:
            return json.load(file)

    except json.JSONDecodeError as e:
        log_exception("load_orders", e)
        return []

    except Exception as e:
        log_exception("load_orders", e)
        return []


def load_bills():

    if not os.path.exists(BILL_FILE):
        return []

    try:
        with open(BILL_FILE, "r") as file:
            return json.load(file)

    except json.JSONDecodeError as e:
        log_exception("load_bills", e)
        return []

    except Exception as e:
        log_exception("load_bills", e)
        return []


def save_bills(bills):

    try:
        os.makedirs(DATABASE_DIR, exist_ok=True)

        with open(BILL_FILE, "w") as file:
            json.dump(bills, file, indent=4)

        return True

    except Exception as e:
        log_exception("save_bills", e)
        print("Bill save karne me error aaya!")
        return False


def generate_bill_id(bills):

    if not bills:
        return "B001"

    highest_number = 0

    for bill in bills:

        bill_id = bill.get("bill_id", "")

        if re.fullmatch(r"B\d+", bill_id):

            number = int(bill_id[1:])

            if number > highest_number:
                highest_number = number

    return f"B{highest_number + 1:03d}"


def get_order_id():

    while True:

        order_id = input("\nEnter Order ID: ").strip().upper()

        if not order_id:

            print("Order ID cannot be empty.")

            log_error("get_order_id", "Order ID cannot be empty.")

            continue

        if not re.fullmatch(r"O\d{3}", order_id):

            print("Invalid Order ID! Example: O001")

            log_error("get_order_id", f"Invalid Order ID format: {order_id}")

            continue

        return order_id


def generate_bill():

    try:

        orders = load_orders()

        if not orders:

            print("\nNo orders found.")

            log_warning("generate_bill", "No orders found.")

            return

        print("\n========== ORDERS ==========")

        for order in orders:

            print(
                f"{order.get('order_id', 'N/A')} | "
                f"{order.get('customer_name', 'N/A')} | "
                f"Table: {order.get('table_no', 'None')} | "
                f"Status: {order.get('status', 'N/A')}"
            )

        order_id = get_order_id()

        selected_order = None

        for order in orders:

            if order.get("order_id", "").upper() == order_id:

                selected_order = order
                break

        if selected_order is None:

            print("Invalid Order ID!")

            log_error("generate_bill", f"Order ID not found: {order_id}")

            return

        if selected_order.get("status", "").lower() == "cancelled":

            print("Cancelled order cannot be billed!")

            log_error("generate_bill", f"Cancelled order cannot be billed: {order_id}")

            return

        bills = load_bills()

        for bill in bills:

            if bill.get("order_id", "").upper() == order_id:

                print("Bill already generated for this order!")

                log_error("generate_bill", f"Bill already exists for order: {order_id}")

                return

        items = selected_order.get("items", [])

        if not items:

            print("Order me koi item nahi hai!")

            log_error("generate_bill", f"No items found in order: {order_id}")

            return

        try:

            subtotal = sum(float(item.get("total", 0)) for item in items)

        except (TypeError, ValueError) as e:

            print("Order item total invalid hai!")

            log_exception("generate_bill", e)

            return

        if subtotal <= 0:

            print("Invalid subtotal!")

            log_error("generate_bill", f"Invalid subtotal for order: {order_id}")

            return

        # Discount only when subtotal is greater than 1000
        if subtotal > DISCOUNT_LIMIT:

            discount_rate = DISCOUNT_RATE

        else:

            discount_rate = 0

        discount = subtotal * discount_rate / 100

        after_discount = subtotal - discount

        tax = after_discount * TAX_RATE / 100

        grand_total = after_discount + tax

        current_datetime = datetime.now()

        bill = {
            "bill_id": generate_bill_id(bills),
            "order_id": selected_order["order_id"],
            "customer_name": selected_order["customer_name"],
            "table_no": selected_order.get("table_no", "None"),
            "date": current_datetime.strftime("%Y-%m-%d"),
            "time": current_datetime.strftime("%H:%M:%S"),
            "items": selected_order.get("items", []),
            "subtotal": round(subtotal, 2),
            "discount_rate": discount_rate,
            "discount": round(discount, 2),
            "tax_rate": TAX_RATE,
            "tax": round(tax, 2),
            "grand_total": round(grand_total, 2),
            "payment_status": "Unpaid",
            "payment_method": "Not Selected",
            "payment_number": "Not Available",
        }

        bills.append(bill)

        if not save_bills(bills):

            bills.pop()
            return

        print("\n========== BILL ==========")

        print("Bill ID:", bill["bill_id"])
        print("Order ID:", bill["order_id"])
        print("Customer:", bill["customer_name"])
        print("Table:", bill["table_no"])
        print("Date:", bill["date"])
        print("Time:", bill["time"])

        print("\nSubtotal:", f"₹{subtotal:.2f}")
        print(f"Discount ({discount_rate}%):", f"₹{discount:.2f}")
        print(f"Tax ({TAX_RATE}%):", f"₹{tax:.2f}")
        print("Grand Total:", f"₹{grand_total:.2f}")

        print("Payment Status:", bill["payment_status"])

        print("\nBill generated successfully!")

    except Exception as e:

        log_exception("generate_bill", e)

        print("Bill generate karte waqt error aaya!")


def view_bills():

    try:

        bills = load_bills()

        if not bills:

            print("\nNo bills found.")
            return

        print("\n========== ALL BILLS ==========")

        for bill in bills:

            print("\n------------------------------")

            print("Bill ID:", bill.get("bill_id", "N/A"))

            print("Order ID:", bill.get("order_id", "N/A"))

            print("Customer:", bill.get("customer_name", "N/A"))

            print("Table:", bill.get("table_no", "None"))

            print("Date:", bill.get("date", "N/A"))

            print("Time:", bill.get("time", "N/A"))

            print("Subtotal:", f"₹{float(bill.get('subtotal', 0)):.2f}")

            print("Discount:", f"₹{float(bill.get('discount', 0)):.2f}")

            print("Tax:", f"₹{float(bill.get('tax', 0)):.2f}")

            print("Grand Total:", f"₹{float(bill.get('grand_total', 0)):.2f}")

            print("Payment Status:", bill.get("payment_status", "Unpaid"))

            print("Payment Method:", bill.get("payment_method", "Not Selected"))

            print("Payment Number:", bill.get("payment_number", "Not Available"))

    except Exception as e:

        log_exception("view_bills", e)

        print("Bills dekhne me error aaya!")

def get_bill_id():

    while True:

        bill_id = input("\nEnter Bill ID: ").strip().upper()

        if not bill_id:

            print("Bill ID cannot be empty.")

            log_error("get_bill_id", "Bill ID cannot be empty.")

            continue

        if not re.fullmatch(r"B\d{3}", bill_id):

            print("Invalid Bill ID! Example: B001")

            log_error("get_bill_id", f"Invalid Bill ID format: {bill_id}")

            continue

        return bill_id


def validate_upi():

    while True:

        upi = input("Enter UPI ID: ").strip()

        if not upi:

            print("UPI ID cannot be empty!")

            log_error("validate_upi", "UPI ID cannot be empty.")

            continue

        if " " in upi:

            print("UPI ID cannot contain spaces!")

            log_error("validate_upi", f"UPI ID contains spaces: {upi}")

            continue

        if upi.count("@") != 1:

            print("Invalid UPI ID! " "Example: name@upi")

            log_error("validate_upi", f"Invalid UPI ID format: {upi}")

            continue

        username, provider = upi.split("@")

        if not username or not provider:

            print("Invalid UPI ID! " "Example: name@upi")

            log_error("validate_upi", f"Invalid UPI ID: {upi}")

            continue

        if not re.fullmatch(r"[A-Za-z0-9._-]+", username):

            print("Invalid UPI username!")

            log_error("validate_upi", f"Invalid UPI username: {upi}")

            continue

        if not re.fullmatch(r"[A-Za-z0-9.-]+", provider):

            print("Invalid UPI provider!")

            log_error("validate_upi", f"Invalid UPI provider: {upi}")

            continue

        return upi


def validate_card():

    while True:

        card = input("Enter 16 digit Card Number: ").strip()

        card = card.replace(" ", "")

        if not card.isdigit():

            print("Card number must contain only digits!")

            log_error("validate_card", "Card number contains non-digit characters.")

            continue

        if len(card) != 16:

            print("Card number must be exactly 16 digits!")

            log_error("validate_card", "Invalid card number length.")

            continue

        break

    while True:

        cvv = input("Enter CVV: ").strip()

        if not cvv.isdigit():

            print("CVV must contain only digits!")

            log_error("validate_card", "CVV contains non-digit characters.")

            continue
        if len(cvv) not in (3, 4):

            print("CVV must be 3 or 4 digits!")

            log_error("validate_card", "Invalid CVV length.")
            continue
        break

    return "**** **** **** " + card[-4:]

def update_payment():
    try:
        bills = load_bills()
        if not bills:

            print("\nNo bills found.")
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

        selected_bill = None

        for bill in bills:
            if bill.get("bill_id", "").upper() == bill_id:
                selected_bill = bill
                break

        if selected_bill is None:
            print("Invalid Bill ID!")
            log_error("update_payment", f"Bill ID not found: {bill_id}")

            return

        if selected_bill.get("payment_status", "Unpaid") == "Paid":

            print("Bill is already paid!")
            log_error("update_payment", f"Bill already paid: {bill_id}")

            return

        print("\n1. Paid")
        print("2. Unpaid")

        while True:

            choice = input("Enter choice: ").strip()
            if choice in ("1", "2"):
                break

            print("Invalid choice! Select 1 or 2.")
            log_error("update_payment", f"Invalid payment status choice: {choice}")

        if choice == "1":
            print("\n1. Cash")
            print("2. UPI")
            print("3. Card")

            while True:
                method = input("Enter payment method: ").strip()

                if method in ("1", "2", "3"):
                    break

                print("Invalid payment method! " "Select 1, 2 or 3.")
                log_error("update_payment", f"Invalid payment method: {method}")

            if method == "1":
                selected_bill["payment_status"] = "Paid"
                selected_bill["payment_method"] = "Cash"
                selected_bill["payment_number"] = "Not Required"

            elif method == "2":

                upi = validate_upi()
                selected_bill["payment_status"] = "Paid"
                selected_bill["payment_method"] = "UPI"
                selected_bill["payment_number"] = upi

            elif method == "3":

                card = validate_card()
                selected_bill["payment_status"] = "Paid"
                selected_bill["payment_method"] = "Card"
                selected_bill["payment_number"] = card

        elif choice == "2":

            selected_bill["payment_status"] = "Unpaid"
            selected_bill["payment_method"] = "Not Selected"
            selected_bill["payment_number"] = "Not Available"

        if not save_bills(bills):
            return

        print("\nPayment updated successfully!")
        print("Bill ID:", selected_bill["bill_id"])
        print("Payment Status:", selected_bill["payment_status"])
        print("Payment Method:", selected_bill["payment_method"])

    except Exception as e:
        log_exception("update_payment", e)
        print("Payment update karte waqt error aaya!")

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
            print("Invalid choice!")
            log_error("billing_menu", f"Invalid menu choice: {choice}")