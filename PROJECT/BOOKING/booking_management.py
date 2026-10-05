import json
import os
from datetime import datetime
from PROJECT.LOGS.error_hendal import error_handler

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_DIR = os.path.join(BASE_DIR, "DATABASE")
FILE_NAME = os.path.join(DATABASE_DIR, "booking.json")

TABLES = {
    "2": ["T01", "T02", "T03", "T04", "T05", "T06", "T07", "T08", "T09", "T10"],
    "4": ["T11", "T12", "T13", "T14", "T15", "T16", "T17", "T18", "T19", "T20"],
    "6": ["T21", "T22", "T23", "T24", "T25"]
}

def load_bookings():
    try:
        if not os.path.exists(FILE_NAME):
            error_handler.log_warning("BookingManagement", "load_bookings", "booking.json file not found")
            return []
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    except Exception as e:
        error_handler.log_exception("BookingManagement", "load_bookings", e)
        return []

def save_bookings(bookings):
    try:
        os.makedirs(DATABASE_DIR, exist_ok=True)
        with open(FILE_NAME, "w") as file:
            json.dump(bookings, file, indent=4)
        return True
    except Exception as e:
        error_handler.log_exception("BookingManagement", "save_bookings", e)
        print("\nBooking data could not be saved.")
        return False

def get_customer_name():
    while True:
        try:
            name = input("\nEnter Customer Name: ").strip()
            if not name:
                print("Name cannot be empty.")
                error_handler.log_error("BookingManagement", "get_customer_name", "Customer name cannot be empty")
            elif len(name) < 3:
                print("Name must contain at least 3 characters.")
                error_handler.log_error("BookingManagement", "get_customer_name", "Customer name has less than 3 characters")
            elif not name.replace(" ", "").isalpha():
                print("Name must contain only letters and spaces.")
                error_handler.log_error("BookingManagement", "get_customer_name", f"Invalid customer name: {name}")
            else:
                return name.title()
        except Exception as e:
            error_handler.log_exception("BookingManagement", "get_customer_name", e)
            print("Something went wrong. Please try again.")

def get_mobile():
    while True:
        try:
            mobile = input("Enter Mobile Number: ").strip()
            if not mobile:
                print("Mobile number cannot be empty.")
                error_handler.log_error("BookingManagement", "get_mobile", "Mobile number cannot be empty")
            elif not mobile.isdigit():
                print("Mobile number must contain only digits.")
                error_handler.log_error("BookingManagement", "get_mobile", "Mobile number contains non-digit characters")
            elif len(mobile) != 10:
                print("Mobile number must be exactly 10 digits.")
                error_handler.log_error("BookingManagement", "get_mobile", "Mobile number is not exactly 10 digits")
            else:
                return mobile
        except Exception as e:
            error_handler.log_exception("BookingManagement", "get_mobile", e)
            print("Something went wrong. Please try again.")

def get_booking_date():
    while True:
        try:
            date = input("Enter Booking Date (DD-MM-YYYY): ").strip()
            if not date:
                print("Booking date cannot be empty.")
                error_handler.log_error("BookingManagement", "get_booking_date", "Booking date cannot be empty")
                continue
            try:
                booking_date = datetime.strptime(date, "%d-%m-%Y")
                today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
                if booking_date < today:
                    print("Booking date cannot be in the past.")
                    error_handler.log_error("BookingManagement", "get_booking_date", f"Past booking date entered: {date}")
                else:
                    return date
            except ValueError:
                print("Invalid date. Use DD-MM-YYYY.")
                error_handler.log_error("BookingManagement", "get_booking_date", f"Invalid booking date: {date}")
        except Exception as e:
            error_handler.log_exception("BookingManagement", "get_booking_date", e)
            print("Something went wrong. Please try again.")

def validate_booking_datetime(booking_date, booking_time):
    try:
        booking_datetime = datetime.strptime(
            f"{booking_date} {booking_time}",
            "%d-%m-%Y %I:%M %p"
        )

        if booking_datetime <= datetime.now():
            print("Booking date and time must be in the future.")
            error_handler.log_error(
                "BookingManagement",
                "validate_booking_datetime",
                f"Past booking date/time entered: {booking_date} {booking_time}"
            )
            return False

        return True

    except ValueError:
        print("Invalid booking date or time.")
        error_handler.log_error(
            "BookingManagement",
            "validate_booking_datetime",
            f"Invalid booking date/time: {booking_date} {booking_time}"
        )
        return False

    except Exception as e:
        error_handler.log_exception(
            "BookingManagement",
            "validate_booking_datetime",
            e
        )
        print("Something went wrong. Please try again.")
        return False


def get_booking_time(booking_date=None):
    while True:
        try:
            time = input("Enter Booking Time (HH:MM AM/PM): ").strip().upper()

            if not time:
                print("Booking time cannot be empty.")
                error_handler.log_error(
                    "BookingManagement",
                    "get_booking_time",
                    "Booking time cannot be empty"
                )
                continue

            try:
                datetime.strptime(time, "%I:%M %p")
            except ValueError:
                print("Invalid time. Use HH:MM AM/PM.")
                error_handler.log_error(
                    "BookingManagement",
                    "get_booking_time",
                    f"Invalid booking time: {time}"
                )
                continue

            if booking_date is not None:
                if not validate_booking_datetime(booking_date, time):
                    continue

            return time

        except Exception as e:
            error_handler.log_exception("BookingManagement", "get_booking_time", e)
            print("Something went wrong. Please try again.")

def get_guests():
    while True:
        try:
            guests = input("Enter Number of Guests: ").strip()
            if not guests:
                print("Number of guests cannot be empty.")
                error_handler.log_error("BookingManagement", "get_guests", "Number of guests cannot be empty")
                continue
            if not guests.isdigit():
                print("Guests must be a number.")
                error_handler.log_error("BookingManagement", "get_guests", f"Invalid guest number: {guests}")
                continue
            guests = int(guests)
            if guests < 1:
                print("Guests must be at least 1.")
                error_handler.log_error("BookingManagement", "get_guests", f"Guest number less than 1: {guests}")
            elif guests > 30:
                print("Maximum 30 guests allowed.")
                error_handler.log_error("BookingManagement", "get_guests", f"More than 30 guests entered: {guests}")
            else:
                return guests
        except Exception as e:
            error_handler.log_exception("BookingManagement", "get_guests", e)
            print("Something went wrong. Please try again.")

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
        if booking.get("booking_date") == booking_date and booking.get("booking_time") == booking_time:
            booked_tables.extend(booking.get("table_number", []))
    available_tables = {}
    for size, tables in TABLES.items():
        available_tables[size] = [table for table in tables if table not in booked_tables]
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
            error_handler.log_warning("BookingManagement", "select_tables", f"No {size}-seater table available")
            return None
        print(f"\nAvailable {size}-seater tables:")
        print(", ".join(available_tables))
        while True:
            table = input(f"Select {size}-seater table: ").strip().upper()
            if table not in available_tables:
                print("Invalid or unavailable table.")
                error_handler.log_error("BookingManagement", "select_tables", f"Invalid or unavailable table: {table}")
                continue
            if table in selected_tables:
                print("Table already selected.")
                error_handler.log_warning("BookingManagement", "select_tables", f"Table already selected: {table}")
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
    try:
        bookings = load_bookings()
        print("\n=========================================")
        print("             NEW BOOKING")
        print("=========================================")
        customer_name = get_customer_name()
        mobile = get_mobile()
        booking_date = get_booking_date()
        booking_time = get_booking_time(booking_date)
        guests = get_guests()
        show_available_tables(bookings, booking_date, booking_time)
        tables = select_tables(bookings, guests, booking_date, booking_time)
        if not tables:
            print("\nBooking could not be completed.")
            error_handler.log_warning("BookingManagement", "new_booking", "Booking could not be completed because table selection failed")
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
            "status": "Pending"
        }
        bookings.append(booking)
        if not save_bookings(bookings):
            return
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
    except Exception as e:
        error_handler.log_exception("BookingManagement", "new_booking", e)
        print("\nBooking could not be created.")

def view_bookings():
    try:
        bookings = load_bookings()
        if not bookings:
            print("\nNo bookings found.")
            error_handler.log_warning("BookingManagement", "view_bookings", "No bookings found")
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
    except Exception as e:
        error_handler.log_exception("BookingManagement", "view_bookings", e)
        print("\nUnable to display bookings.")

def search_booking():
    try:
        bookings = load_bookings()
        if not bookings:
            print("\nNo bookings found.")
            error_handler.log_warning("BookingManagement", "search_booking", "No bookings found")
            return
        booking_id = input("\nEnter Booking ID: ").strip().upper()
        if not booking_id:
            print("\nBooking ID cannot be empty.")
            error_handler.log_error("BookingManagement", "search_booking", "Booking ID cannot be empty")
            return
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
        error_handler.log_error("BookingManagement", "search_booking", f"Booking not found: {booking_id}")
    except Exception as e:
        error_handler.log_exception("BookingManagement", "search_booking", e)
        print("\nUnable to search booking.")

def update_booking():
    try:
        bookings = load_bookings()
        if not bookings:
            print("\nNo bookings found.")
            error_handler.log_warning("BookingManagement", "update_booking", "No bookings found")
            return
        booking_id = input("\nEnter Booking ID: ").strip().upper()
        if not booking_id:
            print("\nBooking ID cannot be empty.")
            error_handler.log_error("BookingManagement", "update_booking", "Booking ID cannot be empty")
            return
        booking = next((item for item in bookings if item["booking_id"] == booking_id), None)
        if booking is None:
            print("\nBooking not found.")
            error_handler.log_error("BookingManagement", "update_booking", f"Booking not found: {booking_id}")
            return
        if booking["status"] == "Cancelled":
            print("\nCancelled booking cannot be updated.")
            error_handler.log_warning("BookingManagement", "update_booking", f"Attempt to update cancelled booking: {booking_id}")
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
            booking["mobile"] = get_mobile()
        elif choice in ("3", "4", "5"):
            new_date = booking["booking_date"]
            new_time = booking["booking_time"]
            new_guests = booking["guests"]
            if choice == "3":
                new_date = get_booking_date()

                if not validate_booking_datetime(new_date, new_time):
                    new_time = get_booking_time(new_date)

            elif choice == "4":
                new_time = get_booking_time(new_date)
            else:
                new_guests = get_guests()
            if not validate_booking_datetime(new_date, new_time):
                print("\nBooking date and time must be in the future.")
                return

            show_available_tables(bookings, new_date, new_time)
            tables = select_tables(bookings, new_guests, new_date, new_time)
            if not tables:
                print("\nBooking update cancelled.")
                error_handler.log_warning("BookingManagement", "update_booking", f"Booking update cancelled: {booking_id}")
                return
            booking["booking_date"] = new_date
            booking["booking_time"] = new_time
            booking["guests"] = new_guests
            booking["table_number"] = tables
        elif choice == "6":
            return
        else:
            print("\nInvalid choice.")
            error_handler.log_error("BookingManagement", "update_booking", f"Invalid update choice: {choice}")
            return
        if not save_bookings(bookings):
            return
        print("\nBooking updated successfully.")
    except Exception as e:
        error_handler.log_exception("BookingManagement", "update_booking", e)
        print("\nBooking could not be updated.")

def change_booking_status():
    try:
        bookings = load_bookings()
        if not bookings:
            print("\nNo bookings found.")
            error_handler.log_warning("BookingManagement", "change_booking_status", "No bookings found")
            return
        booking_id = input("\nEnter Booking ID: ").strip().upper()
        if not booking_id:
            print("\nBooking ID cannot be empty.")
            error_handler.log_error("BookingManagement", "change_booking_status", "Booking ID cannot be empty")
            return
        booking = next((item for item in bookings if item["booking_id"] == booking_id), None)
        if booking is None:
            print("\nBooking not found.")
            error_handler.log_error("BookingManagement", "change_booking_status", f"Booking not found: {booking_id}")
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
            error_handler.log_error("BookingManagement", "change_booking_status", f"Invalid status choice: {choice}")
            return
        booking["status"] = statuses[choice]
        if not save_bookings(bookings):
            return
        print("\n=========================================")
        print("       STATUS UPDATED SUCCESSFULLY")
        print("=========================================")
        print(f"Booking ID : {booking['booking_id']}")
        print(f"New Status : {booking['status']}")
    except Exception as e:
        error_handler.log_exception("BookingManagement", "change_booking_status", e)
        print("\nBooking status could not be updated.")

def cancel_booking():
    try:
        bookings = load_bookings()
        if not bookings:
            print("\nNo bookings found.")
            error_handler.log_warning("BookingManagement", "cancel_booking", "No bookings found")
            return
        booking_id = input("\nEnter Booking ID: ").strip().upper()
        if not booking_id:
            print("\nBooking ID cannot be empty.")
            error_handler.log_error("BookingManagement", "cancel_booking", "Booking ID cannot be empty")
            return
        booking = next((item for item in bookings if item["booking_id"] == booking_id), None)
        if booking is None:
            print("\nBooking not found.")
            error_handler.log_error("BookingManagement", "cancel_booking", f"Booking not found: {booking_id}")
            return
        if booking["status"] == "Cancelled":
            print("\nBooking is already cancelled.")
            error_handler.log_warning("BookingManagement", "cancel_booking", f"Booking already cancelled: {booking_id}")
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
            error_handler.log_warning("BookingManagement", "cancel_booking", f"Booking cancellation stopped: {booking_id}")
            return
        booking["status"] = "Cancelled"
        if not save_bookings(bookings):
            return
        print("\nBooking cancelled successfully.")
        print("Selected tables are now available.")
    except Exception as e:
        error_handler.log_exception("BookingManagement", "cancel_booking", e)
        print("\nBooking could not be cancelled.")

def available_tables_menu():
    try:
        bookings = load_bookings()
        print("\n=========================================")
        print("          CHECK AVAILABLE TABLES")
        print("=========================================")
        booking_date = get_booking_date()
        booking_time = get_booking_time(booking_date)
        show_available_tables(bookings, booking_date, booking_time)
    except Exception as e:
        error_handler.log_exception("BookingManagement", "available_tables_menu", e)
        print("\nUnable to check available tables.")

def booking_management():
    try:
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
                error_handler.log_error("BookingManagement", "booking_management", f"Invalid menu choice: {choice}")
    except Exception as e:
        error_handler.log_exception("BookingManagement", "booking_management", e)
        print("\nBooking Management could not continue.")