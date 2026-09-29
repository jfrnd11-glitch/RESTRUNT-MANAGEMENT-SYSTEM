import json
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_DIR = os.path.join(BASE_DIR, "DATABASE")

ORDER_FILE = os.path.join(DATABASE_DIR, "orders.json")
BILL_FILE = os.path.join(DATABASE_DIR, "bills.json")

TAX_RATE = 5
DISCOUNT_LIMIT = 1000
DISCOUNT_RATE = 10


def load_orders():
    if not os.path.exists(ORDER_FILE):
        return []

    try:
        with open(ORDER_FILE, "r") as file:
            return json.load(file)

    except (FileNotFoundError, json.JSONDecodeError):
        return []


def load_bills():
    if not os.path.exists(BILL_FILE):
        return []

    try:
        with open(BILL_FILE, "r") as file:
            return json.load(file)

    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_bills(bills):
    with open(BILL_FILE, "w") as file:
        json.dump(bills, file, indent=4)


def generate_bill_id(bills):
    if not bills:
        return "B001"

    last_id = bills[-1]["bill_id"]
    number = int(last_id[1:]) + 1

    return f"B{number:03d}"


def generate_bill():
    orders = load_orders()

    if not orders:
        print("\nNo orders found.")
        return

    print("\n========== ORDERS ==========")

    for order in orders:
        print(
            f"{order['order_id']} | "
            f"{order['customer_name']} | "
            f"Table: {order['table_no']} | "
            f"Status: {order['status']}"
        )

    order_id = input("\nEnter Order ID: ").strip().upper()

    selected_order = None

    for order in orders:
        if order["order_id"].upper() == order_id:
            selected_order = order
            break

    if selected_order is None:
        print("Invalid Order ID!")
        return

    if selected_order["status"] == "Cancelled":
        print("Cancelled order cannot be billed!")
        return

    bills = load_bills()

    for bill in bills:
        if bill["order_id"] == selected_order["order_id"]:
            print("Bill already generated for this order!")
            return

    subtotal = 0

    for item in selected_order["items"]:
        subtotal += item["total"]

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
        "table_no": selected_order["table_no"],
        "date": current_datetime.strftime("%Y-%m-%d"),
        "time": current_datetime.strftime("%H:%M:%S"),
        "items": selected_order["items"],
        "subtotal": subtotal,
        "discount_rate": discount_rate,
        "discount": discount,
        "tax_rate": TAX_RATE,
        "tax": tax,
        "grand_total": grand_total,
        "payment_status": "Unpaid",
    }

    bills.append(bill)
    save_bills(bills)

    print("\n========================================")
    print("              FINAL BILL")
    print("========================================")

    print("Bill ID      :", bill["bill_id"])
    print("Order ID     :", bill["order_id"])
    print("Date         :", bill["date"])
    print("Time         :", bill["time"])
    print("Customer     :", bill["customer_name"])
    print("Table Number :", bill["table_no"])

    print("----------------------------------------")

    for item in bill["items"]:
        print(f"{item['name']} x {item['quantity']} = ₹{item['total']:.2f}")

    print("----------------------------------------")

    print(f"Subtotal     : ₹{bill['subtotal']:.2f}")
    print(f"Discount ({bill['discount_rate']}%) : " f"-₹{bill['discount']:.2f}")
    print(f"Tax ({bill['tax_rate']}%)     : " f"₹{bill['tax']:.2f}")

    print("----------------------------------------")

    print(f"Grand Total  : ₹{bill['grand_total']:.2f}")
    print("Payment      :", bill["payment_status"])

    print("========================================")
    print("          BILL GENERATED SUCCESSFULLY")
    print("========================================")


def view_bills():
    bills = load_bills()

    if not bills:
        print("\nNo bills found.")
        return

    print("\n========== ALL BILLS ==========")

    for bill in bills:
        print()
        print("Bill ID      :", bill["bill_id"])
        print("Order ID     :", bill["order_id"])
        print("Date         :", bill.get("date", "N/A"))
        print("Time         :", bill.get("time", "N/A"))
        print("Customer     :", bill["customer_name"])
        print("Table Number :", bill["table_no"])
        print("Subtotal     :", f"₹{bill['subtotal']:.2f}")
        print("Discount     :", f"₹{bill['discount']:.2f}")
        print("Tax          :", f"₹{bill['tax']:.2f}")
        print("Grand Total  :", f"₹{bill['grand_total']:.2f}")
        print("Payment      :", bill["payment_status"])
        print("--------------------------------")


def update_payment():
    bills = load_bills()

    if not bills:
        print("\nNo bills found.")
        return

    print("\n========== BILLS ==========")

    for bill in bills:
        print(
            f"{bill['bill_id']} | "
            f"Order: {bill['order_id']} | "
            f"Amount: ₹{bill['grand_total']:.2f} | "
            f"Payment: {bill['payment_status']}"
        )

    bill_id = input("\nEnter Bill ID: ").strip().upper()

    selected_bill = None

    for bill in bills:
        if bill["bill_id"].upper() == bill_id:
            selected_bill = bill
            break

    if selected_bill is None:
        print("Invalid Bill ID!")
        return

    if selected_bill["payment_status"] == "Paid":
        print("Bill is already paid!")
        return

    print("\n1. Paid")
    print("2. Unpaid")

    choice = input("Enter your choice: ").strip()

    if choice == "1":
        selected_bill["payment_status"] = "Paid"

    elif choice == "2":
        selected_bill["payment_status"] = "Unpaid"

    else:
        print("Invalid choice!")
        return

    save_bills(bills)

    print("\nPayment status updated successfully!")
    print("Bill ID :", selected_bill["bill_id"])
    print("Payment :", selected_bill["payment_status"])


def billing_menu():
    while True:

        print("\n========== BILLING MANAGEMENT ==========")

        print("1. Generate Bill")
        print("2. View Bills")
        print("3. Update Payment")
        print("4. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":

            generate_bill()

        elif choice == "2":

            view_bills()

        elif choice == "3":

            update_payment()

        elif choice == "4":

            print("Exit Billing Management.")
            break

        else:

            print("Invalid choice!")
