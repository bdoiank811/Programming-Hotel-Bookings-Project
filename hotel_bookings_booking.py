#Booking class links one Guest and one Room for a stay period
#CSV columns booking_id, check_in, nights, check_out (derived), guests_count,
from datetime import date, timedelta # import library for date manipulation


class booking :     #represents a room reservation made by a customer at a hotel and the status of that booking  
    allowed_status = ["Confirmed", "Checked-in", "Checked-out", "Cancelled"]
    max_guests = 4 # largest room
    def __init__(self, booking_id, guest, room, check_in, nights, guest_count, status="Confirmed"):
        self.__booking_id = self.__validate_id(booking_id)
        self.__guest = guest
        self.__room = room
        self.__check_in = self.__validate_date(check_in)
        self.__nights = self.__validate_nights(nights)
        self.__guest_count = self.__validate_guest_count(guest_count)
        self.__status = self.__validate_status(status)

    @staticmethod # clean booking id
    def __validate_id(booking_id):
            booking_id = str(booking_id).upper().strip()
            if len(booking_id) < 2 or booking_id[0] != "B" or not booking_id[1:].isdigit():
                raise ValueError(f"booking ID '{booking_id}' must have the right format")
            return booking_id
    
    @staticmethod
    def __validate_date(value):
        if isinstance(value, date):
                return value
        try:
            return date.fromisoformat(str(value).strip())  
        except ValueError:
            raise ValueError(f"Date '{value}' must have the format YYYY-MM-DD.")

    @staticmethod
    def __validate_nights(nights):
        try:
                nights = int(nights)
        except (ValueError, TypeError):
                raise TypeError("Nights must be a integer.")
        if nights < 1:
                raise ValueError("Nights must be at least 1.")
        return nights
        
    @classmethod 
    def __validate_guest_count(cls, guest_count): # checks 1-4 
        try:
            guest_count = int(guest_count)
        except (ValueError, TypeError):
            raise TypeError("Guest count must be an integer.")
        if guest_count < 1 or guest_count > cls.max_guests:
            raise ValueError(f"Guest count must be between 1 and {cls.max_guests}.")
        return guest_count

    @staticmethod
    def check_fit(guest_count, room):
            # used by Hotel.book_room() and update_stay() for new/changed bookings
            if int(guest_count) > room.capacity():
                raise ValueError(f"A {room.get_room_type()} room holds at most {room.capacity()} guests.")

    @classmethod
    def __validate_status(cls, status):
            status = str(status).strip()
            for allowed in cls.allowed_status:
                if status.lower() == allowed.lower():
                    return allowed  # store cleaned up version
            raise ValueError(f"Status '{status}' must be one of {cls.allowed_status}.")






    # getters and setters
    def get_booking_id(self):
            return self.__booking_id

    def get_guest(self):
            return self.__guest

    def get_room(self):
            return self.__room

    def get_check_in(self):
            return self.__check_in

    def get_nights(self):
            return self.__nights

    def get_check_out(self):  # derived not stored
            return self.__check_in + timedelta(days=self.__nights)

    def get_guests_count(self):
            return self.__guests_count

    def get_status(self):
            return self.__status

    def set_status(self, status):
            self.__status = self.__validate_status(status)


    # check_in, nights and guests_count are changed together via update_stay()

    # behaviour
    def calculate_total_cost(self):
            return self.__room.get_room_rate() * self.__nights

    def is_cancelled(self):
            return self.__status == "Cancelled"

    def is_active(self):
            return not self.is_cancelled()

    def cancel(self):
            if self.is_cancelled():
                raise ValueError(f"Booking {self.__booking_id} is already cancelled.")
            self.__status = "Cancelled"

    def overlaps(self, check_in, nights):
            # two stays overlap if each one starts before the other one ends
            check_in = self.__validate_date(check_in)
            check_out = check_in + timedelta(days=self.__validate_nights(nights))
            return check_in < self.get_check_out() and self.__check_in < check_out

    def update_stay(self, check_in, nights, guests_count):
            # validate everything first, only then change anything
            new_check_in = self.__validate_date(check_in)
            new_nights = self.__validate_nights(nights)
            new_guests = self.__validate_guest_count(guests_count)
            self.check_fit(new_guests, self.__room)
            if not self.__room.is_available(new_check_in, new_nights, ignore_booking=self):
                raise ValueError("The room is not available for the new dates.")
            self.__check_in = new_check_in
            self.__nights = new_nights
            self.__guests_count = new_guests

    def remove(self):  # deregister from guest and room
            self.__guest.rm_booking(self.__booking_id)
            self.__room.remove_booking(self.__booking_id)

    def matches(self, **criteria):
            # e.g. booking.matches(status="Cancelled", country="Spain")
            for key, value in criteria.items():
                if value is None:
                    continue  # criterion not used
                if key == "booking_id":
                    if self.__booking_id != str(value).upper().strip():
                        return False
                elif key == "guest_id":
                    if self.__guest.getguest_id() != str(value).upper().strip():
                        return False
                elif key == "hotel_id":
                    if self.__room.get_hotel().get_hotel_id() != str(value).upper().strip():
                        return False
                elif key == "room_type":
                    if self.__room.get_room_type().lower() != str(value).lower():
                        return False
                elif key == "status":
                    if self.__status.lower() != str(value).lower():
                        return False
                elif key == "country":
                    if self.__guest.getcountry().lower() != str(value).lower():
                        return False
                elif key == "start_date":  # stay must start on/after this date
                    if self.__check_in < self.__validate_date(value):
                        return False
                elif key == "end_date":  # stay must end on/before this date
                    if self.get_check_out() > self.__validate_date(value):
                        return False
                else:
                    raise ValueError(f"Unknown search criterion '{key}'.")
            return True

        # special methods
    def __str__(self):
            return (f"{self.__booking_id}: {self.__guest.getname()} in room {self.__room.get_room_id()}, "
                    f"{self.__check_in} to {self.get_check_out()} ({self.__nights} nights), {self.__status}")

    def __eq__(self, other):
            if not isinstance(other, booking):
                return NotImplemented
            return self.__booking_id == other.__booking_id

    def __hash__(self):
            return hash(self.__booking_id)

    def __len__(self):
            return self.__nights

    def __contains__(self, day):  
            return self.__check_in <= self.__validate_date(day) < self.get_check_out()

