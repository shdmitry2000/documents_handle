from transformers import LayoutLMv3ForTokenClassification, LayoutLMv3Tokenizer
from typing import Dict, List
import os

def extract_data(filename: str, fields_to_extract: List) -> Dict:
    """
    Extracts data from an invoice using LayoutLMv3.

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
    model = LayoutLMv3ForTokenClassification.from_pretrained("microsoft/layoutlmv3-base")
    tokenizer = LayoutLMv3Tokenizer.from_pretrained("microsoft/layoutlmv3-base")

    # 1. Load the invoice document (e.g., using Pillow, PyMuPDF)
    # 2. Preprocess the document (e.g., convert to grayscale, resize)
    # 3. Tokenize the document (using LayoutLMv3Tokenizer)
    # 4. Run LayoutLMv3 model (e.g., using `model.predict`)
    # 5. Extract field values based on predicted tokens and their positions
    # 6. Return a dictionary with extracted data

    extracted_data = {
        "invoice_number": "12345",  # Replace with actual extracted value
        "invoice_date": "2023-10-26",  # Replace with actual extracted value
        "amount": "100.00",  # Replace with actual extracted value
        # ... other fields
    }

     # Save result to json folder
    json_file_path = os.path.join(os.getenv("JSON_DIR"), f"{os.path.basename(file_url)}_layoutlmv3.json")
    
    with open(json_file_path, "w") as json_file:
        json.dump({"file_url": file_url, "data": extracted_data}, json_file)

    return json_file_path

