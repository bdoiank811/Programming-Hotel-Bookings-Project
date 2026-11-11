#Guest class is a customer profile that contains the bookings a guest has made.
#csv columns: guest_id, guest_name, guest_country

class guest:   #hotel guest and the list of bookings they made

    def __init__ (self, guest_id, name, country):
        self.__guest_id = self.__validate_id(guest_id)
        self.__name = self.__validate_text(name, "guest name")
        self.__country = self.__validate_text(country, "Guest country")
        self.__bookings = []


@staticmethod # these are the private validation helpers, they are statice methods bc they don't need to use the object itself 
def __validate_id(guest_id):
    guest_id = str(guest_id).upper().strip()
    if len(guest_id) < 2 or guest_id[0] != "g" or not guest_id[1:].isdigit():
        raise ValueError(f"Gueust ID '{guest_id}' must have the format of G001.")
    return guest_id
def __validate_text(value, field):
    value = str(value).strip()
    if not value: raise ValueError(f"{field} can't be empty.")
    return value 

 # next we construct the getters and setters 

def get_guest_id(self):
    return self.__guest_id__  # guest id doesnt need a setter because it is the identity and should not be changed
   
def get_name(self):
        return self.__name
def set_name(self, name):
        self.__name = self.__validate_text(name, "Guest name")

def get_country(self):
        return self.__country
def set_country(self, country):
        self.__country = self.__validate_text(country, "Guest country")

def get_bookings(self): #Return a copy so the internal list can't be changed from outside
        return list(self.__bookings) # also no setter 


    # Behaviour
   
def add_booking(self, booking):
        if booking.get_guest() is not self:
            raise ValueError("This booking belongs to a different guest.")
        if booking in self.__bookings:
            raise ValueError(f"Booking {booking.get_booking_id()} is already registered.")
        self.__bookings.append(booking)

def remove_booking(self, booking_id):
        for booking in self.__bookings:
            if booking.get_booking_id() == booking_id:
                self.__bookings.remove(booking)
                return booking
        raise ValueError(f"Booking {booking_id} is not registered for guest {self.__guest_id}.")
def get_bookings_by_status(self, status):
        return [b for b in self.__bookings if b.get_status().lower() == str(status).lower()]

def calculate_total_spent(self):
        return sum(b.calculate_total_cost() for b in self.get_bookings_by_status("Checked-out"))

    
def get_total_nights(self):
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


    