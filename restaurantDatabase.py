## 

import mysql.connector
from mysql.connector import Error

class RestaurantDatabase:
    def __init__(self,
                 host="localhost",
                 port="3306",
                 database="restaurants_reservations",
                 user='root',
                 password='Ezclap.123'):

        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.connection = None
        self.cursor = None
        self.connect()

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password)
            
            if self.connection.is_connected():
                print("Successfully connected to the database")
        except Error as e:
            print("Error while connecting to MySQL", e)

    def addReservation(self, customer_name, contact_info, reservation_time, number_of_guests, special_requests):
        ''' Method to insert a new reservation into the reservations table '''
        if self.connection.is_connected():
            self.cursor = self.connection.cursor()
            
            # Check if customer already exists
            self.cursor.execute("SELECT customerId FROM customers WHERE customerName = %s AND contactInfo = %s", (customer_name, contact_info))
            result = self.cursor.fetchone()
            
            if result:
                customer_id = result[0]
            else:
                # Add new customer
                self.cursor.execute("INSERT INTO customers (customerName, contactInfo) VALUES (%s, %s)", (customer_name, contact_info))
                self.connection.commit()
                customer_id = self.cursor.lastrowid
            
            # Add reservation
            query = "INSERT INTO reservations (customerId, reservationTime, numberOfGuests, specialRequests) VALUES (%s, %s, %s, %s)"
            self.cursor.execute(query, (customer_id, reservation_time, number_of_guests, special_requests))
            self.connection.commit()
            print("Reservation added successfully")

    def getAllReservations(self):
        ''' Method to get all reservations from the reservations table '''
        if self.connection.is_connected():
            self.cursor = self.connection.cursor()
            query = """
            SELECT r.reservationId, c.customerName, c.contactInfo, r.reservationTime, r.numberOfGuests, r.specialRequests
            FROM reservations r
            JOIN customers c ON r.customerId = c.customerId
            """
            self.cursor.execute(query)
            records = self.cursor.fetchall()
            return records

    def deleteReservation(self, reservation_id):
        ''' Method to delete a reservation from the reservations table '''
        if self.connection.is_connected():
            self.cursor = self.connection.cursor()
            query = "DELETE FROM reservations WHERE reservationId = %s"
            self.cursor.execute(query, (reservation_id,))
            self.connection.commit()
            print("Reservation deleted successfully")

if __name__ == "__main__":
    db = RestaurantDatabase()
    # Example usage
    db.addReservation("John Doe", "555-1234", "2024-05-25 19:00", 4, "Window seat")
    reservations = db.getAllReservations()
    for reservation in reservations:
        print(reservation)
