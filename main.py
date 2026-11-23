from datetime import date, timedelta # import library for date manipulation
import csv

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
        return rate_float

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
    
    def is_available(self, check_in, nights, ignore_booking=None):
            # ignore_booking lets a booking skip itself when its own dates are changed
            for booking in self._bookings:
                if booking is ignore_booking:
                    continue
                if booking.is_active() and booking.overlaps(check_in, nights):
                    return False
            return True

    def add_booking(self, booking_obj):
            self._bookings.append(booking_obj)

    def remove_booking(self, booking_id):
            for booking in self._bookings:
                if booking.get_booking_id() == booking_id:
                    self._bookings.remove(booking)
                    return booking
            raise ValueError(f"Booking {booking_id} is not registered for room {self._room_id}.")
    
# --- Getters and setters
    def get_room_rate(self):
        return self._room_rate
    
    def set_room_rate(self, new_rate):
        self._room_rate = self._validate_rate(new_rate)
    
    def get_room_type(self):
        return self._room_type

    def get_room_id(self):
        return self._room_id

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
booking.overlaps(check_in, nights) which returns True if the booking overlaps that stay
booking.get_booking_id()
Hotel class:
hotel._hotel_id"""


 # Guest class is a customer profile that contains the bookings a guest has made.
# csv columns: guest_id, guest_name, guest_country

class guest:  # hotel guest and the list of bookings they made

    def __init__(self, guest_id, name, country):  # constructor runs when a guest object is created
        self.__guest_id = self.__validate_id(guest_id)  # validate the id  then store it in a private attribute
        self.__name = self.__validate_text(name, "guest name")  # validate the name
        self.__country = self.__validate_text(country, "guest country")  # validate the country
        self.__bookings = []  # every new guest starts with an empty list of bookings
    # private validation helpers they are static methods bc they don't need to use the object itself
    @staticmethod
    def __validate_id(guest_id):
        guest_id = str(guest_id).upper().strip() 
        if len(guest_id) < 2 or guest_id[0] != "G" or not guest_id[1:].isdigit(): 
            raise ValueError(f"Guest ID '{guest_id}' must have the format of G001.") 
        return guest_id  # return clean valid id

    @staticmethod
    def __validate_text(value, field):
        value = str(value).strip() 
        if not value:  
            raise ValueError(f"{field} can't be empty.") 
        return value 

    #getters and setters

    def getguest_id(self):
        return self.__guest_id  # guest id doesnt need a setter because it is the identity and should not be changed

    def getname(self):
        return self.__name  # give back the guest's name

    def setname(self, name):
        self.__name = self.__validate_text(name, "Guest name")  # only store the new name if it passes validation

    def getcountry(self):
        return self.__country  #give back the guest's country

    def setcountry(self, country):
        self.__country = self.__validate_text(country, "Guest country")  # only store the new country if it is valid

    def getbookings(self):  # Return a copy so the internal list can't be changed from outside
        return list(self.__bookings) 

    # Behaviour

    def add_booking(self, booking):  #register a booking with this guest
        if booking.get_guest() is not self: 
            raise ValueError("This booking belongs to a different guest.")  #reject bookings of other guests
        if booking in self.__bookings:  # check for duplicates
            raise ValueError(f"Booking {booking.get_booking_id()} is already registered.")  # reject duplicates
        self.__bookings.append(booking)  
    def rm_booking(self, booking_id): 
        for booking in self.__bookings:  
            if booking.get_booking_id() == booking_id:  #booking with matching id taken out of the list 
                self.__bookings.remove(booking)  
                return booking  
        raise ValueError(f"Booking {booking_id} is not registered for guest {self.__guest_id}.")  

    def bookings_status(self, status):  # returns list of bookings whose status matches the status provided, case insensitive
        return [b for b in self.__bookings if b.get_status().lower() == str(status).lower()]  

    def total_spent(self):  
        return sum(b.calculate_total_cost() for b in self.bookings_status("Checked-out")) 

    def get_totalnights(self): 
        return sum(b.get_nights() for b in self.__bookings if not b.is_cancelled()) 

    # Special methods

    def __str__(self): 
        return f"{self.__guest_id} - {self.__name} ({self.__country})"  

    def __eq__(self, other): 
        if not isinstance(other, guest):  
            return NotImplemented 
        return self.__guest_id == other.__guest_id  
    
    def __hash__(self):  
        return hash(self.__guest_id)  

    def __len__(self):  
        return len(self.__bookings) 

    def __contains__(self, booking): 
        return booking in self.__bookings  

# Conventional-capitalized alias; existing code may continue using guest.
Guest = guest


#Booking class links one Guest and one Room for a stay period
#CSV columns booking_id, check_in, nights, check_out is derived, guest_count,


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
            return self.__guest_count

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
            self.__guest_count = new_guests

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

# Conventional-capitalized alias; existing code may continue using booking.
Booking = booking

class Hotel:
    #validation methods
    @staticmethod
    def _validate_id(hotel_id: str):
      if not isinstance(hotel_id, str) or not hotel_id.strip():
        raise ValueError("Hotel ID must be a non-empty string")
      return hotel_id.strip()
    
    @staticmethod
    def __validate_text(value, field):
      value = str(value).strip() 
      if not value:  
          raise ValueError(f"{field} can't be empty.") 
      return value 

    #getters and setters methods
    def get_hotel_id(self):
      return self.__hotel_id
    
    def get_name(self):
      return self.__name
    
    def get_city(self):
      return self.__city
    
    def get_rooms(self):
      return list(self.__rooms)
    
    def set_hotel_id(self, new_hotel_id: str):
      self.__hotel_id = self._validate_id(new_hotel_id)
    
    def set_name(self, new_name: str):
      self.__name = self.__validate_text(new_name, "hotel_name")
    
    def set_city(self, new_city: str):
      self.__city = self.__validate_text(new_city, "hotel_city")

    #constructor
    def __init__(self, hotel_id: str, name: str, city: str):
        self.__hotel_id = self._validate_id(hotel_id)
        self.__name = self.__validate_text(name, "hotel_name")
        self.__city = self.__validate_text(city, "hotel_city")
        self.__rooms = []


    #behaviour
    
    #Checks that room exist and for dulipcates, adds it 
    #add_room(room): validates the object, rejects a duplicate room_id, then adds the
    #room to the hotel.
    def add_room(self, room_obj):
        if not isinstance(room_obj, Room):
          raise TypeError("room_obj must be a Room.")
        if room_obj in self: #guard since it should fail when it exists
          raise ValueError(f"Room {room_obj.get_room_id()} is already registered.")
        room_obj.set_hotel(self)
        self.__rooms.append(room_obj)
  
    #find_room(room_id): returns the matching Room, or None.
    def find_room(self, room_id): 
        for room in self.__rooms:
          if room.get_room_id() == room_id:
            return room
        return None
    
    #creates the booking by finding a room, checking its availabity and assign it.
    #finds the
    #room, checks that it is available, and creates the Booking. This is the entry point for
    #new reservations.
    def book_room(self, booking_id: str, guest, room_id: str, check_in: str, nights: int, guests_count: int):
        room = self.find_room(room_id)
        #guard for non existing room
        if room == None:
          raise ValueError(f"Room {room_id} is not registered for this Hotel {self.__hotel_id}.")
          #we can presume the room exists now
        #guard for not available
        if room.is_available(check_in, nights) == False:
          raise ValueError(f"Room {room_id} is not available for {check_in} for {nights} nights.")
    
        booking = Booking(booking_id, guest, room, check_in, nights, guests_count)
    
        booking.check_fit(guests_count, room) # already has a raise valueError in it;
        guest.add_booking(booking)
        room.add_booking(booking)
        return booking
    
    #rm_room(room_id): removes a room, only if it has no active bookings.
    def rm_room(self, room_id):
        room = self.find_room(room_id)
        if room is None:
          raise ValueError(f"Room {room_id} is not registered for this Hotel {self.__hotel_id}.")
        for booking in room.get_bookings():
          if booking.is_active():
            #if the room has active booking return
            raise ValueError(f"Room {room_id} has active bookings and cannot be removed.")
        self.__rooms.remove(room)
        return room
    #get_rooms_by_type(room_type): returns all rooms of one category (Single, Double,
    #Family, Suite).
    def get_rooms_by_type(self, room_type):
        #guard if room type is none return all
        if room_type == None:
          return self.get_rooms()
        room_list = []
        for room in self.__rooms:
          if room.get_room_type().lower() == str(room_type).lower():
            room_list.append(room)
        return room_list
        
    # get_available_rooms(check_in, nights, room_type=None): returns rooms free for the
    #requested stay by asking each room’s is_available().
    def get_available_rooms(self, check_in, nights, room_type=None):
      #since we have a default for the room_type, we can do it per room_type
        room_list = self.get_rooms_by_type(room_type)
        available_rooms = []
        for room in room_list:
          if room.is_available(check_in, nights):
            available_rooms.append(room)
        return available_rooms
        
    # get_all_bookings(): collects the bookings of every room in the hotel.
    def get_all_bookings(self):
        all_bookings = []
        for room in self.__rooms:
          all_bookings.extend(room.get_bookings())
        return all_bookings

    # calculate_revenue(): sums the total cost of the hotel’s checked-out bookings.
    def calculate_revenue(self):
        total_revenue = 0
        for booking in self.get_all_bookings():
          if booking.get_status() == "Checked-out":
            total_revenue += booking.calculate_total_cost()
        return total_revenue

    #get_cancellation_rate(): returns the share of the hotel’s bookings that were cancelled.  
    def get_cancellation_rate(self):
        all_bookings = self.get_all_bookings()
        if not all_bookings:
          return 0
        cancelled_bookings = 0
        for booking in all_bookings:
          if booking.is_cancelled():
            cancelled_bookings += 1
        return cancelled_bookings / len(all_bookings)

    #special methods
    def __str__(self): 
        return f"{self.__hotel_id} - {self.__name} ({self.__city})"

    def __eq__(self, other): 
        if not isinstance(other, Hotel):  
            return NotImplemented 
        return self.__hotel_id == other.__hotel_id 
    
    def __hash__(self):  
        return hash(self.__hotel_id)  

    def __len__(self):  
        return len(self.__rooms) 
        
    def __contains__(self, room): 
        return room in self.__rooms  


def load_hotel_bookings_csv(file_path):
    """Load the project's combined hotel/room/guest/booking CSV format.

    Historical CSV capacity mismatches are reported as warnings without
    preventing the records from being loaded. Capacity is still enforced
    when using Hotel.book_room() or Booking.update_stay().
    """
    hotels = {}
    guests = {}
    bookings = []
    warnings = []

    with open(file_path, newline="", encoding="utf-8-sig") as csv_file:
        reader = csv.DictReader(csv_file)
        required_columns = {
            "booking_id", "hotel_id", "hotel_name", "hotel_city",
            "room_id", "room_type", "room_rate", "guest_id",
            "guest_name", "guest_country", "check_in", "nights",
            "check_out", "guests_count", "booking_status",
        }
        missing_columns = required_columns.difference(reader.fieldnames or [])
        if missing_columns:
            missing = ", ".join(sorted(missing_columns))
            raise ValueError(f"CSV is missing required columns: {missing}")

        for row_number, row in enumerate(reader, start=2):
            hotel_id = row["hotel_id"].strip()
            room_id = row["room_id"].strip()
            guest_id = row["guest_id"].strip()

            hotel = hotels.get(hotel_id)
            if hotel is None:
                hotel = Hotel(hotel_id, row["hotel_name"], row["hotel_city"])
                hotels[hotel_id] = hotel
            else:
                if hotel.get_name() != row["hotel_name"].strip():
                    raise ValueError(
                        f"CSV row {row_number}: hotel {hotel_id} has conflicting names."
                    )
                if hotel.get_city() != row["hotel_city"].strip():
                    raise ValueError(
                        f"CSV row {row_number}: hotel {hotel_id} has conflicting cities."
                    )

            room = hotel.find_room(room_id)
            if room is None:
                room = Room(room_id, row["room_type"], row["room_rate"], hotel)
                hotel.add_room(room)
            else:
                if room.get_room_type().lower() != row["room_type"].lower():
                    raise ValueError(
                        f"CSV row {row_number}: room {room_id} has conflicting types."
                    )
                if room.get_room_rate() != float(row["room_rate"]):
                    raise ValueError(
                        f"CSV row {row_number}: room {room_id} has conflicting rates."
                    )

            guest = guests.get(guest_id)
            if guest is None:
                guest = Guest(guest_id, row["guest_name"], row["guest_country"])
                guests[guest_id] = guest
            else:
                if guest.getname() != row["guest_name"].strip():
                    raise ValueError(
                        f"CSV row {row_number}: guest {guest_id} has conflicting names."
                    )
                if guest.getcountry() != row["guest_country"].strip():
                    raise ValueError(
                        f"CSV row {row_number}: guest {guest_id} has conflicting countries."
                    )

            guest_count = int(row["guests_count"])
            try:
                booking.check_fit(guest_count, room)
            except ValueError as error:
                warnings.append({
                    "row": row_number,
                    "booking_id": row["booking_id"].strip(),
                    "room_id": room_id,
                    "guests_count": guest_count,
                    "room_capacity": room.capacity(),
                    "message": str(error),
                })

            booking_obj = Booking(
                row["booking_id"],
                guest,
                room,
                row["check_in"],
                row["nights"],
                guest_count,
                row["booking_status"],
            )
            room.add_booking(booking_obj)
            guest.add_booking(booking_obj)
            bookings.append(booking_obj)

    return {
        "hotels": hotels,
        "guests": guests,
        "bookings": bookings,
        "warnings": warnings,
    }

# menu for user interaction
def ask(prompt):
    # input() with surrounding spaces removed
    return input(prompt).strip()


def choose_hotel(hotels):
    # show all hotels and let the user pick one. returns a Hotel or None
    print("\nHotels:")
    for hotel in hotels.values():
        print(f"  {hotel}")
    hotel_id = ask("Enter hotel ID (e.g. H01): ").upper()
    hotel = hotels.get(hotel_id)
    if hotel is None:
        print("Unknown hotel ID.")
    return hotel


def next_booking_id(bookings):
    # finds the highest existing number and adds 1
    highest = max((int(b.get_booking_id()[1:]) for b in bookings), default=0)
    return f"B{highest + 1:04d}"


def show_rooms(hotels):
    hotel = choose_hotel(hotels)
    if hotel is None:
        return
    room_type = ask("Room type (single/double/family/suite, Enter for all): ") or None
    rooms = hotel.get_rooms_by_type(room_type)
    print(f"\nRooms in {hotel.get_name()}:")
    for room in rooms:
        print(f"  {room} (fits {room.capacity()})")
    if not rooms:
        print("  No rooms found.")


def search_available(hotels):
    hotel = choose_hotel(hotels)
    if hotel is None:
        return
    check_in = ask("Check-in date (YYYY-MM-DD): ")
    nights = ask("Number of nights: ")
    room_type = ask("Room type (Enter for any): ") or None
    rooms = hotel.get_available_rooms(check_in, nights, room_type)
    print("\nAvailable rooms:")
    for room in rooms:
        print(f"  {room} (fits {room.capacity()})")
    if not rooms:
        print("  Nothing available for those dates.")


def book_a_room(data):
    hotels, guests, bookings = data["hotels"], data["guests"], data["bookings"]
    hotel = choose_hotel(hotels)
    if hotel is None:
        return
    check_in = ask("Check-in date (YYYY-MM-DD): ")
    nights = ask("Number of nights: ")
    guests_count = ask("Number of guests: ")

    # show the free rooms so the user can select one
    rooms = hotel.get_available_rooms(check_in, nights)
    if not rooms:
        print("No rooms available for those dates.")
        return
    print("\nAvailable rooms:")
    for number, room in enumerate(rooms, start=1):
        print(f"  {number}. {room} (fits {room.capacity()})")
    choice = ask("Select a room number: ")
    if not choice.isdigit() or not 1 <= int(choice) <= len(rooms):
        print("Invalid choice.")
        return
    room = rooms[int(choice) - 1]

    # existing guest or create a new one
    guest_id = ask("Guest ID (e.g. G001, or Enter for a new guest): ").upper()
    if guest_id:
        guest_obj = guests.get(guest_id)
        if guest_obj is None:
            print("Unknown guest ID.")
            return
    else:
        highest = max((int(g[1:]) for g in guests), default=0)
        guest_id = f"G{highest + 1:03d}"
        guest_obj = Guest(guest_id, ask("Guest name: "), ask("Guest country: "))
        guests[guest_id] = guest_obj

    new_booking = hotel.book_room(next_booking_id(bookings), guest_obj,
                                  room.get_room_id(), check_in, nights, guests_count)
    bookings.append(new_booking)
    print(f"\nBooked! {new_booking}")
    print(f"Total cost: {new_booking.calculate_total_cost():.2f}")


def cancel_booking(bookings):
    booking_id = ask("Booking ID to cancel (e.g. B0001): ").upper()
    for b in bookings:
        if b.get_booking_id() == booking_id:
            b.cancel()
            print(f"Cancelled: {b}")
            return
    print("Booking not found.")


def show_guest(guests):
    guest_obj = guests.get(ask("Guest ID (e.g. G001): ").upper())
    if guest_obj is None:
        print("Unknown guest ID.")
        return
    print(f"\n{guest_obj}")
    for b in guest_obj.getbookings():
        print(f"  {b}")
    print(f"Total nights: {guest_obj.get_totalnights()}, total spent: {guest_obj.total_spent():.2f}")


def show_stats(hotels):
    hotel = choose_hotel(hotels)
    if hotel is None:
        return
    print(f"\n{hotel}")
    print(f"  Rooms: {len(hotel)}")
    print(f"  Bookings: {len(hotel.get_all_bookings())}")
    print(f"  Revenue: {hotel.calculate_revenue():.2f}")
    print(f"  Cancellation rate: {hotel.get_cancellation_rate():.1%}")


def main():
    data = load_hotel_bookings_csv("hotel_booking.csv")
    print(f"Loaded {len(data['bookings'])} bookings from {len(data['hotels'])} hotels.")

    while True:
        print("\n===== HOTEL BOOKINGS =====")
        print("1. Show rooms of a hotel")
        print("2. Search available rooms")
        print("3. Book a room")
        print("4. Cancel a booking")
        print("5. Show a guest and their bookings")
        print("6. Hotel statistics")
        print("0. Quit")
        choice = ask("Choose an option: ")

        try:
            match choice:
                case "1":
                    show_rooms(data["hotels"])
                case "2":
                    search_available(data["hotels"])
                case "3":
                    book_a_room(data)
                case "4":
                    cancel_booking(data["bookings"])
                case "5":
                    show_guest(data["guests"])
                case "6":
                    show_stats(data["hotels"])
                case "0":
                    print("Goodbye!")
                    break
                case _:
                    print("Invalid option, try again.")
        except (ValueError, TypeError) as error:
            # validation errors from the classes end up here instead of crashing
            print(f"Error: {error}")


if __name__ == "__main__":
    main()
