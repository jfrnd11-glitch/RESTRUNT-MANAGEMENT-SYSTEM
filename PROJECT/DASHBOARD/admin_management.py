from colorama import Fore, init
from PROJECT.MENU.menu_management import add_food, view_food, update_food, delete_food

init(autoreset=True)


class AdminManagement:

    def __init__(self, user):
        self.user = user

    def show(self):

        while True:

            print()
            print(Fore.MAGENTA + "🍽️ =========================================")
            print(Fore.YELLOW + "             👨‍💼 ADMIN DASHBOARD")
            print(Fore.MAGENTA + "🍽️ =========================================")

            print(Fore.GREEN + f"👤 Name : {self.user['name']}")
            print(Fore.CYAN + "🔐 Role : ADMIN")

            print(Fore.MAGENTA + "-------------------------------------------")

            print(Fore.CYAN + "1. 📊 Dashboard")
            print(Fore.CYAN + "2. 🍴 Menu Management")
            print(Fore.CYAN + "3. 📅 Booking Management")
            print(Fore.CYAN + "4. 🧾 Order Management")
            print(Fore.CYAN + "5. 💰 Billing")
            print(Fore.CYAN + "6. 📦 Inventory Management")
            print(Fore.CYAN + "7. ➕ Add Waitstaff")
            print(Fore.CYAN + "8. 🗑️ Remove Waitstaff")
            print(Fore.CYAN + "9. 👀 View Waitstaff")
            print(Fore.YELLOW + "10. 🚪 Logout")

            choice = input(Fore.WHITE + "\n👉 Enter your choice: ").strip()

            if choice == "1":

                print(Fore.GREEN + "\n📊 Dashboard opened.")

            elif choice == "2":

                self.menu_management()

            elif choice == "3":

                print(Fore.GREEN + "\n📅 Booking Management opened.")

            elif choice == "4":

                print(Fore.GREEN + "\n🧾 Order Management opened.")

            elif choice == "5":

                print(Fore.GREEN + "\n💰 Billing opened.")

            elif choice == "6":

                print(Fore.GREEN + "\n📦 Inventory Management opened.")

            elif choice == "7":

                print(Fore.GREEN + "\n➕ Add Waitstaff opened.")

            elif choice == "8":

                print(Fore.RED + "\n🗑️ Remove Waitstaff opened.")

            elif choice == "9":

                print(Fore.GREEN + "\n👀 View Waitstaff opened.")

            elif choice == "10":

                print(Fore.YELLOW + "\n🚪 Logging out...")
                break

            else:

                print(Fore.RED + "\n❌ Invalid choice. Please try again.")

    def menu_management(self):

        while True:

            print()
            print(Fore.MAGENTA + "🍴 =========================================")
            print(Fore.YELLOW + "             🍴 MENU MANAGEMENT")
            print(Fore.MAGENTA + "🍴 =========================================")

            print(Fore.CYAN + "1. ➕ Add Food")
            print(Fore.CYAN + "2. 👀 View Food")
            print(Fore.CYAN + "3. ✏️ Update Food")
            print(Fore.CYAN + "4. 🗑️ Delete Food")
            print(Fore.YELLOW + "5. 🔙 Back")

            choice = input(Fore.WHITE + "\n👉 Enter your choice: ").strip()

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

                print(Fore.RED + "\n❌ Invalid choice. Please try again.")
