import json
import os
import re
import msvcrt

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_DIR = os.path.join(BASE_DIR, "DATABASE")
FILE_NAME = os.path.join(DATABASE_DIR, "users.json")


def load_users():

    if not os.path.exists(FILE_NAME):
        return []

    try:
        with open(FILE_NAME, "r") as file:
            return json.load(file)

    except (json.JSONDecodeError, FileNotFoundError):
        return []


def save_users(users):

    os.makedirs(DATABASE_DIR, exist_ok=True)

    with open(FILE_NAME, "w") as file:
        json.dump(users, file, indent=4)


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
            print("*", end="", flush=True)

    return password


def get_user_id(users):

    while True:

        user_id = input("User ID: ").strip()

        if not user_id:
            print("User ID cannot be empty.")

        elif not user_id.isdigit():
            print("User ID must contain digits only.")

        elif any(user["user_id"] == user_id for user in users):
            print("User ID already exists.")

        else:
            return user_id


def get_name():

    while True:

        name = input("Name: ").strip()

        if len(name) < 3:
            print("Name must contain at least 3 characters.")

        elif not all(char.isalpha() or char.isspace() for char in name):
            print("Name can contain only letters and spaces.")

        else:
            return name


def get_email(users):

    while True:

        email = input("Email: ").strip().lower()

        if not email:
            print("Email cannot be empty.")

        elif not re.fullmatch(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", email):
            print("Enter a valid email address.")

        elif any(user["email"].lower() == email for user in users):
            print("Email already registered.")

        else:
            return email


def get_mobile(users):

    while True:

        mobile = input("Mobile Number: ").strip()

        if not mobile:
            print("Mobile number cannot be empty.")

        elif not mobile.isdigit():
            print("Mobile number must contain digits only.")

        elif len(mobile) != 10:
            print("Mobile number must contain exactly 10 digits.")

        elif mobile[0] not in "6789":
            print("Mobile number must start with 6, 7, 8 or 9.")

        elif any(user["mobile"] == mobile for user in users):
            print("Mobile number already registered.")

        else:
            return mobile


def get_aadhaar(users):

    while True:

        aadhaar = input("Aadhaar Number: ").strip()

        if not aadhaar:
            print("Aadhaar number cannot be empty.")

        elif not aadhaar.isdigit():
            print("Aadhaar must contain digits only.")

        elif len(aadhaar) != 12:
            print("Aadhaar must contain exactly 12 digits.")

        elif aadhaar[0] == "0":
            print("Aadhaar cannot start with 0.")

        elif any(user["aadhaar"] == aadhaar for user in users):
            print("Aadhaar already registered.")

        else:
            return aadhaar


def get_valid_password():

    while True:

        password = get_password("Password: ")

        if len(password) < 8:
            print("Password must contain at least 8 characters.")
            continue

        if not re.search(r"[A-Z]", password):
            print("Password must contain an uppercase letter.")
            continue

        if not re.search(r"[a-z]", password):
            print("Password must contain a lowercase letter.")
            continue

        if not re.search(r"[0-9]", password):
            print("Password must contain a number.")
            continue

        if not re.search(r"[^A-Za-z0-9]", password):
            print("Password must contain a special character.")
            continue

        confirm = get_password("Confirm Password: ")

        if password != confirm:
            print("Passwords do not match.")
            continue

        return password


def create_admin():

    users = load_users()

    for user in users:

        if user.get("role") == "admin":
            return False

    print("\nCreate Admin Account")
    print("--------------------")

    user_id = get_user_id(users)
    name = get_name()
    email = get_email(users)
    mobile = get_mobile(users)
    aadhaar = get_aadhaar(users)
    password = get_valid_password()

    admin = {
        "user_id": user_id,
        "name": name,
        "email": email,
        "mobile": mobile,
        "aadhaar": aadhaar,
        "password": password,
        "role": "admin",
    }

    users.append(admin)
    save_users(users)

    print("\nAdmin account created successfully.")
    print("User ID:", user_id)
    print("Name:", name)
    print("Email:", email)

    return True


def add_waitstaff(admin_id):

    users = load_users()

    print("\nAdd Waitstaff")
    print("-------------")

    user_id = get_user_id(users)
    name = get_name()
    email = get_email(users)
    mobile = get_mobile(users)
    aadhaar = get_aadhaar(users)
    password = get_valid_password()

    waitstaff = {
        "user_id": user_id,
        "name": name,
        "email": email,
        "mobile": mobile,
        "aadhaar": aadhaar,
        "password": password,
        "role": "waitstaff",
        "created_by": admin_id,
    }

    users.append(waitstaff)
    save_users(users)

    print("\nWaitstaff account created successfully.")
    print("User ID:", user_id)
    print("Name:", name)
    print("Email:", email)


def remove_waitstaff():

    users = load_users()

    waitstaff = []

    for user in users:

        if user.get("role") == "waitstaff":
            waitstaff.append(user)

    if not waitstaff:
        print("\nNo waitstaff account found.")
        return

    print("\nWaitstaff List")
    print("--------------")

    for user in waitstaff:

        print("User ID:", user["user_id"])
        print("Name:", user["name"])
        print("Email:", user["email"])
        print("--------------------")

    user_id = input("Enter Waitstaff User ID to remove: ").strip()

    for user in users:

        if user.get("user_id") == user_id and user.get("role") == "waitstaff":

            users.remove(user)
            save_users(users)

            print("\nWaitstaff removed successfully.")
            return

    print("\nWaitstaff User ID not found.")


if __name__ == "__main__":
    create_admin()
