
from database import get_db_connection
from werkzeug.security import generate_password_hash
from getpass import getpass


def create_admin():
    print("\n===== CREATE ADMIN ACCOUNT =====")

    name = input("Enter Admin Name: ").strip()
    phone = input("Enter Admin Phone Number: ").strip()
    password = getpass("Enter Admin Password: ")
    confirm_password = getpass("Confirm Admin Password: ")

    if not name or not phone or not password:
        print("All fields are required!")
        return

    if password != confirm_password:
        print("Passwords do not match!")
        return

    if len(password) < 8:
        print("Password must contain at least 8 characters!")
        return

    connection = get_db_connection()

    if not connection:
        print("Database connection failed!")
        return

    cursor = connection.cursor()

    try:
        cursor.execute(
            "SELECT id FROM users WHERE phone = %s",
            (phone,)
        )

        if cursor.fetchone():
            print("This phone number is already registered!")
            return

        password_hash = generate_password_hash(password)

        cursor.execute(
            """
            INSERT INTO users
            (name, phone, password_hash, role, department, semester)
            VALUES (%s, %s, %s, 'admin', 'CSE', 5)
            """,
            (name, phone, password_hash)
        )

        connection.commit()

        print("\nSUCCESS! Admin account created.")
        print("You can now login using your phone and password.")

    except Exception as error:
        connection.rollback()
        print("Error:", error)

    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    create_admin()
