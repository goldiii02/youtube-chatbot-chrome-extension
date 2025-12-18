# YouTube Chatbot Chrome Extension

A production-ready Chrome Extension that allows users to chat with YouTube videos using AI-powered RAG (Retrieval Augmented Generation). The chatbot answers questions based solely on the video's transcript content.

## 🎯 Features

- **Side Panel UI**: Clean, modern chat interface integrated into YouTube
- **Real-time Video Detection**: Automatically detects current YouTube video
- **RAG-powered Q&A**: Uses LangChain with vector embeddings for accurate answers
- **Multiple LLM Support**: OpenAI, Gemini, or local Ollama
- **Vector Database**: FAISS or Chroma for efficient similarity search
- **Transcript Caching**: Caches transcripts to reduce API calls
- **Error Handling**: Graceful handling of private videos, disabled transcripts, and live streams
- **Rate Limiting**: Built-in rate limiting for API protection

## 📁 Project Structure

```
yt-chatbot-extension/
├── backend/
│   ├── main.py                 # FastAPI server
│   ├── rag_pipeline.py         # RAG implementation
│   ├── embeddings.py           # Embedding generation
│   ├── transcript_loader.py    # YouTube transcript fetching
│   ├── config.py               # Configuration management
│   ├── requirements.txt        # Python dependencies
│   └── .env.example           # Environment variables template
├── extension/
│   ├── manifest.json          # Chrome extension manifest (V3)
│   ├── background.js          # Service worker
│   ├── content.js             # Content script for YouTube
│   ├── sidepanel.html         # Side panel UI
│   ├── sidepanel.js           # Side panel logic
│   ├── styles.css             # Styling
│   └── icons/                 # Extension icons (create these)
│       ├── icon16.png
│       ├── icon48.png
│       └── icon128.png
└── README.md                  # This file
```

## 🚀 Quick Start

### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Create virtual environment** (recommended):
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your API keys:
   ```env
   LLM_PROVIDER=openai
   OPENAI_API_KEY=your_openai_api_key_here
   EMBEDDING_PROVIDER=openai
   EMBEDDING_MODEL=text-embedding-ada-002
   ```

5. **Run the backend server**:
   ```bash
   python main.py
   ```
   
   The server will start at `http://localhost:8000`

### Chrome Extension Setup

1. **Open Chrome Extensions page**:
   - Navigate to `chrome://extensions/`
   - Enable "Developer mode" (toggle in top right)

2. **Load the extension**:
   - Click "Load unpacked"
   - Select the `extension` folder

3. **Update API URL** (if backend is not on localhost):
   - Open `extension/sidepanel.js`
   - Update `API_BASE_URL` constant:
     ```javascript
     const API_BASE_URL = 'http://localhost:8000'; // Your backend URL
     ```

4. **Create extension icons**:
   - Create an `icons` folder in the `extension` directory
   - Add three PNG files: `icon16.png`, `icon48.png`, `icon128.png`
   - You can use any image editor or online icon generator

5. **Test the extension**:
   - Navigate to any YouTube video
   - Click the extension icon in the toolbar
   - The side panel should open with the chat interface

## ⚙️ Configuration

### LLM Providers

#### OpenAI (Recommended)
```env
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-...
LLM_MODEL=gpt-3.5-turbo
EMBEDDING_PROVIDER=openai
EMBEDDING_MODEL=text-embedding-ada-002
```

#### Google Gemini
```env
LLM_PROVIDER=gemini
GEMINI_API_KEY=your_gemini_key
EMBEDDING_PROVIDER=gemini
```

#### Ollama (Local)
```env
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama2
EMBEDDING_PROVIDER=local
```

### Vector Database

Choose between FAISS (faster) or Chroma (more features):

```env
VECTOR_DB_TYPE=faiss  # or chroma
```

### RAG Settings

```env
CHUNK_SIZE=1000          # Text chunk size
CHUNK_OVERLAP=200        # Overlap between chunks
TOP_K_RESULTS=3          # Number of chunks to retrieve
```

## 🔌 API Endpoints

### POST /chat
Send a chat message about a YouTube video.

**Request**:
```json
{
  "video_id": "dQw4w9WgXcQ",
  "user_query": "What is this video about?"
}
```

**Response**:
```json
{
  "answer": "This video is about...",
  "success": true,
  "error": null
}
```

### GET /health
Health check endpoint.

**Response**:
```json
{
  "status": "ok",
  "message": "API is healthy"
}
```

### POST /reset/{video_id}
Reset RAG pipeline for a specific video.

## 🎨 Customization

### Styling
Edit `extension/styles.css` to customize the chat UI appearance.

### System Prompt
Modify the prompt template in `backend/rag_pipeline.py` in the `_create_prompt_template()` method.

### Rate Limiting
Adjust rate limits in `backend/config.py`:
```python
RATE_LIMIT_PER_MINUTE=30
```

## 🚢 Deployment

### Backend Deployment

#### Option 1: Render
1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables in Render dashboard

#### Option 2: Railway
1. Create a new project on Railway
2. Connect GitHub repository
3. Railway auto-detects Python and installs dependencies
4. Add environment variables in Railway dashboard
5. Deploy!

#### Option 3: AWS EC2
1. Launch an EC2 instance (Ubuntu)
2. Install Python and dependencies
3. Use PM2 or systemd to run the FastAPI server
4. Configure security groups for port 8000
5. Set up Nginx reverse proxy (recommended)

### Chrome Extension Publishing

1. **Prepare for submission**:
   - Create high-quality icons (16x16, 48x48, 128x128)
   - Take screenshots of the extension in action
   - Write a detailed description

2. **Update manifest.json**:
   - Ensure version number is correct
   - Add store listing details

3. **Update API URL**:
   - Change `API_BASE_URL` in `sidepanel.js` to your deployed backend URL
   - Ensure CORS is configured correctly

4. **Create ZIP file**:
   ```bash
   cd extension
   zip -r ../youtube-chatbot-extension.zip . -x "*.git*" "*.DS_Store"
   ```

5. **Submit to Chrome Web Store**:
   - Go to [Chrome Web Store Developer Dashboard](https://chrome.google.com/webstore/devconsole)
   - Click "New Item"
   - Upload ZIP file
   - Fill in store listing information
   - Submit for review

### Chrome Web Store Checklist

- [ ] Extension icons (16x16, 48x48, 128x128)
- [ ] Store listing screenshots (1280x800 or 640x400)
- [ ] Detailed description
- [ ] Privacy policy URL (if collecting data)
- [ ] Terms of service (if applicable)
- [ ] Support email
- [ ] Category selection
- [ ] Language selection

## 🔒 Security Best Practices

1. **API Keys**: Never commit `.env` file to version control
2. **CORS**: Configure CORS to only allow your extension ID
3. **Rate Limiting**: Enable rate limiting to prevent abuse
4. **Input Validation**: Validate all user inputs
5. **HTTPS**: Use HTTPS for backend in production

## 🐛 Troubleshooting

### Extension not opening side panel
- Check if you're on a YouTube video page
- Verify manifest.json permissions
- Check browser console for errors

### Backend connection errors
- Verify backend is running: `curl http://localhost:8000/health`
- Check `API_BASE_URL` in `sidepanel.js`
- Verify CORS settings in `backend/config.py`

### Transcript errors
- Some videos have transcripts disabled
- Private videos cannot be accessed
- Live streams may not have transcripts

### Rate limiting errors
- Adjust `RATE_LIMIT_PER_MINUTE` in config
- Implement user authentication for higher limits

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For issues and questions, please open an issue on GitHub.

---

**Built with ❤️ using LangChain, FastAPI, and Chrome Extension APIs**

