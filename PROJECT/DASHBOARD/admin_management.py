import json
import os
from datetime import datetime

from PROJECT.MENU.menu_management import MenuManagement
from PROJECT.AUTH.singup import UserManagement
from PROJECT.BOOKING.booking_management import BookingManagement
from PROJECT.ORDER.order_management import OrderManagement
from PROJECT.BILLING.billing_management import BillingManagement
from PROJECT.INVENTORY.inventory_management import InventoryManagement
from PROJECT.LOGS.error_hendal import error_handler

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_DIR = os.path.join(BASE_DIR, "DATABASE")


class AdminManagement:
    def __init__(self, user):
        self.user = user
        self.menu = MenuManagement()
        self.users = UserManagement()
        self.booking = BookingManagement()
        self.order = OrderManagement()
        self.billing = BillingManagement()
        self.inventory = InventoryManagement()

    def show(self):
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

            try:
                if choice == "1":
                    self.dashboard()
                elif choice == "2":
                    self.menu_management()
                elif choice == "3":
                    self.booking.booking_management()
                elif choice == "4":
                    self.order.show()
                elif choice == "5":
                    self.billing.billing_menu()
                elif choice == "6":
                    self.inventory.show()
                elif choice == "7":
                    self.users.add_staff(self.user["user_id"])
                elif choice == "8":
                    self.users.remove_staff()
                elif choice == "9":
                    self.view_staff()
                elif choice == "10":
                    print("Logging out...")
                    break
                else:
                    print("Invalid choice.")
                    error_handler.warning(f"Invalid admin choice: {choice}")
            except Exception as e:
                error_handler.exception(e)
                print("Operation failed. Check error.json.")

    def load_json_file(self, filename):
        path = os.path.join(DATABASE_DIR, filename)
        try:
            with open(path, "r", encoding="utf-8") as file:
                data = json.load(file)
                return data if isinstance(data, list) else []
        except FileNotFoundError:
            return []
        except (json.JSONDecodeError, OSError) as e:
            error_handler.exception(e)
            return []

    def dashboard(self):
        users = self.users.load_users()
        staff = sum(1 for user in users if user.get("role") == "staff")

        print("\n========== DASHBOARD ==========")
        print("Total Staff      :", staff)
        print("Total Menu Items :", self.get_total_menu())
        print("Today's Bookings :", self.get_today_bookings())
        print("Today's Orders   :", self.get_today_orders())
        print(f"Today's Sales    : ₹{self.get_today_sales():.2f}")
        print("Paid Bills       :", self.get_paid_bills())
        print("Unpaid Bills     :", self.get_unpaid_bills())

    def get_total_menu(self):
        menu = self.load_json_file("menu.json")
        if isinstance(menu, list):
            return len(menu)
        return sum(len(items) for items in menu.values()
                   if isinstance(items, (list, dict))) if isinstance(menu, dict) else 0

    def get_today_bookings(self):
        bookings = self.load_json_file("booking.json")
        today = datetime.now().strftime("%d-%m-%Y")
        return sum(
            1 for b in bookings
            if b.get("booking_date") == today
            and b.get("status") != "Cancelled"
        )

    def get_today_orders(self):
        orders = self.load_json_file("orders.json")
        today = datetime.now().strftime("%Y-%m-%d")
        return sum(
            1 for o in orders
            if o.get("date") == today
            and o.get("status") != "Cancelled"
        )

    def get_today_sales(self):
        bills = self.load_json_file("bills.json")
        today = datetime.now().strftime("%Y-%m-%d")
        total = 0
        for bill in bills:
            if bill.get("date") == today and bill.get("payment_status") == "Paid":
                try:
                    total += float(bill.get("grand_total", 0))
                except (TypeError, ValueError) as e:
                    error_handler.exception(e)
        return total

    def get_paid_bills(self):
        bills = self.load_json_file("bills.json")
        return sum(1 for b in bills if b.get("payment_status") == "Paid")

    def get_unpaid_bills(self):
        bills = self.load_json_file("bills.json")
        return sum(1 for b in bills if b.get("payment_status") == "Unpaid")

    def view_staff(self):
        users = self.users.load_users()
        staff = [u for u in users if u.get("role") == "staff"]

        if not staff:
            print("No staff account found.")
            return

        for user in staff:
            print("\nUser ID :", user.get("user_id"))
            print("Name    :", user.get("name"))
            print("Email   :", user.get("email"))
            print("Mobile  :", user.get("mobile"))

    def menu_management(self):
        while True:
            print("\n========== MENU MANAGEMENT ==========")
            print("1. Add Food")
            print("2. View Food")
            print("3. Update Food")
            print("4. Delete Food")
            print("5. Back")

            choice = input("Enter your choice: ").strip()

            if choice == "1":
                self.menu.add_food()
            elif choice == "2":
                self.menu.view_food()
            elif choice == "3":
                self.menu.update_food()
            elif choice == "4":
                self.menu.delete_food()
            elif choice == "5":
                break
            else:
                error_handler.warning(f"Invalid menu choice: {choice}")
                print("Invalid choice.")
