
from datetime import datetime
import json
from typing import List

    
def get_weather( location:str):
    """
    Call this tool when the user wants to get weather information.

    Args:
        location (str): Value with same name from metadata.
        
    Returns:
        str: The current wether
    """
    print("== test_tool ==> tool called")

    return json.dumps(f"The weather in {location} is sunny with a temperature of 25°C.")

