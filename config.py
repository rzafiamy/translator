
# Model configuration (change as needed)
MODEL_NAME = "llama-3.3-70b"  # Can be GPT-3.5, Claude, Mistral, Llama, etc.



import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# LLM API Configuration (Sensitive info stored in .env)
LLM_API_URL = os.getenv("LLM_API_URL", "https://api.example.com/v1/chat/completions")
API_KEY = os.getenv("API_KEY", "your_default_api_key")

# Model configuration
MODEL_NAME = os.getenv("MODEL_NAME", "llama-3.3-70b")  # Change model as needed

# Rate limiting settings
SLEEP_TIME = int(os.getenv("SLEEP_TIME", 10))  # Default: 10 seconds between requests

# System & User Prompt Templates
SYSTEM_PROMPT = os.getenv(
    "SYSTEM_PROMPT",
    "You are a professional FRENCH translator that accurately translates lyrics while keeping the meaning and format intact. You will be given Malagasy Text. Do not add any additional information or explanations. Keep the translation in FRENCH and use the same format as input."
)

USER_PROMPT_TEMPLATE = os.getenv(
    "USER_PROMPT_TEMPLATE",
    "Provide the translation of the following song lyrics into FRENCH without extra comments or introductory. Use the same formatting as input. Escape new line if exists :\n\n{text}"
)

# CSV File Paths
INPUT_CSV_FILE = os.getenv("INPUT_CSV_FILE", "input.csv")
OUTPUT_CSV_FILE = os.getenv("OUTPUT_CSV_FILE", "output.csv")
