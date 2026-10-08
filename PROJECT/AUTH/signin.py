import json
import os
import msvcrt

from PROJECT.LOGS.error_hendal import error_handler

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILE_NAME = os.path.join(BASE_DIR, "DATABASE", "users.json")


class SignIn:

    def load_users(self):
        try:
            with open(FILE_NAME, "r", encoding="utf-8") as file:
                users = json.load(file)
                return users if isinstance(users, list) else []
        except FileNotFoundError:
            error_handler.warning("users.json file not found.")
            return []
        except (json.JSONDecodeError, OSError) as e:
            error_handler.exception(e)
            return []

    def get_password(self):
        print("Password: ", end="", flush=True)
        password = ""

        while True:
            char = msvcrt.getwch()

            if char == "\r":
                print()
                return password
            elif char == "\b":
                if password:
                    password = password[:-1]
                    print("\b \b", end="", flush=True)
            elif char not in ("\x00", "\xe0"):
                password += char
                print("#", end="", flush=True)

    def signin(self):
        try:
            users = self.load_users()

            if not users:
                print("No account found. Create an Admin account first.")
                return None

            while True:
                print("\nSign In")
                print("1. Login with User ID")
                print("2. Login with Email")
                print("3. Back")

                choice = input("Enter choice: ").strip()

                if choice == "3":
                    return None
                elif choice not in ("1", "2"):
                    error_handler.warning("Invalid login choice.")
                    continue

                if choice == "1":
                    value = input("User ID: ").strip()
                    user = next(
                        (u for u in users if u.get("user_id") == value), None
                    )
                else:
                    value = input("Email: ").strip().lower()
                    user = next(
                        (u for u in users
                         if u.get("email", "").lower() == value), None
                    )

                if not value:
                    error_handler.warning("User ID or Email cannot be empty.")
                    continue

                if user is None:
                    error_handler.warning("User ID or Email not found.")
                    continue

                if user.get("password") == self.get_password():
                    print("Login successful.")
                    print("Welcome,", user.get("name", "User"))
                    print("Role:", user.get("role", "staff").title())
                    return user

                error_handler.warning("Incorrect password.")

        except Exception as e:
            error_handler.exception(e)
            print("Something went wrong. Please try again.")
            return None