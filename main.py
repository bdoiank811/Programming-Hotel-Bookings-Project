class Room:
    def _validate_type(self, room_type):
        if not isinstance(room_type, str):
            raise TypeError("Room type must be a string")
        
        allowed_types = ["single", "double", "family", "suite"]
        if room_type.lower() not in allowed_types:
            raise ValueError("Invalid room type")
        else:
            return room_type.strip().capitalize()
    
    def _validate_rate(self, room_rate):
        try:
            rate_float = float(room_rate)
        except (ValueError, TypeError):
            raise TypeError("Room rate must be a number")
        
        if rate_float <= 0:
            raise ValueError("Room rate must be greater than 0")

    def _validate_id(self, room_id):
        if not isinstance(room_id, str) or not room_id.strip():
            raise ValueError("Room ID must be a non-empty string")
        return room_id.strip()
    
    def __init__(self, room_id, room_type, room_rate, hotel):
            self._room_id = self._validate_id(room_id)
            self._room_type = self._validate_type(room_type)
            self._room_rate = self._validate_rate(room_rate)
            self._hotel = hotel
            self._bookings = []

# --- Domain methods ---
    def capacity(self):
        match self._room_type.capitalize():
            case "Single":
                return 1
            case "Double":
                return 2
            case "Family":
                return 4
            case "Suite":
                return 4
    
    def is_available(self, start_date, end_date):
            for booking in self._bookings:
                if booking.is_active and booking.overlaps(start_date, end_date):
                    return False
                return True

    def add_booking(self, booking_obj):
            self._bookings.append(booking_obj)
    
# --- Getters and setters
    def get_room_rate(self):
        return self._room_rate
    
    def set_room_rate(self, new_rate):
        self._room_rate = self._validate_rate(new_rate)
    
    def get_room_type(self):
        return self._room_type

    def set_room_id(self, new_id):
        self._room_id = self._validate_id(new_id)
    
    def get_hotel(self):
        return self._hotel
    
    def set_hotel(self, hotel_obj):
        self._hotel = hotel_obj
    
    def get_bookings(self):
        return self._bookings.copy()
    

# --- dunder methods ---
    def __str__(self):
        return(f"Room id: {self._room_id}, type: {self._room_type}, rate: {self._room_rate:.2f} per night")
    
    def __eq__(self, other):
        if isinstance (other, Room):
            return self._room_id == other._room_id
        else:
            return False
    
    def __len__(self):
        return len(self._bookings)
    
    def __contains__(self, booking_obj):
        return booking_obj in self._bookings

"""IMPORTANT: for the Room class to work, these functions are required in other classes:
Booking class: 
booking.is_active() which returns True if the booking is not cancelled
booking.overlaps(start_date, end_date) which returns True if the booking date overlaps start_date, end_date
Hotel class:
hotel._hotel_id"""