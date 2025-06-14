import mysql.connector
import csv
import pickle
import os

# Database connection function
def connect_db():
    """Create a database connection."""
    try:
        return mysql.connector.connect(
            host='localhost',
            user='root',
            password='1124',
            database='aditi'
        )
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
        return None


# Create Staff Records CSV
def create_staff_csv():
    """Create StaffRec.csv with sample data."""
    staff_data = [
        ['Name', 'Occupation', 'Salary', 'Years of Experience'],
        ['John Doe', 'Chef', 50000, 5],
        ['Aditi Verma', 'Manager', 60000, 7],
        ['Raj Kumar', 'Waiter', 20000, 2],
        ['John Smith ','Cleaner', 15000, 1]
    ]

    with open("StaffRec.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(staff_data)
    print("StaffRec.csv created successfully.")


# Create Reviews Binary File
def create_reviews_binary():
    """Create a binary file for storing customer reviews."""
    reviews = ["Great food and service!", "Ambiance was amazing!", "The food was too spicy."]
    with open("Review.pkl", "wb") as f:
        pickle.dump(reviews, f)
    print("Review.pkl created successfully.")

def connect_db():
    try:
        return mysql.connector.connect(
            host='localhost',
            user='root',
            password='1124',
            database='aditi'
        )
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
        return None

def main_menu():
    print("*******************WELCOME TO AKR RESTRO********************\n")
    print("1. ADMIN PORTAL")
    print("2. CUSTOMER PORTAL")
    print("3. EXIT PORTAL\n")
    try:
        option = int(input("Enter Option Number as you Desire: "))
        if option == 1:
            admin_password()
        elif option == 2:
            cus_portal()
        elif option == 3:
            print("Exiting the program.")
            exit()
        else:
            print("Invalid option. Please try again.")
            main_menu()
    except ValueError:
        print("Invalid input. Please enter a number.")
        main_menu()

def admin_password():
    print("***PASSWORD REQD***")
    password = input("Enter Password for Logging In: ")
    if password == "Y":
        adminpage_basic()
    else:
        print("Incorrect password. Redirecting to main menu.")
        main_menu()

def adminpage_basic():
    print("*******************WELCOME TO ADMIN PAGE********************\n")
    print("1. VIEW STAFF")
    print("2. UPDATE STAFF")
    print("3. VIEW ORDERS")
    print("4. VIEW CUSTOMERS")
    print("5. EXIT PORTAL\n")
    try:
        option = int(input("Enter Option Number as you Desire: "))
        if option == 1:
            staffrec_viewer()
        elif option == 2:
            staffrec_updater()
        elif option == 3:
            order_view()
        elif option == 4:
            view_customers()
        elif option == 5:
            main_menu()
        else:
            print("Invalid option. Please try again.")
            adminpage_basic()
    except ValueError:
        print("Invalid input. Please enter a number.")
        adminpage_basic()

def order_view():
    db = connect_db()
    if db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM orders")
        orders = cursor.fetchall()
        for order in orders:
            print(order)
        db.close()
        go_back = input("Do you want to go back to the admin page? (y/n): ").lower()
        if go_back == 'y':
            adminpage_basic()
        else:
            print("Going back to Main Page")
            main_menu()

def staffrec_updater():
    while True:
        print("\n1. Add Staff")
        print("2. Delete Staff")
        print("3. Exit")
        choice = input("Please choose an option (1/2/3): ").strip()
        if choice == "1":
            with open("StaffRec.csv", "a", newline="") as f:
                fwriter = csv.writer(f)
                if f.tell() == 0:
                    fwriter.writerow(['Name', 'Occupation', 'Salary', 'Years of Experience'])
                name = input("Enter Name: ")
                occupation = input("Enter Occupation: ")
                salary = input("Enter Salary: ")
                experience = input("Enter Years of Experience: ")
                fwriter.writerow([name, occupation, salary, experience])
            print("Staff added successfully.")
        elif choice == "2":
            name_to_delete = input("Enter the name of the staff to delete: ").strip()
            try:
                with open("StaffRec.csv", "r") as f:
                    lines = f.readlines()
                header = lines[0]
                staff_list = lines[1:]
                staff_found = False
                with open("StaffRec.csv", "w", newline="") as f:
                    fwriter = csv.writer(f)
                    f.write(header)
                    for line in staff_list:
                        if name_to_delete not in line:
                            f.write(line)
                        else:
                            staff_found = True
                if staff_found:
                    print(f"Staff member '{name_to_delete}' has been deleted.")
                else:
                    print(f"No staff member found with the name '{name_to_delete}'.")
            except FileNotFoundError:
                print("StaffRec.csv not found. Please add some staff first.")
        elif choice == "3":
            print("Exiting to the main menu...")
            main_menu()
            break
        else:
            print("Invalid choice. Please try again.")

def staffrec_viewer():
    import csv
    try:
        with open("StaffRec.csv", "r", newline="\r\n") as f:
            freader = csv.reader(f)
            for row in freader:
                print(row)
        go_back = input("Do you want to go back to the admin page? (y/n): ").lower()
        if go_back == 'y':
            adminpage_basic()
        else:
            print("Going back to Main Page")
            main_menu()
    except FileNotFoundError:
        print("Staff records file not found.")

def cus_portal():
    while True:
        print("\n1. Register\n2. Login\n3. Exit")
        choice = input("Choose an option: ")
        if choice == '1':
            register_user()
        elif choice == '2':
            login_user()
        elif choice == '3':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")
            main_menu()

def register_user():
    name = input("Enter your name: ")
    email = input("Enter your email: ")
    password = input("Enter your password: ")
    contact_number = input("Enter your contact number: ")
    address = input("Enter your address: ")
    user_data = {
        "name": name,
        "email": email,
        "password": password,
        "contact_number": contact_number,
        "address": address
    }
    file_path = "user_data.pkl"
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        with open(file_path, "rb") as f:
            all_users = pickle.load(f)
    else:
        all_users = []
    all_users.append(user_data)
    with open(file_path, "wb") as f:
        pickle.dump(all_users, f)
    print("Registration successful! Your user data has been saved.")

def login_user():
    email = input("Enter your email: ")
    password = input("Enter your password: ")
    file_path = "user_data.pkl"
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        with open(file_path, "rb") as f:
            all_users = pickle.load(f)
            for user in all_users:
                if user["email"] == email and user["password"] == password:
                    print(f"Login successful! Welcome back, {user['name']}.")
                    cuspage_basic()
            print("Invalid email or password. Please try again.")
    else:
        print("No registered users found. Please register first.")

def cuspage_basic():
    print("*******************WELCOME TO CUSTOMER PAGE********************")
    print("\n")
    print("1. VIEW MENU")
    print("2. PLACE ORDER")
    print("3. LEAVE REVIEW")
    print("4. GO BACK TO MAIN MENU")
    print("\n")
    try:
        w = int(input("Enter Option Number as you Desire: "))
        if w == 1:
            viewmenu()
        elif w == 3:
            review_page()
        elif w == 2:
            orper_placing()
        else:
            main_menu()
    except ValueError:
        print("Invalid input. Please try again.")
        cuspage_basic()

def viewmenu():
    db = connect_db()
    if db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM menu")
        menu_items = cursor.fetchall()
        for item in menu_items:
            print(item)
        db.close()
        if input("Do you wish to place an order? (y/n): ").strip().lower() == 'y':
            orper_placing()
        else:
            cuspage_basic()

def orper_placing():
    db = connect_db()
    if db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM menu")
        menu_items = cursor.fetchall()
        print("Available Menu Items:")
        for item in menu_items:
            print(item)
        try:
            food_item_id = int(input("Enter the serial number of the food item: "))
            quantity = int(input("Enter the quantity: "))
            sql = "INSERT INTO orders (SrNo, Name, Quantity) VALUES (%s, %s, %s)"
            cursor.execute(sql, (food_item_id, "Food Item", quantity))
            db.commit()
            print("Order placed successfully!")
        except ValueError:
            print("Invalid input. Please enter a valid number.")
        db.close()
        go_back = input("Do you want to place another order? (y/n): ").lower()
        if go_back == 'y':
            orper_placing()
        else:
            cuspage_basic()

def review_page():
    import csv
    print("****REVIEW PAGE****")
    print('\n')
    fh=open("Review.csv","a")
    fhwriter= csv.writer(fh)
    fhwriter.writerow(['REVIEWS'])
    ans = 'y'
    while ans == 'y':
        review = input("Please add review: ")
        rec = [review]
        fhwriter.writerow(rec)
        ans = input("Do you wish to continue?(y/n)")
    fh.close()




create_staff_csv()
create_reviews_binary()

main_menu()



