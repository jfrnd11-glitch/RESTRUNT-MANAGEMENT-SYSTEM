import json
import os
import re
from PROJECT.LOGS.error_hendal import error_handler
from PROJECT.config import MENU_FILE, ORDER_FILE

class OrderManagement:

    def log_error(self, function_name, message, level="ERROR"):
        try:
            if level == "WARNING":
                error_handler.log_warning("OrderManagement", function_name, message)
            else:
                error_handler.log_error("OrderManagement", function_name, message)
        except Exception:
            pass

    def load_menu(self):
        try:
            with open(MENU_FILE, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            self.log_error("load_menu", "menu.json file not found.")
        except json.JSONDecodeError:
            self.log_error("load_menu", "Invalid menu.json.")
        except Exception as e:
            self.log_error("load_menu", str(e))
        return {}

    def load_orders(self):
        if not os.path.exists(ORDER_FILE):
            return []

        try:
            with open(ORDER_FILE, "r") as file:
                return json.load(file)
        except Exception as e:
            self.log_error("load_orders", str(e))
            return []

    def save_orders(self, orders):
        try:
            os.makedirs(exist_ok=True)

            with open(ORDER_FILE, "w") as file:
                json.dump(orders, file, indent=4)

            return True
        except Exception as e:
            self.log_error("save_orders", str(e))
            print("Order not saved in database.")
            return False

    def generate_order_id(self, orders):
        numbers = [
            int(order["order_id"][1:])
            for order in orders
            if re.fullmatch(r"O\d+", order.get("order_id", ""))
        ]
        return f"O{max(numbers, default=0) + 1:03d}"

    def get_table_number(self):
        while True:
            table_no = input("Enter table number (T01-T25): ").strip().upper()

            if re.fullmatch(r"T(0[1-9]|1[0-9]|2[0-5])", table_no):
                return table_no

            print("Invalid table number. Use T01 to T25.")
            self.log_error("get_table_number", f"Invalid table: {table_no}", "WARNING")

    def show_orders(self, orders, title="========== ORDERS =========="):
        print(f"\n{title}")

        for order in orders:
            order_type = order.get("order_type", "Dine-In")
            table = order.get("table_no") or "N/A"

            print(
                f"{order.get('order_id', 'N/A')} | "
                f"Type: {order_type} | Table: {table} | "
                f"Status: {order.get('status', 'N/A')}"
            )

    def find_order(self, orders, order_id):
        for order in orders:
            if order.get("order_id", "").upper() == order_id:
                return order
        return None

    def get_order_id(self):
        while True:
            order_id = input("\nEnter Order ID: ").strip().upper()

            if re.fullmatch(r"O\d{3}", order_id):
                return order_id

            print("Invalid Order ID. Example: O001")
            self.log_error("get_order_id", f"Invalid Order ID: {order_id}", "WARNING")

    def create_order(self):
        menu = self.load_menu()
        orders = self.load_orders()

        if not menu:
            print("\nNo menu items found.")
            self.log_error("create_order", "No menu items found.", "WARNING")
            return

        print("\n========== CREATE ORDER ==========")
        print("1. Dine-In")
        print("2. Takeaway")

        while True:
            choice = input("Select order type: ").strip()

            if choice == "1":
                order_type = "Dine-In"
                table_no = self.get_table_number()
                break
            elif choice == "2":
                order_type = "Takeaway"
                table_no = None
                break

            print("Select 1 or 2.")
            self.log_error("create_order", f"Invalid order type: {choice}", "WARNING")

        items = []

        while True:
            categories = list(menu.keys())

            print("\n---------- CATEGORIES ----------")
            for i, category in enumerate(categories, 1):
                print(f"{i}. {category}")
            print("0. Finish Order")

            choice = input("Enter category: ").strip()

            if choice == "0":
                break

            if not choice.isdigit() or not 1 <= int(choice) <= len(categories):
                print("Invalid category choice.")
                self.log_error("create_order", f"Invalid category: {choice}", "WARNING")
                continue

            category = categories[int(choice) - 1]
            foods = menu[category]
            food_names = list(foods.keys())

            while True:
                print(f"\n---------- {category.upper()} ----------")

                for i, name in enumerate(food_names, 1):
                    price_data = foods[name]

                    if isinstance(price_data, dict):
                        prices = " | ".join(
                            f"{size}: ₹{price}" for size, price in price_data.items()
                        )
                        print(f"{i}. {name} ({prices})")
                    else:
                        print(f"{i}. {name} - ₹{price_data}")

                print("0. Back")
                choice = input("Enter food: ").strip()

                if choice == "0":
                    break

                if not choice.isdigit() or not 1 <= int(choice) <= len(food_names):
                    print("Invalid food choice.")
                    self.log_error("create_order", f"Invalid food: {choice}", "WARNING")
                    continue

                food_name = food_names[int(choice) - 1]
                price_data = foods[food_name]
                selected_size = "Regular"

                if isinstance(price_data, dict):
                    sizes = list(price_data.keys())

                    for i, size in enumerate(sizes, 1):
                        print(f"{i}. {size} - ₹{price_data[size]}")

                    size_choice = input("Enter size: ").strip()

                    if not size_choice.isdigit() or not 1 <= int(size_choice) <= len(sizes):
                        print("Invalid size choice.")
                        self.log_error("create_order", f"Invalid size: {size_choice}", "WARNING")
                        continue

                    selected_size = sizes[int(size_choice) - 1]
                    selected_price = float(price_data[selected_size])
                else:
                    selected_price = float(price_data)

                quantity_input = input("Enter quantity: ").strip()

                if not quantity_input.isdigit() or int(quantity_input) <= 0:
                    print("Quantity must be greater than 0.")
                    self.log_error("create_order", f"Invalid quantity: {quantity_input}", "WARNING")
                    continue

                quantity = int(quantity_input)
                item_total = round(selected_price * quantity, 2)

                items.append({
                    "category": category,
                    "name": food_name,
                    "size": selected_size,
                    "price": selected_price,
                    "quantity": quantity,
                    "total": item_total
                })

                print(f"{food_name} ({selected_size}) x {quantity} = ₹{item_total:.2f}")

                another = input("Add another food from this category? (y/n): ").strip().lower()
                if another != "y":
                    break

        if not items:
            print("No food selected. Order cancelled.")
            self.log_error("create_order", "No items selected.", "WARNING")
            return

        total = round(sum(item["total"] for item in items), 2)

        order = {
            "order_id": self.generate_order_id(orders),
            "order_type": order_type,
            "table_no": table_no,
            "items": items,
            "total": total,
            "status": "Pending"
        }

        orders.append(order)

        if not self.save_orders(orders):
            return

        print("\n========== ORDER CREATED ==========")
        print("Order ID:", order["order_id"])
        print("Order Type:", order_type)

        if table_no:
            print("Table Number:", table_no)

        for item in items:
            print(
                f"{item['name']} ({item['size']}) x "
                f"{item['quantity']} = ₹{item['total']:.2f}"
            )

        print(f"Total: ₹{total:.2f}")
        print("Status:", order["status"])
        print("Order saved successfully!")

    def view_orders(self):
        orders = self.load_orders()

        if not orders:
            print("\nNo orders found.")
            return

        for order in orders:
            self.show_orders([order], "========== ORDER DETAILS ==========")

            for item in order.get("items", []):
                print(
                    f"{item.get('name', 'Unknown')} "
                    f"({item.get('size', 'Regular')}) x "
                    f"{item.get('quantity', 1)} = "
                    f"₹{float(item.get('total', 0)):.2f}"
                )

            print(f"Total: ₹{float(order.get('total', 0)):.2f}")
            print("-" * 40)

    def update_order_status(self):
        orders = self.load_orders()

        if not orders:
            print("\nNo orders found.")
            return

        self.show_orders(orders)
        order_id = self.get_order_id()
        order = self.find_order(orders, order_id)

        if order is None:
            print("Order ID not found.")
            self.log_error("update_order_status", f"Order not found: {order_id}", "WARNING")
            return

        if order.get("status") in ("Cancelled", "Served"):
            print("This order status cannot be changed.")
            return

        statuses = {
            "1": "Pending",
            "2": "Preparing",
            "3": "Ready",
            "4": "Served"
        }

        for key, status in statuses.items():
            print(f"{key}. {status}")

        choice = input("Select new status: ").strip()

        if choice not in statuses:
            print("Invalid choice.")
            self.log_error("update_order_status", f"Invalid status: {choice}", "WARNING")
            return

        order["status"] = statuses[choice]

        if self.save_orders(orders):
            print("Order status updated successfully!")

    def cancel_order(self):
        orders = self.load_orders()

        if not orders:
            print("\nNo orders found.")
            return

        self.show_orders(orders)
        order_id = self.get_order_id()
        order = self.find_order(orders, order_id)

        if order is None:
            print("Order ID not found.")
            self.log_error("cancel_order", f"Order not found: {order_id}", "WARNING")
            return

        if order.get("status") == "Served":
            print("Served order cannot be cancelled.")
            return

        if order.get("status") == "Cancelled":
            print("Order is already cancelled.")
            return

        order["status"] = "Cancelled"

        if self.save_orders(orders):
            print("Order cancelled successfully!")

    def show(self):
        while True:
            print("\n========== ORDER MANAGEMENT ==========")
            print("1. Create Order")
            print("2. View Orders")
            print("3. Update Order Status")
            print("4. Cancel Order")
            print("5. Exit")

            choice = input("Enter your choice: ").strip()

            if choice == "1":
                self.create_order()
            elif choice == "2":
                self.view_orders()
            elif choice == "3":
                self.update_order_status()
            elif choice == "4":
                self.cancel_order()
            elif choice == "5":
                print("Exit Order Management.")
                break
            else:
                print("Invalid choice.")
                self.log_error("show", f"Invalid choice: {choice}", "WARNING")


def order_menu():
    OrderManagement().show()