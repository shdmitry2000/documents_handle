import json
import time
from dotenv import find_dotenv, load_dotenv
import openai
from openai.types.beta.threads.run import Run
import os

MODEL_NAME=os.getenv("MODEL",default="gpt-4o")


class AssistentAgent:
    
    def __init__(self, instructions: str,name=None, tools=None,tool_resources=None):
        self.client = openai.OpenAI()#api_key=OPENAI_API_KEY)
        self.assistant = self.client.beta.assistants.create(
            name="test Assistant",
            instructions=instructions,
            model=MODEL_NAME,
            tools=tools,
            tool_resources=tool_resources,
            )
        
        
        
        self.assistant_id=self.assistant.id
        
        
            
        # if not tools is None :
        #     self.assistant = self.client.beta.assistants.update(
        #             assistant_id=self.assistant_id,
        #             instructions=instructions,
        #             tools=tools,
        #             )

    def useVectorStore(self,vectorstore_id):
        self.assistant = self.client.beta.assistants.update(
            assistant_id=self.assistant_id,
            tool_resources={"file_search": {"vector_store_ids": [vectorstore_id]}},
            )
        
       

    def create_thread(self):
        self.thread = self.client.beta.threads.create()
        self.thread_id=self.thread.id
        # self.thread_id="thread_4eWNJiBNrc8A6lDW5RONS5j9"

    def add_message(self, message):
        print('message',message,'thread',self.thread_id)
        self.client.beta.threads.messages.create(
            thread_id=self.thread_id,
            role="user",
            content=message
        )

    def get_last_message(self):
        return self.client.beta.threads.messages.list(
            thread_id=self.thread_id
        ).data[0].content[0].text.value



    
    def _create_run(self):
        return self.client.beta.threads.runs.create(
            thread_id=self.thread_id,
            assistant_id=self.assistant_id,
            # tools=self._get_tools_in_open_ai_format(),
            # instructions=self.instructions
            # instructions=f"""
            #     # Your name is: {self.name}
            #     Your personality is: {self.personality}

            #     Metadata related to this conversation:
            #     {{
            #         "breakfast_count": {count}
            #     }}
            # """,
        )
        
    def _create_run_pool(self):
        return   self.client.beta.threads.runs.create_and_poll(
            thread_id=self.thread_id, 
            assistant_id=self.assistant_id
                # tools=self._get_tools_in_open_ai_format(),
                # instructions=self.instructions
                # instructions=f"""
                #     # Your name is: {self.name}
                #     Your personality is: {self.personality}

                #     Metadata related to this conversation:
                #     {{
                #         "breakfast_count": {count}
                #     }}
                # """,
            )


    def _retrieve_run(self, run: Run):
        return self.client.beta.threads.runs.retrieve(
            run_id=run.id, thread_id=self.thread_id)

    def _cancel_run(self, run: Run):
        self.client.beta.threads.runs.cancel(
            run_id=run.id, thread_id=self.thread_id)

    
    
    def _run(self, run: Run):
        status = run.status
        while status != "completed":
            if status == 'failed':
                raise Exception(f"Run failed with error: {run.last_error}")
            if status == 'expired':
                raise Exception("Run expired.")
            # if status == 'requires_action':
            #     self._call_tools(
            #         run.id, run.required_action.submit_tool_outputs.tool_calls)
            else:
                print("def _run(self, run: Run) : else")

    

    def run_agent(self):
        
        
        # run = self.client.beta.threads.runs.create_and_poll(
        #     thread_id=self.thread_id, assistant_id=self.assistant_id
        # )

        

        


    
        
        # if run.status == 'completed': 
        #     messages = list(self.client.beta.threads.messages.list(thread_id=self.thread_id, run_id=run.id))
        #     print(messages) 
        # else: 
        #     print(run.status)

        # message_content = messages[0].content[0].text

        # print ("message_text",message_content.value)


        run = self._create_run_pool()
        self._run(run)
        message = self.get_last_message()
        return message

class ExistingAssistentAgent(AssistentAgent):
    
    def __init__(self, assistant_id,instructions=None):
        self.client = openai.OpenAI()#api_key=OPENAI_API_KEY)
        self.assistant_id=assistant_id
        if not instructions is None:
            self.assistant = self.client.beta.assistants.update(
                    assistant_id=self.assistant_id,
                    instructions=instructions,
                    model=MODEL_NAME,
                    )

if __name__ == "__main__": 
    question='מה הגבלות שימוש?'
    # question="תחזור על התשובה"
    
    
    
    assistant_id='asst_m8VRfdOHwdBICrHslQEU9BvB'
    # thread_id="thread_4eWNJiBNrc8A6lDW5RONS5j9"
    vector_store_id="vs_eckM54esesEAzQ87iKh4cNXr"
    
    # agent =AssistentAgent(
    #     instructions ="""
    #         אתה צאט בוט ידידותי ואנושי של אפליקצית ביט להעברת כספים, תענה בצורה הכי נחמדה ופשוטה על השאלות בהסתמך רק המידע שסופק
    #         """,
    #     name=None, 
    #     tools=[{"type": "file_search"}],
    #     tool_resources={"file_search": {"vector_store_ids": [vector_store_id]}},
    # )
    
    agent = ExistingAssistentAgent(assistant_id= assistant_id)
   
    
    agent.create_thread()
    
    agent.add_message(question)
    
    answer = agent.run_agent()
    
    
    print(answer)


    
    
  
    
