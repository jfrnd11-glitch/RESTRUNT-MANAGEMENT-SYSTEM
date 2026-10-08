import json
import os
import re
import msvcrt
import uuid

from PROJECT.LOGS.error_hendal import error_handler
from PROJECT.config import USER_FILE
FILE_NAME = USER_FILE


class UserManagement:

    def load_users(self):
        try:
            with open(FILE_NAME, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            return []
        except (json.JSONDecodeError, OSError) as e:
            error_handler.exception(e)
            return []

    def save_users(self, users):
        try:
            os.makedirs(os.path.dirname(FILE_NAME), exist_ok=True)
            with open(FILE_NAME, "w", encoding="utf-8") as file:
                json.dump(users, file, indent=4)
            return True
        except OSError as e:
            error_handler.exception(e)
            return False

    def get_password(self, message):
        print(message, end="", flush=True)
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

    def create_admin(self):
        users = self.load_users()

        if any(u.get("role") == "admin" for u in users):
            return

        user_id = input("User ID: ").strip()
        name = input("Name: ").strip()
        email = input("Email: ").strip().lower()
        mobile = input("Mobile: ").strip()
        aadhaar = input("Aadhaar: ").strip()
        password = self.get_password("Password: ")

        if not user_id.isdigit() or len(name) < 3:
            error_handler.warning("Invalid User ID or Name.")
            return

        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[A-Za-z]{2,}", email):
            error_handler.warning("Invalid email.")
            return

        if not re.fullmatch(r"[6-9]\d{9}", mobile):
            error_handler.warning("Invalid mobile number.")
            return

        if not re.fullmatch(r"[1-9]\d{11}", aadhaar):
            error_handler.warning("Invalid Aadhaar number.")
            return

        if any(u.get("user_id") == user_id for u in users):
            error_handler.warning("User ID already exists.")
            return

        if any(u.get("email", "").lower() == email for u in users):
            error_handler.warning("Email already registered.")
            return

        if any(u.get("mobile") == mobile for u in users):
            error_handler.warning("Mobile already registered.")
            return

        if any(u.get("aadhaar") == aadhaar for u in users):
            error_handler.warning("Aadhaar already registered.")
            return

        if (
            len(password) < 8
            or not re.search(r"[A-Z]", password)
            or not re.search(r"[a-z]", password)
            or not re.search(r"\d", password)
            or not re.search(r"[^A-Za-z0-9]", password)
        ):
            error_handler.warning("Password does not meet requirements.")
            return

        if password != self.get_password("Confirm Password: "):
            error_handler.warning("Passwords do not match.")
            return

        users.append(
            {
                "user_id": user_id,
                "name": name,
                "email": email,
                "mobile": mobile,
                "aadhaar": aadhaar,
                "password": password,
                "role": "admin",
            }
        )

        if self.save_users(users):
            print("Admin created successfully.")

    def add_staff(self, admin_id):
        users = self.load_users()

        name = input("Name: ").strip()
        email = input("Email: ").strip().lower()
        mobile = input("Mobile: ").strip()
        aadhaar = input("Aadhaar: ").strip()
        password = self.get_password("Password: ")

        if len(name) < 3 or not re.fullmatch(r"[^@\s]+@[^@\s]+\.[A-Za-z]{2,}", email):
            error_handler.warning("Invalid name or email.")
            return

        if not re.fullmatch(r"[6-9]\d{9}", mobile):
            error_handler.warning("Invalid mobile number.")
            return

        if not re.fullmatch(r"[1-9]\d{11}", aadhaar):
            error_handler.warning("Invalid Aadhaar number.")
            return

        if any(
            u.get("email", "").lower() == email
            or u.get("mobile") == mobile
            or u.get("aadhaar") == aadhaar
            for u in users
        ):
            error_handler.warning("Email, mobile or Aadhaar already registered.")
            return

        if (
            len(password) < 8
            or not re.search(r"[A-Z]", password)
            or not re.search(r"[a-z]", password)
            or not re.search(r"\d", password)
            or not re.search(r"[^A-Za-z0-9]", password)
        ):
            error_handler.warning("Password does not meet requirements.")
            return

        if password != self.get_password("Confirm Password: "):
            error_handler.warning("Passwords do not match.")
            return

        staff_id = str(uuid.uuid4().int)[:10]

        while any(u.get("user_id") == staff_id for u in users):
            staff_id = str(uuid.uuid4().int)[:10]

        users.append(
            {
                "user_id": staff_id,
                "name": name,
                "email": email,
                "mobile": mobile,
                "aadhaar": aadhaar,
                "password": password,
                "role": "staff",
                "created_by": admin_id,
            }
        )

        if self.save_users(users):
            print("Staff created successfully.")
            print("Staff ID:", staff_id)

    def remove_staff(self):
        users = self.load_users()
        staff = [u for u in users if u.get("role") == "staff"]

        if not staff:
            print("No staff found.")
            return

        for user in staff:
            print(user["user_id"], user["name"])

        staff_id = input("Enter Staff ID: ").strip()
        users = [
            u
            for u in users
            if not (u.get("user_id") == staff_id and u.get("role") == "staff")
        ]

        if self.save_users(users):
            print("Staff removed successfully.")