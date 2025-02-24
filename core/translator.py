import requests
import time
import os
from collections import defaultdict
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

        payload = {
            "model": MODEL_NAME,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": USER_PROMPT_TEMPLATE.format(text=text)}
            ],
            "temperature": 0.7
        }

        try:
            response = requests.post(self.api_url, json=payload, headers=headers)
            if response.status_code == 200:
                return response.json().get("choices", [{}])[0].get("message", {}).get("content", text)
            print(f"⚠️ Warning: API request failed with status {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"❌ Error: API request failed - {e}")

        return text  # Return original text on failure

    def translate_lyrics(self, structured_data, output_file):
        """Translates full songs instead of strophes using an LLM API and saves progress every 10 songs."""
        translated_data = []
        checkpoint_interval = 1  # Save progress every 10 songs

        # Group lyrics by song_num
        songs = defaultdict(list)
        for song_num, strophe, lyrics in structured_data:
            songs[song_num].append((strophe, lyrics))

        # Check for existing translations to avoid reprocessing
        existing_translations = self._load_existing_translations(output_file)

        with open(output_file, "a", encoding="utf-8") as f:  # Append mode
            for index, (song_num, strophes) in enumerate(songs.items()):
                if str(song_num) in existing_translations:
                    print(f"⏭️ Skipping already translated song {song_num}")
                    translated_lyrics = existing_translations[str(song_num)]
                else:
                    # Combine all strophes for the current song
                    full_lyrics = "\n".join(lyrics for _, lyrics in strophes)
                    print(f"🎵 Translating song {song_num}...")

                    translated_lyrics = self._rate_limited_translation(full_lyrics)
                    translated_data.append((song_num, translated_lyrics))

                    # Save progress every `checkpoint_interval` songs
                    if (index + 1) % checkpoint_interval == 0:
                        self._save_partial_translations(translated_data, f)
                        translated_data = []  # Clear memory after saving

            # Save any remaining translations at the end
            if translated_data:
                self._save_partial_translations(translated_data, f)

        print(f"✅ Translation completed! Progress saved in {output_file}")

    def _rate_limited_translation(self, text):
        """Helper function to add delay between API calls."""
        translated_text = self.translate_text(text)
        time.sleep(SLEEP_TIME)
        return translated_text

    def _save_partial_translations(self, translated_data, file_handle):
        """Save translations to file incrementally to prevent data loss."""
        for song_num, lyrics in translated_data:
            file_handle.write(f'"{song_num}"\t{lyrics}\n')
        file_handle.flush()  # Force write to disk
        print(f"💾 Progress saved - {len(translated_data)} songs written.")

    def _load_existing_translations(self, output_file):
        """Load previously translated songs from output file to prevent re-translation."""
        existing = {}
        if os.path.exists(output_file):
            with open(output_file, "r", encoding="utf-8") as f:
                for line in f:
                    parts = line.strip().split("\t")
                    if len(parts) == 2:
                        song_num, lyrics = parts
                        existing[song_num.strip('"')] = lyrics
        return existing
