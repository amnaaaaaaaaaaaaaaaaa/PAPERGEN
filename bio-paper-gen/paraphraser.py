import requests
import streamlit as st
from typing import List

# IMPORTANT: Ensure you have your Hugging Face API key in .streamlit/secrets.toml
# e.g., HUGGINGFACE_API_KEY = "hf_xxxxxxxxxxxxxxxxxxx"
try:
    API_TOKEN = st.secrets["HUGGINGFACE_API_KEY"] 
    HEADERS = {"Authorization": f"Bearer {API_TOKEN}"} 
    API_URL = "https://api-inference.huggingface.co/models/Vamsi/T5_Paraphrase_Paws" 
except KeyError:
    st.error("Please set your HUGGINGFACE_API_KEY in .streamlit/secrets.toml")
    API_TOKEN = "" # Use an empty string to prevent immediate crash if not set

class ParaphraseConfig:
    def __init__(self, enabled: bool, model_name: str, max_length=256, num_return_sequences=1):
        self.enabled = enabled
        self.model_name = model_name
        self.max_length = max_length
        self.num_return_sequences = num_return_sequences

class Paraphraser:
    """Uses the Hugging Face Inference API for paraphrasing."""
    def __init__(self, config: ParaphraseConfig):
        self.config = config

    def _query_api(self, payload):
        """Sends a request to the Hugging Face Inference API."""
        if not API_TOKEN:
             return [{"error": "API token not set in secrets."}]

        response = requests.post(API_URL, headers=HEADERS, json=payload)
        return response.json()

    def paraphrase(self, text: str) -> str:
        if not self.config.enabled:
            return text

        # Build the payload for the API call
        payload = {
            "inputs": text,
            "options": {"wait_for_model": True},
            "parameters": {
                "max_length": self.config.max_length,
                "num_return_sequences": self.config.num_return_sequences,
                "temperature": 1.5,
            }
        }
        
        try:
            output = self._query_api(payload)
            
            # Handle API errors
            if isinstance(output, dict) and "error" in output:
                st.warning(f"Paraphrasing API Error: {output.get('error', 'Unknown Error')}")
                return text
            
            # Extract generated text
            if isinstance(output, list) and output:
                return output[0].get('generated_text', text).strip()
            
        except Exception as e:
            # Handle connection or other exceptions
            st.warning(f"Paraphrasing failed due to connection error: {e}")
            return text 

        return text
