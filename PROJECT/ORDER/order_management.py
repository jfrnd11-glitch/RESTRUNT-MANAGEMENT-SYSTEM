import json
import os
import re

from PROJECT.LOGS.error_hendal import error_handler

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_DIR = os.path.join(BASE_DIR, "DATABASE")

MENU_FILE = os.path.join(DATABASE_DIR, "menu.json")
ORDER_FILE = os.path.join(DATABASE_DIR, "orders.json")


def log_error(function_name, message, level="ERROR"):
    try:
        if level == "WARNING":
            error_handler.log_warning("OrderManagement", function_name, message)
        else:
            error_handler.log_error("OrderManagement", function_name, message)
    except Exception:
        pass


def load_menu():
    try:
        with open(MENU_FILE, "r") as file:
            return json.load(file)

    except FileNotFoundError:
        log_error("load_menu", "menu.json file not found.")
        return {}

    except json.JSONDecodeError:
        log_error("load_menu", "menu.json contains invalid JSON.")
        return {}

    except Exception as e:
        log_error("load_menu", str(e))
        return {}


def load_orders():
    if not os.path.exists(ORDER_FILE):
        return []

    try:
        with open(ORDER_FILE, "r") as file:
            return json.load(file)

    except FileNotFoundError:
        return []

    except json.JSONDecodeError:
        log_error("load_orders", "orders.json contains invalid JSON.")
        return []

    except Exception as e:
        log_error("load_orders", str(e))
        return []


def save_orders(orders):
    try:
        os.makedirs(DATABASE_DIR, exist_ok=True)

        with open(ORDER_FILE, "w") as file:
            json.dump(orders, file, indent=4)

        return True

    except Exception as e:
        log_error("save_orders", str(e))
        print("Order database me save nahi ho saka.")
        return False


def generate_order_id(orders):
    if not orders:
        return "O001"

    try:
        last_id = orders[-1]["order_id"]
        number = int(last_id[1:]) + 1
        return f"O{number:03d}"

    except Exception as e:
        log_error("generate_order_id", str(e))
        return "O001"


def get_customer_name():

    while True:

        name = input("Enter customer name: ").strip()

        if not name:
            print("Customer name cannot be empty.")
            log_error("get_customer_name", "Customer name cannot be empty.", "WARNING")
            continue

        if not name.replace(" ", "").isalpha():
            print("Name must contain only letters and spaces.")
            log_error("get_customer_name", f"Invalid customer name: {name}", "WARNING")
            continue

        if len(name.replace(" ", "")) < 3:
            print("Name must contain at least 3 letters.")
            log_error(
                "get_customer_name", "Customer name has less than 3 letters.", "WARNING"
            )
            continue

        return name.title()


def get_table_number():

    while True:

        table_no = input("Enter table number (T01-T25): ").strip().upper()

        if not table_no:
            print("Table number cannot be empty.")
            log_error("get_table_number", "Table number cannot be empty.", "WARNING")
            continue

        if not re.fullmatch(r"T(0[1-9]|1[0-9]|2[0-5])", table_no):
            print("Invalid table number. Use T01 to T25.")
            log_error(
                "get_table_number", f"Invalid table number: {table_no}", "WARNING"
            )
            continue

        return table_no


def create_order():

    menu = load_menu()
    orders = load_orders()

    if not menu:
        print("\nNo menu items found.")
        log_error("create_order", "No menu items found.", "WARNING")
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

            print("Invalid choice. Please select 1 or 2.")

            log_error(
                "create_order",
                f"Invalid order type choice: {order_type_choice}",
                "WARNING",
            )

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

            print("Invalid category choice.")

            log_error(
                "create_order", f"Invalid category input: {category_choice}", "WARNING"
            )

            continue

        category_choice = int(category_choice)

        if category_choice < 1 or category_choice > len(categories):

            print("Invalid category choice.")

            log_error(
                "create_order",
                f"Category number out of range: {category_choice}",
                "WARNING",
            )

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

                    print(f"{i}. {food_name} " f"({' | '.join(prices)})")

                else:

                    print(f"{i}. {food_name} - ₹{price_data}")

            print("0. Back")

            food_choice = input("\nEnter food: ").strip()

            if food_choice == "0":
                break

            if not food_choice.isdigit():

                print("Invalid food choice.")

                log_error(
                    "create_order", f"Invalid food input: {food_choice}", "WARNING"
                )

                continue

            food_choice = int(food_choice)

            if food_choice < 1 or food_choice > len(food_names):

                print("Invalid food choice.")

                log_error(
                    "create_order",
                    f"Food number out of range: {food_choice}",
                    "WARNING",
                )

                continue

            food_name = food_names[food_choice - 1]
            price_data = foods[food_name]

            selected_size = "Regular"
            selected_price = 0

            if isinstance(price_data, dict):

                sizes = list(price_data.keys())

                print(f"\n---------- {food_name} ----------")

                for i, size in enumerate(sizes, start=1):
                    print(f"{i}. {size} - ₹{price_data[size]}")

                while True:

                    size_choice = input("\nEnter size: ").strip()

                    if not size_choice.isdigit():

                        print("Invalid size choice.")

                        log_error(
                            "create_order",
                            f"Invalid size input: {size_choice}",
                            "WARNING",
                        )

                        continue

                    size_choice = int(size_choice)

                    if size_choice < 1 or size_choice > len(sizes):

                        print("Invalid size choice.")

                        log_error(
                            "create_order",
                            f"Size number out of range: {size_choice}",
                            "WARNING",
                        )

                        continue

                    selected_size = sizes[size_choice - 1]
                    selected_price = price_data[selected_size]

                    break

            else:

                selected_price = price_data

            while True:

                quantity = input("Enter quantity: ").strip()

                if not quantity:

                    print("Quantity cannot be empty.")

                    log_error("create_order", "Quantity cannot be empty.", "WARNING")

                    continue

                if not quantity.isdigit():

                    print("Quantity must contain only digits.")

                    log_error(
                        "create_order", f"Invalid quantity: {quantity}", "WARNING"
                    )

                    continue

                quantity = int(quantity)

                if quantity <= 0:

                    print("Quantity must be greater than 0.")

                    log_error(
                        "create_order", f"Invalid quantity value: {quantity}", "WARNING"
                    )

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
                f"\n{food_name} "
                f"({selected_size}) x {quantity} "
                f"added successfully."
            )

            print(f"Item Total: ₹{item_total}")

            while True:

                another = (
                    input("\nAdd another food from this category? (y/n): ")
                    .strip()
                    .lower()
                )

                if another == "y":
                    break

                if another == "n":
                    break

                print("Please enter only y or n.")

                log_error("create_order", f"Invalid y/n choice: {another}", "WARNING")

            if another == "n":
                break

    if not items:

        print("\nNo food selected. Order cancelled.")

        log_error(
            "create_order", "Order cancelled because no food was selected.", "WARNING"
        )

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

    if not save_orders(orders):
        return

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
        print(f"Order Type   : {order.get('order_type', 'Dine-In')}")

        if order.get("order_type") == "Dine-In":
            print(f"Table Number : {order.get('table_no')}")
        else:
            print("Table Number : N/A")

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


def get_order_id():

    while True:

        order_id = input("\nEnter Order ID: ").strip().upper()

        if not order_id:

            print("Order ID cannot be empty.")

            log_error("get_order_id", "Order ID cannot be empty.", "WARNING")

            continue

        if not re.fullmatch(r"O\d{3}", order_id):

            print("Invalid Order ID. Example: O001")

            log_error("get_order_id", f"Invalid Order ID format: {order_id}", "WARNING")

            continue

        return order_id


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
            f"Table: "
            f"{order.get('table_no') if order.get('order_type', 'Dine-In') == 'Dine-In' else 'N/A'} | "
            f"Status: {order['status']}"
        )

    order_id = get_order_id()

    selected_order = None

    for order in orders:

        if order["order_id"].upper() == order_id:
            selected_order = order
            break

    if selected_order is None:

        print("Order ID not found.")

        log_error("update_order_status", f"Order ID not found: {order_id}", "WARNING")

        return

    if selected_order["status"] == "Cancelled":

        print("Cancelled order status cannot be changed.")

        log_error(
            "update_order_status",
            f"Attempted to update cancelled order: {order_id}",
            "WARNING",
        )

        return

    if selected_order["status"] == "Served":

        print("Order is already served.")

        log_error(
            "update_order_status",
            f"Attempted to update served order: {order_id}",
            "WARNING",
        )

        return

    print("\n1. Pending")
    print("2. Preparing")
    print("3. Ready")
    print("4. Served")

    while True:

        choice = input("Select new status: ").strip()

        statuses = {"1": "Pending", "2": "Preparing", "3": "Ready", "4": "Served"}

        if choice in statuses:
            break

        print("Invalid choice. Please select 1 to 4.")

        log_error("update_order_status", f"Invalid status choice: {choice}", "WARNING")

    selected_order["status"] = statuses[choice]

    if not save_orders(orders):
        return

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
            f"Table: "
            f"{order.get('table_no') if order.get('order_type', 'Dine-In') == 'Dine-In' else 'N/A'} | "
            f"Status: {order['status']}"
        )

    order_id = get_order_id()

    selected_order = None

    for order in orders:

        if order["order_id"].upper() == order_id:
            selected_order = order
            break

    if selected_order is None:

        print("Order ID not found.")

        log_error("cancel_order", f"Order ID not found: {order_id}", "WARNING")

        return

    if selected_order["status"] == "Served":

        print("Served order cannot be cancelled.")

        log_error(
            "cancel_order", f"Attempted to cancel served order: {order_id}", "WARNING"
        )

        return

    if selected_order["status"] == "Cancelled":

        print("Order is already cancelled.")

        log_error("cancel_order", f"Order already cancelled: {order_id}", "WARNING")

        return

    selected_order["status"] = "Cancelled"

    if not save_orders(orders):
        return

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

            print("Invalid choice. Please select 1 to 5.")

            log_error("order_menu", f"Invalid menu choice: {choice}", "WARNING")
