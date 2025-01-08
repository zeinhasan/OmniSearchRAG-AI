# OmniSearchRAG-AI
OmniSearchRAG AI: Unified Knowledge Retrieval with Multi-Model Integration (GEMINI, Deepseek), FAISS Vector Database, and Open Web Search

# OmniSearchRAG-AI

**Unified Knowledge Retrieval with Multi-Model Integration**

OmniSearchRAG-AI is a powerful project designed to provide seamless knowledge retrieval across multiple data sources, including structured databases, unstructured documents, and open web content. By integrating state-of-the-art language models (GEMINI and Deepseek), a FAISS vector database, and Google Custom Search, this project offers a robust solution for intelligent search and data analysis.

---

## Features

- **Multi-Source Data Integration**:
  - **Structured Data**: MySQL, BigQuery.
  - **Unstructured Data**: PDF, Excel, TXT files.
  - **Open Web Search**: Google Custom Search API.

- **Advanced Language Models**:
  - **GEMINI**: For natural language understanding and generation.
  - **Deepseek**: For context-aware search and retrieval.

- **Vector Database**:
  - **FAISS**: Efficient similarity search and clustering of dense vectors.

- **Scalable Storage**:
  - External storage support for large datasets (PDF, Excel, TXT).

- **FastAPI Endpoints**:
  - RESTful API for querying structured data, unstructured documents, and web content.
  - Automatic Swagger UI documentation at `/docs`.

---

## Architecture Overview

1. **Data Ingestion**:
   - Structured data is ingested from MySQL and BigQuery.
   - Unstructured data (PDF, Excel, TXT) is processed and stored in external storage.
   - Open web data is fetched using Google Custom Search API.

2. **Data Processing**:
   - Text data is vectorized using pre-trained models.
   - FAISS is used for efficient indexing and retrieval of vectors.

3. **Query Handling**:
   - User queries are processed by GEMINI or Deepseek models.
   - FAISS retrieves the most relevant documents or data points.
   - Results are ranked and presented to the user.

4. **API Endpoints**:
   - FastAPI handles user queries and returns results in JSON format.
   - Swagger UI provides interactive API documentation.
---

## Installation

### Prerequisites

- Python 3.8+ (Tested on Python 3.11)
- MySQL Database
- Google Cloud BigQuery
- Google Custom Search API Key
- FAISS Library
- External Storage (for PDF, Excel, TXT files)

### Step-by-Step Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/zeinhasan/OmniSearchRAG-AI
   cd OmniSearch-AI
2. Set Up a Virtual Environment (Optional but Recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
3. Install Dependencies:
    ```bash
    pip install -r requirements.txt
4. Set Up Environment Variables:

    Create a .env file in the root directory and add the following:
    ```bash
    # .env
    # Model Configuration
    DEEPSEEK_API_KEY=your_deepseek_api_key
    GEMINI_API_KEY=your_gemini_api_key
    
    # Database Configuration
    MYSQL_HOST=your_myqsl_host
    MYSQL_USER=your_myqsl_username
    MYSQL_PASSWORD=your_myqsl_password
    MYSQL_DATABASE=your_myqsl_database
    
    BIGQUERY_PROJECT_ID=your_bigquery_projectid
    BIGQUERY_DATASET_ID=your_dataset_id
    GOOGLE_APPLICATION_CREDENTIALS=path/to/your/service-account.json
    
    # Google Cloud Storage Configuration
    GCS_BUCKET_NAME=your_gcs_bucket_name

    # Google Search API Configuration
    GOOGLE_SEARCH_API_KEY=your_google_custom_search_api_key
    GOOGLE_CSE_ID=your_google_cse_id
5. Run the FastAPI Application
    ```bash 
    uvicorn main:app --reload
6. Access the API:
    - Interactive Swagger UI: http://127.0.0.1:8000/docs
    - Redoc UI: http://127.0.0.1:8000/redoc

## API Endpoints
Here’s the **API Endpoints Documentation** in **Markdown format** for your FastAPI application:

---

### Base URL
`http://127.0.0.1:5001`

---

### 1. **Query Endpoint**
This endpoint processes user queries, integrates external context (if provided), and generates a response using the specified model. It also logs the conversation history in the database.

- **Endpoint**: `POST /query`
- **Request Body**:
  ```json
  {
    "user_id": "string",  // Unique identifier for the user
    "query": "string",    // User's query
    "model_name": "string",  // Name of the model to use (e.g., "gemini", "deepseek")
    "storage_type": "string",  // Type of database to use (e.g., "mysql", "bigquery")
    "max_history": 10,  // Maximum number of historical interactions to retrieve
    "gcs_file_names": ["file1.txt", "file2.pdf"]  // Optional: List of GCS file names for external context
  }
  ```

- **Response**:
  ```json
  {
    "user_id": "string",  // User ID provided in the request
    "response_status": "success",  // Status of the response
    "timestamp": "2023-10-01T12:34:56.789Z",  // Timestamp of the response
    "response": "string"  // Generated response from the model
  }
  ```

- **Example Request**:
  ```bash
  curl -X POST "http://127.0.0.1:5001/query" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "12345",
    "query": "What is machine learning?",
    "model_name": "gemini",
    "storage_type": "mysql",
    "max_history": 5,
    "gcs_file_names": ["ml_guide.pdf"]
  }'
  ```

- **Example Response**:
  ```json
  {
    "user_id": "12345",
    "response_status": "success",
    "timestamp": "2023-10-01T12:34:56.789Z",
    "response": "Machine learning is a subset of artificial intelligence that focuses on building systems that can learn from data."
  }
  ```

---

## 2. **Check Handlers Endpoint**
This endpoint checks the functionality of all handlers (database, model, external source, storage, and FAISS) and returns their status.

- **Endpoint**: `GET /check-handlers`
- **Response**:
  ```json
  {
    "database_mysql": "OK",  // Status of MySQL database handler
    "database_bigquery": "OK",  // Status of BigQuery database handler
    "model_gemini": "OK - Response: Test response",  // Status of Gemini model handler
    "external_source": "OK",  // Status of external source handler (e.g., Google Custom Search)
    "storage": "OK",  // Status of storage handler
    "faiss": "OK"  // Status of FAISS handler
  }
  ```

- **Example Request**:
  ```bash
  curl -X GET "http://127.0.0.1:5001/check-handlers"
  ```

- **Example Response**:
  ```json
  {
    "database_mysql": "OK",
    "database_bigquery": "OK",
    "model_gemini": "OK - Response: Test response",
    "external_source": "OK",
    "storage": "OK",
    "faiss": "OK"
  }
  ```

---

## Error Responses

If an error occurs, the API will return an HTTP 500 status code with the following response:

- **Response**:
  ```json
  {
    "detail": "string"  // Error message describing the issue
  }
  ```

- **Example Error Response**:
  ```json
  {
    "detail": "Database connection failed: Connection refused."
  }
  ```

---

## CORS Configuration
The API is configured to allow cross-origin requests from all domains (`*`). This can be customized in the `CORSMiddleware` settings.

---


## Example Use Case

1. A user sends a query to the `/query` endpoint with their user ID, query, and optional GCS file names for context.
2. The API retrieves the user's conversation history from the database.
3. If GCS file names are provided, the API fetches external context from the specified files.
4. The query and context are passed to the specified model (e.g., Gemini) to generate a response.
5. The response is logged in the database and returned to the user.

---

## Repository Structure

```
OmniSearch-AI/
│
├── main.py                   # FastAPI application entry point
├── models/
│   ├── model_handler.py      # Handles model interactions (e.g., Gemini, Deepseek)
│   ├── database_handler.py   # Handles database interactions (MySQL, BigQuery)
│   ├── external_source_handler.py  # Handles external sources (e.g., Google Custom Search)
│   ├── storage_handler.py    # Handles file storage (e.g., GCS)
│   └── faiss_handler.py      # Handles FAISS vector database operations
├── schemas/
│   └── request_models.py     # Defines Pydantic models for request validation
├── .env                      # Environment variables (e.g., API keys, database credentials)
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation
```
