from PROJECT.MENU.menu_management import MenuManagement
from PROJECT.BOOKING.booking_management import BookingManagement
from PROJECT.ORDER.order_management import OrderManagement
from PROJECT.BILLING.billing_management import BillingManagement
from PROJECT.LOGS.error_hendal import error_handler

class StaffManagement:
    def __init__(self, user):
        self.user = user
        self.menu = MenuManagement()
        self.booking = BookingManagement()
        self.order = OrderManagement()
        self.billing = BillingManagement()

    def show(self):
        try:
            while True:
                print("\n=========================================")
                print("           STAFF DASHBOARD")
                print("=========================================")
                print("Name :", self.user["name"])
                print("Role : STAFF")
                print("-----------------------------------------")
                print("1. View Menu")
                print("2. Booking Management")
                print("3. Order Management")
                print("4. Update Order")
                print("5. Billing")
                print("6. Back")

                choice = input("\nEnter your choice: ").strip()

                if choice == "1":
                    self.menu.view_food()
                elif choice == "2":
                    self.booking.booking_management()
                elif choice == "3":
                    self.order.show()
                elif choice == "4":
                    self.order.update_order_status()
                elif choice == "5":
                    self.billing.billing_menu()
                elif choice == "6":
                    print("\nReturning to previous menu.")
                    break
                else:
                    print("\nInvalid choice.")
                    error_handler.warning(
                        f"StaffManagement: Invalid choice: {choice}"
                    )

        except Exception as e:
            error_handler.exception(e)
            print("\nSomething went wrong.")
