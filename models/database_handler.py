import mysql.connector
from google.cloud import bigquery
from config import DATABASE_CONFIG
import datetime


class DatabaseHandler:
    def __init__(self, db_type: str):
        """
        Initialize the database handler based on the database type.
        Supported types: 'mysql', 'bigquery'.
        """
        self.db_type = db_type
        self.config = DATABASE_CONFIG.get(db_type)
        if not self.config:
            raise ValueError(f"Database type '{db_type}' is not supported or misconfigured.")

    def get_history(self, user_id: str, limit: int = 20) -> list:
        """
        Retrieve conversation history for a user from the database.
        If the user does not exist, they will be implicitly added when inserting history.
        """
        return self._get_history(user_id, limit)

    def insert_history(self, user_id: str, query: str, response: str) -> None:
        """
        Insert a new conversation entry into the database.
        If the user does not exist, they will be implicitly added.
        """
        self._insert_history(user_id, query, response)

    def _get_history(self, user_id: str, limit: int) -> list:
        """
        Retrieve conversation history for a user from the database.
        """
        if self.db_type == "mysql":
            return self._get_history_mysql(user_id, limit)
        elif self.db_type == "bigquery":
            return self._get_history_bigquery(user_id, limit)
        else:
            raise ValueError(f"Unsupported database type: {self.db_type}")

    def _insert_history(self, user_id: str, query: str, response: str) -> None:
        """
        Insert a new conversation entry into the database.
        """
        if self.db_type == "mysql":
            self._insert_history_mysql(user_id, query, response)
        elif self.db_type == "bigquery":
            self._insert_history_bigquery(user_id, query, response)
        else:
            raise ValueError(f"Unsupported database type: {self.db_type}")

    def _get_history_mysql(self, user_id: str, limit: int) -> list:
        """
        Retrieve conversation history from MySQL.
        """
        try:
            connection = mysql.connector.connect(
                host=self.config["host"],
                user=self.config["user"],
                password=self.config["password"],
                database=self.config["database"]
            )
            cursor = connection.cursor(dictionary=True)

            # Query to fetch history
            query = """
                SELECT query, response, timestamp
                FROM conversation_history
                WHERE user_id = %s
                ORDER BY timestamp DESC
                LIMIT %s
            """
            cursor.execute(query, (user_id, limit))
            history = cursor.fetchall()

            # Close connection
            cursor.close()
            connection.close()

            return history
        except Exception as e:
            raise Exception(f"MySQL Error: {str(e)}")

    def _insert_history_mysql(self, user_id: str, query: str, response: str) -> None:
        """
        Insert a new conversation entry into MySQL.
        """
        try:
            connection = mysql.connector.connect(
                host=self.config["host"],
                user=self.config["user"],
                password=self.config["password"],
                database=self.config["database"]
            )
            cursor = connection.cursor()

            # Query to insert history
            insert_query = """
                INSERT INTO conversation_history (user_id, query, response, timestamp)
                VALUES (%s, %s, %s, %s)
            """
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute(insert_query, (user_id, query, response, timestamp))
            connection.commit()

            # Close connection
            cursor.close()
            connection.close()
        except Exception as e:
            raise Exception(f"MySQL Insert Error: {str(e)}")

    def _get_history_bigquery(self, user_id: str, limit: int) -> list:
        """
        Retrieve conversation history from BigQuery.
        """
        try:
            client = bigquery.Client.from_service_account_json(self.config["credentials_path"])

            # Query to fetch history
            query = f"""
                SELECT query, response, timestamp
                FROM `{self.config["project_id"]}.{self.config["dataset_id"]}.conversation_history`
                WHERE user_id = @user_id
                ORDER BY timestamp DESC
                LIMIT @limit
            """
            query_params = [
                bigquery.ScalarQueryParameter("user_id", "STRING", user_id),
                bigquery.ScalarQueryParameter("limit", "INT64", limit),
            ]
            job_config = bigquery.QueryJobConfig(query_parameters=query_params)
            query_job = client.query(query, job_config=job_config)
            history = [dict(row) for row in query_job]

            return history
        except Exception as e:
            raise Exception(f"BigQuery Error: {str(e)}")

    def _insert_history_bigquery(self, user_id: str, query: str, response: str) -> None:
        """
        Insert a new conversation entry into BigQuery.
        """
        try:
            client = bigquery.Client.from_service_account_json(self.config["credentials_path"])

            # Define the table reference
            table_ref = f"{self.config['project_id']}.{self.config['dataset_id']}.conversation_history"

            # Prepare the row to insert
            row = {
                "user_id": user_id,
                "query": query,
                "response": response,
                "timestamp": datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
            }

            # Insert the row
            errors = client.insert_rows_json(table_ref, [row])
            if errors:
                raise Exception(f"BigQuery Insert Errors: {errors}")
        except Exception as e:
            raise Exception(f"BigQuery Insert Error: {str(e)}")