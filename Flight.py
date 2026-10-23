from abc import ABC, abstractmethod


# Base class - Abstraction
class Passenger(ABC):
    def __init__(self, name, age):
        self.name = name
        self.age = age

    @abstractmethod
    def get_discount(self):
        pass

    def get_type(self):
        return "Passenger"


# Inheritance
class RegularPassenger(Passenger):
    def get_discount(self):
        return 0.0

    def get_type(self):
        return "Regular"


class StudentPassenger(Passenger):
    def get_discount(self):
        return 0.10

    def get_type(self):
        return "Student"


# Flight class
class Flight:
    def __init__(self, code, airline, source, destination,
                 seats, base_fare):
        self.code = code
        self.airline = airline
        self.source = source
        self.destination = destination
        self.__available_seats = seats
        self.base_fare = base_fare

    @property
    def available_seats(self):
        return self.__available_seats

    def reserve_seats(self, count):
        if count <= self.__available_seats:
            self.__available_seats -= count
            return True
        return False

    def display(self):
        print(
            f"{self.code} | {self.airline} | "
            f"{self.source} to {self.destination} | "
            f"Seats: {self.available_seats} | "
            f"Fare: Rs.{self.base_fare}"
        )


# Booking class
class Booking:
    def __init__(self, booking_id, flight, passenger,
                 tickets, subtotal, discount, total):
        self.booking_id = booking_id
        self.flight = flight
        self.passenger = passenger
        self.tickets = tickets
        self.subtotal = subtotal
        self.discount = discount
        self.total = total

    def display_summary(self):
        print("\n========== BOOKING SUMMARY ==========")
        print("Booking ID:", self.booking_id)
        print("Flight:", self.flight.code)
        print("Airline:", self.flight.airline)
        print("Route:", self.flight.source, "to",
              self.flight.destination)
        print("Passenger:", self.passenger.name)
        print("Age:", self.passenger.age)
        print("Passenger Type:", self.passenger.get_type())
        print("Tickets:", self.tickets)
        print("Base fare per ticket: Rs.",
              self.flight.base_fare)
        print("Subtotal: Rs.", self.subtotal)
        print("Discount: Rs.", self.discount)
        print("Final amount: Rs.", self.total)
        print("=====================================")


# Main application
class FlightBookingSystem:
    def __init__(self):
        self.flights = [
            Flight("PN101", "Kiran Air", "Pune",
                   "Delhi", 20, 4000),
            Flight("MB202", "Sky India", "Mumbai",
                   "Bengaluru", 15, 3500),
            Flight("PN303", "Kiran Air", "Pune",
                   "Hyderabad", 25, 3000)
        ]
        self.bookings = []
        self.next_booking_id = 1001

    def display_flights(self):
        print("\n----------- AVAILABLE FLIGHTS -----------")
        for flight in self.flights:
            flight.display()

    def find_flight(self, code):
        for flight in self.flights:
            if flight.code.lower() == code.lower():
                return flight
        return None

    def book_flight(self):
        try:
            code = input("Enter flight code: ").strip()
            flight = self.find_flight(code)

            if flight is None:
                print("Error: Invalid flight code.")
                return

            name = input("Enter passenger name: ").strip()
            if not name:
                print("Error: Passenger name cannot be blank.")
                return

            age = int(input("Enter age: "))
            if age <= 0:
                print("Error: Age must be greater than 0.")
                return

            passenger_type = input(
                "Passenger type (Regular/Student): "
            ).strip().lower()

            if passenger_type == "regular":
                passenger = RegularPassenger(name, age)
            elif passenger_type == "student":
                passenger = StudentPassenger(name, age)
            else:
                print("Error: Enter Regular or Student.")
                return

            tickets = int(input("Enter number of tickets: "))
            if tickets <= 0:
                print("Error: Tickets must be greater than 0.")
                return

            if tickets > flight.available_seats:
                print("Booking failed: Not enough seats available.")
                return

            # Polymorphism: same method, different passenger types
            subtotal = flight.base_fare * tickets
            discount = subtotal * passenger.get_discount()
            total = subtotal - discount

            # Update seats only after validation
            flight.reserve_seats(tickets)

            booking = Booking(
                f"BK{self.next_booking_id}",
                flight, passenger, tickets,
                subtotal, discount, total
            )

            self.bookings.append(booking)
            self.next_booking_id += 1

            print("\nBooking confirmed!")
            booking.display_summary()

        except ValueError:
            print("Error: Please enter valid numeric values.")

    def view_booking(self):
        if not self.bookings:
            print("No confirmed booking found.")
        else:
            self.bookings[-1].display_summary()

    def run(self):
        while True:
            print("\n===== WELCOME TO KIRAN AIR BOOKING =====")
            print("1. View Flights")
            print("2. Book Flight")
            print("3. View Booking")
            print("4. Exit")

            choice = input("Enter choice: ").strip()

            if choice == "1":
                self.display_flights()
            elif choice == "2":
                self.book_flight()
            elif choice == "3":
                self.view_booking()
            elif choice == "4":
                print("Thank you for using Kiran Air Booking!")
                break
            else:
                print("Invalid choice. Please select 1 to 4.")


if __name__ == "__main__":
    app = FlightBookingSystem()
    app.run()