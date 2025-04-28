import random
import sqlite3
from datetime import datetime

print('Welcome to the Password Generator')

# Create database connection and table
def setup_database():
    conn = sqlite3.connect('passwords.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            service_name TEXT NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    return conn

# Initialize database connection
conn = setup_database()

#Defing the type of Character Need for Lower Case Letter
lower_case = 'abcdefghijklmnopqrstuvwxyz'
#Defing the type of Characters need for upper case letter
upper_case = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
# Defing the type numbers that can be used for a password
number = '0123456789'

special_characters = '!@#$%^&*()'

#Combing All Characters

all_characters = lower_case + upper_case + number + special_characters
#I want there to be a min and max amount of chacters the users can input
min_length= 8
max_length = 16


# I do not want to the user to have to keep pressing the run button so I used a While Loop Continuously Run the Program
while True:
    try:
        # Ask the user for the password length
        password_length = input(f"How many characters do you want in your password? (Between {min_length} and {max_length}): ").strip()
        password_length = int(password_length)  # Convert to an integer

        # Validate the password length
        if password_length < min_length:
            print(f"Password length must be at least {min_length} characters. Please try again.")
        elif password_length > max_length:
            print(f"Password length must not exceed {max_length} characters. Please try again.")
        else:
            # Generate the password if the input is valid
            password = ''.join(random.sample(all_characters, password_length))
            print("Your generated password is:", password)

            # Ask if the user wants to save the password
            save_password = input("Would you like to save this password? (yes/no): ").strip().lower()
            if save_password == 'yes':
                service_name = input("Enter a name for this password (e.g., 'Gmail', 'Facebook'): ").strip()
                cursor = conn.cursor()
                cursor.execute('INSERT INTO passwords (service_name, password) VALUES (?, ?)', 
                             (service_name, password))
                conn.commit()
                print("Password saved successfully to database!")

            # Ask if the user wants to generate another password
            again = input("Do you want to generate another password? (yes/no): ").strip().lower()
            if again != 'yes':
                print("Thank you for using the Password Generator!")
                break
    except ValueError:
        print("Invalid input. Please enter a number.")

# Close the database connection when the program ends
conn.close()

