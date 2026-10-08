import json
import os
from colorama import init, Fore

init(autoreset=True)
from PROJECT.config import MENU_FILE
FILE_NAME = MENU_FILE

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


class MenuManagement:

    def load_menu(self):
        try:
            with open(FILE_NAME, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError:
            print(Fore.RED + "menu.json file contains invalid JSON!")
            return {}

    def save_menu(self, menu):
        os.makedirs(os.path.dirname(FILE_NAME), exist_ok=True)
        with open(FILE_NAME, "w") as file:
            json.dump(menu, file, indent=4)

    def get_name(self):
        while True:
            name = input(Fore.CYAN + "Food Name: ").strip()

            if len(name) < 2:
                print(Fore.RED + "Food name must contain at least 2 characters!")
            elif not all(char.isalpha() or char.isspace() for char in name):
                print(Fore.RED + "Food name can contain only letters and spaces!")
            else:
                return name

    def get_price(self):
        while True:
            try:
                price = float(input(Fore.CYAN + "Price: ").strip())

                if price <= 0:
                    print(Fore.RED + "Price must be greater than 0!")
                    continue

                return int(price) if price.is_integer() else price
            except ValueError:
                print(Fore.RED + "Please enter a valid price!")

    def select_category(self):
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

    def select_price_type(self):
        print(Fore.YELLOW + "\nSelect Price Type:")
        print("1. Single Price")
        print("2. Half / Full")
        print("3. Small / Medium / Full")
        print("4. Small / Medium / Large")
        print("5. Medium / Large")

        price_types = {
            "1": ["Price"],
            "2": ["Half", "Full"],
            "3": ["Small", "Medium", "Full"],
            "4": ["Small", "Medium", "Large"],
            "5": ["Medium", "Large"],
        }

        while True:
            choice = input(Fore.CYAN + "Enter choice: ").strip()

            if choice in price_types:
                return price_types[choice]

            print(Fore.RED + "Invalid choice!")

    def get_size_prices(self, sizes):
        if sizes == ["Price"]:
            return self.get_price()

        prices = {}

        for size in sizes:
            print(Fore.YELLOW + f"\n{size} Price")
            prices[size] = self.get_price()

        return prices

    def add_food(self):
        menu = self.load_menu()
        print(Fore.MAGENTA + "\n========== ADD FOOD ==========")

        category = self.select_category()
        food_name = self.get_name()

        if food_name in menu.get(category, {}):
            print(Fore.RED + "Food already exists in this category!")
            return

        sizes = self.select_price_type()
        menu.setdefault(category, {})[food_name] = self.get_size_prices(sizes)
        self.save_menu(menu)

        print(Fore.GREEN + "\nFood added successfully!")

    def print_menu_table(self, foods):
        food_list = list(foods.items())

        if all(not isinstance(price, dict) for _, price in food_list):
            print("+----+------------------------------+--------+")
            print("| No | Item Name                    | Price  |")
            print("+----+------------------------------+--------+")

            for index, (name, price) in enumerate(food_list, 1):
                print(f"| {index:<2} | {name:<28} | ₹{price:<5} |")

            print("+----+------------------------------+--------+")
            return

        sizes = []
        for _, price in food_list:
            if isinstance(price, dict):
                for size in price:
                    if size not in sizes:
                        sizes.append(size)

        mixed = any(not isinstance(price, dict) for _, price in food_list)
        line = "+----+------------------------------+" + "----------+" * len(sizes)
        if mixed:
            line += "--------+"

        print(line)
        print("| No | Item Name                    |", end="")

        for size in sizes:
            print(f" {size:<8} |", end="")

        print(" Price  |" if mixed else "")
        print(line)

        for index, (name, price) in enumerate(food_list, 1):
            print(f"| {index:<2} | {name:<28} |", end="")

            for size in sizes:
                amount = price.get(size, "-") if isinstance(price, dict) else "-"
                value = f"₹{amount}" if amount != "-" else "-"
                print(f" {value:<8} |", end="")

            if mixed:
                amount = price if not isinstance(price, dict) else "-"
                value = f"₹{amount}" if amount != "-" else "-"
                print(f" {value:<6} |")
            else:
                print()

        print(line)

    def view_food(self):
        menu = self.load_menu()
        print(Fore.MAGENTA + "\n========== MENU ==========")

        if not menu:
            print(Fore.YELLOW + "No food available!")
            return

        for category, foods in menu.items():
            if foods:
                print(Fore.YELLOW + f"\n========== {category.upper()} ==========")
                self.print_menu_table(foods)

    def find_food(self, menu):
        category = self.select_category()

        if not menu.get(category):
            print(Fore.RED + "\nNo food found in this category!")
            return None, None

        foods = list(menu[category])

        print(Fore.YELLOW + f"\n--- {category} ---")
        for index, name in enumerate(foods, 1):
            print(f"{index}. {name}")

        while True:
            try:
                choice = int(input(Fore.CYAN + "Enter food choice: ").strip())

                if 1 <= choice <= len(foods):
                    return category, foods[choice - 1]

                print(Fore.RED + "Invalid food choice!")
            except ValueError:
                print(Fore.RED + "Please enter a number!")

    def update_food(self):
        menu = self.load_menu()
        print(Fore.MAGENTA + "\n========== UPDATE FOOD ==========")

        category, name = self.find_food(menu)
        if name is None:
            return

        print("\n1. Update Name")
        print("2. Update Category")
        print("3. Update Price")
        print("4. Back")

        while True:
            choice = input(Fore.CYAN + "Enter choice: ").strip()

            if choice == "1":
                new_name = self.get_name()

                if new_name != name and new_name in menu[category]:
                    print(Fore.RED + "Food already exists!")
                    continue

                menu[category][new_name] = menu[category].pop(name)
                self.save_menu(menu)
                print(Fore.GREEN + "Food name updated successfully!")
                break

            elif choice == "2":
                new_category = self.select_category()

                if new_category == category:
                    print(Fore.YELLOW + "Food is already in this category!")
                    continue

                if name in menu.get(new_category, {}):
                    print(Fore.RED + "Food already exists in this category!")
                    continue

                menu.setdefault(new_category, {})[name] = menu[category].pop(name)
                self.save_menu(menu)
                print(Fore.GREEN + "Food category updated successfully!")
                break

            elif choice == "3":
                old_price = menu[category][name]

                if isinstance(old_price, dict):
                    sizes = list(old_price)

                    for index, size in enumerate(sizes, 1):
                        print(f"{index}. {size} - ₹{old_price[size]}")

                    while True:
                        try:
                            selected = int(input("Enter size choice: ").strip())

                            if 1 <= selected <= len(sizes):
                                size = sizes[selected - 1]
                                menu[category][name][size] = self.get_price()
                                break

                            print(Fore.RED + "Invalid choice!")
                        except ValueError:
                            print(Fore.RED + "Please enter a number!")
                else:
                    menu[category][name] = self.get_price()

                self.save_menu(menu)
                print(Fore.GREEN + "Food price updated successfully!")
                break

            elif choice == "4":
                break

            else:
                print(Fore.RED + "Invalid choice!")

    def delete_food(self):
        menu = self.load_menu()
        print(Fore.MAGENTA + "\n========== DELETE FOOD ==========")

        category, name = self.find_food(menu)
        if name is None:
            return

        print(Fore.YELLOW + f"\nFood: {name}")
        print(Fore.YELLOW + f"Category: {category}")

        price = menu[category][name]
        if isinstance(price, dict):
            for size, amount in price.items():
                print(f"{size}: ₹{amount}")
        else:
            print(f"Price: ₹{price}")

        confirm = input("Are you sure? (yes/no): ").strip().lower()

        if confirm == "yes":
            del menu[category][name]
            self.save_menu(menu)
            print(Fore.GREEN + "Food deleted successfully!")
        elif confirm == "no":
            print(Fore.YELLOW + "Delete cancelled!")
        else:
            print(Fore.RED + "Please enter yes or no!")

    def show(self):
        while True:
            print(Fore.MAGENTA + "\n========== MENU MANAGEMENT ==========")
            print(Fore.CYAN + "1. Add Food")
            print(Fore.CYAN + "2. View Food")
            print(Fore.CYAN + "3. Update Food")
            print(Fore.CYAN + "4. Delete Food")
            print(Fore.YELLOW + "5. Back")

            choice = input(Fore.CYAN + "Enter choice: ").strip()

            if choice == "1":
                self.add_food()
            elif choice == "2":
                self.view_food()
            elif choice == "3":
                self.update_food()
            elif choice == "4":
                self.delete_food()
            elif choice == "5":
                break
            else:
                print(Fore.RED + "Invalid choice!")


def menu_management():
    MenuManagement().show()
