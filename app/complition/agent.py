import json
import time
from dotenv import find_dotenv, load_dotenv
from openai import OpenAI

from openai.types.beta.threads.run import Run
import os

import docstring_parser
# from execute import execute_python_code


MODEL_NAME=os.getenv("MODEL",default="gpt-4o")



class Agent:

    def __init__(self, initial_instructions=None):
        self.client = OpenAI()  # api_key=OPENAI_API_KEY)
        self.messages = []
        self.functions_metadata = {}
        self.functions = {}
        self.tool_belt=None
        self.tool_choice=None

        # Initialize with system instructions if provided
        if not initial_instructions is None:
            print("put initial instruction")
            self.add_message( initial_instructions,"system")


    def add_message(self, content,role="user"):
        """Add a message to the conversation history.
        
        Args:
            content (str): The content of the message.
            role (str): The role of the message sender ('user', 'system', or 'assistant').
            
        """
        if role not in ["user", "system", "assistant"]:
            raise ValueError("Role must be 'user', 'system', or 'assistant'.")
        self.messages.append({"role": role, "content": content})


    def add_instruction(self, content):
        """Add an instruction to guide the model's behavior.
        
        Args:
            content (str): The instruction content.
        """
        self.add_message(content, role="system")


        
    def add_tools(self,tools: dict[str, callable],tool_choice=None)  :
        self.tool_belt = tools
        self.tool_choice=tool_choice
    
    def _call_tools(self,  tool_calls: list[dict]):
        for tool_call in tool_calls:
            print(tool_call)
            function = tool_call.function
            # we extract the arguments from the function. They are in JSON so we need to load them with the json module.
            function_args = json.loads(function.arguments)
            
            # we map the function name to our Agent's tool belt
            function_to_call = self.tool_belt[function.name]
            # we call the found function with the provided arguments
            function_response = function_to_call(**function_args)
            
            self.messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "function",
                    "name": function.name,
                    "content": function_response,
            })
            
            
        
         
    def run_agent(self):
        """Generate a response from the agent using the OpenAI API.
        
        Returns:
            str: The content of the generated response.
        """
        if not self.tool_belt is None:
            tools=self._get_tools_in_open_ai_format()
            print("tools",tools)
            response = self.client.chat.completions.create(
                model=MODEL_NAME,
                messages=self.messages,
                tools=tools,
                tool_choice="auto"
                # tool_choice=self.tool_choice if self.tool_choice else None 
            )
            
            # print("run assistant")
            replay = response.choices[0].message.content
            print( response.choices[0].message)
            print(r"function_call" in response.choices[0].message)
            self._call_tools(response.choices[0].message.tool_calls)
            print("finished call tools")           
               
        
        response = self.client.chat.completions.create(
            model=MODEL_NAME,
            messages=self.messages,
            tools=tools if self.tool_belt else None,
            tool_choice="none" if self.tool_belt else None
            
        )
        
        
        replay = response.choices[0].message.content
        self.add_message(replay,role="assistant")
        
        return replay



    
    def _get_tools_in_open_ai_format(self):
        python_type_to_json_type = {
            "str": "string",
            "int": "number",
            "float": "number",
            "bool": "boolean",
            "list": "array",
            "dict": "object"
        }

        return [
            {
                "type": "function",
                "function": {
                    "name": tool.__name__,
                    "description": docstring_parser.parse(tool.__doc__).short_description,
                    "parameters": {
                        "type": "object",
                        "properties": {
                            p.arg_name: {
                                "type": python_type_to_json_type.get(p.type_name, "string"),
                                "description": p.description
                            }
                            for p in docstring_parser.parse(tool.__doc__).params

                        },
                        "required": [
                            p.arg_name
                            for p in docstring_parser.parse(tool.__doc__).params
                            if not p.is_optional
                        ]
                    }
                }
            }
            for tool in self.tool_belt.values()
        ]

   
        
       
    
    def get_last_message(self):
        """Get the last message in the conversation history.
        
        Returns:
            dict: The last message in the conversation history.
        """
        if self.messages:
            return self.messages[-1]
        return None    


    def run(self):
        """Execute the agent and return the generated response.
        
        Returns:
            str: The content of the generated response.
        """
        return self.run_agent()    



if __name__ == "__main__": 
    initial_instructions = [
        "You are a helpful assistant.",
        "Always be polite and provide detailed answers."
    ]

    agent = Agent( initial_instructions=initial_instructions)
    # content=["The weather in Washington is sunny with a temperature of 25°C"]
    content=[ " question : מי אני ? \n answer : הי, אני צ'אטבוט שנוצר לעזור למשתמשים עם שאלות ובעיות שקשורות לאפליקציית bit והתשובות שלי מוגבלות לנושאים אלו בלבד. אם לא הצלחתי לעזור תוכלו תמיד לפנות למוקד השירות למספר *6428. מוקד שירות הלקוחות של bit זמין בימים א' עד ה' בין השעות 9:00-17:00 ובימי ו' בין השעות 8:30-13:00.\n", " question : שלום לך בוט נחמד \n answer : הי, אני צ'אטבוט שנוצר לעזור למשתמשים עם שאלות ובעיות שקשורות לאפליקציית bit והתשובות שלי מוגבלות לנושאים אלו בלבד. אם לא הצלחתי לעזור תוכלו תמיד לפנות למוקד השירות למספר *6428. מוקד שירות הלקוחות של bit זמין בימים א' עד ה' בין השעות 9:00-17:00 ובימי ו' בין השעות 8:30-13:00.\n", " question : רציתי להתלונן על ביט. ניסיתי להעביר כסף ולא הצלחתי! \n answer : הי, אני צ'אטבוט שנוצר לעזור למשתמשים עם שאלות ובעיות שקשורות לאפליקציית bit והתשובות שלי מוגבלות לנושאים אלו בלבד. אם לא הצלחתי לעזור תוכלו תמיד לפנות למוקד השירות למספר *6428. מוקד שירות הלקוחות של bit זמין בימים א' עד ה' בין השעות 9:00-17:00 ובימי ו' בין השעות 8:30-13:00.\n"]
    agent.add_message(content=' '.join(content),role="system")
    
    
    agent.add_message("Hello, how are you?")
    # agent.add_message("Can you tell me the weather in New York?")
    agent.add_message("Can you tell me the weather in Washington?")

    
    # from tools import get_weather
    
    # tools={        
    #     get_weather.__name__:get_weather ,
    #     }

    # agent.add_tools(tools=tools)
    # Running the agent to generate a response
    reply = agent.run()
    print("Agent's reply:", reply)

    # Retrieving and printing the last message in the conversation history
    last_message = agent.get_last_message()
    print("Last message:", last_message)