# schemas/request_models.py
from pydantic import BaseModel
from typing import List, Optional, Literal

class QueryRequest(BaseModel):
    """
    Request model for the /query endpoint.
    """
    query: str  # The user's query
    model_name: Literal["deepseek", "gemini"]  # Selected model
    storage_type: Literal["mysql", "bigquery", "gcs"]  # Selected storage
    user_id: str  # User ID for history tracking
    max_history: Optional[int] = 20  # Maximum history entries to retrieve
    gcs_file_names: Optional[List[str]] = None  # List of file names in GCS for external context

class ExternalSourceRequest(BaseModel):
    """
    Request model for the /external-source endpoint.
    """
    source_type: Literal["google_search", "pdf", "excel", "docs"]  # Type of external source
    source_name: str  # Query for Google Search or file name for GCS