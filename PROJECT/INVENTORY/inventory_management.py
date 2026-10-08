import json
import os
from PROJECT.LOGS.error_hendal import error_handler

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_DIR = os.path.join(BASE_DIR, "DATABASE")
INVENTORY_FILE = os.path.join(DATABASE_DIR, "inventory.json")
LOW_STOCK_LIMIT = 10


class InventoryManagement:

    def load_inventory(self):
        if not os.path.exists(INVENTORY_FILE):
            return []

        try:
            with open(INVENTORY_FILE, "r") as file:
                return json.load(file)
        except Exception as e:
            error_handler.log_exception("InventoryManagement", "load_inventory", e)
            return []

    def save_inventory(self, inventory):
        try:
            os.makedirs(DATABASE_DIR, exist_ok=True)

            with open(INVENTORY_FILE, "w") as file:
                json.dump(inventory, file, indent=4)
        except Exception as e:
            error_handler.log_exception("InventoryManagement", "save_inventory", e)
            print("Inventory save karne me error aaya!")

    def generate_item_id(self, inventory):
        if not inventory:
            return "I001"

        number = max(int(item["item_id"][1:]) for item in inventory) + 1
        return f"I{number:03d}"

    def add_item(self):
        try:
            inventory = self.load_inventory()

            name = input("\nEnter Item Name: ").strip()
            if not name:
                print("Item name cannot be empty!")
                return

            category = input("Enter Category: ").strip()
            if not category:
                print("Category cannot be empty!")
                return

            quantity = input("Enter Quantity: ").strip()
            if not quantity.isdigit():
                print("Quantity must be a number!")
                return

            unit = input("Enter Unit (kg/litre/packet/piece): ").strip()
            if not unit:
                print("Unit cannot be empty!")
                return

            if any(item["name"].lower() == name.lower() for item in inventory):
                print("Item already exists!")
                return

            item = {
                "item_id": self.generate_item_id(inventory),
                "name": name,
                "category": category,
                "quantity": int(quantity),
                "unit": unit
            }

            inventory.append(item)
            self.save_inventory(inventory)

            print("\nInventory item added successfully!")
            print("Item ID:", item["item_id"])

        except Exception as e:
            error_handler.log_exception("InventoryManagement", "add_item", e)
            print("Item add karte waqt error aaya!")

    def view_inventory(self):
        try:
            inventory = self.load_inventory()

            if not inventory:
                print("\nNo inventory items found.")
                return

            print("\n" + "=" * 75)
            print("INVENTORY")
            print("=" * 75)
            print(f"{'ID':<8}{'ITEM NAME':<25}{'CATEGORY':<18}{'QUANTITY':<12}{'UNIT':<10}")
            print("-" * 75)

            for item in inventory:
                print(
                    f"{item.get('item_id', 'N/A'):<8}"
                    f"{item.get('name', 'N/A'):<25}"
                    f"{item.get('category', 'N/A'):<18}"
                    f"{item.get('quantity', 0):<12}"
                    f"{item.get('unit', ''):<10}"
                )

            print("=" * 75)

        except Exception as e:
            error_handler.log_exception("InventoryManagement", "view_inventory", e)
            print("Inventory dekhne me error aaya!")

    def update_stock(self):
        try:
            inventory = self.load_inventory()

            if not inventory:
                print("\nNo inventory items found.")
                return

            self.view_inventory()
            item_id = input("\nEnter Item ID: ").strip().upper()

            item = next(
                (i for i in inventory if i.get("item_id", "").upper() == item_id),
                None
            )

            if item is None:
                print("Invalid Item ID!")
                return

            quantity = input("Enter New Quantity: ").strip()
            if not quantity.isdigit():
                print("Quantity must be a number!")
                return

            item["quantity"] = int(quantity)
            self.save_inventory(inventory)
            print("\nStock updated successfully!")

        except Exception as e:
            error_handler.log_exception("InventoryManagement", "update_stock", e)
            print("Stock update karte waqt error aaya!")

    def delete_item(self):
        try:
            inventory = self.load_inventory()

            if not inventory:
                print("\nNo inventory items found.")
                return

            self.view_inventory()
            item_id = input("\nEnter Item ID: ").strip().upper()

            item = next(
                (i for i in inventory if i.get("item_id", "").upper() == item_id),
                None
            )

            if item is None:
                print("Invalid Item ID!")
                return

            inventory.remove(item)
            self.save_inventory(inventory)
            print("\nInventory item deleted successfully!")

        except Exception as e:
            error_handler.log_exception("InventoryManagement", "delete_item", e)
            print("Item delete karte waqt error aaya!")

    def low_stock(self):
        try:
            inventory = self.load_inventory()

            if not inventory:
                print("\nNo inventory items found.")
                return

            print("\n" + "=" * 60)
            print("LOW STOCK ITEMS")
            print("=" * 60)
            print(f"{'ID':<8}{'ITEM NAME':<25}{'QUANTITY':<12}{'UNIT':<10}")
            print("-" * 60)

            found = False

            for item in inventory:
                if int(item.get("quantity", 0)) <= LOW_STOCK_LIMIT:
                    print(
                        f"{item.get('item_id', 'N/A'):<8}"
                        f"{item.get('name', 'N/A'):<25}"
                        f"{item.get('quantity', 0):<12}"
                        f"{item.get('unit', ''):<10}"
                    )
                    found = True

            if not found:
                print("No low stock items.")

            print("=" * 60)

        except Exception as e:
            error_handler.log_exception("InventoryManagement", "low_stock", e)
            print("Low stock check karte waqt error aaya!")

    def show(self):
        while True:
            print("\n========== INVENTORY MANAGEMENT ==========")
            print("1. Add Item")
            print("2. View Inventory")
            print("3. Update Stock")
            print("4. Delete Item")
            print("5. Low Stock")
            print("6. Exit")

            choice = input("Enter choice: ").strip()

            if choice == "1":
                self.add_item()
            elif choice == "2":
                self.view_inventory()
            elif choice == "3":
                self.update_stock()
            elif choice == "4":
                self.delete_item()
            elif choice == "5":
                self.low_stock()
            elif choice == "6":
                print("Inventory Management closed.")
                break
            else:
                error_handler.log_warning(
                    "InventoryManagement", "show", "Invalid menu choice"
                )
                print("Invalid choice!")


def inventory_menu():
    InventoryManagement().show()