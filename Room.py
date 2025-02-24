from Database import Database

class Room:
    def __init__(self, db, room_id, room_type, hotel_id, room_number, capacity, rating, price_USD,room_status):
        self.db = db
        self.__room_id = room_id
        self.room_type = room_type
        self.hotel_id = hotel_id
        self.room_number = room_number
        self.capacity = capacity
        self.rating = rating
        self.__price_USD = price_USD
        self.room_status = room_status

    @property
    def price_USD(self):
        return self.__price_USD

    @price_USD.setter
    def price_USD(self, value):
        if value < 0:
            raise ValueError("Price cannot be negative")
        
        self.__price_USD = value

    @property
    def room_id(self):
        return self.__room_id
    
    def get_bookings(self):
        response = self.db.client.table("bookings").select("*").eq("room_id", self.room_id).execute()
        bookings = response.data
        return bookings

    def add_booking(self, booking_date, guest_name, guest_phone, payment_method, status):
        params = {
            "room_id": self.room_id,
            "hotel_id": self.hotel_id,
            "booking_date": booking_date,
            "guest_name": guest_name,
            "guest_phone": guest_phone,
            "payment_method": payment_method,
            "status": status 
        }
        self.db.client.table("bookings").insert(params).execute() 



class SuiteRoom(Room):
    def __init__(self, db, room_id, room_type, hotel_id, room_number, capacity, rating, price_USD,room_status):
        super().__init__(db, room_id, room_type, hotel_id, room_number, capacity, rating, price_USD,room_status)
        self.__hasPool = True
        self.minibar = {
            "snacks": ["chips", "nuts", "chocolates"],
            "drinks": ["soda", "water", "beer"]
        }

    @property
    def hasPool(self):
        return self.__hasPool

    def get_minibar(self):
        return self.minibar
    
    def clean_pool(self):
        print("Cleaning the pool")
        

def load_rooms(db, data):
    rooms = []
    for room in data:
        if "suite" in room["room_type"].lower():
            room_obj = SuiteRoom(db, **room)
        else:
            room_obj = Room(db, **room)
        rooms.append(room_obj)
    return rooms


if __name__ == "__main__":  
    db = Database()
    response = db.client.table("hotel_rooms").select("*").execute()
    hotel_rooms = response.data
    
    rooms = load_rooms(db, hotel_rooms)

    for room in rooms:
        if isinstance(room, SuiteRoom):
            print(f"Room {room.room_number}({room.room_type}):")
            room.clean_pool()
            # print(room.get_minibar())

    