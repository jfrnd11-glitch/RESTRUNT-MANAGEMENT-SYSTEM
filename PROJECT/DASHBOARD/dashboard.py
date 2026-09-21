from colorama import Fore, Style


class Dashboard:

    def __init__(self, user):
        self.user = user

    def show(self):
        role = self.user["role"]

        print("\n" + Fore.CYAN + "=" * 50)
        print(Fore.MAGENTA + "        🍽️ RESTAURANT DASHBOARD")
        print(Fore.CYAN + "=" * 50)

        print(Fore.GREEN + f"👤 Name : {self.user['name']}")
        print(Fore.YELLOW + f"🔐 Role : {role.upper()}")

        print(Fore.CYAN + "=" * 50)

        if role == "admin":
            self.admin_dashboard()

        elif role == "waitstaff":
            self.waitstaff_dashboard()

    def admin_dashboard(self):
        print(Fore.GREEN + "1. 📊 Dashboard")
        print(Fore.GREEN + "2. 🍴 Menu Management")
        print(Fore.GREEN + "3. 📅 Booking Management")
        print(Fore.GREEN + "4. 🧾 Order Management")
        print(Fore.GREEN + "5. 💰 Billing")
        print(Fore.GREEN + "6. 📦 Inventory Management")
        print(Fore.GREEN + "7. 👨‍🍳 Add Waitstaff")
        print(Fore.GREEN + "8. 🗑️ Remove Waitstaff")
        print(Fore.GREEN + "9. 👥 View Waitstaff")
        print(Fore.RED + "10. 🚪 Logout")

    def waitstaff_dashboard(self):
        print(Fore.GREEN + "1. 📊 Dashboard")
        print(Fore.GREEN + "2. 🍴 View Menu")
        print(Fore.GREEN + "3. 📅 Booking Management")
        print(Fore.GREEN + "4. 🧾 Order Management")
        print(Fore.GREEN + "5. 🔄 Update Order")
        print(Fore.GREEN + "6. 💰 Billing")
        print(Fore.RED + "7. 🚪 Logout")