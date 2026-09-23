import json
import os
from colorama import init, Fore

init(autoreset=True)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILE_NAME = os.path.join(BASE_DIR, "DATABASE", "menu.json")


CATEGORIES = [
    "Breakfast",
    "Starter",
    "Soup",
    "Salad",
    "Main Course",
    "Rice & Biryani",
    "Roti / Naan",
    "Chinese",
    "Fast Food",
    "Combo",
    "Dessert",
    "Beverages",
    "Tea & Coffee",
]


def load_menu():
    try:
        with open(FILE_NAME, "r") as file:
            return json.load(file)

    except FileNotFoundError:
        return {}


def save_menu(menu):
    with open(FILE_NAME, "w") as file:
        json.dump(menu, file, indent=4)


def get_name():
    while True:
        name = input(Fore.CYAN + "Food Name: ").strip()

        if not name:
            print(Fore.RED + "Food name cannot be empty!")

        elif len(name) < 2:
            print(Fore.RED + "Food name must contain at least 2 characters!")

        elif not all(char.isalpha() or char.isspace() for char in name):
            print(Fore.RED + "Food name can contain only letters and spaces!")

        else:
            return name


def get_price():
    while True:
        try:
            price = float(input(Fore.CYAN + "Price: ").strip())

            if price <= 0:
                print(Fore.RED + "Price must be greater than 0!")

            else:
                return int(price) if price.is_integer() else price

        except ValueError:
            print(Fore.RED + "Please enter a valid price!")


def select_category():
    print(Fore.YELLOW + "\nSelect Category:")

    for index, category in enumerate(CATEGORIES, start=1):
        print(f"{index}. {category}")

    while True:
        try:
            choice = int(input(Fore.CYAN + "Enter choice: ").strip())

            if 1 <= choice <= len(CATEGORIES):
                return CATEGORIES[choice - 1]

            print(Fore.RED + "Invalid category choice!")

        except ValueError:
            print(Fore.RED + "Please enter a number!")


def add_food():
    menu = load_menu()

    print(Fore.MAGENTA + "\n========== ADD FOOD ==========")

    category = select_category()
    food_name = get_name()

    if category not in menu:
        menu[category] = {}

    if food_name in menu[category]:
        print(Fore.RED + "\n❌ Food already exists in this category!")
        return

    price = get_price()

    menu[category][food_name] = price

    save_menu(menu)

    print(Fore.GREEN + "\n✅ Food added successfully!")
    print(Fore.GREEN + f"🍴 Food     : {food_name}")
    print(Fore.GREEN + f"📂 Category : {category}")
    print(Fore.GREEN + f"💰 Price    : ₹{price}")


def view_food():
    menu = load_menu()

    print(Fore.MAGENTA + "\n========== MENU ==========")

    if not menu:
        print(Fore.YELLOW + "No food available!")
        return

    for category, foods in menu.items():

        print()
        print(Fore.YELLOW + f"--- {category} ---")

        for food_name, price in foods.items():
            print(Fore.CYAN + f"{food_name} : ₹{price}")


def find_food(menu):
    category = select_category()

    if category not in menu or not menu[category]:
        print(Fore.RED + "\n❌ No food found in this category!")
        return None, None

    print(Fore.YELLOW + f"\n--- {category} ---")

    foods = list(menu[category].keys())

    for index, food_name in enumerate(foods, start=1):
        print(f"{index}. {food_name} : ₹{menu[category][food_name]}")

    while True:
        try:
            choice = int(input(Fore.CYAN + "Enter food choice: ").strip())

            if 1 <= choice <= len(foods):
                return category, foods[choice - 1]

            print(Fore.RED + "Invalid food choice!")

        except ValueError:
            print(Fore.RED + "Please enter a number!")


def update_food():
    menu = load_menu()

    print(Fore.MAGENTA + "\n========== UPDATE FOOD ==========")

    category, food_name = find_food(menu)

    if food_name is None:
        return

    print(Fore.YELLOW + f"\nFood: {food_name}")
    print(Fore.YELLOW + f"Price: ₹{menu[category][food_name]}")

    print()
    print("1. Update Name")
    print("2. Update Category")
    print("3. Update Price")
    print("4. Back")

    while True:

        choice = input(Fore.CYAN + "Enter choice: ").strip()

        if choice == "1":

            new_name = get_name()

            if new_name in menu[category]:
                print(Fore.RED + "Food already exists!")

            else:
                price = menu[category][food_name]

                del menu[category][food_name]
                menu[category][new_name] = price

                save_menu(menu)

                print(Fore.GREEN + "✅ Food name updated successfully!")
                break

        elif choice == "2":

            new_category = select_category()

            if new_category == category:
                print(Fore.YELLOW + "Food is already in this category!")

            elif food_name in menu[new_category]:
                print(Fore.RED + "Food already exists in this category!")

            else:
                price = menu[category][food_name]

                del menu[category][food_name]
                menu[new_category][food_name] = price

                save_menu(menu)

                print(Fore.GREEN + "✅ Food category updated successfully!")
                break

        elif choice == "3":

            new_price = get_price()

            menu[category][food_name] = new_price

            save_menu(menu)

            print(Fore.GREEN + "✅ Food price updated successfully!")
            break

        elif choice == "4":

            break

        else:

            print(Fore.RED + "Invalid choice!")


def delete_food():
    menu = load_menu()

    print(Fore.MAGENTA + "\n========== DELETE FOOD ==========")

    category, food_name = find_food(menu)

    if food_name is None:
        return

    price = menu[category][food_name]

    print(Fore.YELLOW + f"\nFood    : {food_name}")
    print(Fore.YELLOW + f"Category: {category}")
    print(Fore.YELLOW + f"Price   : ₹{price}")

    confirm = input(Fore.CYAN + "\nAre you sure? (yes/no): ").strip().lower()

    if confirm == "yes":

        del menu[category][food_name]

        save_menu(menu)

        print(Fore.GREEN + "\n✅ Food deleted successfully!")

    elif confirm == "no":

        print(Fore.YELLOW + "\nDelete cancelled!")

    else:

        print(Fore.RED + "\nPlease enter yes or no!")


def menu_management():

    while True:

        print(Fore.MAGENTA + "\n========== MENU MANAGEMENT ==========")

        print(Fore.CYAN + "1. ➕ Add Food")
        print(Fore.CYAN + "2. 👀 View Food")
        print(Fore.CYAN + "3. ✏️ Update Food")
        print(Fore.CYAN + "4. 🗑️ Delete Food")
        print(Fore.YELLOW + "5. 🚪 Back")

        choice = input(Fore.CYAN + "Enter choice: ").strip()

        if choice == "1":

            add_food()

        elif choice == "2":

            view_food()

        elif choice == "3":

            update_food()

        elif choice == "4":

            delete_food()

        elif choice == "5":

            break

        else:

            print(Fore.RED + "Invalid choice!")
