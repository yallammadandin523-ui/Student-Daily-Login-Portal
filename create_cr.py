
from getpass import getpass
from werkzeug.security import generate_password_hash
from database import get_db_connection


def create_cr():

    print("\n===== CREATE CR ACCOUNT =====")

    name = input("Enter CR Name: ").strip()
    phone = input("Enter CR Phone Number: ").strip()
    email = input("Enter CR Email: ").strip()

    password = getpass("Enter CR Password: ")
    confirm_password = getpass("Confirm CR Password: ")

    if not name or not phone or not password:
        print("ERROR: Name, phone and password are required.")
        return

    if password != confirm_password:
        print("ERROR: Passwords do not match.")
        return

    connection = get_db_connection()

    if not connection:
        print("Database connection failed!")
        return

    cursor = connection.cursor()

    try:
        cursor.execute("""
            INSERT INTO users
            (name, email, phone, password_hash, role,
             department, semester, is_active)
            VALUES (%s, %s, %s, %s, 'cr', 'CSE', 5, TRUE)
        """, (
            name,
            email or None,
            phone,
            generate_password_hash(password)
        ))

        connection.commit()

        print("\nSUCCESS! CR account created.")

    except Exception as e:
        connection.rollback()
        print("ERROR:", e)

    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    create_cr()
