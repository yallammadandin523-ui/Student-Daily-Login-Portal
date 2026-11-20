
import mysql.connector
from mysql.connector import Error
from config import Config


def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME
        )

        if connection.is_connected():
            return connection

    except Error as e:
        print("MySQL Connection Error:", e)

    return None


if __name__ == "__main__":
    connection = get_db_connection()

    if connection:
        print("SUCCESS: MySQL Database Connected!")
        connection.close()
    else:
        print("FAILED: Check MySQL server, password and database.")
