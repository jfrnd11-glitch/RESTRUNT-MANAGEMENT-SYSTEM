from colorama import init, Fore

from PROJECT.AUTH.signin import signin
from PROJECT.AUTH.singup import create_admin, add_waitstaff

from PROJECT.DASHBOARD.admin_management import AdminManagement
from PROJECT.DASHBOARD.waitstaff_management import WaitstaffManagement

init(autoreset=True)


# ==============================
# MAIN MENU
# ==============================


def main():

    create_admin()

    while True:

        print()
        print(Fore.MAGENTA + "🍽️ =========================================")
        print(Fore.YELLOW + "       🍴 RESTAURANT MANAGEMENT SYSTEM 🍴")
        print(Fore.MAGENTA + "🍽️ =========================================")

        print(Fore.CYAN + "🔐 1. Sign In")
        print(Fore.RED + "🚪 2. Exit")

        choice = input(Fore.WHITE + "\n👉 Enter your choice: ").strip()

        if choice == "1":

            user = signin()

            if user:

                if user["role"] == "admin":

                    AdminManagement(user).show()

                elif user["role"] == "waitstaff":

                    WaitstaffManagement(user).show()

        elif choice == "2":

            print(Fore.GREEN + "\n👋 Thank you for using Restaurant Management System.")

            break

        else:

            print(Fore.RED + "\n❌ Invalid choice. Please try again.")
