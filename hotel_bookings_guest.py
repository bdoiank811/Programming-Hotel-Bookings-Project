
 # Guest class is a customer profile that contains the bookings a guest has made.
# csv columns: guest_id, guest_name, guest_country

class guest:  # hotel guest and the list of bookings they made

    def __init__(self, guest_id, name, country):  # constructor runs when a guest object is created
        self.__guest_id = self.__validate_id(guest_id)  # validate the id  then store it in a private attribute
        self.__name = self.__validate_text(name, "guest name")  # validate the name
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
        return sum(b.total_cost() for b in self.bookings_status("Checked-out")) 

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


    
