
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")

    DB_HOST = os.getenv("DB_HOST")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_NAME = os.getenv(
        "DB_NAME",
        "student_daily_login_db"
    )

    DB_PORT = int(os.getenv("DB_PORT", "4000"))

    DB_SSL_CA = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "isrgrootx1.pem"
)

    UPLOAD_FOLDER = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "daily_screenshots"
    )

    MAX_CONTENT_LENGTH = 5 * 1024 * 1024
