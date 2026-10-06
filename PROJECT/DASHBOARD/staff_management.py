from PROJECT.MENU.menu_management import view_food
from PROJECT.BOOKING.booking_management import booking_management
from PROJECT.ORDER.order_management import order_menu, update_order_status
from PROJECT.BILLING.billing_management import billing_menu
from PROJECT.LOGS.error_hendal import error_handler

class StaffManagement:
    def __init__(self, user):
        self.user = user

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
                    view_food()
                elif choice == "2":
                    booking_management()
                elif choice == "3":
                    order_menu()
                elif choice == "4":
                    update_order_status()
                elif choice == "5":
                    billing_menu()
                elif choice == "6":
                    print("\nReturning to previous menu.")
                    break
                else:
                    print("\nInvalid choice.")
                    error_handler.log_error(
                        "StaffManagement", "show",
                        f"Invalid choice: {choice}"
                    )

        except Exception as e:
            error_handler.log_exception("StaffManagement", "show", e)
            print("\nSomething went wrong.")
