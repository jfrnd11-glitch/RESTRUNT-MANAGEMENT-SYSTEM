
import json
import os
import re
from datetime import datetime, timedelta

from PROJECT.config import BOOKING_FILE
from PROJECT.LOGS.error_hendal import error_handler

TABLES = {
    "2": [f"T{i:02}" for i in range(1, 11)],
    "4": [f"T{i:02}" for i in range(11, 21)],
    "6": [f"T{i:02}" for i in range(21, 26)]
}


class BookingManagement:
    def load_bookings(self):
        try:
            with open(BOOKING_FILE, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return []
        except (json.JSONDecodeError, OSError) as e:
            error_handler.exception(e)
            return []

    def save_bookings(self, bookings):
        try:
            os.makedirs(os.path.dirname(BOOKING_FILE), exist_ok=True)
            with open(BOOKING_FILE, "w") as file:
                json.dump(bookings, file, indent=4)
        except OSError as e:
            error_handler.exception(e)
            print("Booking NOT SAVE.")

    def generate_booking_id(self, bookings):
        numbers = [
            int(b["booking_id"][1:])
            for b in bookings
            if b.get("booking_id", "")[1:].isdigit()
        ]
        return f"B{max(numbers, default=0) + 1:04}"

    def get_duration(self):
        while True:
            duration = input("Booking duration (hours): ").strip()
            if duration.isdigit() and int(duration) > 0:
                return int(duration)
            print("DUSACTION TIME 1 SE JAYDA HONA CHAIYE.")
            error_handler.warning("Invalid booking duration.")

    def get_guests(self):
        while True:
            guests = input("Number of guests: ").strip()
            if guests.isdigit() and int(guests) > 0:
                return int(guests)
            print("Kam se kam 1 guest hona chahiye.")
            error_handler.warning("Invalid guest count.")

    def get_booking_datetime(self):
        while True:
            date = input("Booking date (DD-MM-YYYY): ").strip()
            time = input("Booking time (HH:MM AM/PM): ").strip()

            try:
                booking_dt = datetime.strptime(
                    f"{date} {time}", "%d-%m-%Y %I:%M %p"
                )
                if booking_dt > datetime.now():
                    return booking_dt
                print("ENTER FUCTURE TIME AND DATE")
            except ValueError:
                print("Date YA TIME FORMATE IS ROUNG.")

            error_handler.warning("Invalid booking date or time.")

    def get_available_tables(self, bookings, booking_dt, duration):
        available = {size: [] for size in TABLES}
        end_time = booking_dt + timedelta(hours=duration)

        for size, tables in TABLES.items():
            for table in tables:
                occupied = False

                for booking in bookings:
                    if (
                        table not in booking.get("table_number", [])
                        and booking.get("table_number") != table
                    ):
                        continue

                    if booking.get("status") in ("Cancelled", "Completed"):
                        continue

                    try:
                        old_dt = datetime.strptime(
                            f'{booking["booking_date"]} '
                            f'{booking["booking_time"]}',
                            "%d-%m-%Y %I:%M %p"
                        )
                        old_duration = int(booking.get("duration", 1))
                        old_end = old_dt + timedelta(hours=old_duration)

                        if booking_dt < old_end and end_time > old_dt:
                            occupied = True
                            break
                    except (ValueError, KeyError, TypeError):
                        continue

                if not occupied:
                    available[size].append(table)

        return available

    def select_tables(self, guests, available):
        selected = []
        remaining = guests

        while remaining > 0:
            if remaining > 4:
                sizes = ["6", "4", "2"]
            elif remaining > 2:
                sizes = ["4", "2", "6"]
            else:
                sizes = ["2", "4", "6"]

            size = next((s for s in sizes if available[s]), None)

            if size is None:
                print("Itne guests ke liye available tables nahi hain.")
                return []

            print(f"\nAvailable {size}-seater tables:")
            for i, table in enumerate(available[size], 1):
                print(f"{i}. {table}")

            choice = input("Table number select karein: ").strip()

            if not choice.isdigit() or not 1 <= int(choice) <= len(available[size]):
                print("Invalid table selection.")
                continue

            table = available[size].pop(int(choice) - 1)
            selected.append(table)
            remaining -= int(size)

        return selected

    def create_booking(self):
        bookings = self.load_bookings()

        name = input("Customer name: ").strip()
        if len(name) < 3 or not name.replace(" ", "").isalpha():
            print("Valid name enter karein.")
            error_handler.warning("Invalid customer name.")
            return

        mobile = input("Mobile number: ").strip()
        if not re.fullmatch(r"\d{10}", mobile):
            print("Mobile number 10 digits ka hona chahiye.")
            error_handler.warning("Invalid mobile number.")
            return

        booking_dt = self.get_booking_datetime()
        guests = self.get_guests()
        duration = self.get_duration()

        available = self.get_available_tables(
            bookings, booking_dt, duration
        )
        tables = self.select_tables(guests, available)

        if not tables:
            return

        booking = {
            "booking_id": self.generate_booking_id(bookings),
            "customer_name": name,
            "mobile": mobile,
            "booking_date": booking_dt.strftime("%d-%m-%Y"),
            "booking_time": booking_dt.strftime("%I:%M %p"),
            "guests": guests,
            "duration": duration,
            "table_number": tables,
            "status": "Pending"
        }

        bookings.append(booking)
        self.save_bookings(bookings)
        print(f"Booking successful. Booking ID: {booking['booking_id']}")
        print(f"Tables: {', '.join(tables)}")

    def view_bookings(self):
        bookings = self.load_bookings()

        if not bookings:
            print("Koi booking nahi hai.")
            return

        for b in bookings:
            tables = b.get("table_number", [])
            if isinstance(tables, str):
                tables = [tables]

            print("-" * 40)
            print("Booking ID:", b.get("booking_id"))
            print("Customer:", b.get("customer_name"))
            print("Mobile:", b.get("mobile"))
            print("Date:", b.get("booking_date"))
            print("Time:", b.get("booking_time"))
            print("Guests:", b.get("guests"))
            print("Duration:", b.get("duration", 1), "hours")
            print("Tables:", ", ".join(tables))
            print("Status:", b.get("status"))

    def search_booking(self):
        booking_id = input("Booking ID: ").strip().upper()
        bookings = self.load_bookings()

        for booking in bookings:
            if booking.get("booking_id") == booking_id:
                print(json.dumps(booking, indent=4))
                return

        print("Booking nahi mili.")

    def update_status(self):
        booking_id = input("Booking ID: ").strip().upper()
        bookings = self.load_bookings()

        for booking in bookings:
            if booking.get("booking_id") == booking_id:
                print("1. Pending")
                print("2. Completed")
                print("3. Cancelled")

                choice = input("Choice: ").strip()
                statuses = {
                    "1": "Pending",
                    "2": "Completed",
                    "3": "Cancelled"
                }

                if choice in statuses:
                    booking["status"] = statuses[choice]
                    self.save_bookings(bookings)
                    print("Booking status updated.")
                else:
                    print("Invalid choice.")
                return

        print("Booking nahi mili.")

    def update_booking(self):
        booking_id = input("Booking ID: ").strip().upper()
        bookings = self.load_bookings()

        for booking in bookings:
            if booking.get("booking_id") != booking_id:
                continue

            if booking.get("status") in ("Cancelled", "Completed"):
                print("Is booking ko update nahi kar sakte.")
                return

            print("1. Customer name")
            print("2. Mobile number")
            print("3. Booking date and time")
            print("4. Guests and tables")
            print("5. Duration")

            choice = input("Choice: ").strip()

            if choice == "1":
                name = input("New name: ").strip()
                if len(name) >= 3 and name.replace(" ", "").isalpha():
                    booking["customer_name"] = name
                else:
                    print("Invalid name.")
                    return

            elif choice == "2":
                mobile = input("New mobile: ").strip()
                if re.fullmatch(r"\d{10}", mobile):
                    booking["mobile"] = mobile
                else:
                    print("Invalid mobile number.")
                    return

            elif choice == "3":
                new_dt = self.get_booking_datetime()
                booking["booking_date"] = new_dt.strftime("%d-%m-%Y")
                booking["booking_time"] = new_dt.strftime("%I:%M %p")

            elif choice == "4":
                booking["guests"] = self.get_guests()

            elif choice == "5":
                booking["duration"] = self.get_duration()

            else:
                print("Invalid choice.")
                return

            self.save_bookings(bookings)
            print("Booking updated.")
            return

        print("Booking nahi mili.")

    def booking_management(self):
        while True:
            print("\n--- TABLE BOOKING MANAGEMENT ---")
            print("1. Create Booking")
            print("2. View Bookings")
            print("3. Search Booking")
            print("4. Update Booking")
            print("5. Update Booking Status")
            print("6. Back")

            choice = input("Choice: ").strip()

            if choice == "1":
                self.create_booking()
            elif choice == "2":
                self.view_bookings()
            elif choice == "3":
                self.search_booking()
            elif choice == "4":
                self.update_booking()
            elif choice == "5":
                self.update_status()
            elif choice == "6":
                break
            else:
                print("Invalid choice.")
                error_handler.warning("Invalid booking menu choice.")