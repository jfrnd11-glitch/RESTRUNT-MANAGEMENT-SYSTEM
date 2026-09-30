from PROJECT.AUTH.signin import signin
from PROJECT.AUTH.singup import create_admin

from PROJECT.DASHBOARD.admin_management import AdminManagement
from PROJECT.DASHBOARD.staff_management import StaffManagement

from PROJECT.LOGS.error_hendal import error_handler


def main():

    try:

        create_admin()

        while True:

            print()
            print("=========================================")
            print("      RESTAURANT MANAGEMENT SYSTEM")
            print("=========================================")

            print("1. Admin Login")
            print("2. Staff Login")
            print("3. Exit")

            choice = input("Enter your choice: ").strip()

            if choice == "1":

                user = signin()

                if user is None:
                    continue

                if user["role"] == "admin":
                    AdminManagement(user).show()

                else:
                    print("This account is not an Admin account.")

            elif choice == "2":

                user = signin()

                if user is None:
                    continue

                if user["role"] == "staff":
                    StaffManagement(user).show()

                else:
                    print("This account is not a Staff account.")

            elif choice == "3":

                print("\nThank you for using Restaurant Management System.")
                break

            else:

                print("\nInvalid choice. Please enter 1, 2 or 3.")

                error_handler.log_error(
                    "Main", "main", f"Invalid choice entered: {choice}"
                )

    except Exception as error:

        error_handler.log_exception("Main", "main", error)

        print("\nSomething went wrong.")
        print("Error has been saved in error.json.")


main()
