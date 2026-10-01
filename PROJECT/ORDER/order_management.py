import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_DIR = os.path.join(BASE_DIR, "DATABASE")

MENU_FILE = os.path.join(DATABASE_DIR, "menu.json")
ORDER_FILE = os.path.join(DATABASE_DIR, "orders.json")


def load_menu():
    try:
        with open(MENU_FILE, "r") as file:
            return json.load(file)

    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def load_orders():
    if not os.path.exists(ORDER_FILE):
        return []

    try:
        with open(ORDER_FILE, "r") as file:
            return json.load(file)

    except (json.JSONDecodeError, FileNotFoundError):
        return []


def save_orders(orders):
    with open(ORDER_FILE, "w") as file:
        json.dump(orders, file, indent=4)


def generate_order_id(orders):
    if not orders:
        return "O001"

    last_id = orders[-1]["order_id"]
    number = int(last_id[1:]) + 1

    return f"O{number:03d}"


def get_customer_name():
    while True:
        name = input("Enter customer name: ").strip()

        if not name:
            print("Customer name cannot be empty!")
            continue

        if not all(char.isalpha() or char.isspace() for char in name):
            print("Name must contain only letters and spaces!")
            continue

        if len(name.replace(" ", "")) < 3:
            print("Name must contain at least 3 letters!")
            continue

        return name


def get_table_number():
    while True:
        table_no = input("Enter table number: ").strip().upper()

        if not table_no:
            print("Table number cannot be empty!")
            continue

        if not table_no.startswith("T"):
            print("Table number must start with T!")
            continue

        if not table_no[1:].isdigit():
            print("Invalid table number!")
            continue

        return table_no


def create_order():

    menu = load_menu()
    orders = load_orders()

    if not menu:
        print("\nNo menu items found!")
        return

    print("\n========== CREATE ORDER ==========")

    customer_name = get_customer_name()

    print("\n1. Dine-In")
    print("2. Takeaway")

    while True:
        order_type_choice = input("Select order type: ").strip()

        if order_type_choice == "1":
            order_type = "Dine-In"
            table_no = get_table_number()
            break

        elif order_type_choice == "2":
            order_type = "Takeaway"
            table_no = None
            break

        else:
            print("Invalid choice!")

    items = []
    total = 0

    while True:

        print("\n---------- CATEGORIES ----------")

        categories = list(menu.keys())

        for i, category in enumerate(categories, start=1):
            print(f"{i}. {category}")

        print("0. Finish Order")

        category_choice = input("\nEnter category: ").strip()

        if category_choice == "0":
            break

        if not category_choice.isdigit():
            print("Invalid category choice!")
            continue

        category_choice = int(category_choice)

        if category_choice < 1 or category_choice > len(categories):
            print("Invalid category choice!")
            continue

        category = categories[category_choice - 1]

        foods = menu[category]

        while True:

            print(f"\n---------- {category.upper()} ----------")

            food_names = list(foods.keys())

            for i, food_name in enumerate(food_names, start=1):

                price_data = foods[food_name]

                if isinstance(price_data, dict):

                    prices = []

                    for size, price in price_data.items():
                        prices.append(f"{size}: ₹{price}")

                    price_text = " | ".join(prices)

                    print(f"{i}. {food_name} ({price_text})")

                else:

                    print(f"{i}. {food_name} - ₹{price_data}")

            print("0. Back")

            food_choice = input("\nEnter food: ").strip()

            if food_choice == "0":
                break

            if not food_choice.isdigit():
                print("Invalid food choice!")
                continue

            food_choice = int(food_choice)

            if food_choice < 1 or food_choice > len(food_names):
                print("Invalid food choice!")
                continue

            food_name = food_names[food_choice - 1]

            price_data = foods[food_name]

            selected_size = ""
            selected_price = 0

            if isinstance(price_data, dict):

                sizes = list(price_data.keys())

                print(f"\n---------- {food_name} ----------")

                for i, size in enumerate(sizes, start=1):
                    print(f"{i}. {size} - ₹{price_data[size]}")

                while True:

                    size_choice = input("\nEnter size: ").strip()

                    if not size_choice.isdigit():
                        print("Invalid size choice!")
                        continue

                    size_choice = int(size_choice)

                    if size_choice < 1 or size_choice > len(sizes):
                        print("Invalid size choice!")
                        continue

                    selected_size = sizes[size_choice - 1]
                    selected_price = price_data[selected_size]

                    break

            else:

                selected_price = price_data
                selected_size = "Regular"

            while True:

                quantity = input("Enter quantity: ").strip()

                if not quantity.isdigit():
                    print("Quantity must contain only digits!")
                    continue

                quantity = int(quantity)

                if quantity <= 0:
                    print("Quantity must be greater than 0!")
                    continue

                break

            item_total = selected_price * quantity

            items.append(
                {
                    "category": category,
                    "name": food_name,
                    "size": selected_size,
                    "price": selected_price,
                    "quantity": quantity,
                    "total": item_total,
                }
            )

            total += item_total

            print(
                f"\n{food_name} ({selected_size}) " f"x {quantity} added successfully."
            )

            print(f"Item Total: ₹{item_total}")

            another = (
                input("\nAdd another food from this category? (y/n): ").strip().lower()
            )

            if another != "y":
                break

    if not items:
        print("\nNo food selected. Order cancelled.")
        return

    order = {
        "order_id": generate_order_id(orders),
        "customer_name": customer_name,
        "order_type": order_type,
        "table_no": table_no,
        "items": items,
        "total": total,
        "status": "Pending",
    }

    orders.append(order)

    save_orders(orders)

    print("\n========== ORDER CREATED ==========")

    print(f"Order ID     : {order['order_id']}")
    print(f"Customer     : {order['customer_name']}")
    print(f"Order Type   : {order['order_type']}")

    if order["order_type"] == "Dine-In":
        print(f"Table Number : {order['table_no']}")

    print("\nItems:")

    for item in order["items"]:

        print(
            f"{item['name']} "
            f"({item['size']}) x {item['quantity']} "
            f"= ₹{item['total']}"
        )

    print("-----------------------------------")

    print(f"Total        : ₹{order['total']}")
    print(f"Status       : {order['status']}")

    print("Order saved successfully!")


def view_orders():

    orders = load_orders()

    if not orders:
        print("\nNo orders found.")
        return

    print("\n========== ALL ORDERS ==========")

    for order in orders:

        print(f"\nOrder ID     : {order['order_id']}")
        print(f"Customer     : {order['customer_name']}")
        print(f"Table Number : {order['table_no']}")
        print(f"Status       : {order['status']}")

        print("\nItems:")

        for item in order["items"]:

            print(
                f"  {item['name']} "
                f"({item['size']}) "
                f"x {item['quantity']} "
                f"= ₹{item['total']}"
            )

        print(f"Total        : ₹{order['total']}")
        print("-" * 40)


def update_order_status():

    orders = load_orders()

    if not orders:
        print("\nNo orders found.")
        return

    print("\n========== ORDERS ==========")

    for order in orders:

        print(
            f"{order['order_id']} | "
            f"{order['customer_name']} | "
            f"Type: {order.get('order_type', 'Dine-In')} | "
            f"Table: {order.get('table_no') if order.get('order_type', 'Dine-In') == 'Dine-In' else 'N/A'} | "
            f"Status: {order['status']}"
        )

    order_id = input("\nEnter Order ID: ").strip().upper()

    selected_order = None

    for order in orders:

        if order["order_id"].upper() == order_id:

            selected_order = order
            break

    if selected_order is None:

        print("Invalid Order ID!")
        return

    if selected_order["status"] == "Cancelled":

        print("Cancelled order status cannot be changed!")
        return

    if selected_order["status"] == "Served":

        print("Order is already served!")
        return

    print("\n1. Pending")
    print("2. Preparing")
    print("3. Ready")
    print("4. Served")

    choice = input("Select new status: ").strip()

    status_list = {"1": "Pending", "2": "Preparing", "3": "Ready", "4": "Served"}

    if choice not in status_list:

        print("Invalid choice!")
        return

    selected_order["status"] = status_list[choice]

    save_orders(orders)

    print("\nOrder status updated successfully!")

    print(f"Order ID : {selected_order['order_id']}")
    print(f"Status   : {selected_order['status']}")


def cancel_order():

    orders = load_orders()

    if not orders:
        print("\nNo orders found.")
        return

    print("\n========== ORDERS ==========")

    for order in orders:

        print(
            f"{order['order_id']} | "
            f"{order['customer_name']} | "
            f"Type: {order.get('order_type', 'Dine-In')} | "
            f"Table: {order.get('table_no') if order.get('order_type', 'Dine-In') == 'Dine-In' else 'N/A'} | "
            f"Status: {order['status']}"
        )

    order_id = input("\nEnter Order ID: ").strip().upper()

    selected_order = None

    for order in orders:

        if order["order_id"].upper() == order_id:

            selected_order = order
            break

    if selected_order is None:

        print("Invalid Order ID!")
        return

    if selected_order["status"] == "Served":

        print("Served order cannot be cancelled!")
        return

    if selected_order["status"] == "Cancelled":

        print("Order is already cancelled!")
        return

    selected_order["status"] = "Cancelled"

    save_orders(orders)

    print("\nOrder cancelled successfully!")

    print(f"Order ID : {selected_order['order_id']}")
    print(f"Status   : {selected_order['status']}")


def order_menu():

    while True:

        print("\n========== ORDER MANAGEMENT ==========")

        print("1. Create Order")
        print("2. View Orders")
        print("3. Update Order Status")
        print("4. Cancel Order")
        print("5. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":

            create_order()

        elif choice == "2":

            view_orders()

        elif choice == "3":

            update_order_status()

        elif choice == "4":

            cancel_order()

        elif choice == "5":

            print("Exit Order Management.")
            break

        else:

            print("Invalid choice!")
