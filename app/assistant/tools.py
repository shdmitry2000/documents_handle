
from datetime import datetime
import json
from typing import List
breakfast_count=1

def eat_next_meal(breakfast_count: int):
    """
    Call this tool when user wants you to eat another meal.

    Args:
        breakfast_count (int): Value with same name from metadata.

    Returns:
        str: The meal you should eat next.
    """
    print("== eat_next_meal ==> tool called")
    if breakfast_count == 2:
        return "You have already eaten breakfast twice today. You eat lunch now."
    if breakfast_count == 1:
        breakfast_count += 1
        return "You have only eaten one breakfast today. You eat second breakfast now."


def tell_the_date():
    """
    Call this tool when the user wants to know the date.

    Returns:
        str: The current date
    """
    print("== tell_the_date ==> tool called")
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"The date is {current_date}"


def test_tool() -> List[str]:
    """
    Call this tool when the user wants to run the test.

    Returns:
        List[str]: A list containing stringsT . need to return 1-st sentence
    """
    print("== test_tool ==> tool called")

    return json.dumps(["sentence 1"])
    # return 