import json
import os
import msvcrt

from colorama import init, Fore

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
# SIGN IN
# ==============================


def signin():

    users = load_users()

    if not users:

        print()
        print(Fore.RED + "❌ No account found.")

        print(Fore.YELLOW + "⚠️ Please create an Admin account first.")

        return None

    print()
    print(Fore.MAGENTA + "🍽️ =======================================")

    print(Fore.YELLOW + "             🔐 SIGN IN")

    print(Fore.MAGENTA + "🍽️ =======================================")

    user_id = input(Fore.CYAN + "🆔 User ID: ").strip()

    password = get_password("🔑 Password: ")

    for user in users:

        if user["user_id"] == user_id and user["password"] == password:

            print()
            print(Fore.GREEN + "✅ Login successful!")

            print(Fore.CYAN + f"👋 Welcome, {user['name']}!")

            print(Fore.YELLOW + f"👤 Role: {user['role'].title()}")

            return user

    print()
    print(Fore.RED + "❌ Invalid User ID or Password.")

    return None
