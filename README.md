# 🪷 Kavya-Kanaja Backend

AI-powered backend for the Kavya-Kanaja Kannada poetry learning app.
Built with **FastAPI** + **Groq API** + **Llama 3.3 70B**.

## Stack
- **FastAPI** — Python web framework
- **Groq API** — Ultra-fast LLM inference
- **Llama 3.3 70B** — AI model for poem explanations
- **Render** — Free cloud hosting

## Local Setup

### 1. Clone and enter the folder
```bash
cd Kavya_Kanaja_Backend
```

### 2. Create virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set your Groq API key
```bash
cp .env.example .env
# Open .env and paste your key from https://console.groq.com
```

### 5. Run the server
```bash
uvicorn main:app --reload --port 8000
```

### 6. Test it
Open http://localhost:8000/docs — you'll see the interactive API documentation.

## API Reference

### POST /explain

**Request:**
```json
{
  "text": "ಕತ್ತಲೆಯ ನಡುವೆ ಒಂದು ಕಿರಣ ಮೂಡಿತು",
  "language": "en",
  "mode": "full"
}
```

**Response:**
```json
{
  "meaning": "...",
  "line_explanation": "...",
  "word_meanings": "...",
  "theme": "...",
  "summary": "...",
  "story": "..."
}
```

| Field | Values | Description |
|-------|--------|-------------|
| `language` | `en`, `kn` | Response language |
| `mode` | `full`, `word` | Full poem or single word |

## Deploy to Render

1. Push this folder to a GitHub repository
2. Go to [render.com](https://render.com) → New → Web Service
3. Connect your GitHub repo
4. Render auto-detects `render.yaml`
5. Add `GROQ_API_KEY` in Environment tab
6. Click **Deploy**

Your API will be live at: `https://kavya-kanaja-backend.onrender.com`

## Update Android app

In `utils/Constants.kt`, replace:
```kotlin
const val BASE_URL = "https://your-api-server.com/"
```
with:
```kotlin
const val BASE_URL = "https://kavya-kanaja-backend.onrender.com/"
```