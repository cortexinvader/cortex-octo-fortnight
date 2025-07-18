import os
import json
import google.generativeai as genai
from config import GEMINI_API_KEY
from core.instruction_builder import build_system_instruction


class GeminiAI:
    def __init__(self, model_name="gemini-1.5-flash"):
        self.api_key = GEMINI_API_KEY
        self.system_instruction = build_system_instruction()
        self.model_name = model_name
        self._configure_client()

    def _configure_client(self):
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(model_name=self.model_name)

    def send_message(self, user_message):
        # Compose prompt
        prompt = f"{self.system_instruction}\n\nUser: {user_message}\nAssistant:"

        # Send to Gemini
        try:
            response = self.model.generate_content(prompt)
            if hasattr(response, "text"):
                return response.text.strip()
            else:
                return "⚠️ No text response from Gemini."
        except Exception as e:
            return f"⚠️ Gemini Error: {str(e)}"
