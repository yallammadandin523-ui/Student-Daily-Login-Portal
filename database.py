
import mysql.connector
from mysql.connector import Error
from config import Config


def get_db_connection():
    try:
        if not Config.DB_HOST or not Config.DB_USER or not Config.DB_PASSWORD:
            raise ValueError("Database environment variables are missing.")

        if not Config.DB_SSL_CA:
            raise ValueError("TiDB SSL CA certificate path is missing.")

        connection = mysql.connector.connect(
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME,
            ssl_ca=Config.DB_SSL_CA,
            ssl_verify_cert=True,
            ssl_verify_identity=True,
            connection_timeout=15
        )

        if connection.is_connected():
            return connection

        return None

    except (Error, ValueError) as e:
        print("Database Connection Error:", e)
        return None


if __name__ == "__main__":
    connection = get_db_connection()

    if connection:
        print("SUCCESS: TiDB Cloud Database Connected!")
        connection.close()
    else:
        print("FAILED: Check TiDB credentials and SSL certificate.")
