import os
import time
from app.db import save_to_mongodb

def watch_folder():
    json_dir = os.getenv("JSON_DIR")
    processed_files = set()

    while True:
        for file_name in os.listdir(json_dir):
            if file_name not in processed_files:
                file_path = os.path.join(json_dir, file_name)
                module_name = file_name.split("_")[-1].split(".")[0]
                
                # Load the JSON data from the file
                with open(file_path) as json_file:
                    json_data = json_file.read()
                
                # Save JSON data to MongoDB
                save_to_mongodb(file_name=file_name, module_name=module_name, json_data=json_data, status="Pending")
                
                # Mark the file as processed
                processed_files.add(file_name)

        time.sleep(10)  # Check every 10 seconds
