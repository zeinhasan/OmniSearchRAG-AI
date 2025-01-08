from datetime import datetime  # Import datetime for timestamp
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models.model_handler import ModelHandler
from models.database_handler import DatabaseHandler
from models.external_source_handler import ExternalSourceHandler
from models.storage_handler import StorageHandler
from models.faiss_handler import FaissHandler
from schemas.request_models import QueryRequest
from typing import Dict

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.post("/query")
async def query(request: QueryRequest):
    try:
        # Initialize handlers
        model = ModelHandler(request.model_name)
        db = DatabaseHandler(request.storage_type)
        storage = StorageHandler()
        source = ExternalSourceHandler()

        # Get user history from the database
        history = db.get_history(request.user_id, request.max_history)

        # Get external context if GCS files are specified
        external_context = ""
        if request.gcs_file_names:
            external_context = source.get_external_context(request.query, request.gcs_file_names)

        # Combine query and external context
        full_prompt = f"{request.query}\n\nContext:\n{external_context}" if external_context else request.query

        # Generate response using the model
        response = model.generate_response(full_prompt, history)

        # Insert the conversation into the database
        db.insert_history(request.user_id, request.query, response["answer"])

        # Prepare the response with additional fields
        response_data = {
            "user_id": request.user_id,  # Include the user_id in the response
            "response_status": "success",  # Indicate the status of the response   
            "timestamp": datetime.now().isoformat(),  # Add current timestamp
            "response": response,
        }

        return response_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/check-handlers")
async def check_handlers() -> Dict[str, str]:
    """
    Endpoint to check the functionality of all handlers.
    """
    results = {}

    try:
        # Check DatabaseHandler (MySQL)
        db_mysql = DatabaseHandler("mysql")
        db_mysql.get_history(user_id="ADMIN", limit=1)
        results["database_mysql"] = "OK"
    except Exception as e:
        results["database_mysql"] = f"Error: {str(e)}"

    try:
        # Check DatabaseHandler (BigQuery)
        db_bigquery = DatabaseHandler("bigquery")
        db_bigquery.get_history(user_id="ADMIN", limit=1)
        results["database_bigquery"] = "OK"
    except Exception as e:
        results["database_bigquery"] = f"Error: {str(e)}"

    try:
        # Check ModelHandler (Gemini)
        model_gemini = ModelHandler("gemini")
        response = model_gemini.generate_response("Test query", [])
        results["model_gemini"] = f"OK - Response: {response['answer']}"
    except Exception as e:
        results["model_gemini"] = f"Error: {str(e)}"

    try:
        # Check ExternalSourceHandler
        source = ExternalSourceHandler()
        source.search_google("Test query")
        results["external_source"] = "OK"
    except Exception as e:
        results["external_source"] = f"Error: {str(e)}"

    try:
        # Check StorageHandler
        storage = StorageHandler()
        storage.upload_file("test.txt", "test.txt")
        results["storage"] = "OK"
    except Exception as e:
        results["storage"] = f"Error: {str(e)}"

    try:
        # Check FaissHandler
        faiss_handler = FaissHandler()
        faiss_handler.add_documents(["Test document"])
        faiss_handler.search("Test query")
        results["faiss"] = "OK"
    except Exception as e:
        results["faiss"] = f"Error: {str(e)}"

    return results

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5001)