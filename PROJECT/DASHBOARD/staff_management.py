from PROJECT.MENU.menu_management import view_food
from PROJECT.BOOKING.booking_management import booking_management
from PROJECT.ORDER.order_management import order_menu
from PROJECT.ORDER.order_management import order_menu, update_order_status
from PROJECT.BILLING.billing_management import billing_menu

class StaffManagement:

    def __init__(self, user):
        self.user = user

    def show(self):

        while True:

            print()
            print("=========================================")
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

                self.order_management()

            elif choice == "4":

                self.update_order()

            elif choice == "5":

                self.billing()

            elif choice == "6":

                print("\nReturning to previous menu.")
                break

            else:

                print("\nInvalid choice. Please try again.")

    def booking_management(self):
                
        booking_management()

    def order_management(self):

        order_menu()

    def update_order(self):

        update_order_status()

    def billing(self):

        billing_menu()