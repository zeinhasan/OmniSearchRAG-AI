import os
import google.generativeai as genai
from config import MODEL_CONFIG

class ModelHandler:
    def __init__(self, model_name: str):
        """
        Initialize the model handler based on the selected model.
        Supported models: 'deepseek', 'gemini'.
        """
        self.model_name = model_name
        self.config = MODEL_CONFIG.get(model_name)
        if not self.config:
            raise ValueError(f"Model '{model_name}' is not supported or misconfigured.")

        # Configure Gemini if selected
        if self.model_name == "gemini":
            genai.configure(api_key=self.config["api_key"])
            self.model = genai.GenerativeModel(
                model_name="gemini-2.0-flash-exp",
                generation_config={
                    "temperature": 1,
                    "top_p": 0.95,
                    "top_k": 40,
                    "max_output_tokens": 8192,
                },
            )
            # Initialize chat session with empty history
            self.chat_session = self.model.start_chat(history=[])

    def generate_response(self, prompt: str, history: list) -> dict:
        """
        Generate a response from the selected model.
        :param prompt: The user's query.
        :param history: Conversation history.
        :return: Model's response.
        """
        if self.model_name == "deepseek":
            headers = {
                "Authorization": f"Bearer {self.config['api_key']}",
                "Content-Type": "application/json"
            }
            data = {
                "prompt": prompt,
                "history": history
            }
            try:
                response = requests.post(self.config['endpoint'], headers=headers, data=json.dumps(data))
                response.raise_for_status()
                return response.json()
            except requests.exceptions.RequestException as e:
                raise Exception(f"DeepSeek API Error: {str(e)}")
        elif self.model_name == "gemini":
            try:
                # Send the user's prompt to the chat session
                response = self.chat_session.send_message(prompt)
                # Update the history with the new interaction
                self.chat_session.history.extend([
                    {"role": "user", "parts": [prompt]},
                    {"role": "model", "parts": [response.text]},
                ])
                return {"answer": response.text}
            except Exception as e:
                raise Exception(f"Gemini API Error: {str(e)}")
        else:
            raise ValueError(f"Unsupported model: {self.model_name}")