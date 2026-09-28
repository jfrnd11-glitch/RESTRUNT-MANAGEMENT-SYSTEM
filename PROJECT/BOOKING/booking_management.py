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

        name = input("Customer Name: ").strip()

        if len(name) < 3:
            print("Name must contain at least 3 characters.")

        elif not all(char.isalpha() or char.isspace() for char in name):
            print("Name can contain only letters and spaces.")

        else:
            return name


def get_mobile(bookings, current_mobile=None):

    while True:

        mobile = input("Mobile Number: ").strip()

        if not mobile:
            print("Mobile number cannot be empty.")

        elif not mobile.isdigit():
            print("Mobile number must contain digits only.")

        elif len(mobile) != 10:
            print("Mobile number must contain exactly 10 digits.")

        elif mobile[0] not in "6789":
            print("Mobile number must start with 6, 7, 8 or 9.")

        elif any(
            booking.get("mobile") == mobile
            and booking.get("status") != "Cancelled"
            and mobile != current_mobile
            for booking in bookings
        ):
            print("This mobile number already has a booking.")

        else:
            return mobile


def get_booking_date():

    while True:

        date = input("Booking Date (DD-MM-YYYY): ").strip()

        try:

            booking_date = datetime.strptime(date, "%d-%m-%Y").date()

            if booking_date < datetime.now().date():
                print("Booking date cannot be in the past.")

            else:
                return date

        except ValueError:
            print("Enter date in DD-MM-YYYY format.")


def get_booking_time():

    while True:

        time = input("Booking Time (HH:MM AM/PM): ").strip().upper()

        try:

            datetime.strptime(time, "%I:%M %p")
            return time

        except ValueError:
            print("Enter time in HH:MM AM/PM format.")


def get_guests():

    while True:

        guests = input("Number of Guests: ").strip()

        if not guests.isdigit():
            print("Number of guests must contain digits only.")

        elif int(guests) <= 0:
            print("Number of guests must be greater than 0.")

        else:
            return int(guests)


def get_tables_for_guests(guests):

    if guests <= 2:
        return ["2"]

    elif guests <= 4:
        return ["4"]

    elif guests <= 6:
        return ["6"]

    elif guests <= 8:
        return ["6", "2"]

    elif guests <= 10:
        return ["6", "4"]

    elif guests <= 12:
        return ["6", "6"]

    else:
        tables = []

        while guests > 6:
            tables.append("6")
            guests -= 6

        if guests > 0:
            if guests <= 2:
                tables.append("2")
            elif guests <= 4:
                tables.append("4")
            else:
                tables.append("6")

        return tables


def get_available_tables(bookings, booking_date, booking_time):

    booked_tables = []

    for booking in bookings:

        if (
            booking.get("booking_date") == booking_date
            and booking.get("booking_time") == booking_time
            and booking.get("status") != "Cancelled"
        ):

            tables = booking.get("table_number", [])

            if isinstance(tables, str):
                tables = [tables]

            booked_tables.extend(tables)

    available_tables = {"2": [], "4": [], "6": []}

    for size, table_list in TABLES.items():

        for table in table_list:

            if table not in booked_tables:
                available_tables[size].append(table)

    return available_tables


def assign_tables(bookings, guests, booking_date, booking_time):

    required_tables = get_tables_for_guests(guests)

    available_tables = get_available_tables(bookings, booking_date, booking_time)

    assigned_tables = []

    for size in required_tables:

        size = str(size)

        if not available_tables[size]:
            return None

        table = available_tables[size].pop(0)
        assigned_tables.append(table)

    return assigned_tables


def generate_booking_id(bookings):

    number = 1

    while True:

        booking_id = "B" + str(number).zfill(3)

        exists = any(booking.get("booking_id") == booking_id for booking in bookings)

        if not exists:
            return booking_id

        number += 1


def new_booking():

    bookings = load_bookings()

    print()
    print("=========================================")
    print("             NEW BOOKING")
    print("=========================================")

    customer_name = get_customer_name()

    mobile = get_mobile(bookings)

    booking_date = get_booking_date()

    booking_time = get_booking_time()

    guests = get_guests()

    tables = assign_tables(bookings, guests, booking_date, booking_time)

    if tables is None:
        print()
        print("Required tables are not available for this date and time.")
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
        "status": "Confirmed",
    }

    bookings.append(booking)

    save_bookings(bookings)

    print()
    print("Booking created successfully.")
    print("Booking ID:", booking_id)
    print("Table:", ", ".join(tables))


def view_bookings():

    bookings = load_bookings()

    print()
    print("=========================================")
    print("             ALL BOOKINGS")
    print("=========================================")

    if not bookings:
        print("No bookings found.")
        return

    for booking in bookings:

        print("Booking ID :", booking["booking_id"])
        print("Name       :", booking["customer_name"])
        print("Mobile     :", booking["mobile"])
        print("Date       :", booking["booking_date"])
        print("Time       :", booking["booking_time"])
        print("Guests     :", booking["guests"])

        tables = booking.get("table_number", [])

        if isinstance(tables, str):
            tables = [tables]

        print("Table      :", ", ".join(tables))
        print("Status     :", booking["status"])
        print("-----------------------------------------")


def search_booking():

    bookings = load_bookings()

    if not bookings:
        print("\nNo bookings found.")
        return

    print()
    print("=========================================")
    print("           SEARCH BOOKING")
    print("=========================================")

    search = input("Enter Booking ID or Mobile Number: ").strip()

    found = False

    for booking in bookings:

        if (
            booking["booking_id"].lower() == search.lower()
            or booking["mobile"] == search
        ):

            print()
            print("Booking ID :", booking["booking_id"])
            print("Name       :", booking["customer_name"])
            print("Mobile     :", booking["mobile"])
            print("Date       :", booking["booking_date"])
            print("Time       :", booking["booking_time"])
            print("Guests     :", booking["guests"])

            tables = booking.get("table_number", [])

            if isinstance(tables, str):
                tables = [tables]

            print("Table      :", ", ".join(tables))
            print("Status     :", booking["status"])

            found = True
            break

    if not found:
        print("\nBooking not found.")


def update_booking():

    bookings = load_bookings()

    if not bookings:
        print("\nNo bookings found.")
        return

    print()
    print("=========================================")
    print("           UPDATE BOOKING")
    print("=========================================")

    booking_id = input("Enter Booking ID: ").strip().upper()

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

    print("\nLeave input empty to keep the old value.")

    name = input(f"Customer Name [{booking['customer_name']}]: ").strip()

    if name:

        if len(name) < 3 or not all(char.isalpha() or char.isspace() for char in name):
            print("Invalid name.")
            return

        booking["customer_name"] = name

    mobile = input(f"Mobile Number [{booking['mobile']}]: ").strip()

    if mobile:

        if not mobile.isdigit() or len(mobile) != 10:
            print("Invalid mobile number.")
            return

        if mobile[0] not in "6789":
            print("Mobile number must start with 6, 7, 8 or 9.")
            return

        for item in bookings:

            if (
                item["booking_id"] != booking_id
                and item.get("mobile") == mobile
                and item.get("status") != "Cancelled"
            ):
                print("This mobile number already has a booking.")
                return

        booking["mobile"] = mobile

    old_date = booking["booking_date"]
    old_time = booking["booking_time"]
    old_guests = booking["guests"]
    old_tables = booking.get("table_number", [])

    date = input(f"Booking Date [{old_date}]: ").strip()

    if date:

        try:

            booking_date = datetime.strptime(date, "%d-%m-%Y").date()

            if booking_date < datetime.now().date():
                print("Booking date cannot be in the past.")
                return

        except ValueError:
            print("Invalid date.")
            return

    else:
        date = old_date

    time = input(f"Booking Time [{old_time}]: ").strip().upper()

    if time:

        try:
            datetime.strptime(time, "%I:%M %p")

        except ValueError:
            print("Invalid time.")
            return

    else:
        time = old_time

    guests_input = input(f"Number of Guests [{old_guests}]: ").strip()

    if guests_input:

        if not guests_input.isdigit():
            print("Invalid number of guests.")
            return

        guests = int(guests_input)

        if guests <= 0:
            print("Number of guests must be greater than 0.")
            return

    else:
        guests = old_guests

    date_or_time_changed = date != old_date or time != old_time

    guests_changed = guests != old_guests

    if date_or_time_changed or guests_changed:

        new_tables = assign_tables(
            [item for item in bookings if item["booking_id"] != booking_id],
            guests,
            date,
            time,
        )

        if new_tables is None:
            print("\nRequired tables are not available " "for the new date and time.")
            return

        booking["table_number"] = new_tables

    else:
        booking["table_number"] = old_tables

    booking["booking_date"] = date
    booking["booking_time"] = time
    booking["guests"] = guests

    save_bookings(bookings)

    print("\nBooking updated successfully.")

    tables = booking.get("table_number", [])

    if isinstance(tables, str):
        tables = [tables]

    print("Table:", ", ".join(tables))


def cancel_booking():

    bookings = load_bookings()

    if not bookings:
        print("\nNo bookings found.")
        return

    print()
    print("=========================================")
    print("           CANCEL BOOKING")
    print("=========================================")

    booking_id = input("Enter Booking ID: ").strip().upper()

    for booking in bookings:

        if booking["booking_id"] == booking_id:

            if booking["status"] == "Cancelled":
                print("\nBooking is already cancelled.")
                return

            booking["status"] = "Cancelled"

            save_bookings(bookings)

            print("\nBooking cancelled successfully.")
            print("Assigned tables are now available.")
            return

    print("\nBooking not found.")


def booking_management():

    while True:

        print()
        print("=========================================")
        print("          BOOKING MANAGEMENT")
        print("=========================================")

        print("1. New Booking")
        print("2. View Bookings")
        print("3. Search Booking")
        print("4. Update Booking")
        print("5. Cancel Booking")
        print("6. Back")

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
            cancel_booking()

        elif choice == "6":
            break

        else:
            print("\nInvalid choice. Please try again.")