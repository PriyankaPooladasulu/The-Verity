
import os
from pathlib import Path
from dotenv import load_dotenv
import mysql.connector

# Load the .env file from this project folder
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path, override=True)

try:
    connection = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

    if connection.is_connected():
        print("SUCCESS! Python connected to MySQL.")
        print("Database:", connection.database)

    connection.close()

except mysql.connector.Error as error:
    print("Connection failed:", error)
