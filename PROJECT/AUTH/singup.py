import json
import os
import re
import msvcrt
import uuid
from PROJECT.LOGS.error_hendal import error_handler

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_DIR = os.path.join(BASE_DIR, "DATABASE")
FILE_NAME = os.path.join(DATABASE_DIR, "users.json")


def load_users():
    if not os.path.exists(FILE_NAME):
        error_handler.error("users.json file not found.")
        return []
    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError) as e:
        error_handler.exception(e)
        return []


def save_users(users):
    try:
        os.makedirs(DATABASE_DIR, exist_ok=True)
        with open(FILE_NAME, "w", encoding="utf-8") as file:
            json.dump(users, file, indent=4, ensure_ascii=False)
        return True
    except OSError as e:
        error_handler.exception(e)
        print("Unable to save user data.")
        return False


def get_password(message):
    print(message, end="", flush=True)
    password = ""

    while True:
        char = msvcrt.getwch()
        if char == "\r":
            print()
            return password
        if char == "\b":
            if password:
                password = password[:-1]
                print("\b \b", end="", flush=True)
        elif char not in ("\x00", "\xe0"):
            password += char
            print("#", end="", flush=True)


def get_user_id(users):
    while True:
        user_id = input("User ID: ").strip()
        if not user_id.isdigit() or not user_id:
            error_handler.warning("User ID must contain digits only.")
        elif any(u.get("user_id") == user_id for u in users):
            error_handler.warning("User ID already exists.")
        else:
            return user_id


def generate_staff_id(users):
    while True:
        staff_id = str(uuid.uuid4().int)[:10]
        if not any(u.get("user_id") == staff_id for u in users):
            return staff_id


def get_name():
    while True:
        name = input("Name: ").strip()
        if len(name) >= 3 and all(c.isalpha() or c.isspace() for c in name):
            return name
        error_handler.warning("Name must contain at least 3 letters and spaces only.")


def get_email(users):
    while True:
        email = input("Email: ").strip().lower()
        if not re.fullmatch(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", email):
            error_handler.warning("Enter a valid email address.")
        elif any(u.get("email", "").lower() == email for u in users):
            error_handler.warning("Email already registered.")
        else:
            return email


def get_mobile(users):
    while True:
        mobile = input("Mobile Number: ").strip()
        if not re.fullmatch(r"[6-9]\d{9}", mobile):
            error_handler.warning(
                "Mobile must be 10 digits and start with 6, 7, 8 or 9."
            )
        elif any(u.get("mobile") == mobile for u in users):
            error_handler.warning("Mobile number already registered.")
        else:
            return mobile


def get_aadhaar(users):
    while True:
        aadhaar = input("Aadhaar Number: ").strip()
        if not re.fullmatch(r"[1-9]\d{11}", aadhaar):
            error_handler.warning(
                "Aadhaar must contain 12 digits and cannot start with 0."
            )
        elif any(u.get("aadhaar") == aadhaar for u in users):
            error_handler.warning("Aadhaar already registered.")
        else:
            return aadhaar


def get_valid_password():
    while True:
        password = get_password("Password: ")
        if (
            len(password) < 8
            or not re.search(r"[A-Z]", password)
            or not re.search(r"[a-z]", password)
            or not re.search(r"\d", password)
            or not re.search(r"[^A-Za-z0-9]", password)
        ):
            error_handler.warning(
                "Password needs 8+ characters, uppercase, lowercase, number and special character."
            )
            continue

        if password != get_password("Confirm Password: "):
            error_handler.warning("Passwords do not match.")
            continue
        return password


def create_admin():
    users = load_users()
    if any(u.get("role") == "admin" for u in users):
        return False

    try:
        print("\nCreate Admin Account")
        user_id = get_user_id(users)
        name = get_name()
        email = get_email(users)
        mobile = get_mobile(users)
        aadhaar = get_aadhaar(users)
        password = get_valid_password()

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

        if save_users(users):
            print("\nAdmin account created successfully.")
            print("User ID:", user_id)
            print("Name:", name)
            print("Email:", email)
            return True
        return False

    except Exception as e:
        error_handler.exception(e)
        print("Unable to create Admin account.")
        return False


def add_staff(admin_id):
    try:
        users = load_users()
        print("\nAdd Staff")
        name = get_name()
        email = get_email(users)
        mobile = get_mobile(users)
        aadhaar = get_aadhaar(users)
        password = get_valid_password()
        user_id = generate_staff_id(users)

        users.append(
            {
                "user_id": user_id,
                "name": name,
                "email": email,
                "mobile": mobile,
                "aadhaar": aadhaar,
                "password": password,
                "role": "staff",
                "created_by": admin_id,
            }
        )

        if save_users(users):
            print("\nStaff account created successfully.")
            print("Staff ID:", user_id)
            print("Name:", name)
            print("Email:", email)

    except Exception as e:
        error_handler.exception(e)
        print("Unable to create Staff account.")


def remove_staff():
    try:
        users = load_users()
        staff = [u for u in users if u.get("role") == "staff"]

        if not staff:
            print("\nNo staff account found.")
            return

        print("\nStaff List")
        for user in staff:
            print(f"Staff ID: {user['user_id']} | Name: {user['name']} | Email: {user['email']}")

        user_id = input("Enter Staff User ID to remove: ").strip()
        staff_user = next((u for u in staff if u.get("user_id") == user_id), None)

        if not staff_user:
            error_handler.warning("Staff User ID not found.")
            return

        users.remove(staff_user)
        if save_users(users):
            print("Staff removed successfully.")

    except Exception as e:
        error_handler.exception(e)
        print("Unable to remove Staff.")