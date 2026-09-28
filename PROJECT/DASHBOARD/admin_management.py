from PROJECT.MENU.menu_management import add_food, view_food, update_food, delete_food
from PROJECT.AUTH.singup import add_waitstaff, remove_waitstaff, load_users
from PROJECT.BOOKING.booking_management import booking_management


class AdminManagement:

    def __init__(self, user):
        self.user = user

    def show(self):

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
            print("7. Add Waitstaff")
            print("8. Remove Waitstaff")
            print("9. View Waitstaff")
            print("10. Logout")

            choice = input("\nEnter your choice: ").strip()

            if choice == "1":

                self.dashboard()

            elif choice == "2":

                self.menu_management()

            elif choice == "3":

                  booking_management()

            elif choice == "4":

                print("\nOrder Management opened.")

            elif choice == "5":

                print("\nBilling opened.")

            elif choice == "6":

                print("\nInventory Management opened.")

            elif choice == "7":

                add_waitstaff(self.user["user_id"])

            elif choice == "8":

                remove_waitstaff()

            elif choice == "9":

                users = load_users()

                print("\nWaitstaff List")
                print("---------------")

                found = False

                for user in users:

                    if user.get("role") == "waitstaff":

                        print("User ID:", user["user_id"])
                        print("Name:", user["name"])
                        print("Email:", user["email"])
                        print("Mobile:", user["mobile"])
                        print("--------------------")

                        found = True

                if not found:
                    print("No waitstaff account found.")

            elif choice == "10":

                print("\nLogging out...")
                break

            else:

                print("\nInvalid choice. Please try again.")

    def dashboard(self):

        users = load_users()

        total_waitstaff = 0

        for user in users:

            if user.get("role") == "waitstaff":
                total_waitstaff += 1

        print()
        print("=========================================")
        print("             ADMIN DASHBOARD")
        print("=========================================")

        print("Name :", self.user["name"])
        print("Role : ADMIN")

        print("-----------------------------------------")

        print("Total Waitstaff  :", total_waitstaff)
        print("Total Menu Items : Coming Soon")
        print("Total Bookings   : Coming Soon")
        print("Total Orders     : Coming Soon")
        print("Total Sales      : Coming Soon")

        print("-----------------------------------------")

    def menu_management(self):

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