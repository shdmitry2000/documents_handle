from fastapi import FastAPI, UploadFile, File
import os
from app.workers import process_file

app = FastAPI()

# Load .env variables
from app.config import load_env
load_env()

DOCUMENTS_DIR = os.getenv("DOCUMENTS_DIR")

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...),prompt=None):
    file_path = os.path.join(DOCUMENTS_DIR, file.filename)
    
    # Save the uploaded file to the documents directory
    with open(file_path, "wb") as f:
        f.write(await file.read())

    prompt_file_name=file.filename + ".prompt"
    prompt_file_path = os.path.join(DOCUMENTS_DIR, prompt_file_name)

    file_id=file.filename.split(".")[0] + datetime.now().strftime("%Y%m%d%H%M%S")

    if not prompt is None : 
        with open(prompt_path, "wb") as f:
        f.write(prompt)
        
    # Start the parallel document processing
    process_file(file_path,prompt,file_id)

    return {"status": "File uploaded and processing started", "filename": file.filename , "promptfile": prompt_file_name , "file_id" : file_id }




@app.post("/llm-check/{filename}")
async def llm_file_check(
    filename: str,
    fields_to_extract: List[str] = Form(...),  # Use Form for POST data
    file_url: str = Form(...),
):

    """
    Processes a document using only the LLM-based file check graph.
    """
    try:
        llm = Gemini(model_name=GEMINI_MODEL, temperature=0.7)  # Use environment variable
        results = process_gemini(filename, fields_to_extract) 

        save_results(results, filename, "llm")
        save_to_db(filename, "llm", results, "pending") 

        return JSONResponse(
            {"message": "Document processed successfully", "results": results}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during processing: {str(e)}")



@app.post("/fine-tune")
async def run_fine_tuning():
    """Runs the fine-tuning process."""
    fine_tune_module()
    return JSONResponse({"message": "Fine-tuning process initiated."})

    