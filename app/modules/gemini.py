from langchain.llms import Gemini
from typing import Dict, List
import os


# def extract_data_gemini(filename: str, fields_to_extract: List, file_url: str) -> Dict:

def extract_data(file_url: str, prompt: str,file_id :str ) -> Dict:
    """
    Extracts data from an invoice using Gemini (LLM).

    Args:
        file_url: The URL of the invoice file.
        prompt:   The prompt is exist.
        file_id:  The id of the file
        

    Returns:
        A dictionary containing the extracted data:
            {
                "invoice_number": "12345",
                "invoice_date": "2023-10-26",
                "amount": "100.00",
                # ... other fields
            }
    """
    
    # file_path = os.path.join(UPLOAD_DIRECTORY, filename)
    llm = Gemini(model_name=GEMINI_MODEL, temperature=0.7)  # Use environment variable
    
    prompt=get_default_prompt(file_url,prompt)
    # Use Gemini's `generate` method to process the prompt and get the results
    response = llm(prompt)  # Call the LLM with the prompt

    # Parse the response to extract the desired field values.
    extracted_data = {
        "invoice_number": "12345",  # Replace with actual extracted value
        "invoice_date": "2023-10-26",  # Replace with actual extracted value
        "amount": "100.00",  # Replace with actual extracted value
        # ... other fields
    }

    json_file_path = os.path.join(os.getenv("JSON_DIR"), f"{os.path.basename(file_url)}_gemini.json")
    with open(json_file_path, "w") as json_file:
        json.dump({"file_url": file_url, "data": extracted_data}, json_file)
    return json_file_path



    

def get_default_prompt(file_path,prompt=None):
    if prompt is None:
        prompt = f"Extract all fields from the invoice document at {file_url} as json format"
   
    return prompt     
     
    # """ get all recipte data from this document as json format. 
    # it should include: tax, amount, supplier, and is refund or not """
