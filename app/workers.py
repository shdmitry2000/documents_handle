from concurrent.futures import ThreadPoolExecutor
from app.modules import layoutlmv3, donut, gemini, metadata

def process_file(file_path,prompt,file_id):

    # check who is need to extract data - gemini by default
    # check if prompt exist ()
    # gemini.extract_data_gemirecived from client , 
    # if not get default prompt according to file type
    
    detectedProccessor=getProccessor(file_path)

    detectedProccessor.extract_data(file_path: str, prompt: str,file_id :str ) -> Dict:
    
def getProccessor(file_path):
    return gemini
