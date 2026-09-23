from colorama import Fore, init

init(autoreset=True)


class WaitstaffManagement:

    def __init__(self, user):
        self.user = user

    def show(self):

        while True:

            print()
            print(Fore.MAGENTA + "🍽️ =========================================")
            print(Fore.YELLOW + "            👨‍🍳 WAITSTAFF DASHBOARD")
            print(Fore.MAGENTA + "🍽️ =========================================")

            print(Fore.GREEN + f"👤 Name : {self.user['name']}")
            print(Fore.CYAN + "🔐 Role : WAITSTAFF")

            print(Fore.MAGENTA + "-------------------------------------------")

            print(Fore.CYAN + "🍴 1. View Menu")
            print(Fore.CYAN + "📅 2. Booking Management")
            print(Fore.CYAN + "🧾 3. Order Management")
            print(Fore.CYAN + "🔄 4. Update Order")
            print(Fore.CYAN + "💰 5. Billing")
            print(Fore.YELLOW + "🔙 6. Back")

            choice = input(Fore.WHITE + "\n👉 Enter your choice: ").strip()

            if choice == "1":
                self.view_menu()

            elif choice == "2":
                self.booking_management()

            elif choice == "3":
                self.order_management()

            elif choice == "4":
                self.update_order()

            elif choice == "5":
                self.billing()

            elif choice == "6":
                print(Fore.YELLOW + "\n🔙 Returning...")
                break

            else:
                print(Fore.RED + "\n❌ Invalid choice. Please try again.")

    def view_menu(self):

        print()
        print(Fore.GREEN + "🍴 View Menu opened.")
        print(Fore.YELLOW + "👉 Waitstaff can view available food items.")

    def booking_management(self):

        print()
        print(Fore.GREEN + "📅 Booking Management opened.")
        print(Fore.YELLOW + "👉 Booking module will be connected here.")

    def order_management(self):

        print()
        print(Fore.GREEN + "🧾 Order Management opened.")
        print(Fore.YELLOW + "👉 Order module will be connected here.")

    def update_order(self):

        print()
        print(Fore.GREEN + "🔄 Update Order opened.")
        print(Fore.YELLOW + "👉 Order update module will be connected here.")

    def billing(self):

        print()
        print(Fore.GREEN + "💰 Billing opened.")
        print(Fore.YELLOW + "👉 Billing module will be connected here.")
