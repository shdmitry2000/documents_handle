import json
import time
from dotenv import find_dotenv, load_dotenv
import openai
from openai.types.beta.threads.run import Run
import os

import docstring_parser

load_dotenv(find_dotenv())

MODEL_NAME=os.getenv("MODEL",default="gpt-4o")
    
class Agent:
    def __init__(self, session: str, instructions: str,  tools=None):
        self.session = session
        self.instructions = instructions
        self.tool_belt = tools

        self.client = openai.OpenAI()#api_key=OPENAI_API_KEY)
        if not tools is None:
                
            self.assistant = self.client.beta.assistants.create(
                name=self.session,
                instructions=self.instructions ,
                model=MODEL_NAME 
            )
        else:
            self.assistant = self.client.beta.assistants.create(
                name=self.session,
                instructions=self.instructions ,
                tools=self.tool_belt,
                model=MODEL_NAME 
            )
        
        
        self.assistant_id=self.assistant.id

    def create_thread(self):
        self.thread = self.client.beta.threads.create()

    def add_message(self, message):
        self.client.beta.threads.messages.create(
            thread_id=self.thread.id,
            role="user",
            content=message
        )

    def get_last_message(self):
        value=self.client.beta.threads.messages.list(
            thread_id=self.thread.id
        ).data[0].content[0].text.value
        return value

    def get_last_message_source(self):
        content=self.client.beta.threads.messages.list(
            thread_id=self.thread.id
        ).data[0].content[0]
        return content

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

    def _create_run(self):
        if self.tool_belt is None:
            return self.client.beta.threads.runs.create(
                thread_id=self.thread.id,
                assistant_id=self.assistant_id,
                instructions=self.instructions
            )
        else:
            return self.client.beta.threads.runs.create(
                thread_id=self.thread.id,
                assistant_id=self.assistant_id,
                tools=self._get_tools_in_open_ai_format(),
                instructions=self.instructions
                
            )
        
    def _create_run_pool(self):
        if self.tool_belt is None:
            return self.client.beta.threads.runs.create_and_poll(
                thread_id=self.thread.id,
                assistant_id=self.assistant_id,
                instructions=self.instructions
            )
        else:
            return self.client.beta.threads.runs.create_and_poll(
                thread_id=self.thread.id,
                assistant_id=self.assistant_id,
                tools=self._get_tools_in_open_ai_format(),
                instructions=self.instructions
               
            )


    def _retrieve_run(self, run: Run):
        return self.client.beta.threads.runs.retrieve(
            run_id=run.id, thread_id=self.thread.id)

    def _cancel_run(self, run: Run):
        self.client.beta.threads.runs.cancel(
            run_id=run.id, thread_id=self.thread.id)

    def _call_tools(self, run_id: str, tool_calls: list[dict]):
        tool_outputs = []

        # we iterate over all the tool_calls to deal with them individually
        for tool_call in tool_calls:
            # we get the function object from the tool_call
            function = tool_call.function
            # we extract the arguments from the function. They are in JSON so we need to load them with the json module.
            function_args = json.loads(function.arguments)
            # we map the function name to our Agent's tool belt
            function_to_call = self.tool_belt[function.name]
            # we call the found function with the provided arguments
            function_response = function_to_call(**function_args)
            # we append the response to the tool_outputs list
            tool_outputs.append(
                {"tool_call_id": tool_call.id, "output": function_response})

        # we submit the tool outputs to OpenAI
        self.client.beta.threads.runs.submit_tool_outputs(
            thread_id=self.thread.id,
            run_id=run_id,
            tool_outputs=tool_outputs
        )

    def _poll_run(self, run: Run):
        status = run.status
        start_time = time.time()
        while status != "completed":
            if status == 'failed':
                raise Exception(f"Run failed with error: {run.last_error}")
            if status == 'expired':
                raise Exception("Run expired.")
            if status == 'requires_action':
                self._call_tools(
                    run.id, run.required_action.submit_tool_outputs.tool_calls)

            time.sleep(2)
            run = self._retrieve_run(run)
            status = run.status

            elapsed_time = time.time() - start_time
            if elapsed_time > 120:  # 2 minutes
                self._cancel_run(run)
                raise Exception("Run took longer than 2 minutes.")

    def _run(self, run: Run):
        status = run.status
        while status != "completed":
            if status == 'failed':
                raise Exception(f"Run failed with error: {run.last_error}")
            if status == 'expired':
                raise Exception("Run expired.")
            if status == 'requires_action':
                self._call_tools(
                    run.id, run.required_action.submit_tool_outputs.tool_calls)
            else:
                print("def _run(self, run: Run) : else")

    # def run_agent(self):
    #     run = self._create_run_pool()
    #     self._run(run)
    #     message = self.get_last_message()
    #     return message

    def run_agent(self):
        run = self._create_run()
        self._poll_run(run)
        message = self.get_last_message()
        return message
    

if __name__ == "__main__": 
    pass

    
    
  
    
