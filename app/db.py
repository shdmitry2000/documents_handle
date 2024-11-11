import os
from pymongo import MongoClient
from datetime import datetime
import json

# Load MongoDB connection details from environment
MONGODB_URI = os.getenv("MONGODB_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")

# Connect to MongoDB
client = MongoClient(MONGODB_URI)
db = client[DATABASE_NAME]
collection = db['documents']

# Function to insert data into MongoDB
def save_to_mongodb(file_name, module_name, json_data, status):
    # Create a document to insert into MongoDB
    document = {
        "file_name": file_name,
        "module_name": module_name,
        "json_data": json.loads(json_data),  # Assuming JSON is passed as a string
        "auto_checked": False,
        "human_checked": False,
        "check_date": datetime.now(),
        "status": status
    }
    collection.insert_one(document)

# Function to retrieve failed documents (for fine-tuning)
def get_failed_documents():
    return collection.find({"status": "Failed"})


