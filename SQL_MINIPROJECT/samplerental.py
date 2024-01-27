import mysql.connector as sqlc

def check_and_initialize_db():
    try:
        connection = sqlc.connect(
            host="your_host",
            user="your_username",
            password="your_password",
            database="mysql"
        )
        cursor = connection.cursor()

        # Check if the database exists
        cursor.execute("SHOW DATABASES LIKE 'RENTALDEMO'")
        database_exists = cursor.fetchone()
        if not database_exists:
            initialize_db(cursor)
        else:
            # Database exists, check if the tables exist
            cursor.execute("USE RENTALDEMO")
            cursor.execute("SHOW TABLES LIKE 'REGISTRATION'")
            registration_table_exists = cursor.fetchone()

            if not registration_table_exists:
                initialize_db(cursor)

        cursor.close()
        connection.close()
    except sqlc.Error as err:
        print("Something went wrong: {}".format(err))

def initialize_db(cursor):
    try:
        # Create database if it doesn't exist and use it
        cursor.execute("CREATE DATABASE IF NOT EXISTS RENTALDEMO;")
        cursor.execute("USE RENTALDEMO;")

        # Create the REGISTRATION table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS REGISTRATION (
                USER_ID INT AUTO_INCREMENT PRIMARY KEY,
                USERNAME VARCHAR(50) UNIQUE NOT NULL,
                PASSWORD VARCHAR(50) NOT NULL
            );
        """)
        
        # Create the PUBLISHER2 table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS PUBLISHER2 (
                Name VARCHAR(255) PRIMARY KEY,
                Address VARCHAR(255),
                Phone VARCHAR(20)  
            );
        """)
        
        # Create the BOOK2 table with the appropriate foreign key
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS BOOK2 (
                BookID INT PRIMARY KEY AUTO_INCREMENT,
                Title VARCHAR(255),
                PublisherName VARCHAR(255),
                PublicationYear INT,
                CONSTRAINT book_publishername FOREIGN KEY(PublisherName) REFERENCES PUBLISHER2(Name)
            );
        """)
        
        # Create the BOOK_AUTHOR2 table with the appropriate foreign key
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS BOOK_AUTHOR2 (
                BookID INT,
                Author_Name VARCHAR(255),
                PRIMARY KEY(BookID, Author_Name),
                FOREIGN KEY(BookID) REFERENCES BOOK2(BookID) ON DELETE CASCADE
            );
        """)

          # Create the RENTED table with appropriate foreign key
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS RENTED (
                PURCHASE_ID INT AUTO_INCREMENT PRIMARY KEY,
                USER_ID INT,
                BOOK_NAME VARCHAR(100) NOT NULL,
                PUBLISHER_NAME VARCHAR(100) NOT NULL,
                FOREIGN KEY (USER_ID) REFERENCES REGISTRATION(USER_ID),
                FOREIGN KEY (PUBLISHER_NAME) REFERENCES PUBLISHER2(Name)
            );
        """)
    except sqlc.Error as err:
        print("Something went wrong: {}".format(err))

# Function to register new user
def register(cursor, conn):
    username = input("Choose a username: ")
    password = input("Choose a password: ")
    try:
        cursor.execute("INSERT INTO REGISTRATION(USERNAME, PASSWORD) VALUES(%s, %s)", (username, password))
        conn.commit()
        print("Registration successful!\nPlease log in with your new account.")
        login_flow(cursor, conn)  # Proceed to login after registration
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))

# Function to validate login
def login(cursor, username, password):
    cursor.execute("SELECT * FROM REGISTRATION WHERE USERNAME=%s AND PASSWORD=%s", (username, password))
    account = cursor.fetchone()
    return account is not None

# Login flow that can be called separately
def login_flow(cursor, conn):
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    if login(cursor, username, password):
        print("Logged in successfully!")
        user_id = get_user_id(cursor, username)  # Fetch the user ID for the username
        purchase_flow(cursor, conn, user_id)  # Proceed to purchase after successful login
    else:
        print("Login failed. Please check your username and password.")

# Function to get user_id based on username
def get_user_id(cursor, username):
    cursor.execute("SELECT USER_ID FROM REGISTRATION WHERE USERNAME = %s", (username,))
    result = cursor.fetchone()
    return result[0] if result else None

#NOTE HAVE TO INSERT MORE VALUES AND ALSO WORK ON DUEDATE AND DATEOUT
def insert_initial_records(cursor):
    publisher_inserts = [
        "INSERT INTO PUBLISHER2 VALUES('Willey', 'Mangalore', '98745521');",
        "INSERT INTO PUBLISHER2 VALUES('Wesley','Mangalore','98745421');",
       " INSERT INTO PUBLISHER2 VALUES('Nathan','Mangalore','98741121');",
        "INSERT INTO PUBLISHER2 VALUES('Hana','Mangalore','98742121');",
        "INSERT INTO PUBLISHER2 VALUES('Sara','Mangalore','987486721');",
        "INSERT INTO PUBLISHER2 VALUES('Wiliam','Mangalore','98743421');"
    ]

    book_inserts = [
        "INSERT INTO BOOK2 VALUES('8011', 'Mangaloredatabase', 'Willey', '2001');",
       " INSERT INTO BOOK2 VALUES('8012','Bangaldatabase','Wesley', '2002');",
        "INSERT INTO BOOK2 VALUES('8013','Bangaloredatabase','Nathan', '2003');",
        "INSERT INTO BOOK2 VALUES('8014','Newdatabase','Hana', '2004');",
        "INSERT INTO BOOK2 VALUES('8015','Finedatabase','Sara', '2005');",
        "INSERT INTO BOOK2 VALUES('8016','Okedatabase','Wiliam', '2006');"
    ]

    book_authors = [
        "INSERT INTO BOOK_AUTHOR2 VALUES('8011','Mangaloredatabase');",
        "INSERT INTO BOOK_AUTHOR2 VALUES('8012','Bangaldatabase');",
        "INSERT INTO BOOK_AUTHOR2 VALUES('8013','Bangaloredatabase');",
       " INSERT INTO BOOK_AUTHOR2 VALUES('8014','Newdatabase');",
        "INSERT INTO BOOK_AUTHOR2 VALUES('8015','Finedatabase');",
        "INSERT INTO BOOK_AUTHOR2 VALUES('8016','Okedatabase');"

    ]

    for insertion_query in publisher_inserts + book_inserts + book_authors:  # Add more lists as needed
        try:
            cursor.execute(insertion_query)
        except sqlc.Error as err:
            print(f"An error occurred: {err}")

    conn.commit()

# Function to handle book purchase
def purchase(cursor, conn, user_id, book_name, publisher_name):
    try:
        cursor.execute("""
            INSERT INTO RENTED(PUBLISHER_NAME, USER_ID, BOOK_NAME)
            VALUES(%s, %s, %s);""", (publisher_name, user_id, book_name))
        cursor.execute("SELECT LAST_INSERT_ID()")  # Execute the query to obtain the last inserted ID
        purchase_id = cursor.fetchone()[0]  # Retrieve the last inserted ID
        conn.commit()
        print("Purchase successful! Your purchase ID is:", purchase_id)
        return purchase_id
    except sqlc.Error as err:
        print("Something went wrong: {}".format(err))


# Purchase flow that can be called separately
def purchase_flow(cursor, conn, user_id):
    book_name = input("Enter the book name you want to rent: ")
    publisher_name = input("Enter the publisher name: ")
    days = int(input("Enter the number of days you want to rent the book (7-30 days): "))
    if 7 <= days <= 30:
        purchase_id = purchase(cursor, conn, user_id, book_name, publisher_name)
        if purchase_id:
            print("Book rented successfully for", days, "days. Purchase ID:", purchase_id)
    else:
        print("Invalid number of days. Please choose a value between 7 and 30.")

# Main menu function
def main_menu(cursor, conn):
    print("Welcome to BOOKRENTALDEMO")
    action = input("Type 'register' to create a new account or 'login' to access your account: ").lower()
    if action == 'register':
        register(cursor, conn)
    elif action == 'login':
        login_flow(cursor, conn)
    elif action == 'purchase':
        user_id = input("Enter your user ID: ")
        purchase_flow(cursor, conn, user_id)
    else:
        print("Invalid option, please type 'register', 'login', or 'purchase'.")

# Connect to MySQL
conn = sqlc.connect(host='localhost', user=input("Enter your MySQL username: "), password=input("Enter your MySQL password: "))
cursor = conn.cursor()

# Call the function to check and initialize the database
check_and_initialize_db()

initialize_db(cursor)  # Initialize the database and tables
insert_initial_records(cursor)


# Call the main menu function at the end of the script to start the process
main_menu(cursor, conn)

# Close the cursor and connection
cursor.close()
conn.close()
