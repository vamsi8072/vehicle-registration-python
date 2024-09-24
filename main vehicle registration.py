import random
import mysql.connector
from datetime import datetime

print("\t\t\t\t\tRTO\t")
print("\t\t\t\t\t~~~")
print("\t\t\t\t WELCOME TO VEHICLE REGISTRATION")
print("\t\t\t\t ~~~~~~~ ~~ ~~~~~~~ ~~~~~~~~~~~~")

db_config = {
    'host': 'localhost',
    'user': 'root', 
    'password': '234689',  
    'database': 'vehiclereg' 
}

def get_db_connection():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

users = {"vamsi@gmail.com": "********"}

def generate_otp():
    return str(random.randint(1000, 9999))

def verify_otp(sent_otp):
    entered_otp = input("Enter the OTP sent to your phone: ")
    return entered_otp == sent_otp

def login():
    print("\nLogin to Username And Password")
    username = input("Username: ")
    password = input("Password: ")
    if username in users and users[username] == password:
        print("Login successful!")
        return True
    else:
        print("Invalid username or password.")
        return False

def add_vehicle():
    conn = get_db_connection()
    if not conn:
        print("Database connection failed.")
        return
    cursor = conn.cursor()

    print("Enter Owner and Vehicle Details:")
    name = input("Name: ")
    address = input("Address: ")
    age = int(input("Age: "))
    if age < 18:
        print("You Are Not Eligible")
        return

    email = input("Email (example@gmail.com): ")
    while not email.endswith('@gmail.com'):
        print("Invalid email. Please enter a valid Gmail address.")
        email = input("Email (example@gmail.com): ")

    phone_number = input("Phone Number (10 digits): ")
    while not (phone_number.isdigit() and len(phone_number) == 10):
        print("Invalid phone number. Please enter a 10-digit number.")
        phone_number = input("Phone Number (10 digits): ")

    input("OTP should be sent in (phone number or email): ")
    print("OTP has been sent successfully")
    otp = generate_otp()
    print(f"OTP for verification: {otp}")
    if not verify_otp(otp):
        print("OTP verification failed. Vehicle registration aborted.")
        return

    aadhar_number = input("Aadhar Number: ")
    while not (aadhar_number.isdigit() and len(aadhar_number) == 12):
        print("Invalid Aadhar number. Please enter a 12-digit Aadhar number.")
        aadhar_number = input("Aadhar Number: ")

    driving_license = input("Driving License Number: ")
    input("Vehicle Type (Bike/Car/Auto/Lorry): ")
    vehicle_production_company = input("Production Company: ")
    input("Vehicle Model: ")
    dob = input("Date of Birth (DD-MM-YYYY): ")
    ownership = input("Ownership (1st/2nd/...): ")
    year_of_manufacture = int(input("Year of Manufacture (YYYY): "))
    year_of_buying = int(input("Year of Buying (YYYY): "))
    reg_number = input("Vehicle Registration Number: ")
    chasis_number = input("Chasis Number: ")
    weight = int(input("Weight (in Kg): "))
    cc = input("Cubic Capacity (CC): ")
    engine_number = input("Engine Number: ")
    color = input("Color: ")
    fuel_type = input("Fuel Type (Petrol/Diesel/Speed): ")
    capacity = input("Capacity (in liters): ")
    num_of_cylinders = input("Number of Cylinders: ")
    seating_capacity = input("Seating Capacity: ")

    try:
        insert_query = """
        INSERT INTO vehicles(name, address, email, phone_number, aadhar_number, driving_license,
                              vehicle_production_company, dob, ownership, year_of_manufacture,
                              year_of_buying, reg_number, chasis_number, weight, cc, engine_number,
                              color, fuel_type, capacity, num_of_cylinders, seating_capacity)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        data = (name, address, email, phone_number, aadhar_number, driving_license,
                vehicle_production_company, dob, ownership, year_of_manufacture,
                year_of_buying, reg_number, chasis_number, weight, cc, engine_number,
                color, fuel_type, capacity, num_of_cylinders, seating_capacity)
        cursor.execute(insert_query, data)
        conn.commit()
        print("Vehicle Registered Successfully!")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def search_vehicle(reg_number):
    conn = get_db_connection()
    if not conn:
        print("Database connection failed.")
        return
    cursor = conn.cursor(dictionary=True)

    try:
        search_query = "SELECT * FROM vehicles WHERE reg_number = %s"
        cursor.execute(search_query, (reg_number,))
        result = cursor.fetchone()
        if result:
            print("\t\tVehicle Found!")
            print_vehicle_details(result)
        else:
            print("\t\tVehicle not found.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

def display_vehicles():
    conn = get_db_connection()
    if not conn:
        print("Database connection failed.")
        return
    cursor = conn.cursor(dictionary=True)

    try:
        select_query = "SELECT name, phone_number, reg_number FROM vehicles"
        cursor.execute(select_query)
        results = cursor.fetchall()
        if not results:
            print("\t\tNo vehicles registered.")
        else:
            print("\t\tRegistered Vehicles:")
            for vehicle in results:
                print(f"Owner Name: {vehicle['name']}")
                print(f"Phone Number: {vehicle['phone_number']}")
                print(f"Vehicle Number: {vehicle['reg_number']}")
                print("-" * 30)
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

def delete_vehicle(reg_number):
    conn = get_db_connection()
    if not conn:
        print("Database connection failed.")
        return
    cursor = conn.cursor()

    try:
        delete_query = "DELETE FROM vehicles WHERE reg_number = %s"
        cursor.execute(delete_query, (reg_number,))
        if cursor.rowcount == 0:
            print("\t\tVehicle not found.")
        else:
            conn.commit()
            print("\t\tVehicle removed successfully!")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def update_vehicle():
    conn = get_db_connection()
    if not conn:
        print("Database connection failed.")
        return
    cursor = conn.cursor()

    reg_number = input("Enter vehicle registration number to update: ")

    
    search_query = "SELECT * FROM vehicles WHERE reg_number = %s"
    cursor.execute(search_query, (reg_number,))
    vehicle = cursor.fetchone()

    if not vehicle:
        print("\t\tVehicle not found.")
        cursor.close()
        conn.close()
        return

    print("\t\tUpdating Vehicle Information")
    print("Leave the field blank if you do not want to change the value.")

    
    name = input(f"Name ({vehicle[0]}): ") or vehicle[0]
    address = input(f"Address ({vehicle[1]}): ") or vehicle[1]
    email = input(f"Email ({vehicle[2]}): ") or vehicle[2]
    phone_number = input(f"Phone Number ({vehicle[3]}): ") or vehicle[3]
    aadhar_number = input(f"Aadhar Number ({vehicle[4]}): ") or vehicle[4]
    driving_license = input(f"Driving License Number ({vehicle[5]}): ") or vehicle[5]
    dob = input(f"Date of Birth ({vehicle[7]}): ") or vehicle[7]
    ownership = input(f"Ownership ({vehicle[8]}): ") or vehicle[8]

    update_query = """
    UPDATE vehicles
    SET name = %s, address = %s, email = %s, phone_number = %s,  aadhar_number = %s, driving_license = %s, dob = %s, ownership = %s
    WHERE reg_number = %s"""

    data = (name, address, email, phone_number, aadhar_number,
            driving_license, dob, ownership, reg_number)

    try:
        cursor.execute(update_query, data)
        conn.commit()
        print("Vehicle details updated successfully!")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def print_vehicle_details(vehicle):
    print(f"Name: {vehicle['name']}")
    print(f"Address: {vehicle['address']}")
    print(f"Email: {vehicle['email']}")
    print(f"Phone Number: {vehicle['phone_number']}")
    print(f"Aadhar Number: {vehicle['aadhar_number']}")
    print(f"Driving License Number: {vehicle['driving_license']}")
    print(f"Vehicle Production Company: {vehicle['vehicle_production_company']}")
    print(f"Date of Birth: {vehicle['dob']}")
    print(f"Ownership: {vehicle['ownership']}")
    print(f"Year of Manufacture: {vehicle['year_of_manufacture']}")
    print(f"Year of Buying: {vehicle['year_of_buying']}")
    print(f"Registration Number: {vehicle['reg_number']}")
    print(f"Chasis Number: {vehicle['chasis_number']}")
    print(f"Weight: {vehicle['weight']}")
    print(f"Cubic Capacity (CC): {vehicle['cc']}")
    print(f"Engine Number: {vehicle['engine_number']}")
    print(f"Color: {vehicle['color']}")
    print(f"Fuel Type: {vehicle['fuel_type']}")
    print(f"Capacity: {vehicle['capacity']}")
    print(f"Number of Cylinders: {vehicle['num_of_cylinders']}")
    print(f"Seating Capacity: {vehicle['seating_capacity']}")

if __name__ == "__main__":
    if login():
        while True:
            print("\nVehicle Registration System")
            print("1. Add a new vehicle")
            print("2. Search for a vehicle")
            print("3. Display all vehicles")
            print("4. Delete a vehicle")
            print("5. Update a vehicle")
            print("6. Exit")

            choice = input("Enter your choice: ")

            if choice == "1":
                add_vehicle()
            elif choice == "2":
                reg_number = input("Enter vehicle registration number to search: ")
                search_vehicle(reg_number)
            elif choice == "3":
                display_vehicles()
            elif choice == "4":
                reg_number = input("Enter vehicle registration number to delete: ")
                delete_vehicle(reg_number)
            elif choice == "5":
                update_vehicle()
            elif choice == "6":
                print("Exiting...")
                print("\t\tTHANK YOU!...")
                break
            else:
                print("Invalid choice. Please enter a number from 1 to 6.")
