import pymongo
import os
from dotenv import load_dotenv

load_dotenv()

# Replace with your MongoDB connection string
MONGO_URI = os.getenv("DB_URL")

# Create MongoDB client
client = pymongo.MongoClient(MONGO_URI)

# Select database
db = client["zkylhine"]
