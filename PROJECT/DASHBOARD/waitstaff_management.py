from PROJECT.MENU.menu_management import view_food
from PROJECT.BOOKING.booking_management import booking_management


class WaitstaffManagement:

    def __init__(self, user):
        self.user = user

    def show(self):

        while True:

            print()
            print("=========================================")
            print("           WAITSTAFF DASHBOARD")
            print("=========================================")

            print("Name :", self.user["name"])
            print("Role : WAITSTAFF")

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

        print()
        print("Booking Management opened.")
        print("Booking module will be connected here.")

    def order_management(self):

        print()
        print("Order Management opened.")
        print("Order module will be connected here.")

    def update_order(self):

        print()
        print("Update Order opened.")
        print("Order update module will be connected here.")

    def billing(self):

        print()
        print("Billing opened.")
        print("Billing module will be connected here.")