# Setup Guide - YouTube Chatbot Extension

## Prerequisites

- Python 3.8 or higher
- Google Chrome browser
- API keys for your chosen LLM provider (OpenAI, Gemini, or Ollama)

## Step-by-Step Setup

### 1. Backend Setup

#### Step 1.1: Install Python Dependencies

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
```

#### Step 1.2: Configure Environment Variables

Copy the example environment file:
```bash
cp env.example .env
```

Edit `.env` and add your API keys. For OpenAI (recommended):
```env
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-your-actual-api-key-here
EMBEDDING_PROVIDER=openai
EMBEDDING_MODEL=text-embedding-ada-002
```

#### Step 1.3: Run the Backend Server

```bash
python main.py
```

The server should start at `http://localhost:8000`. Test it:
```bash
curl http://localhost:8000/health
```

### 2. Chrome Extension Setup

#### Step 2.1: Create Extension Icons

Create an `icons` folder in the `extension` directory:
```bash
mkdir extension/icons
```

You need three icon files:
- `icon16.png` (16x16 pixels)
- `icon48.png` (48x48 pixels)
- `icon128.png` (128x128 pixels)

You can:
- Use an online icon generator
- Create simple icons with any image editor
- Use placeholder images for testing

#### Step 2.2: Configure API URL

Open `extension/sidepanel.js` and verify the API URL:
```javascript
const API_BASE_URL = 'http://localhost:8000';
```

For production, change this to your deployed backend URL.

#### Step 2.3: Load Extension in Chrome

1. Open Chrome and navigate to `chrome://extensions/`
2. Enable "Developer mode" (toggle in top right)
3. Click "Load unpacked"
4. Select the `extension` folder
5. The extension should appear in your extensions list

#### Step 2.4: Test the Extension

1. Navigate to any YouTube video (e.g., `https://www.youtube.com/watch?v=dQw4w9WgXcQ`)
2. Click the extension icon in the Chrome toolbar
3. The side panel should open on the right
4. Try asking a question about the video

## Troubleshooting

### Backend Issues

**Problem**: `ModuleNotFoundError` for LangChain
**Solution**: Make sure you're using Python 3.8+ and installed all requirements:
```bash
pip install --upgrade -r requirements.txt
```

**Problem**: `OPENAI_API_KEY not set`
**Solution**: Check your `.env` file exists and has the correct key. Make sure it's in the `backend` directory.

**Problem**: Port 8000 already in use
**Solution**: Change `API_PORT` in `.env` or kill the process using port 8000.

### Extension Issues

**Problem**: Side panel doesn't open
**Solution**: 
- Make sure you're on a YouTube video page
- Check browser console (F12) for errors
- Verify manifest.json is valid JSON

**Problem**: "Cannot connect to backend"
**Solution**:
- Verify backend is running: `curl http://localhost:8000/health`
- Check `API_BASE_URL` in `sidepanel.js`
- Ensure CORS is configured in `backend/config.py`

**Problem**: "Transcript not available"
**Solution**:
- Some videos have transcripts disabled
- Private videos cannot be accessed
- Live streams may not have transcripts
- Try a different video

## Next Steps

- Read the main [README.md](README.md) for detailed documentation
- Customize the UI in `extension/styles.css`
- Adjust RAG settings in `backend/config.py`
- Deploy backend to production (see README.md)

## Quick Test

Test the complete flow:

1. Start backend: `cd backend && python main.py`
2. Open Chrome extension
3. Go to: https://www.youtube.com/watch?v=dQw4w9WgXcQ
4. Click extension icon
5. Ask: "What is this video about?"

If everything works, you should see an AI-generated answer!

