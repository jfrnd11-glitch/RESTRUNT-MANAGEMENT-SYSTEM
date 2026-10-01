import json
import os
from datetime import datetime
from PROJECT.LOGS.error_hendal import error_handler

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

    except Exception as e:
        error_handler.log_exception("Billing", "load_orders", e)
        return []


def load_bills():
    if not os.path.exists(BILL_FILE):
        return []

    try:
        with open(BILL_FILE, "r") as file:
            return json.load(file)

    except Exception as e:
        error_handler.log_exception("Billing", "load_bills", e)
        return []


def save_bills(bills):
    try:
        os.makedirs(DATABASE_DIR, exist_ok=True)

        with open(BILL_FILE, "w") as file:
            json.dump(bills, file, indent=4)

    except Exception as e:
        error_handler.log_exception("Billing", "save_bills", e)
        print("Bill save karne me error aaya!")


def generate_bill_id(bills):
    if not bills:
        return "B001"

    number = int(bills[-1]["bill_id"][1:]) + 1
    return f"B{number:03d}"


def generate_bill():
    try:
        orders = load_orders()

        if not orders:
            print("\nNo orders found.")
            error_handler.log_warning("Billing", "generate_bill", "No orders found")
            return

        print("\n========== ORDERS ==========")

        for order in orders:
            print(
                f"{order['order_id']} | "
                f"{order['customer_name']} | "
                f"Table: {order.get('table_no', 'None')} | "
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

        if selected_order["status"].lower() == "cancelled":
            print("Cancelled order cannot be billed!")
            return

        bills = load_bills()

        for bill in bills:
            if bill.get("order_id", "").upper() == order_id:
                print("Bill already generated for this order!")
                return

        subtotal = sum(
            float(item.get("total", 0)) for item in selected_order.get("items", [])
        )

        if subtotal >= DISCOUNT_LIMIT:
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
            "subtotal": subtotal,
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

        save_bills(bills)

        print("\n========== BILL ==========")
        print("Bill ID:", bill["bill_id"])
        print("Order ID:", bill["order_id"])
        print("Customer:", bill["customer_name"])
        print("Table:", bill["table_no"])

        print("\nSubtotal:", f"₹{subtotal:.2f}")
        print("Discount:", f"₹{discount:.2f}")
        print("Tax:", f"₹{tax:.2f}")
        print("Grand Total:", f"₹{grand_total:.2f}")

        print("Payment Status:", bill["payment_status"])

        print("\nBill generated successfully!")

        error_handler.log_info(
            "Billing",
            "generate_bill",
            f"Bill generated successfully: {bill['bill_id']}",
        )

    except Exception as e:
        error_handler.log_exception("Billing", "generate_bill", e)

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

        error_handler.log_info(
            "Billing", "view_bills", f"{len(bills)} bill(s) displayed"
        )

    except Exception as e:
        error_handler.log_exception("Billing", "view_bills", e)

        print("Bills dekhne me error aaya!")


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

        bill_id = input("\nEnter Bill ID: ").strip().upper()

        selected_bill = None

        for bill in bills:
            if bill.get("bill_id", "").upper() == bill_id:
                selected_bill = bill
                break

        if selected_bill is None:
            print("Invalid Bill ID!")
            return

        if selected_bill.get("payment_status", "Unpaid") == "Paid":
            print("Bill is already paid!")
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

                selected_bill["payment_status"] = "Paid"
                selected_bill["payment_method"] = "Cash"
                selected_bill["payment_number"] = "Not Required"

            elif method == "2":

                upi = input("Enter UPI ID: ").strip()

                if not upi:
                    print("UPI ID cannot be empty!")
                    return

                selected_bill["payment_status"] = "Paid"
                selected_bill["payment_method"] = "UPI"
                selected_bill["payment_number"] = upi

            elif method == "3":

                card = input("Enter 16 digit Card Number: ").replace(" ", "")

                if not card.isdigit() or len(card) != 16:
                    print("Card number must be exactly 16 digits!")
                    return

                selected_bill["payment_status"] = "Paid"
                selected_bill["payment_method"] = "Card"
                selected_bill["payment_number"] = "**** **** **** " + card[-4:]

            else:
                print("Invalid payment method!")
                return

        elif choice == "2":

            selected_bill["payment_status"] = "Unpaid"
            selected_bill["payment_method"] = "Not Selected"
            selected_bill["payment_number"] = "Not Available"

        else:
            print("Invalid choice!")
            return

        save_bills(bills)

        print("\nPayment updated successfully!")

        error_handler.log_info(
            "Billing", "update_payment", f"Payment updated for Bill: {bill_id}"
        )

    except Exception as e:
        error_handler.log_exception("Billing", "update_payment", e)

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

            error_handler.log_info(
                "Billing", "billing_menu", "Billing Management closed"
            )

            print("Billing Management closed.")
            break

        else:
            print("Invalid choice!")
