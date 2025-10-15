import pymongo
import os
from dotenv import load_dotenv

load_dotenv()
DB_URL = os.getenv("DB_URL")

# Replace with your MongoDB connection string
MONGO_URI = DB_URL

# Create MongoDB client
client = pymongo.MongoClient(MONGO_URI)

# Select database
db = client["zkylhine"]

# Optional: quick function to check connection at startup
async def test_connection():
    try:
        await client.server_info()  # Will raise if cannot connect
        print("[MongoDB] Connected successfully.")
    except Exception as e:
        print(f"[MongoDB] Connection failed: {e}")