# config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Model Configuration
MODEL_CONFIG = {
    "deepseek": {
        "api_key": os.getenv("DEEPSEEK_API_KEY"),
        "endpoint": "https://api.deepseek.com/v1/chat/completions"
    },
    "gemini": {
        "api_key": os.getenv("GEMINI_API_KEY")
    }
}

# Database Configuration
DATABASE_CONFIG = {
    "mysql": {
        "host": os.getenv("MYSQL_HOST"),
        "user": os.getenv("MYSQL_USER"),
        "password": os.getenv("MYSQL_PASSWORD"),
        "database": os.getenv("MYSQL_DATABASE")
    },
    "bigquery": {
        "project_id": os.getenv("BIGQUERY_PROJECT_ID"),
        "dataset_id": os.getenv("BIGQUERY_DATASET_ID"),
        "credentials_path": os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    }
}

# Google Cloud Storage Configuration
GCS_CONFIG = {
    "bucket_name": os.getenv("GCS_BUCKET_NAME"),
    "credentials_path": os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
}

# Google Search API Configuration
GOOGLE_SEARCH_CONFIG = {
    "api_key": os.getenv("GOOGLE_SEARCH_API_KEY"),
    "cse_id": os.getenv("GOOGLE_CSE_ID")
}