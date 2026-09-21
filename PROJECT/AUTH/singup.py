import json
import os
import re
import msvcrt

from colorama import init, Fore, Style

# ==============================
# COLORAMA
# ==============================

init(autoreset=True)


# ==============================
# DATABASE PATH
# ==============================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_DIR = os.path.join(BASE_DIR, "DATABASE")
FILE_NAME = os.path.join(DATABASE_DIR, "users.json")


# ==============================
# LOAD USERS
# ==============================


def load_users():
    if not os.path.exists(FILE_NAME):
        return []

    try:
        with open(FILE_NAME, "r") as file:
            return json.load(file)

    except (json.JSONDecodeError, FileNotFoundError):
        return []


# ==============================
# SAVE USERS
# ==============================


def save_users(users):
    os.makedirs(DATABASE_DIR, exist_ok=True)

    with open(FILE_NAME, "w") as file:
        json.dump(users, file, indent=4)


# ==============================
# PASSWORD INPUT
# ==============================


def get_password(message):

    print(Fore.CYAN + message, end="", flush=True)

    password = ""

    while True:

        char = msvcrt.getwch()

        if char == "\r":
            print()
            break

        elif char == "\b":

            if password:
                password = password[:-1]
                print("\b \b", end="", flush=True)

        else:

            password += char
            print("*", end="", flush=True)

    return password


# ==============================
# USER ID
# ==============================


def get_user_id(users):

    while True:

        user_id = input(Fore.CYAN + "🆔 User ID: ").strip()

        if not user_id.isdigit():

            print(Fore.RED + "❌ User ID must contain digits only.")

        elif any(user["user_id"] == user_id for user in users):

            print(Fore.RED + "❌ User ID already exists.")

        else:

            return user_id


# ==============================
# NAME
# ==============================


def get_name():

    while True:

        name = input(Fore.CYAN + "👤 Name: ").strip()

        if len(name) < 3:

            print(Fore.RED + "❌ Name must contain at least 3 characters.")

        elif not all(char.isalpha() or char.isspace() for char in name):

            print(Fore.RED + "❌ Name can contain only letters and spaces.")

        else:

            return name


# ==============================
# MOBILE
# ==============================


def get_mobile(users):

    while True:

        mobile = input(Fore.CYAN + "📱 Mobile Number: ").strip()

        if not mobile.isdigit():

            print(Fore.RED + "❌ Mobile number must contain digits only.")

        elif len(mobile) != 10:

            print(Fore.RED + "❌ Mobile number must contain exactly 10 digits.")

        elif any(user["mobile"] == mobile for user in users):

            print(Fore.RED + "❌ Mobile number already registered.")

        else:

            return mobile


# ==============================
# AADHAAR
# ==============================


def get_aadhaar(users):

    while True:

        aadhaar = input(Fore.CYAN + "🪪 Aadhaar Number: ").strip()

        if not aadhaar.isdigit():

            print(Fore.RED + "❌ Aadhaar must contain digits only.")

        elif len(aadhaar) != 12:

            print(Fore.RED + "❌ Aadhaar must contain exactly 12 digits.")

        elif any(user["aadhaar"] == aadhaar for user in users):

            print(Fore.RED + "❌ Aadhaar already registered.")

        else:

            return aadhaar


# ==============================
# PASSWORD VALIDATION
# ==============================


def get_valid_password():

    while True:

        password = get_password("🔑 Password: ")

        if len(password) < 8:

            print(Fore.RED + "❌ Password must contain at least 8 characters.")
            continue

        if not re.search(r"[A-Z]", password):

            print(Fore.RED + "❌ Password must contain an uppercase letter.")
            continue

        if not re.search(r"[a-z]", password):

            print(Fore.RED + "❌ Password must contain a lowercase letter.")
            continue

        if not re.search(r"[0-9]", password):

            print(Fore.RED + "❌ Password must contain a number.")
            continue

        if not re.search(r"[^A-Za-z0-9]", password):

            print(Fore.RED + "❌ Password must contain a special character.")
            continue

        confirm_password = get_password("🔁 Confirm Password: ")

        if password != confirm_password:

            print(Fore.RED + "❌ Passwords do not match.")
            continue

        return password


# ==============================
# CREATE ADMIN
# ==============================


def create_admin():

    users = load_users()

    if any(user["role"] == "admin" for user in users):
        return

    print()
    print(Fore.MAGENTA + "🍽️ =======================================")

    print(Fore.YELLOW + "        👨‍💼 CREATE ADMIN ACCOUNT")

    print(Fore.MAGENTA + "🍽️ =======================================")

    user_id = get_user_id(users)

    name = get_name()

    mobile = get_mobile(users)

    aadhaar = get_aadhaar(users)

    password = get_valid_password()

    admin = {
        "user_id": user_id,
        "name": name,
        "mobile": mobile,
        "aadhaar": aadhaar,
        "password": password,
        "role": "admin",
    }

    users.append(admin)

    save_users(users)

    print()
    print(Fore.GREEN + "✅ Admin account created successfully!")

    print(Fore.CYAN + f"👤 Name: {name}")

    print(Fore.CYAN + f"🆔 User ID: {user_id}")

    print(Fore.YELLOW + "👨‍💼 Role: Admin")


# ==============================
# ADD WAITSTAFF
# ==============================


def add_waitstaff(admin_id):

    users = load_users()

    print()
    print(Fore.MAGENTA + "🍽️ =======================================")

    print(Fore.YELLOW + "          👨‍🍳 ADD WAITSTAFF")

    print(Fore.MAGENTA + "🍽️ =======================================")

    user_id = get_user_id(users)

    name = get_name()

    mobile = get_mobile(users)

    aadhaar = get_aadhaar(users)

    password = get_valid_password()

    waitstaff = {
        "user_id": user_id,
        "name": name,
        "mobile": mobile,
        "aadhaar": aadhaar,
        "password": password,
        "role": "waitstaff",
        "created_by": admin_id,
    }

    users.append(waitstaff)

    save_users(users)

    print()
    print(Fore.GREEN + "✅ Waitstaff account created successfully!")

    print(Fore.CYAN + f"👤 Name: {name}")

    print(Fore.CYAN + f"🆔 User ID: {user_id}")

    print(Fore.YELLOW + "👨‍🍳 Role: Waitstaff")


# ==============================
# RUN
# ==============================

if __name__ == "__main__":

    create_admin()