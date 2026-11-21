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


def create_tables():
    connection = get_db_connection()

    if not connection:
        print("Database connection failed!")
        return False

    cursor = connection.cursor()

    try:
        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(150) NOT NULL UNIQUE,
                phone VARCHAR(15) NOT NULL UNIQUE,
                password_hash VARCHAR(255) NOT NULL,
                role VARCHAR(20) NOT NULL DEFAULT 'student',
                usn VARCHAR(30) UNIQUE,
                semester INT DEFAULT 5,
                department VARCHAR(50) DEFAULT 'CSE',
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Screenshot submissions
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS submissions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                submission_date DATE NOT NULL,
                image_filename VARCHAR(255) NOT NULL,
                image_path VARCHAR(500) NOT NULL,
                image_hash VARCHAR(64) NOT NULL UNIQUE,
                uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE KEY unique_user_submission_day
                    (user_id, submission_date)
            )
        """)

        # Daily reports
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS daily_reports (
                id INT AUTO_INCREMENT PRIMARY KEY,
                report_date DATE NOT NULL UNIQUE,
                uploaded_count INT DEFAULT 0,
                not_uploaded_count INT DEFAULT 0,
                generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                excel_path VARCHAR(500),
                zip_path VARCHAR(500)
            )
        """)

        connection.commit()

        print("SUCCESS: Database tables created!")
        print("Tables: users, submissions, daily_reports")

        return True

    except Error as e:
        connection.rollback()
        print("Table Creation Error:", e)
        return False

    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    connection = get_db_connection()

    if connection:
        print("SUCCESS: TiDB Cloud Database Connected!")
        connection.close()

        create_tables()
    else:
        print("FAILED: Database connection failed!")