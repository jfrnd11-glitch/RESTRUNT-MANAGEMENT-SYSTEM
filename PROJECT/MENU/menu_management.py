import json
import os
from colorama import init, Fore

init(autoreset=True)


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILE_NAME = os.path.join(BASE_DIR, "DATABASE", "menu.json")


CATEGORIES = [
    "Breakfast",
    "South Indian",
    "North Indian",
    "North Indian Thali",
    "South Indian Thali",
    "Starter",
    "Soup",
    "Salad",
    "Main Course",
    "Rice & Biryani",
    "Roti / Naan",
    "Tandoor",
    "Chinese",
    "Fast Food",
    "Snacks",
    "Mughlai",
    "Combo",
    "Dessert",
    "Beverages",
    "Tea & Coffee",
]


# =========================
# LOAD MENU
# =========================


def load_menu():

    try:

        with open(FILE_NAME, "r") as file:
            return json.load(file)

    except FileNotFoundError:

        return {}

    except json.JSONDecodeError:

        print(Fore.RED + "menu.json file contains invalid JSON!")
        return {}


# =========================
# SAVE MENU
# =========================


def save_menu(menu):

    with open(FILE_NAME, "w") as file:

        json.dump(menu, file, indent=4)


# =========================
# GET FOOD NAME
# =========================


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


# =========================
# GET PRICE
# =========================


def get_price():

    while True:

        try:

            price = float(input(Fore.CYAN + "Price: ").strip())

            if price <= 0:

                print(Fore.RED + "Price must be greater than 0!")

            else:

                if price.is_integer():

                    return int(price)

                return price

        except ValueError:

            print(Fore.RED + "Please enter a valid price!")


# =========================
# SELECT CATEGORY
# =========================


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


# =========================
# SELECT PRICE TYPE
# =========================


def select_price_type():

    print(Fore.YELLOW + "\nSelect Price Type:")

    print("1. Single Price")
    print("2. Half / Full")
    print("3. Small / Medium / Full")
    print("4. Small / Medium / Large")
    print("5. Medium / Large")

    while True:

        choice = input(Fore.CYAN + "Enter choice: ").strip()

        if choice == "1":

            return ["Price"]

        elif choice == "2":

            return ["Half", "Full"]

        elif choice == "3":

            return ["Small", "Medium", "Full"]

        elif choice == "4":

            return ["Small", "Medium", "Large"]

        elif choice == "5":

            return ["Medium", "Large"]

        else:

            print(Fore.RED + "Invalid choice!")


# =========================
# GET SIZE PRICES
# =========================


def get_size_prices(sizes):

    if sizes == ["Price"]:

        return get_price()

    prices = {}

    for size in sizes:

        print(Fore.YELLOW + f"\n{size} Price")

        prices[size] = get_price()

    return prices


# =========================
# ADD FOOD
# =========================


def add_food():

    menu = load_menu()

    print(Fore.MAGENTA + "\n========== ADD FOOD ==========")

    category = select_category()

    food_name = get_name()

    if category not in menu:

        menu[category] = {}

    if food_name in menu[category]:

        print(Fore.RED + "\nFood already exists in this category!")

        return

    sizes = select_price_type()

    price = get_size_prices(sizes)

    menu[category][food_name] = price

    save_menu(menu)

    print(Fore.GREEN + "\nFood added successfully!")


# =========================
# VIEW FOOD
# =========================


def view_food():

    menu = load_menu()

    print(Fore.MAGENTA + "\n========== MENU ==========")

    if not menu:

        print(Fore.YELLOW + "No food available!")

        return

    for category, foods in menu.items():

        if not foods:

            continue

        print()

        print(
            Fore.YELLOW
            + f"==================== {category.upper()} ===================="
        )

        food_list = list(foods.items())

        # -------------------------
        # SINGLE PRICE
        # -------------------------

        if all(not isinstance(price, dict) for _, price in food_list):

            print("+----+------------------------------+--------+")

            print("| No | Item Name                    | Price  |")

            print("+----+------------------------------+--------+")

            for index, (food_name, price) in enumerate(food_list, start=1):

                print(f"| {index:<2} | " f"{food_name:<28} | " f"₹{price:<5} |")

            print("+----+------------------------------+--------+")

            continue

        # -------------------------
        # SIZE BASED FOOD
        # -------------------------

        size_list = []

        for _, price in food_list:

            if isinstance(price, dict):

                for size in price:

                    if size not in size_list:

                        size_list.append(size)

        # -------------------------
        # MIXED PRICE CATEGORY
        # -------------------------

        has_single_price = any(not isinstance(price, dict) for _, price in food_list)

        if has_single_price:

            print(
                "+----+------------------------------+"
                + "----------" * len(size_list)
                + "--------+"
            )

            print("| No | Item Name                    |", end="")

            for size in size_list:

                print(f" {size:<8} |", end="")

            print(" Price  |")

            print(
                "+----+------------------------------+"
                + "----------" * len(size_list)
                + "--------+"
            )

            for index, (food_name, price) in enumerate(food_list, start=1):

                print(f"| {index:<2} | " f"{food_name:<28} |", end="")

                if isinstance(price, dict):

                    for size in size_list:

                        amount = price.get(size, "-")

                        if amount == "-":

                            print(f" {'-':<8} |", end="")

                        else:

                            print(f" ₹{amount:<6} |", end="")

                    print(f" {'-':<6} |")

                else:

                    for _ in size_list:

                        print(f" {'-':<8} |", end="")

                    print(f" ₹{price:<5} |")

            print(
                "+----+------------------------------+"
                + "----------" * len(size_list)
                + "--------+"
            )

        else:

            print("+----+------------------------------+", end="")

            for _ in size_list:

                print("----------+", end="")

            print()

            print("| No | Item Name                    |", end="")

            for size in size_list:

                print(f" {size:<8} |", end="")

            print()

            print("+----+------------------------------+", end="")

            for _ in size_list:

                print("----------+", end="")

            print()

            for index, (food_name, price) in enumerate(food_list, start=1):

                print(f"| {index:<2} | " f"{food_name:<28} |", end="")

                for size in size_list:

                    amount = price.get(size, "-")

                    if amount == "-":

                        print(f" {'-':<8} |", end="")

                    else:

                        print(f" ₹{amount:<6} |", end="")

                print()

            print("+----+------------------------------+", end="")

            for _ in size_list:

                print("----------+", end="")

            print()


# =========================
# FIND FOOD
# =========================


def find_food(menu):

    category = select_category()

    if category not in menu:

        print(Fore.RED + "\nNo food found in this category!")

        return None, None

    if not menu[category]:

        print(Fore.RED + "\nNo food found in this category!")

        return None, None

    print(Fore.YELLOW + f"\n--- {category} ---")

    foods = list(menu[category].keys())

    for index, food_name in enumerate(foods, start=1):

        print(f"{index}. {food_name}")

    while True:

        try:

            choice = int(input(Fore.CYAN + "Enter food choice: ").strip())

            if 1 <= choice <= len(foods):

                return (category, foods[choice - 1])

            print(Fore.RED + "Invalid food choice!")

        except ValueError:

            print(Fore.RED + "Please enter a number!")


# =========================
# UPDATE FOOD
# =========================


def update_food():

    menu = load_menu()

    print(Fore.MAGENTA + "\n========== UPDATE FOOD ==========")

    category, food_name = find_food(menu)

    if food_name is None:

        return

    print(Fore.YELLOW + f"\nFood: {food_name}")

    print("\n1. Update Name")

    print("2. Update Category")

    print("3. Update Price")

    print("4. Back")

    while True:

        choice = input(Fore.CYAN + "Enter choice: ").strip()

        # -------------------------
        # UPDATE NAME
        # -------------------------

        if choice == "1":

            new_name = get_name()

            if new_name in menu[category]:

                print(Fore.RED + "Food already exists!")

            else:

                menu[category][new_name] = menu[category][food_name]

                del menu[category][food_name]

                save_menu(menu)

                print(Fore.GREEN + "Food name updated successfully!")

                break

        # -------------------------
        # UPDATE CATEGORY
        # -------------------------

        elif choice == "2":

            new_category = select_category()

            if new_category == category:

                print(Fore.YELLOW + "Food is already in this category!")

                continue

            if new_category not in menu:

                menu[new_category] = {}

            if food_name in menu[new_category]:

                print(Fore.RED + "Food already exists in this category!")

                continue

            menu[new_category][food_name] = menu[category][food_name]

            del menu[category][food_name]

            save_menu(menu)

            print(Fore.GREEN + "Food category updated successfully!")

            break

        # -------------------------
        # UPDATE PRICE
        # -------------------------

        elif choice == "3":

            old_price = menu[category][food_name]

            if isinstance(old_price, dict):

                print(Fore.YELLOW + "\nSelect size to update:")

                sizes = list(old_price.keys())

                for index, size in enumerate(sizes, start=1):

                    print(f"{index}. " f"{size} - " f"₹{old_price[size]}")

                while True:

                    try:

                        size_choice = int(input(Fore.CYAN + "Enter choice: ").strip())

                        if 1 <= size_choice <= len(sizes):

                            selected_size = sizes[size_choice - 1]

                            new_price = get_price()

                            menu[category][food_name][selected_size] = new_price

                            save_menu(menu)

                            print(
                                Fore.GREEN
                                + f"{selected_size} price updated successfully!"
                            )

                            break

                        print(Fore.RED + "Invalid choice!")

                    except ValueError:

                        print(Fore.RED + "Please enter a number!")

            else:

                new_price = get_price()

                menu[category][food_name] = new_price

                save_menu(menu)

                print(Fore.GREEN + "Food price updated successfully!")

            break

        # -------------------------
        # BACK
        # -------------------------

        elif choice == "4":

            break

        else:

            print(Fore.RED + "Invalid choice!")


# =========================
# DELETE FOOD
# =========================


def delete_food():

    menu = load_menu()

    print(Fore.MAGENTA + "\n========== DELETE FOOD ==========")

    category, food_name = find_food(menu)

    if food_name is None:

        return

    price = menu[category][food_name]

    print(Fore.YELLOW + f"\nFood     : {food_name}")

    print(Fore.YELLOW + f"Category : {category}")

    if isinstance(price, dict):

        for size, amount in price.items():

            print(Fore.YELLOW + f"{size:<9}: ₹{amount}")

    else:

        print(Fore.YELLOW + f"Price    : ₹{price}")

    confirm = input(Fore.CYAN + "\nAre you sure? (yes/no): ").strip().lower()

    if confirm == "yes":

        del menu[category][food_name]

        save_menu(menu)

        print(Fore.GREEN + "\nFood deleted successfully!")

    elif confirm == "no":

        print(Fore.YELLOW + "\nDelete cancelled!")

    else:

        print(Fore.RED + "\nPlease enter yes or no!")


# =========================
# MENU MANAGEMENT
# =========================


def menu_management():

    while True:

        print(Fore.MAGENTA + "\n========== MENU MANAGEMENT ==========")

        print(Fore.CYAN + "1. Add Food")

        print(Fore.CYAN + "2. View Food")

        print(Fore.CYAN + "3. Update Food")

        print(Fore.CYAN + "4. Delete Food")

        print(Fore.YELLOW + "5. Back")

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
