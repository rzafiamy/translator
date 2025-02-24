import html

class CSVParser:
    """Class to manually parse a tab-separated CSV file and decode lyrics."""

    def __init__(self, file_path):
        self.file_path = file_path

    def load_csv(self):
        """Manually read the CSV file and return a list of parsed rows."""
        parsed_data = []

        with open(self.file_path, "r", encoding="utf-8") as file:
            for line_num, line in enumerate(file, start=1):
                line = line.strip()  # Remove leading/trailing whitespace

                # Skip empty lines
                if not line:
                    continue  

                # Ensure exactly 2 columns (sequence & lyrics)
                parts = line.split("\t")
                if len(parts) != 2:
                    print(f"⚠️ Warning: Skipping malformed line {line_num}: {line}")
                    continue  # Skip problematic lines

                sequence, lyrics = parts
                parsed_data.append((sequence.strip(), lyrics.strip()))

        return parsed_data

    def parse_and_clean(self, raw_data):
        """Parse song number & strophe, decode HTML entities, and return structured data."""
        structured_data = []

        for line_num, (sequence, lyrics) in enumerate(raw_data, start=1):
            try:
                # Extract song number & strophe
                sequence = sequence.strip('"')  # Remove surrounding quotes
                song_num, strophe = sequence.split(" ")

                # Decode HTML entities in lyrics
                lyrics = html.unescape(lyrics)

                structured_data.append((song_num, strophe, lyrics))

            except ValueError:
                print(f"⚠️ Warning: Skipping malformed sequence in line {line_num}: {sequence}")
                continue  # Skip lines with incorrect format

        return structured_data
