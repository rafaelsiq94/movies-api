import os
from dotenv import load_dotenv

load_dotenv()

CSV_FILE = os.getenv("CSV_FILE")
DB_URI = os.getenv("DB_URI")
DEVELOPMENT = os.getenv("DEVELOPMENT")
