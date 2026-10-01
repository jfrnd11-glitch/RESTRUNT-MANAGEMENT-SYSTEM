import json
import os
import msvcrt

from PROJECT.LOGS.error_hendal import error_handler

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_DIR = os.path.join(BASE_DIR, "DATABASE")
FILE_NAME = os.path.join(DATABASE_DIR, "users.json")


def load_users():

    if not os.path.exists(FILE_NAME):
        return []

    try:
        with open(FILE_NAME, "r") as file:
            return json.load(file)

    except (json.JSONDecodeError, FileNotFoundError) as e:
        error_handler.log_exception("Signin", "load_users", e)
        return []


def get_password(message):

    print(message, end="", flush=True)

    password = ""

    while True:

        char = msvcrt.getwch()

        if char == "\r":
            print()
            break

        if char == "\b":

            if password:
                password = password[:-1]
                print("\b \b", end="", flush=True)

        else:
            password += char
            print("#", end="", flush=True)

    return password


def signin():

    try:

        users = load_users()

        if not users:
            print("\nNo account found.")
            print("Please create an Admin account first.")
            return None

        while True:

            print("\nSign In")
            print("-------")
            print("1. Login with User ID")
            print("2. Login with Email")
            print("3. Back")

            choice = input("Enter choice: ").strip()

            if choice == "1":

                user_id = input("User ID: ").strip()

                if not user_id:
                    print("User ID cannot be empty.")
                    continue

                user = None

                for item in users:
                    if item.get("user_id") == user_id:
                        user = item
                        break

                if user is None:
                    print("User ID not found.")
                    continue

                password = get_password("Password: ")

                if user.get("password") == password:

                    print("\nLogin successful.")
                    print("Welcome,", user.get("name"))
                    print("Role:", user.get("role").title())

                    return user

                print("Incorrect password.")

            elif choice == "2":

                email = input("Email: ").strip().lower()

                if not email:
                    print("Email cannot be empty.")
                    continue

                user = None

                for item in users:
                    if item.get("email", "").lower() == email:
                        user = item
                        break

                if user is None:
                    print("Email not found.")
                    continue

                password = get_password("Password: ")

                if user.get("password") == password:

                    print("\nLogin successful.")
                    print("Welcome,", user.get("name"))
                    print("Role:", user.get("role").title())

                    return user

                print("Incorrect password.")

            elif choice == "3":

                return None

            else:

                print("Invalid choice. Please enter 1, 2 or 3.")

    except Exception as e:

        error_handler.log_exception("Signin", "signin", e)

        print("Something went wrong. Please try again.")

        return None