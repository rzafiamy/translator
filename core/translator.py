import requests
import time
from config import LLM_API_URL, API_KEY, SLEEP_TIME, SYSTEM_PROMPT, USER_PROMPT_TEMPLATE, MODEL_NAME

class Translator:
    """Class to handle translation via a generic LLM API."""

    def __init__(self):
        self.api_url = LLM_API_URL
        self.api_key = API_KEY

    def translate_text(self, text):
        """Send text to an LLM API and return the translated response."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        # Prepare the chat-based request for any OpenAI-compatible LLM API
        payload = {
            "model": MODEL_NAME,  # Model name is configurable
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": USER_PROMPT_TEMPLATE.format(text=text)}
            ],
            "temperature": 0.7  # Adjust for creativity level
        }

        try:
            response = requests.post(self.api_url, json=payload, headers=headers)
            if response.status_code == 200:
                return response.json().get("choices", [{}])[0].get("message", {}).get("content", text)  
            print(f"⚠️ Warning: API request failed with status {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"❌ Error: API request failed - {e}")

        return text  # Return original text on failure

    def translate_lyrics(self, structured_data):
        """Translates lyrics using an LLM API with rate limiting."""
        translated_data = []

        for song_num, strophe, lyrics in structured_data:
            print(f"Translating song {song_num}, strophe {strophe}...")
            translated_lyrics = self._rate_limited_translation(lyrics)
            translated_data.append((song_num, strophe, translated_lyrics))

        return translated_data

    def _rate_limited_translation(self, text):
        """Helper function to add delay between API calls."""
        translated_text = self.translate_text(text)
        time.sleep(SLEEP_TIME)  # Prevent hitting API rate limits
        return translated_text
