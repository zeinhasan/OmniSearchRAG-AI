# models/external_source_handler.py
import requests
from google.cloud import storage
from config import GOOGLE_SEARCH_CONFIG, GCS_CONFIG
import PyPDF2
from io import BytesIO
from models.faiss_handler import FaissHandler

class ExternalSourceHandler:
    def __init__(self):
        # Google Search API Configuration
        self.google_api_key = GOOGLE_SEARCH_CONFIG['api_key']
        self.google_cse_id = GOOGLE_SEARCH_CONFIG['cse_id']

        # Google Cloud Storage Configuration
        self.gcs_client = storage.Client.from_service_account_json(GCS_CONFIG['credentials_path'])
        self.bucket_name = GCS_CONFIG['bucket_name']

        # FAISS Handler
        self.faiss_handler = FaissHandler()

    def search_google(self, query: str) -> str:
        """
        Search Google using the Custom Search JSON API and return a summary of the results.
        """
        url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={self.google_api_key}&cx={self.google_cse_id}"
        response = requests.get(url)
        if response.status_code == 200:
            results = response.json()
            summary = "Google Search Results:\n"
            for item in results.get("items", []):
                summary += f"- {item['title']}: {item['snippet']}\n"
            return summary
        else:
            raise Exception(f"Google Search API Error: {response.status_code} - {response.text}")

    def read_pdf_from_gcs(self, file_name: str) -> str:
        """
        Read a PDF file from Google Cloud Storage and extract text.
        """
        bucket = self.gcs_client.bucket(self.bucket_name)
        blob = bucket.blob(file_name)
        pdf_file = BytesIO(blob.download_as_bytes())

        reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text

    def get_optimal_documents(self, query: str, file_names: list) -> list:
        """
        Retrieve the most relevant documents from GCS using FAISS.
        """
        documents = [self.read_pdf_from_gcs(file_name) for file_name in file_names]
        self.faiss_handler.add_documents(documents)
        relevant_indices = self.faiss_handler.search(query)
        return [documents[i] for i in relevant_indices]

    def get_external_context(self, query: str, file_names: list) -> str:
        """
        Fetch and process external data to be used as context for the AI.
        """
        relevant_docs = self.get_optimal_documents(query, file_names)
        google_results = self.search_google(query)
        return "Relevant Documents:\n" + "\n".join(relevant_docs) + "\n\nGoogle Search Results:\n" + google_results