import json
import os

from PROJECT.MENU.menu_management import add_food, view_food, update_food, delete_food
from PROJECT.AUTH.singup import add_staff, remove_staff, load_users
from PROJECT.BOOKING.booking_management import booking_management
from PROJECT.ORDER.order_management import order_menu
from PROJECT.BILLING.billing_management import billing_menu
from PROJECT.LOGS.error_hendal import error_handler

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_DIR = os.path.join(BASE_DIR, "DATABASE")


class AdminManagement:

    def __init__(self, user):
        self.user = user

    def show(self):

        try:

            while True:

                print()
                print("=========================================")
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

                    print("\nInventory Management opened.")

                elif choice == "7":

                    add_staff(self.user["user_id"])

                elif choice == "8":

                    remove_staff()

                elif choice == "9":

                    users = load_users()

                    print("\nStaff List")
                    print("----------")

                    found = False

                    for user in users:

                        if user.get("role") == "staff":

                            print("User ID:", user["user_id"])
                            print("Name:", user["name"])
                            print("Email:", user["email"])
                            print("Mobile:", user["mobile"])
                            print("--------------------")

                            found = True

                    if not found:
                        print("No staff account found.")

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

    def dashboard(self):

        try:

            users = load_users()

            total_staff = 0

            for user in users:

                if user.get("role") == "staff":
                    total_staff += 1

            total_menu = self.get_total_menu()
            total_bookings = self.get_total_bookings()
            total_orders = self.get_total_orders()
            total_sales = self.get_total_sales()

            print()
            print("=========================================")
            print("             ADMIN DASHBOARD")
            print("=========================================")

            print("Name :", self.user["name"])
            print("Role : ADMIN")

            print("-----------------------------------------")

            print("Total Staff      :", total_staff)
            print("Total Menu Items :", total_menu)
            print("Total Bookings   :", total_bookings)
            print("Total Orders     :", total_orders)
            print("Total Sales      : ₹", total_sales)

            print("-----------------------------------------")

        except Exception as e:

            error_handler.log_exception("AdminManagement", "dashboard", e)

            print("\nUnable to load dashboard.")

    def get_total_menu(self):

        file_path = os.path.join(DATABASE_DIR, "menu.json")

        try:

            with open(file_path, "r") as file:
                menu = json.load(file)

            total = 0

            for category in menu.values():

                if isinstance(category, dict):
                    total += len(category)

            return total

        except FileNotFoundError as e:

            error_handler.log_exception("AdminManagement", "get_total_menu", e)

            return 0

        except json.JSONDecodeError as e:

            error_handler.log_exception("AdminManagement", "get_total_menu", e)

            return 0

        except Exception as e:

            error_handler.log_exception("AdminManagement", "get_total_menu", e)

            return 0

    def get_total_bookings(self):

        file_path = os.path.join(DATABASE_DIR, "booking.json")

        try:

            with open(file_path, "r") as file:
                bookings = json.load(file)

            if isinstance(bookings, list):
                return len(bookings)

            return 0

        except FileNotFoundError as e:

            error_handler.log_exception("AdminManagement", "get_total_bookings", e)

            return 0

        except json.JSONDecodeError as e:

            error_handler.log_exception("AdminManagement", "get_total_bookings", e)

            return 0

        except Exception as e:

            error_handler.log_exception("AdminManagement", "get_total_bookings", e)

            return 0

    def get_total_orders(self):

        file_path = os.path.join(DATABASE_DIR, "orders.json")

        try:

            with open(file_path, "r") as file:
                orders = json.load(file)

            if isinstance(orders, list):
                return len(orders)

            return 0

        except FileNotFoundError as e:

            error_handler.log_exception("AdminManagement", "get_total_orders", e)

            return 0

        except json.JSONDecodeError as e:

            error_handler.log_exception("AdminManagement", "get_total_orders", e)

            return 0

        except Exception as e:

            error_handler.log_exception("AdminManagement", "get_total_orders", e)

            return 0

    def get_total_sales(self):

        file_path = os.path.join(DATABASE_DIR, "bills.json")

        try:

            with open(file_path, "r") as file:
                bills = json.load(file)

            total_sales = 0

            if isinstance(bills, list):

                for bill in bills:

                    total_sales += bill.get("final_amount", 0)

            return total_sales

        except FileNotFoundError as e:

            error_handler.log_exception("AdminManagement", "get_total_sales", e)

            return 0

        except json.JSONDecodeError as e:

            error_handler.log_exception("AdminManagement", "get_total_sales", e)

            return 0

        except Exception as e:

            error_handler.log_exception("AdminManagement", "get_total_sales", e)

            return 0

    def menu_management(self):

        try:

            while True:

                print()
                print("=========================================")
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
