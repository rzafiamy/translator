# 🎵 CSV Song Lyrics Translator

## 📌 Description
This script reads a **CSV file** containing song lyrics with **HTML-encoded text** and translates them using an **LLM API**.  
It supports **any OpenAI-compatible API** (e.g., OpenAI, Azure OpenAI, TogetherAI, Local LLMs like Llama).

## ⚙️ Setup

### 1️⃣ Install Dependencies
Make sure you have Python installed, then run:
```bash
pip install -r requirements.txt
```

### 2️⃣ Configure Environment Variables
Before running the script, **set up your API details**:  
1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
2. Open `.env` and update the values:
   ```ini
   LLM_API_URL=https://your-llm-api.com/v1/chat/completions
   API_KEY=your_secret_api_key
   MODEL_NAME=llama-3.3-70b
   ```

## 🚀 Usage
Run the script with:
```bash
python manager.py --input input.csv --output translated_output.csv
```
If **no arguments** are provided, it defaults to values from `.env`.

## 📝 Notes
- **The script saves translations incrementally** (after each song) to prevent data loss.
- **Rate limiting is implemented** (`SLEEP_TIME`) to avoid API request blocking.
- **Ensure your API key is valid** before running the script.

## 🔹 Key Features
✅ **No external CSV libraries required** (fully manual parsing)  
✅ **Decodes HTML entities** (e.g., `&eacute; → é`)  
✅ **Translates lyrics using an OpenAI-compatible LLM**  
✅ **Handles API rate limiting with automatic delays**  
✅ **Saves progress after each song to avoid losing translations**  

---
🛠 **Built with Python** 🐍 | 💡 Supports OpenAI-Compatible LLMs  
🎵 **Enjoy seamless song translation!** 🌍🎶  