from Database import Database
from datetime import datetime
from Room import Room
import sys

class RoomBookingSystem:
    def __init__(self):
        self.db = Database()
        self.load_rooms()

    def load_rooms(self):
        """Load all rooms from the database"""
        response = self.db.client.table("hotel_rooms").select("*").execute()
        self.rooms = [Room(self.db, **room_data) for room_data in response.data]

    def filter_rooms(self, min_price, max_price, min_capacity):
        """Filter rooms based on price range and capacity"""
        return [
            room for room in self.rooms
            if min_price <= room.price_USD <= max_price and room.capacity >= min_capacity
        ]

    def display_rooms(self, rooms):
        """Display room information in a formatted table"""
        print("\nAvailable Rooms:")
        print("-" * 80)
        print(f"{'Room ID':<10} {'Type':<15} {'Number':<10} {'Capacity':<10} {'Price':<10} {'Rating':<8} {'Status':<10}")
        print("-" * 80)
        
        for room in rooms:
            print(
                f"{room.room_id:<10} "
                f"{room.room_type:<15} "
                f"{room.room_number:<10} "
                f"{room.capacity:<10} "
                f"${room.price_USD:<9} "
                f"{room.rating:<8} "
                f"{room.room_status:<10}"
            )
        print("-" * 80)

    def get_user_input(self, prompt, validation_func=None, error_message=None):
        """Get and validate user input"""
        while True:
            try:
                user_input = input(prompt)
                if validation_func and not validation_func(user_input):
                    raise ValueError(error_message or "Invalid input")
                return user_input
            except ValueError as e:
                print(f"Error: {e}")

    def book_room(self, room_id):
        """Book a specific room"""
        try:
            # Find the room
            room = next((room for room in self.rooms if room.room_id == room_id), None)
            if not room:
                print("Room not found.")
                return False

            if room.room_status.lower() != 'vacant':
                print("This room is not available for booking.")
                return False

            # Get booking details
            booking_date = self.get_user_input(
                "Enter booking date (YYYY-MM-DD): ",
                lambda x: datetime.strptime(x, "%Y-%m-%d"),
                "Please enter a valid date in YYYY-MM-DD format"
            )
            
            guest_name = self.get_user_input(
                "Enter guest name: ",
                lambda x: len(x.strip()) > 0,
                "Name cannot be empty"
            )
            
            guest_phone = self.get_user_input(
                "Enter guest phone number: ",
                lambda x: len(x.strip()) > 0,
                "Phone number cannot be empty"
            )
            
            payment_method = self.get_user_input(
                "Enter payment method (cash/card): ",
                lambda x: x.lower() in ['cash', 'card'],
                "Please enter either 'cash' or 'card'"
            )

            # Add the booking
            room.add_booking(
                booking_date=booking_date,
                guest_name=guest_name,
                guest_phone=guest_phone,
                payment_method=payment_method,
                status="confirmed"
            )

            print("\nBooking successful!")
            return True

        except Exception as e:
            print(f"An error occurred while booking: {e}")
            return False

    def run(self):
        """Main program loop"""
        while True:
            print("\n=== Hotel Room Booking System ===")
            print("1. Search rooms by price and capacity")
            print("2. View all rooms")
            print("3. Book a room")
            print("4. View room bookings")
            print("5. Exit")

            choice = self.get_user_input(
                "\nEnter your choice (1-5): ",
                lambda x: x in ['1', '2', '3', '4', '5'],
                "Please enter a number between 1 and 5"
            )

            if choice == '1':
                min_price = float(self.get_user_input(
                    "Enter minimum price: ",
                    lambda x: float(x) >= 0,
                    "Price must be non-negative"
                ))
                max_price = float(self.get_user_input(
                    "Enter maximum price: ",
                    lambda x: float(x) >= min_price,
                    f"Price must be greater than or equal to {min_price}"
                ))
                min_capacity = int(self.get_user_input(
                    "Enter minimum capacity: ",
                    lambda x: int(x) > 0,
                    "Capacity must be positive"
                ))

                filtered_rooms = self.filter_rooms(min_price, max_price, min_capacity)
                self.display_rooms(filtered_rooms)

            elif choice == '2':
                self.display_rooms(self.rooms)

            elif choice == '3':
                room_id = self.get_user_input("Enter room ID to book: ")
                self.book_room(room_id)

            elif choice == '4':
                room_id = self.get_user_input("Enter room ID to view bookings: ")
                room = next((room for room in self.rooms if room.room_id == room_id), None)
                if room:
                    bookings = room.get_bookings()
                    print("\nBookings for room", room_id)
                    print("-" * 80)
                    for booking in bookings:
                        print(f"Date: {booking['booking_date']}")
                        print(f"Guest: {booking['guest_name']}")
                        print(f"Status: {booking['status']}")
                        print("-" * 80)
                else:
                    print("Room not found.")

            elif choice == '5':
                print("Thank you for using the Hotel Room Booking System!")
                sys.exit(0)

if __name__ == "__main__":
    booking_system = RoomBookingSystem()
    booking_system.run()