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
                        "AdminManagement", "show",
                        f"Invalid choice entered: {choice}"
                    )

        except Exception as e:
            error_handler.log_exception("AdminManagement", "show", e)
            print("\nSomething went wrong.")

    def dashboard(self):
        try:
            users = load_users()
            staff = sum(1 for user in users if user.get("role") == "staff")

            print("\n=========================================")
            print("             ADMIN DASHBOARD")
            print("=========================================")
            print("Name :", self.user["name"])
            print("Role : ADMIN")
            print("-----------------------------------------")
            print("Total Staff        :", staff)
            print("Total Menu Items   :", self.get_total_menu())
            print("-----------------------------------------")
            print("Today's Bookings   :", self.get_today_bookings())
            print("Today's Orders     :", self.get_today_orders())
            print("Today's Sales      : ₹" f"{self.get_today_sales():.2f}")
            print("-----------------------------------------")
            print("Paid Bills         :", self.get_paid_bills())
            print("Unpaid Bills       :", self.get_unpaid_bills())
            print("-----------------------------------------")

        except Exception as e:
            error_handler.log_exception("AdminManagement", "dashboard", e)
            print("\nUnable to load dashboard.")

    def load_json_file(self, filename, function_name):
        file_path = os.path.join(DATABASE_DIR, filename)

        try:
            if not os.path.exists(file_path):
                return []

            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)

            return data if isinstance(data, list) else data

        except Exception as e:
            error_handler.log_exception("AdminManagement", function_name, e)
            return []

    def get_total_menu(self):
        try:
            menu = self.load_json_file("menu.json", "get_total_menu")

            if isinstance(menu, list):
                return len(menu)

            total = 0

            for items in menu.values():
                if isinstance(items, list):
                    total += len(items)
                elif isinstance(items, dict):
                    total += len(items)

            return total

        except Exception as e:
            error_handler.log_exception("AdminManagement", "get_total_menu", e)
            return 0

    def get_today_bookings(self):
        try:
            bookings = self.load_json_file("booking.json", "get_today_bookings")
            today = datetime.now().strftime("%d-%m-%Y")

            return sum(
                1 for booking in bookings
                if booking.get("date") == today
                and str(booking.get("status", "")).lower() != "cancelled"
            )

        except Exception as e:
            error_handler.log_exception("AdminManagement", "get_today_bookings", e)
            return 0

    def get_today_orders(self):
        try:
            orders = self.load_json_file("orders.json", "get_today_orders")
            today = datetime.now().strftime("%d-%m-%Y")

            return sum(
                1 for order in orders
                if order.get("date") == today
                and str(order.get("status", "")).lower() != "cancelled"
            )

        except Exception as e:
            error_handler.log_exception("AdminManagement", "get_today_orders", e)
            return 0

    def get_today_sales(self):
        try:
            bills = self.load_json_file("bills.json", "get_today_sales")
            today = datetime.now().strftime("%d-%m-%Y")
            total = 0

            for bill in bills:
                if (
                    bill.get("date") == today
                    and str(bill.get("payment_status", "")).lower() == "paid"
                ):
                    try:
                        total += float(bill.get("grand_total", 0))
                    except (TypeError, ValueError):
                        error_handler.log_error(
                            "AdminManagement",
                            "get_today_sales",
                            f"Invalid bill amount: {bill.get('grand_total')}"
                        )

            return total

        except Exception as e:
            error_handler.log_exception("AdminManagement", "get_today_sales", e)
            return 0

    def get_paid_bills(self):
        try:
            bills = self.load_json_file("bills.json", "get_paid_bills")

            return sum(
                1 for bill in bills
                if str(bill.get("payment_status", "")).lower() == "paid"
            )

        except Exception as e:
            error_handler.log_exception("AdminManagement", "get_paid_bills", e)
            return 0

    def get_unpaid_bills(self):
        try:
            bills = self.load_json_file("bills.json", "get_unpaid_bills")

            return sum(
                1 for bill in bills
                if str(bill.get("payment_status", "")).lower() == "unpaid"
            )

        except Exception as e:
            error_handler.log_exception("AdminManagement", "get_unpaid_bills", e)
            return 0

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
                        f"Invalid choice entered: {choice}"
                    )

        except Exception as e:
            error_handler.log_exception("AdminManagement", "menu_management", e)
            print("\nSomething went wrong in Menu Management.")