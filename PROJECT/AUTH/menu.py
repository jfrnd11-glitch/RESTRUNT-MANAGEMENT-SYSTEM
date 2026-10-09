from PROJECT.AUTH.signin import SignIn
from PROJECT.DASHBOARD.admin_management import AdminManagement
from PROJECT.DASHBOARD.staff_management import StaffManagement
from PROJECT.LOGS.error_hendal import error_handler


def main():
    try:
        login = SignIn()

        while True:
            print("\n=========================================")
            print("      RESTAURANT MANAGEMENT SYSTEM")
            print("=========================================")
            print("1. Admin Login")
            print("2. Staff Login")
            print("3. Exit")

            choice = input("Enter your choice: ").strip()

            if choice == "1":
                user = login.signin()

                if user and user.get("role") == "admin":
                    AdminManagement(user).show()
                elif user:
                    print("This is not an Admin account.")

            elif choice == "2":
                user = login.signin()

                if user and user.get("role") == "staff":
                    StaffManagement(user).show()
                elif user:
                    print("This is not a Staff account.")

            elif choice == "3":
                print("Thank you for using Restaurant Management System.")
                break

            else:
                error_handler.warning("Invalid main menu choice.")
                print("Please enter 1, 2 or 3.")

    except Exception as error:
        error_handler.exception(error)
        print("Something went wrong. Check error.json for details.")


if __name__ == "__main__":
    main()
