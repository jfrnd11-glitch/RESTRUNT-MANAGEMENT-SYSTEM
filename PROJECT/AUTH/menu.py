from colorama import init, Fore

from signin import signin
from singup import create_admin, add_waitstaff

init(autoreset=True)


# ==============================
# ADMIN MENU
# ==============================


def admin_menu(user):

    while True:

        print()
        print(Fore.MAGENTA + "🍽️ =========================================")
        print(Fore.YELLOW + "             👨‍💼 ADMIN DASHBOARD")
        print(Fore.MAGENTA + "🍽️ =========================================")

        print(Fore.CYAN + "📊 1. Dashboard")
        print(Fore.CYAN + "🍴 2. Menu Management")
        print(Fore.CYAN + "📅 3. Booking Management")
        print(Fore.CYAN + "🧾 4. Order Management")
        print(Fore.CYAN + "💰 5. Billing")
        print(Fore.CYAN + "📦 6. Inventory Management")
        print(Fore.GREEN + "👨‍🍳 7. Add Waitstaff")
        print(Fore.RED + "🗑️ 8. Remove Waitstaff")
        print(Fore.GREEN + "👥 9. View Waitstaff")
        print(Fore.YELLOW + "🚪 10. Logout")

        choice = input(Fore.WHITE + "\n👉 Enter your choice: ").strip()

        if choice == "1":

            print(Fore.GREEN + "\n📊 Dashboard opened.")

        elif choice == "2":

            print(Fore.GREEN + "\n🍴 Menu Management opened.")

        elif choice == "3":

            print(Fore.GREEN + "\n📅 Booking Management opened.")

        elif choice == "4":

            print(Fore.GREEN + "\n🧾 Order Management opened.")

        elif choice == "5":

            print(Fore.GREEN + "\n💰 Billing opened.")

        elif choice == "6":

            print(Fore.GREEN + "\n📦 Inventory Management opened.")

        elif choice == "7":

            add_waitstaff(user["user_id"])

        elif choice == "8":

            print(Fore.RED + "\n🗑️ Remove Waitstaff opened.")

        elif choice == "9":

            print(Fore.GREEN + "\n👥 View Waitstaff opened.")

        elif choice == "10":

            print(Fore.YELLOW + "\n🔒 Admin logged out.")
            break

        else:

            print(Fore.RED + "\n❌ Invalid choice. Please try again.")


# ==============================
# WAITSTAFF MENU
# ==============================

def waitstaff_menu(user):

    while True:

        print()
        print(Fore.MAGENTA + "🍽️ =========================================")
        print(Fore.YELLOW + "            👨‍🍳 WAITSTAFF DASHBOARD")
        print(Fore.MAGENTA + "🍽️ =========================================")

        print(Fore.CYAN + "📊 1. Dashboard")
        print(Fore.CYAN + "🍴 2. View Menu")
        print(Fore.CYAN + "📅 3. Booking Management")
        print(Fore.CYAN + "🧾 4. Order Management")
        print(Fore.GREEN + "🔄 5. Update Order")
        print(Fore.CYAN + "💰 6. Billing")
        print(Fore.YELLOW + "🚪 7. Logout")

        choice = input(Fore.WHITE + "\n👉 Enter your choice: ").strip()

        if choice == "1":

            print(Fore.GREEN + "\n📊 Dashboard opened.")

        elif choice == "2":

            print(Fore.GREEN + "\n🍴 Menu opened.")

        elif choice == "3":

            print(Fore.GREEN + "\n📅 Booking Management opened.")

        elif choice == "4":

            print(Fore.GREEN + "\n🧾 Order Management opened.")

        elif choice == "5":

            print(Fore.GREEN + "\n🔄 Update Order opened.")

        elif choice == "6":

            print(Fore.GREEN + "\n💰 Billing opened.")

        elif choice == "7":

            print(Fore.YELLOW + "\n🔒 Waitstaff logged out.")
            break

        else:

            print(Fore.RED + "\n❌ Invalid choice. Please try again.")


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

                    admin_menu(user)

                elif user["role"] == "waitstaff":

                    waitstaff_menu(user)

        elif choice == "2":

            print(Fore.GREEN + "\n👋 Thank you for using Restaurant Management System.")

            break

        else:

            print(Fore.RED + "\n❌ Invalid choice. Please try again.")

main()
