import json
import os
from datetime import datetime

from PROJECT.MENU.menu_management import add_food, view_food, update_food, delete_food

from PROJECT.AUTH.singup import add_staff, remove_staff, load_users

from PROJECT.BOOKING.booking_management import booking_management
from PROJECT.ORDER.order_management import order_menu
from PROJECT.BILLING.billing_management import billing_menu
from PROJECT.INVENTORY.inventory_management import inventory_menu
from PROJECT.LOGS.error_hendal import error_handler

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_DIR = os.path.join(BASE_DIR, "DATABASE")


class AdminManagement:

    def __init__(self, user):
        self.user = user

    # =========================
    # ADMIN MENU
    # =========================

    def show(self):
        try:
            while True:

                print("\n=========================================")
                print("            ADMIN DASHBOARD")
                print("=========================================")
                print("Name :", self.user["name"])
                print("Role : ADMIN")
                print("-----------------------------------------")
                print("1. Dashboard")
                print("2. Menu Management")
                print("3. Booking Management")
                print("4. Order Management")
                print("5. Billing")
                print("6. Inventory Management")
                print("7. Add Staff")
                print("8. Remove Staff")
                print("9. View Staff")
                print("10. Logout")

                choice = input("\nEnter your choice: ").strip()

                if choice == "1":
                    self.dashboard()

                elif choice == "2":
                    self.menu_management()

                elif choice == "3":
                    booking_management()

                elif choice == "4":
                    order_menu()

                elif choice == "5":
                    billing_menu()

                elif choice == "6":
                    inventory_menu()

                elif choice == "7":
                    add_staff(self.user["user_id"])

                elif choice == "8":
                    remove_staff()

                elif choice == "9":
                    self.view_staff()

                elif choice == "10":
                    print("\nLogging out...")
                    break

                else:
                    print("\nInvalid choice. Please try again.")

                    error_handler.log_error(
                        "AdminManagement", "show", f"Invalid choice entered: {choice}"
                    )

        except Exception as e:
            error_handler.log_exception("AdminManagement", "show", e)

            print("\nSomething went wrong.")

    # =========================
    # DASHBOARD
    # =========================

    def dashboard(self):

        try:
            users = load_users()

            total_staff = 0

            for user in users:
                if user.get("role") == "staff":
                    total_staff += 1

            total_menu = self.get_total_menu()

            today_bookings = self.get_today_bookings()

            today_orders = self.get_today_orders()

            today_sales = self.get_today_sales()

            paid_bills = self.get_paid_bills()

            unpaid_bills = self.get_unpaid_bills()

            print("\n=========================================")
            print("             ADMIN DASHBOARD")
            print("=========================================")
            print("Name :", self.user["name"])
            print("Role : ADMIN")
            print("-----------------------------------------")

            print("Total Staff        :", total_staff)
            print("Total Menu Items   :", total_menu)

            print("-----------------------------------------")

            print("Today's Bookings   :", today_bookings)
            print("Today's Orders     :", today_orders)

            print("Today's Sales      : ₹" f"{today_sales:.2f}")

            print("-----------------------------------------")

            print("Paid Bills         :", paid_bills)
            print("Unpaid Bills       :", unpaid_bills)

            print("-----------------------------------------")

        except Exception as e:

            error_handler.log_exception("AdminManagement", "dashboard", e)

            print("\nUnable to load dashboard.")

    # =========================
    # READ JSON FILE
    # =========================

    def load_json_file(self, filename, function_name):

        file_path = os.path.join(DATABASE_DIR, filename)

        try:

            if not os.path.exists(file_path):
                return []

            with open(file_path, "r", encoding="utf-8") as file:

                data = json.load(file)

            if isinstance(data, list):
                return data

            return []

        except json.JSONDecodeError as e:

            error_handler.log_exception("AdminManagement", function_name, e)

            return []

        except Exception as e:

            error_handler.log_exception("AdminManagement", function_name, e)

            return []

    # =========================
    # TOTAL MENU
    # =========================

    def get_total_menu(self):

        try:

            menu = self.load_json_file("menu.json", "get_total_menu")

            total = 0

            if isinstance(menu, list):

                return len(menu)

            if isinstance(menu, dict):

                for category in menu.values():

                    if isinstance(category, list):
                        total += len(category)

                    elif isinstance(category, dict):
                        total += len(category)

            return total

        except Exception as e:

            error_handler.log_exception("AdminManagement", "get_total_menu", e)

            return 0

    # =========================
    # TODAY'S BOOKINGS
    # =========================

    def get_today_bookings(self):

        try:

            bookings = self.load_json_file("booking.json", "get_today_bookings")

            today = datetime.now().strftime("%d-%m-%Y")

            total = 0

            for booking in bookings:

                if not isinstance(booking, dict):
                    continue

                booking_date = str(booking.get("date", "")).strip()

                status = str(booking.get("status", "")).strip().lower()

                if booking_date == today and status != "cancelled":
                    total += 1

            return total

        except Exception as e:

            error_handler.log_exception("AdminManagement", "get_today_bookings", e)

            return 0

    # =========================
    # TODAY'S ORDERS
    # =========================

    def get_today_orders(self):

        try:

            orders = self.load_json_file("orders.json", "get_today_orders")

            today = datetime.now().strftime("%d-%m-%Y")

            total = 0

            for order in orders:

                if not isinstance(order, dict):
                    continue

                order_date = str(order.get("date", "")).strip()

                status = str(order.get("status", "")).strip().lower()

                if order_date == today and status != "cancelled":
                    total += 1

            return total

        except Exception as e:

            error_handler.log_exception("AdminManagement", "get_today_orders", e)

            return 0

    # =========================
    # TODAY'S SALES
    # =========================

    def get_today_sales(self):

        try:

            bills = self.load_json_file("bills.json", "get_today_sales")

            today = datetime.now().strftime("%d-%m-%Y")

            total_sales = 0

            for bill in bills:

                if not isinstance(bill, dict):
                    continue

                bill_date = str(bill.get("date", "")).strip()

                payment_status = str(bill.get("payment_status", "")).strip().lower()

                if bill_date == today and payment_status == "paid":

                    amount = bill.get("grand_total", 0)

                    try:
                        total_sales += float(amount)

                    except (TypeError, ValueError) as e:

                        error_handler.log_error(
                            "AdminManagement",
                            "get_today_sales",
                            f"Invalid bill amount: {amount}",
                        )

            return total_sales

        except Exception as e:

            error_handler.log_exception("AdminManagement", "get_today_sales", e)

            return 0

    # =========================
    # PAID BILLS
    # =========================

    def get_paid_bills(self):

        try:

            bills = self.load_json_file("bills.json", "get_paid_bills")

            total = 0

            for bill in bills:

                if not isinstance(bill, dict):
                    continue

                status = str(bill.get("payment_status", "")).strip().lower()

                if status == "paid":
                    total += 1

            return total

        except Exception as e:

            error_handler.log_exception("AdminManagement", "get_paid_bills", e)

            return 0

    # =========================
    # UNPAID BILLS
    # =========================

    def get_unpaid_bills(self):

        try:

            bills = self.load_json_file("bills.json", "get_unpaid_bills")

            total = 0

            for bill in bills:

                if not isinstance(bill, dict):
                    continue

                status = str(bill.get("payment_status", "")).strip().lower()

                if status == "unpaid":
                    total += 1

            return total

        except Exception as e:

            error_handler.log_exception("AdminManagement", "get_unpaid_bills", e)

            return 0

    # =========================
    # VIEW STAFF
    # =========================

    def view_staff(self):

        try:

            users = load_users()

            print("\n=========================================")
            print("              STAFF LIST")
            print("=========================================")

            found = False

            for user in users:

                if user.get("role") == "staff":

                    print("User ID :", user.get("user_id"))
                    print("Name    :", user.get("name"))
                    print("Email   :", user.get("email"))
                    print("Mobile  :", user.get("mobile"))
                    print("-----------------------------------------")

                    found = True

            if not found:
                print("No staff account found.")

        except Exception as e:

            error_handler.log_exception("AdminManagement", "view_staff", e)

            print("\nUnable to load staff list.")

    # =========================
    # MENU MANAGEMENT
    # =========================

    def menu_management(self):

        try:

            while True:

                print("\n=========================================")
                print("             MENU MANAGEMENT")
                print("=========================================")
                print("1. Add Food")
                print("2. View Food")
                print("3. Update Food")
                print("4. Delete Food")
                print("5. Back")

                choice = input("\nEnter your choice: ").strip()

                if choice == "1":
                    add_food()

                elif choice == "2":
                    view_food()

                elif choice == "3":
                    update_food()

                elif choice == "4":
                    delete_food()

                elif choice == "5":
                    break

                else:

                    print("\nInvalid choice. Please try again.")

                    error_handler.log_error(
                        "AdminManagement",
                        "menu_management",
                        f"Invalid choice entered: {choice}",
                    )

        except Exception as e:

            error_handler.log_exception("AdminManagement", "menu_management", e)

            print("\nSomething went wrong in Menu Management.")
