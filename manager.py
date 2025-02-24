#manager.py

import argparse
from core.csv_parser import CSVParser
from core.translator import Translator
from config import INPUT_CSV_FILE, OUTPUT_CSV_FILE

def main(input_file, output_file):
    """Main function to parse, translate, and save CSV file manually."""
    print("📂 Loading CSV file...")
    parser = CSVParser(input_file)
    raw_data = parser.load_csv()
    structured_data = parser.parse_and_clean(raw_data)

    print("🌍 Translating lyrics (this may take some time)...")
    translator = Translator()
    translator.translate_lyrics(structured_data, output_file)  # Now passes output_file

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Translate a CSV file of song lyrics using an LLM API.")
    parser.add_argument("--input", type=str, default=INPUT_CSV_FILE, help="Path to input CSV file.")
    parser.add_argument("--output", type=str, default=OUTPUT_CSV_FILE, help="Path to output CSV file.")

    args = parser.parse_args()
    main(args.input, args.output)
