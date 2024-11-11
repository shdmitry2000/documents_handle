import os
import mimetypes
from typing import Dict, List

def extract_data(filename: str, fields_to_extract: List) -> Dict:
    """
    Extracts data from an invoice based on file metadata.

    Args:
        filename: The name of the invoice file.
        fields_to_extract: A list of fields to extract.

    Returns:
        A dictionary containing the extracted data (based on metadata).
    """
    file_path = os.path.join(UPLOAD_DIRECTORY, filename)

    # 1. Get file metadata using `os.stat`, `mimetypes`, etc.
    file_size = os.stat(file_path).st_size
    mime_type = mimetypes.guess_type(file_path)[0]

    extracted_data = {
        "invoice_number": "12345",  # Replace with actual extracted value
        "invoice_date": "2023-10-26",  # Replace with actual extracted value
        "amount": "100.00",  # Replace with actual extracted value
        # ... other fields
    }

     # Save result to json folder
    json_file_path = os.path.join(os.getenv("JSON_DIR"), f"{os.path.basename(file_url)}_metadata.json")
    
    with open(json_file_path, "w") as json_file:
        json.dump({"file_url": file_url, "data": extracted_data}, json_file)

    return json_file_path

