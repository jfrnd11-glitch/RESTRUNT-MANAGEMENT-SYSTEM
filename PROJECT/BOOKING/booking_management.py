import json
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_DIR = os.path.join(BASE_DIR, "DATABASE")
FILE_NAME = os.path.join(DATABASE_DIR, "booking.json")


TABLES = {
    "2": ["T01", "T02", "T03", "T04", "T05", "T06", "T07", "T08", "T09", "T10"],
    "4": ["T11", "T12", "T13", "T14", "T15", "T16", "T17", "T18", "T19", "T20"],
    "6": ["T21", "T22", "T23", "T24", "T25"],
}


def load_bookings():
    if not os.path.exists(FILE_NAME):
        return []

    try:
        with open(FILE_NAME, "r") as file:
            return json.load(file)

    except (json.JSONDecodeError, FileNotFoundError):
        return []


def save_bookings(bookings):
    os.makedirs(DATABASE_DIR, exist_ok=True)

    with open(FILE_NAME, "w") as file:
        json.dump(bookings, file, indent=4)


def get_customer_name():
    while True:
        name = input("\nEnter Customer Name: ").strip()

        if len(name) < 3:
            print("Name must contain at least 3 characters.")
        elif not name.replace(" ", "").isalpha():
            print("Name must contain only letters and spaces.")
        else:
            return name.title()


def get_mobile(bookings, current_mobile=None):
    while True:
        mobile = input("Enter Mobile Number: ").strip()

        if not mobile.isdigit():
            print("Mobile number must contain only digits.")

        elif len(mobile) != 10:
            print("Mobile number must be exactly 10 digits.")

        elif mobile == current_mobile:
            return mobile

        else:
            return mobile


def get_booking_date():
    while True:
        date = input("Enter Booking Date (DD-MM-YYYY): ").strip()

        try:
            booking_date = datetime.strptime(date, "%d-%m-%Y")
            today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

            if booking_date < today:
                print("Booking date cannot be in the past.")
            else:
                return date

        except ValueError:
            print("Invalid date. Use DD-MM-YYYY.")


def get_booking_time():
    while True:
        time = input("Enter Booking Time (HH:MM AM/PM): ").strip().upper()

        try:
            datetime.strptime(time, "%I:%M %p")
            return time

        except ValueError:
            print("Invalid time. Use HH:MM AM/PM.")


def get_guests():
    while True:
        guests = input("Enter Number of Guests: ").strip()

        if not guests.isdigit():
            print("Guests must be a number.")
            continue

        guests = int(guests)

        if guests < 1:
            print("Guests must be at least 1.")

        elif guests > 30:
            print("Maximum 30 guests allowed.")

        else:
            return guests


def get_tables_for_guests(guests):
    tables = []

    while guests >= 6:
        tables.append("6")
        guests -= 6

    if guests > 4:
        tables.append("6")

    elif guests > 2:
        tables.append("4")

    elif guests > 0:
        tables.append("2")

    return tables


def get_available_tables(bookings, booking_date, booking_time):
    booked_tables = []

    for booking in bookings:

        if booking.get("status") == "Cancelled":
            continue

        if (
            booking.get("booking_date") == booking_date
            and booking.get("booking_time") == booking_time
        ):
            booked_tables.extend(booking.get("table_number", []))

    available_tables = {}

    for size, tables in TABLES.items():
        available_tables[size] = [
            table for table in tables if table not in booked_tables
        ]

    return available_tables


def show_available_tables(bookings, booking_date, booking_time):
    available = get_available_tables(bookings, booking_date, booking_time)

    print("\n=========================================")
    print("          AVAILABLE TABLES")
    print("=========================================")

    print(f"Date : {booking_date}")
    print(f"Time : {booking_time}")

    for size, tables in available.items():

        print(f"\n{size}-Seater Tables:")

        if tables:
            print("  " + ", ".join(tables))
        else:
            print("  No tables available.")


def select_tables(bookings, guests, booking_date, booking_time):
    required_tables = get_tables_for_guests(guests)

    available = get_available_tables(bookings, booking_date, booking_time)

    selected_tables = []

    print("\n=========================================")
    print("          TABLE SELECTION")
    print("=========================================")

    print(f"Guests: {guests}")

    for size in required_tables:

        available_tables = available.get(size, [])

        if not available_tables:
            print(f"\nNo {size}-seater table available.")
            return None

        print(f"\nAvailable {size}-seater tables:")
        print(", ".join(available_tables))

        while True:
            table = input(f"Select {size}-seater table: ").strip().upper()

            if table not in available_tables:
                print("Invalid or unavailable table.")
                continue

            if table in selected_tables:
                print("Table already selected.")
                continue

            selected_tables.append(table)
            break

    return selected_tables


def generate_booking_id(bookings):
    number = len(bookings) + 1

    while True:
        booking_id = f"B{number:04d}"

        if not any(booking.get("booking_id") == booking_id for booking in bookings):
            return booking_id

        number += 1


def new_booking():
    bookings = load_bookings()

    print("\n=========================================")
    print("             NEW BOOKING")
    print("=========================================")

    customer_name = get_customer_name()
    mobile = get_mobile(bookings)
    booking_date = get_booking_date()
    booking_time = get_booking_time()
    guests = get_guests()

    show_available_tables(bookings, booking_date, booking_time)

    tables = select_tables(bookings, guests, booking_date, booking_time)

    if not tables:
        print("\nBooking could not be completed.")
        return

    booking_id = generate_booking_id(bookings)

    booking = {
        "booking_id": booking_id,
        "customer_name": customer_name,
        "mobile": mobile,
        "booking_date": booking_date,
        "booking_time": booking_time,
        "guests": guests,
        "table_number": tables,
        "status": "Pending",
    }

    bookings.append(booking)
    save_bookings(bookings)

    print("\n=========================================")
    print("       BOOKING CREATED SUCCESSFULLY")
    print("=========================================")
    print(f"Booking ID : {booking_id}")
    print(f"Customer   : {customer_name}")
    print(f"Mobile     : {mobile}")
    print(f"Date       : {booking_date}")
    print(f"Time       : {booking_time}")
    print(f"Guests     : {guests}")
    print(f"Tables     : {', '.join(tables)}")
    print("Status     : Pending")


def view_bookings():
    bookings = load_bookings()

    if not bookings:
        print("\nNo bookings found.")
        return

    print("\n=========================================")
    print("             ALL BOOKINGS")
    print("=========================================")

    for booking in bookings:
        print("\n-----------------------------------------")
        print(f"Booking ID : {booking['booking_id']}")
        print(f"Customer   : {booking['customer_name']}")
        print(f"Mobile     : {booking['mobile']}")
        print(f"Date       : {booking['booking_date']}")
        print(f"Time       : {booking['booking_time']}")
        print(f"Guests     : {booking['guests']}")
        print(f"Tables     : {', '.join(booking['table_number'])}")
        print(f"Status     : {booking['status']}")

    print("-----------------------------------------")


def search_booking():
    bookings = load_bookings()

    if not bookings:
        print("\nNo bookings found.")
        return

    booking_id = input("\nEnter Booking ID: ").strip().upper()

    for booking in bookings:

        if booking["booking_id"] == booking_id:

            print("\n=========================================")
            print("          BOOKING DETAILS")
            print("=========================================")

            print(f"Booking ID : {booking['booking_id']}")
            print(f"Customer   : {booking['customer_name']}")
            print(f"Mobile     : {booking['mobile']}")
            print(f"Date       : {booking['booking_date']}")
            print(f"Time       : {booking['booking_time']}")
            print(f"Guests     : {booking['guests']}")
            print(f"Tables     : {', '.join(booking['table_number'])}")
            print(f"Status     : {booking['status']}")

            return

    print("\nBooking not found.")


def update_booking():
    bookings = load_bookings()

    if not bookings:
        print("\nNo bookings found.")
        return

    booking_id = input("\nEnter Booking ID: ").strip().upper()

    booking = None

    for item in bookings:
        if item["booking_id"] == booking_id:
            booking = item
            break

    if booking is None:
        print("\nBooking not found.")
        return

    if booking["status"] == "Cancelled":
        print("\nCancelled booking cannot be updated.")
        return

    print("\n=========================================")
    print("           UPDATE BOOKING")
    print("=========================================")

    print(f"Customer : {booking['customer_name']}")
    print(f"Date     : {booking['booking_date']}")
    print(f"Time     : {booking['booking_time']}")
    print(f"Guests   : {booking['guests']}")
    print(f"Tables   : {', '.join(booking['table_number'])}")

    print("\n1. Customer Name")
    print("2. Mobile Number")
    print("3. Date")
    print("4. Time")
    print("5. Guests")
    print("6. Back")

    choice = input("\nEnter your choice: ").strip()

    if choice == "1":
        booking["customer_name"] = get_customer_name()

    elif choice == "2":
        booking["mobile"] = get_mobile(bookings, booking["mobile"])

    elif choice in ("3", "4", "5"):

        new_date = booking["booking_date"]
        new_time = booking["booking_time"]
        new_guests = booking["guests"]

        if choice == "3":
            new_date = get_booking_date()

        elif choice == "4":
            new_time = get_booking_time()

        elif choice == "5":
            new_guests = get_guests()

        show_available_tables(bookings, new_date, new_time)

        tables = select_tables(bookings, new_guests, new_date, new_time)

        if not tables:
            print("\nBooking update cancelled.")
            return

        booking["booking_date"] = new_date
        booking["booking_time"] = new_time
        booking["guests"] = new_guests
        booking["table_number"] = tables

    elif choice == "6":
        return

    else:
        print("\nInvalid choice.")
        return

    save_bookings(bookings)

    print("\nBooking updated successfully.")


def change_booking_status():
    bookings = load_bookings()

    if not bookings:
        print("\nNo bookings found.")
        return

    booking_id = input("\nEnter Booking ID: ").strip().upper()

    booking = None

    for item in bookings:
        if item["booking_id"] == booking_id:
            booking = item
            break

    if booking is None:
        print("\nBooking not found.")
        return

    print("\n=========================================")
    print("          CHANGE BOOKING STATUS")
    print("=========================================")

    print(f"Booking ID : {booking['booking_id']}")
    print(f"Customer   : {booking['customer_name']}")
    print(f"Date       : {booking['booking_date']}")
    print(f"Time       : {booking['booking_time']}")
    print(f"Current    : {booking['status']}")

    print("\n1. Pending")
    print("2. Confirmed")
    print("3. Completed")
    print("4. Cancelled")
    print("5. Back")

    choice = input("\nEnter new status: ").strip()

    statuses = {"1": "Pending", "2": "Confirmed", "3": "Completed", "4": "Cancelled"}

    if choice == "5":
        return

    if choice not in statuses:
        print("\nInvalid choice.")
        return

    booking["status"] = statuses[choice]

    save_bookings(bookings)

    print("\n=========================================")
    print("       STATUS UPDATED SUCCESSFULLY")
    print("=========================================")
    print(f"Booking ID : {booking['booking_id']}")
    print(f"New Status : {booking['status']}")


def cancel_booking():
    bookings = load_bookings()

    if not bookings:
        print("\nNo bookings found.")
        return

    booking_id = input("\nEnter Booking ID: ").strip().upper()

    booking = None

    for item in bookings:
        if item["booking_id"] == booking_id:
            booking = item
            break

    if booking is None:
        print("\nBooking not found.")
        return

    if booking["status"] == "Cancelled":
        print("\nBooking is already cancelled.")
        return

    print("\n=========================================")
    print("           CANCEL BOOKING")
    print("=========================================")

    print(f"Booking ID : {booking['booking_id']}")
    print(f"Customer   : {booking['customer_name']}")
    print(f"Date       : {booking['booking_date']}")
    print(f"Time       : {booking['booking_time']}")

    confirm = input("\nAre you sure you want to cancel? (Y/N): ").strip().upper()

    if confirm != "Y":
        print("\nCancellation stopped.")
        return

    booking["status"] = "Cancelled"

    save_bookings(bookings)

    print("\nBooking cancelled successfully.")
    print("Selected tables are now available.")


def available_tables_menu():
    bookings = load_bookings()

    print("\n=========================================")
    print("          CHECK AVAILABLE TABLES")
    print("=========================================")

    booking_date = get_booking_date()
    booking_time = get_booking_time()

    show_available_tables(bookings, booking_date, booking_time)


def booking_management():
    while True:

        print("\n=========================================")
        print("          BOOKING MANAGEMENT")
        print("=========================================")

        print("1. New Booking")
        print("2. View Bookings")
        print("3. Search Booking")
        print("4. Update Booking")
        print("5. Change Booking Status")
        print("6. Cancel Booking")
        print("7. Available Tables")
        print("8. Back")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            new_booking()

        elif choice == "2":
            view_bookings()

        elif choice == "3":
            search_booking()

        elif choice == "4":
            update_booking()

        elif choice == "5":
            change_booking_status()

        elif choice == "6":
            cancel_booking()

        elif choice == "7":
            available_tables_menu()

        elif choice == "8":
            break

        else:
            print("\nInvalid choice. Please try again.")
