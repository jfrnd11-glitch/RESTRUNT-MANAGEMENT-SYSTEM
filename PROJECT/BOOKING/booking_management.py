import json
import os
from datetime import datetime, timedelta

from PROJECT.LOGS.error_hendal import error_handler

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILE_NAME = os.path.join(BASE_DIR, "DATABASE", "booking.json")

TABLES = {
    "2": [f"T{i:02d}" for i in range(1, 11)],
    "4": [f"T{i:02d}" for i in range(11, 21)],
    "6": [f"T{i:02d}" for i in range(21, 26)]
}


class BookingManagement:

    def load_bookings(self):
        try:
            with open(FILE_NAME, "r", encoding="utf-8") as file:
                data = json.load(file)
                return data if isinstance(data, list) else []
        except FileNotFoundError:
            return []
        except (json.JSONDecodeError, OSError) as e:
            error_handler.exception(e)
            return []

    def save_bookings(self, bookings):
        try:
            os.makedirs(os.path.dirname(FILE_NAME), exist_ok=True)
            with open(FILE_NAME, "w", encoding="utf-8") as file:
                json.dump(bookings, file, indent=4)
            return True
        except OSError as e:
            error_handler.exception(e)
            print("Booking data could not be saved.")
            return False

    def get_input(self, message):
        while True:
            value = input(message).strip()
            if value:
                return value
            error_handler.warning("Empty input entered.")
            print("Input cannot be empty.")

    def get_name(self):
        while True:
            name = self.get_input("Customer Name: ")
            if len(name) >= 3 and name.replace(" ", "").isalpha():
                return name.title()
            error_handler.warning("Invalid customer name.")
            print("Name must contain at least 3 letters.")

    def get_mobile(self):
        while True:
            mobile = self.get_input("Mobile Number: ")
            if len(mobile) == 10 and mobile.isdigit():
                return mobile
            error_handler.warning("Invalid mobile number.")
            print("Enter a 10-digit mobile number.")

    def get_date(self):
        while True:
            date = self.get_input("Booking Date (DD-MM-YYYY): ")
            try:
                booking_date = datetime.strptime(date, "%d-%m-%Y")
                if booking_date.date() >= datetime.now().date():
                    return date
            except ValueError:
                pass

            error_handler.warning("Invalid booking date.")
            print("Enter a valid current or future date.")

    def get_time(self, date):
        while True:
            time = self.get_input("Booking Time (HH:MM AM/PM): ").upper()
            try:
                booking_time = datetime.strptime(
                    f"{date} {time}", "%d-%m-%Y %I:%M %p"
                )
                if booking_time > datetime.now():
                    return time
            except ValueError:
                pass

            error_handler.warning("Invalid booking date or time.")
            print("Enter a future time in HH:MM AM/PM format.")

    def get_number(self, message, minimum, maximum):
        while True:
            value = self.get_input(message)
            if value.isdigit() and minimum <= int(value) <= maximum:
                return int(value)
            error_handler.warning("Invalid number entered.")
            print(f"Enter a number between {minimum} and {maximum}.")

    def get_booking_range(self, booking):
        try:
            start = datetime.strptime(
                booking["booking_date"] + " " + booking["booking_time"],
                "%d-%m-%Y %I:%M %p"
            )
            end = start + timedelta(hours=int(booking.get("duration", 1)))
            return start, end
        except (KeyError, ValueError, TypeError):
            return None, None

    def get_available_tables(self, bookings, date, time, duration, exclude_id=None):
        start = datetime.strptime(
            date + " " + time, "%d-%m-%Y %I:%M %p"
        )
        end = start + timedelta(hours=duration)
        booked = []

        for booking in bookings:
            if booking.get("status") == "Cancelled":
                continue
            if booking.get("booking_id") == exclude_id:
                continue

            old_start, old_end = self.get_booking_range(booking)

            if old_start and start < old_end and end > old_start:
                booked.extend(booking.get("table_number", []))

        return {
            size: [table for table in tables if table not in booked]
            for size, tables in TABLES.items()
        }

    def show_available_tables(self, available, date, time, duration):
        end = datetime.strptime(
            date + " " + time, "%d-%m-%Y %I:%M %p"
        ) + timedelta(hours=duration)

        print("\nAvailable Tables")
        print("Date:", date)
        print("Time:", time)
        print("Duration:", duration, "hour(s)")
        print("End Time:", end.strftime("%I:%M %p"))

        for size, tables in available.items():
            print(f"{size}-Seater:", ", ".join(tables) or "No tables")

    def select_tables(self, bookings, guests, date, time, duration, exclude_id=None):
        available = self.get_available_tables(
            bookings, date, time, duration, exclude_id
        )

        selected = []
        remaining = guests

        while remaining > 0:
            size = "6" if remaining > 4 else "4" if remaining > 2 else "2"
            tables = available[size]

            if not tables:
                print("Required table is not available.")
                error_handler.warning("Required booking table unavailable.")
                return None

            print(f"Available {size}-Seater:", ", ".join(tables))
            table = self.get_input("Select Table: ").upper()

            if table not in tables:
                print("Invalid or unavailable table.")
                error_handler.warning("Invalid table selected.")
                continue

            selected.append(table)
            available[size].remove(table)
            remaining -= int(size)

        return selected

    def generate_booking_id(self, bookings):
        number = 1
        while any(b.get("booking_id") == f"B{number:04d}" for b in bookings):
            number += 1
        return f"B{number:04d}"

    def new_booking(self):
        bookings = self.load_bookings()

        print("\nNew Booking")
        name = self.get_name()
        mobile = self.get_mobile()
        date = self.get_date()
        time = self.get_time(date)
        duration = self.get_number("Duration (hours, 1-12): ", 1, 12)
        guests = self.get_number("Number of Guests (1-30): ", 1, 30)

        available = self.get_available_tables(bookings, date, time, duration)
        self.show_available_tables(available, date, time, duration)

        tables = self.select_tables(bookings, guests, date, time, duration)

        if not tables:
            print("Booking could not be completed.")
            return

        booking = {
            "booking_id": self.generate_booking_id(bookings),
            "customer_name": name,
            "mobile": mobile,
            "booking_date": date,
            "booking_time": time,
            "duration": duration,
            "guests": guests,
            "table_number": tables,
            "status": "Pending"
        }

        bookings.append(booking)

        if self.save_bookings(bookings):
            print("Booking created successfully.")
            print("Booking ID:", booking["booking_id"])
            print("Tables:", ", ".join(tables))

    def view_bookings(self):
        bookings = self.load_bookings()

        if not bookings:
            print("No bookings found.")
            return

        for booking in bookings:
            print("\nBooking ID:", booking.get("booking_id"))
            print("Customer:", booking.get("customer_name"))
            print("Mobile:", booking.get("mobile"))
            print("Date:", booking.get("booking_date"))
            print("Time:", booking.get("booking_time"))
            print("Duration:", booking.get("duration", 1), "hour(s)")
            print("Guests:", booking.get("guests"))
            print("Tables:", ", ".join(booking.get("table_number", [])))
            print("Status:", booking.get("status"))

    def search_booking(self):
        bookings = self.load_bookings()
        booking_id = self.get_input("Enter Booking ID: ").upper()

        booking = next(
            (b for b in bookings if b.get("booking_id") == booking_id), None
        )

        if booking:
            print("\nBooking Details")
            for key, value in booking.items():
                print(f"{key}: {value}")
        else:
            print("Booking not found.")
            error_handler.warning("Booking not found.")

    def update_booking(self):
        bookings = self.load_bookings()
        booking_id = self.get_input("Enter Booking ID: ").upper()

        booking = next(
            (b for b in bookings if b.get("booking_id") == booking_id), None
        )

        if not booking or booking.get("status") == "Cancelled":
            print("Booking not found or already cancelled.")
            return

        print("\n1. Customer Name")
        print("2. Mobile Number")
        print("3. Date, Time, Guests and Tables")
        print("4. Duration")
        print("5. Back")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            booking["customer_name"] = self.get_name()
        elif choice == "2":
            booking["mobile"] = self.get_mobile()
        elif choice in ("3", "4"):
            date = booking["booking_date"]
            time = booking["booking_time"]
            guests = booking["guests"]
            duration = booking.get("duration", 1)

            if choice == "3":
                date = self.get_date()
                time = self.get_time(date)
                guests = self.get_number("Number of Guests (1-30): ", 1, 30)
            duration = self.get_number("Duration (hours, 1-12): ", 1, 12)

            available = self.get_available_tables(
                bookings, date, time, duration, booking_id
            )
            self.show_available_tables(available, date, time, duration)
            tables = self.select_tables(
                bookings, guests, date, time, duration, booking_id
            )

            if not tables:
                print("Booking update cancelled.")
                return

            booking["booking_date"] = date
            booking["booking_time"] = time
            booking["guests"] = guests
            booking["duration"] = duration
            booking["table_number"] = tables

        elif choice == "5":
            return
        else:
            error_handler.warning("Invalid booking update choice.")
            print("Invalid choice.")
            return

        if self.save_bookings(bookings):
            print("Booking updated successfully.")

    def change_booking_status(self):
        bookings = self.load_bookings()
        booking_id = self.get_input("Enter Booking ID: ").upper()

        booking = next(
            (b for b in bookings if b.get("booking_id") == booking_id), None
        )

        if not booking:
            print("Booking not found.")
            return

        print("1. Pending")
        print("2. Confirmed")
        print("3. Completed")
        print("4. Cancelled")

        statuses = {
            "1": "Pending",
            "2": "Confirmed",
            "3": "Completed",
            "4": "Cancelled"
        }

        choice = input("Select Status: ").strip()

        if choice not in statuses:
            error_handler.warning("Invalid booking status.")
            print("Invalid choice.")
            return

        booking["status"] = statuses[choice]

        if self.save_bookings(bookings):
            print("Status updated:", booking["status"])

    def cancel_booking(self):
        bookings = self.load_bookings()
        booking_id = self.get_input("Enter Booking ID: ").upper()

        booking = next(
            (b for b in bookings if b.get("booking_id") == booking_id), None
        )

        if not booking:
            print("Booking not found.")
            return

        if booking.get("status") == "Cancelled":
            print("Booking is already cancelled.")
            return

        confirm = input("Cancel this booking? (Y/N): ").strip().upper()

        if confirm == "Y":
            booking["status"] = "Cancelled"
            if self.save_bookings(bookings):
                print("Booking cancelled. Table is available again.")

    def available_tables_menu(self):
        bookings = self.load_bookings()
        date = self.get_date()
        time = self.get_time(date)
        duration = self.get_number("Duration (hours, 1-12): ", 1, 12)

        available = self.get_available_tables(bookings, date, time, duration)
        self.show_available_tables(available, date, time, duration)

    def booking_management(self):
        while True:
            print("\nBooking Management")
            print("1. New Booking")
            print("2. View Bookings")
            print("3. Search Booking")
            print("4. Update Booking")
            print("5. Change Booking Status")
            print("6. Cancel Booking")
            print("7. Available Tables")
            print("8. Back")

            choice = input("Enter choice: ").strip()

            actions = {
                "1": self.new_booking,
                "2": self.view_bookings,
                "3": self.search_booking,
                "4": self.update_booking,
                "5": self.change_booking_status,
                "6": self.cancel_booking,
                "7": self.available_tables_menu
            }

            if choice == "8":
                break
            elif choice in actions:
                try:
                    actions[choice]()
                except Exception as e:
                    error_handler.exception(e)
                    print("Booking operation failed.")
            else:
                error_handler.warning("Invalid booking menu choice.")
                print("Invalid choice.")