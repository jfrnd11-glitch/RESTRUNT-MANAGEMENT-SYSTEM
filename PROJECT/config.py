import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_DIR = os.path.join(BASE_DIR, "DATABASE")

USER_FILE = os.path.join(DATABASE_DIR, "users.json")
MENU_FILE = os.path.join(DATABASE_DIR, "menu.json")
BOOKING_FILE = os.path.join(DATABASE_DIR, "booking.json")
ORDER_FILE = os.path.join(DATABASE_DIR, "orders.json")
BILL_FILE = os.path.join(DATABASE_DIR, "bills.json")
HISTORY_FILE = os.path.join(DATABASE_DIR, "history.json")
INVENTORY_FILE = os.path.join(DATABASE_DIR, "inventry.json")

LOW_STOCK_LIMIT = 5