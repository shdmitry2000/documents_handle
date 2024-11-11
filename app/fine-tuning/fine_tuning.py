from app.db import get_failed_documents

def fine_tuning():
    failed_docs = get_failed_documents()
    
    for doc in failed_docs:
        print(f"Failed record: {doc['file_name']} from {doc['module_name']}")

    return True