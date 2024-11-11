import os
import anyio
import pandas as pd
from agent import Agent
# from existingassistentagent import ExistedAssistentAgent
from asyncer import asyncify
# from agent import Agent

              
name=  "category checker"     
personal_assistent="""
you must help to categoize question according to examples,
use only existed in examples categoryes!
if 2 or more categories can be used show all with coma separated.
if in question asking about specific place or specific time or specific peuple or specific organization give category :specific_data.

"""
# if you shure about category give answer:not sure
examples=""



# Replace with the actual directory path
directory_path = "/Users/dmitryshlymovich/workspace/chatgpt/tests/llm_test_prj/data/"

def load_and_preprocess_data(directory_path):
  """Loads and preprocesses Excel files from a given directory.

  Args:
    directory_path: The path to the directory containing Excel files.

  Returns:
    A list of preprocessed DataFrames, one for each Excel file.
  """

  dataframes = []
  for file in os.listdir(directory_path):
    if file.endswith('.xlsx'):
      file_path = os.path.join(directory_path, file)
      df = pd.read_excel(file_path)
      # Print all column names
      print("df.column",df.columns)
      
      for col in df.columns:
        if "קטגוריות" in col or  "category" in col:
            df['category'] = df[col].astype(str).str.split(',')
        if "שאלות" in col  or  "question" in col:
            df['question'] = df[col]

      dataframes.append(df)
  return dataframes

# 
# training_file = "/Users/dmitryshlymovich/workspace/chatgpt/tests/llm_test_prj/data/ex1.xlsx"
# def load_and_preprocess_data(file_path):
#     df = pd.read_excel(file_path)
#     df['question'] = df['שאלות']
#     df['category'] = df['קטגוריות'].apply(lambda x: x.split(','))
#     return df
# 
# training_data = load_and_preprocess_data(training_file)
training_data = load_and_preprocess_data(directory_path) 
              
agent = Agent(session=name,
             instructions= f"""
                Your name is: {name}
                Your task is: {personal_assistent}
                examples:{training_data}
            """ 
            )
            # ,
            #   tools={
            #       eat_next_meal.__name__: eat_next_meal,
            #       tell_the_date.__name__: tell_the_date ,
            #       test_tool.__name__:test_tool ,
            #   }
            #   )


# assistentAgent = Agent(assistant_id= "asst_m8VRfdOHwdBICrHslQEU9BvB" )



async def runAgentTools():
    await  asyncify(agent.create_thread)()

    while True:
        user_input = input("User: ")
        if user_input.lower() == 'exit':
            print("Exiting the agent...")
            break
        await  asyncify(agent.add_message)(user_input)
        answer = await asyncify( agent.run_agent)()
        print(f"Assistant: {answer}")


async def runAssistentAgent():
    # Main execution
    
    await  asyncify(agent.create_thread)()
    
    while True:
        user_input = input("User: ")
        if user_input.lower() == 'exit':
            print("Exiting the agent...")
            break
        await  asyncify(agent.add_message)(user_input)
        answer = await asyncify( agent.run_agent)()
        print(f"Assistant: {answer}")
        # sources=agent.get_last_message_source()
        # print(f"Assistant: {answer} sources: {sources}")


anyio.run(runAssistentAgent)