# models/storage_handler.py
from google.cloud import storage
from config import GCS_CONFIG

class StorageHandler:
    def __init__(self):
        """
        Initialize the Google Cloud Storage handler.
        """
        self.bucket_name = GCS_CONFIG["bucket_name"]
        self.client = storage.Client.from_service_account_json(GCS_CONFIG["credentials_path"])

    def upload_file(self, file_path: str, destination_name: str) -> str:
        """
        Upload a file to Google Cloud Storage.
        :param file_path: Path to the local file.
        :param destination_name: Name of the file in GCS.
        :return: Public URL of the uploaded file.
        """
        try:
            bucket = self.client.bucket(self.bucket_name)
            blob = bucket.blob(destination_name)
            blob.upload_from_filename(file_path)
            return blob.public_url
        except Exception as e:
            raise Exception(f"GCS Upload Error: {str(e)}")

    def download_file(self, source_name: str, destination_path: str) -> str:
        """
        Download a file from Google Cloud Storage.
        :param source_name: Name of the file in GCS.
        :param destination_path: Path to save the downloaded file.
        :return: Path to the downloaded file.
        """
        try:
            bucket = self.client.bucket(self.bucket_name)
            blob = bucket.blob(source_name)
            blob.download_to_filename(destination_path)
            return destination_path
        except Exception as e:
            raise Exception(f"GCS Download Error: {str(e)}")