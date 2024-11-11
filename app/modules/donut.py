from transformers import DonutModel, DonutProcessor
from typing import Dict, List
import os

def extract_data_donut(filename: str, fields_to_extract: List) -> Dict:
    """
    Extracts data from an invoice using Donut.

    Args:
        filename: The name of the invoice file.
        fields_to_extract: A list of fields to extract (e.g., "invoice_number", "invoice_date").

    Returns:
        A dictionary containing the extracted data:
            {
                "invoice_number": "12345",
                "invoice_date": "2023-10-26",
                "amount": "100.00",
                # ... other fields
            }
    """
    file_path = os.path.join(UPLOAD_DIRECTORY, filename)
    model = DonutModel.from_pretrained("google/donut-base-cased")
    processor = DonutProcessor.from_pretrained("google/donut-base-cased")

    # 1. Load the invoice document 
    # 2. Use Donut's `generate` method for OCR and token classification
    # 3. Extract field values based on predicted tokens and their positions
    # 4. Return a dictionary with extracted data

    extracted_data = {
        "invoice_number": "12345",  # Replace with actual extracted value
        "invoice_date": "2023-10-26",  # Replace with actual extracted value
        "amount": "100.00",  # Replace with actual extracted value
        # ... other fields
    }

    json_file_path = os.path.join(os.getenv("JSON_DIR"), f"{os.path.basename(file_url)}_donut.json")
    with open(json_file_path, "w") as json_file:
        json.dump({"file_url": file_url, "data": extracted_data}, json_file)
    return json_file_path