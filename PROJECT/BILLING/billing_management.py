import json
import os
import re
from datetime import datetime

from PROJECT.LOGS.error_hendal import error_handler

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_DIR = os.path.join(BASE_DIR, "DATABASE")
ORDER_FILE = os.path.join(DATABASE_DIR, "orders.json")
BILL_FILE = os.path.join(DATABASE_DIR, "bills.json")


class BillingManagement:

    TAX_RATE = 5
    DISCOUNT_LIMIT = 1000
    DISCOUNT_RATE = 10

    def log_error(self, function, message, level="ERROR"):
        if level == "WARNING":
            error_handler.log_warning("Billing", function, message)
        else:
            error_handler.log_error("Billing", function, message)

    def load_data(self, file_name):
        if not os.path.exists(file_name):
            return []

        try:
            with open(file_name, "r", encoding="utf-8") as file:
                data = json.load(file)
                return data if isinstance(data, list) else []
        except (json.JSONDecodeError, OSError) as e:
            error_handler.exception(e)
            return []

    def save_bills(self, bills):
        try:
            os.makedirs(DATABASE_DIR, exist_ok=True)

            with open(BILL_FILE, "w", encoding="utf-8") as file:
                json.dump(bills, file, indent=4)

            return True
        except OSError as e:
            error_handler.exception(e)
            print("Unable to save bills.")
            return False

    def generate_bill_id(self, bills):
        numbers = [
            int(b["bill_id"][1:])
            for b in bills
            if re.fullmatch(r"B\d+", b.get("bill_id", ""))
        ]
        return f"B{max(numbers, default=0) + 1:03d}"

    def get_order_id(self):
        while True:
            order_id = input("Enter Order ID: ").strip().upper()

            if re.fullmatch(r"O\d{3}", order_id):
                return order_id

            print("Invalid Order ID. Example: O001")
            self.log_error("get_order_id", order_id, "WARNING")

    def get_customer_name(self):
        while True:
            name = input("Enter Customer Name: ").strip()

            if len(name) >= 3 and all(c.isalpha() or c.isspace() for c in name):
                return name.title()

            print("Name must contain at least 3 letters.")
            self.log_error("get_customer_name", name, "WARNING")

    def get_mobile(self):
        while True:
            mobile = input("Enter Mobile Number: ").strip()

            if re.fullmatch(r"[6-9]\d{9}", mobile):
                return mobile

            print("Enter a valid 10-digit mobile number.")
            self.log_error("get_mobile", mobile, "WARNING")

    def generate_bill(self):
        orders = self.load_data(ORDER_FILE)
        bills = self.load_data(BILL_FILE)

        if not orders:
            print("No orders found.")
            return

        for order in orders:
            print(
                order.get("order_id"),
                "| Table:",
                order.get("table_no") or "None",
                "| Status:",
                order.get("status", "N/A"),
            )

        order_id = self.get_order_id()
        order = next(
            (o for o in orders if o.get("order_id", "").upper() == order_id), None
        )

        if order is None or order.get("status", "").lower() == "cancelled":
            print("Order not found or order is cancelled.")
            self.log_error("generate_bill", order_id, "WARNING")
            return

        if any(b.get("order_id", "").upper() == order_id for b in bills):
            print("Bill already generated.")
            return

        items = order.get("items", [])

        try:
            subtotal = sum(float(item["total"]) for item in items)
            if not items or subtotal <= 0:
                print("Order has no valid items.")
                return
        except (KeyError, TypeError, ValueError) as e:
            error_handler.exception(e)
            print("Invalid order item total.")
            return

        customer_name = self.get_customer_name()
        mobile = self.get_mobile()

        discount_rate = self.DISCOUNT_RATE if subtotal > self.DISCOUNT_LIMIT else 0
        discount = round(subtotal * discount_rate / 100, 2)
        after_discount = subtotal - discount
        tax = round(after_discount * self.TAX_RATE / 100, 2)
        grand_total = round(after_discount + tax, 2)
        now = datetime.now()

        bill = {
            "bill_id": self.generate_bill_id(bills),
            "order_id": order_id,
            "customer_name": customer_name,
            "mobile": mobile,
            "table_no": order.get("table_no"),
            "date": now.strftime("%Y-%m-%d"),
            "time": now.strftime("%H:%M:%S"),
            "items": items,
            "subtotal": round(subtotal, 2),
            "discount_rate": discount_rate,
            "discount": discount,
            "tax_rate": self.TAX_RATE,
            "tax": tax,
            "grand_total": grand_total,
            "payment_status": "Unpaid",
            "payment_method": "Not Selected",
            "payment_number": "Not Available",
        }

        bills.append(bill)

        if not self.save_bills(bills):
            return

        print("\n========== BILL ==========")
        print("Bill ID:", bill["bill_id"])
        print("Order ID:", order_id)
        print("Customer:", customer_name)
        print("Mobile:", mobile)
        print("Table:", bill["table_no"] or "None")
        print("Date:", bill["date"])
        print("\nItems:")

        for item in items:
            name = item.get("name", item.get("item_name", "Unknown"))
            qty = item.get("quantity", item.get("qty", 1))
            price = float(item.get("price", 0))
            total = float(item.get("total", price * int(qty)))
            print(f"{name} x {qty} | ₹{price:.2f} | ₹{total:.2f}")

        print(f"\nSubtotal: ₹{subtotal:.2f}")
        print(f"Discount ({discount_rate}%): ₹{discount:.2f}")
        print(f"Tax ({self.TAX_RATE}%): ₹{tax:.2f}")
        print(f"Grand Total: ₹{grand_total:.2f}")
        print("Payment Status: Unpaid")
        print("Bill generated successfully.")

    def view_bills(self):
        bills = self.load_data(BILL_FILE)

        if not bills:
            print("No bills found.")
            return

        for bill in bills:
            print("\n------------------------------")
            print("Bill ID:", bill.get("bill_id"))
            print("Order ID:", bill.get("order_id"))
            print("Customer:", bill.get("customer_name"))
            print("Mobile:", bill.get("mobile"))
            print("Date:", bill.get("date"))
            print("Items:")

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

    def get_bill_id(self):
        while True:
            bill_id = input("Enter Bill ID: ").strip().upper()

            if re.fullmatch(r"B\d{3,}", bill_id):
                return bill_id

            print("Invalid Bill ID. Example: B001")
            self.log_error("get_bill_id", bill_id, "WARNING")

    def validate_upi(self):
        while True:
            upi = input("Enter UPI ID: ").strip()

            if re.fullmatch(r"[A-Za-z0-9._-]+@[A-Za-z0-9.-]+", upi):
                return upi

            print("Invalid UPI ID. Example: name@upi")
            self.log_error("validate_upi", "Invalid UPI", "WARNING")

    def validate_card(self):
        while True:
            card = input("Enter 16 digit Card Number: ").strip().replace(" ", "")

            if card.isdigit() and len(card) == 16:
                break

            print("Card number must contain 16 digits.")
            self.log_error("validate_card", "Invalid card number", "WARNING")

        while True:
            cvv = input("Enter CVV: ").strip()

            if cvv.isdigit() and len(cvv) in (3, 4):
                break

            print("CVV must contain 3 or 4 digits.")
            self.log_error("validate_card", "Invalid CVV", "WARNING")

        return "**** **** **** " + card[-4:]

    def update_payment(self):
        bills = self.load_data(BILL_FILE)

        if not bills:
            print("No bills found.")
            return

        for bill in bills:
            print(
                bill.get("bill_id"),
                "|",
                bill.get("customer_name"),
                "|",
                f"₹{float(bill.get('grand_total', 0)):.2f}",
                "|",
                bill.get("payment_status", "Unpaid"),
            )

        bill_id = self.get_bill_id()
        bill = next((b for b in bills if b.get("bill_id", "").upper() == bill_id), None)

        if bill is None:
            print("Bill ID not found.")
            self.log_error("update_payment", bill_id, "WARNING")
            return

        if bill.get("payment_status") == "Paid":
            print("Bill is already paid.")
            return

        print("1. Paid")
        print("2. Unpaid")
        choice = input("Enter choice: ").strip()

        if choice == "1":
            print("1. Cash")
            print("2. UPI")
            print("3. Card")
            method = input("Enter payment method: ").strip()

            if method == "1":
                payment_method = "Cash"
                payment_number = "Not Required"
            elif method == "2":
                payment_method = "UPI"
                payment_number = self.validate_upi()
            elif method == "3":
                payment_method = "Card"
                payment_number = self.validate_card()
            else:
                print("Invalid payment method.")
                self.log_error("update_payment", method, "WARNING")
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
            self.log_error("update_payment", choice, "WARNING")
            return

        if self.save_bills(bills):
            print("Payment updated successfully.")
            print("Bill ID:", bill["bill_id"])
            print("Payment Status:", bill["payment_status"])
            print("Payment Method:", bill["payment_method"])

    def billing_menu(self):
        while True:
            print("\n========== BILLING MANAGEMENT ==========")
            print("1. Generate Bill")
            print("2. View Bills")
            print("3. Update Payment")
            print("4. Exit")

            choice = input("Enter choice: ").strip()

            if choice == "1":
                self.generate_bill()
            elif choice == "2":
                self.view_bills()
            elif choice == "3":
                self.update_payment()
            elif choice == "4":
                print("Billing Management closed.")
                break
            else:
                print("Invalid choice.")
                self.log_error("billing_menu", choice, "WARNING")
