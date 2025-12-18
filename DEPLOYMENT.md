# Deployment Guide

## Backend Deployment Options

### Option 1: Render (Recommended for Beginners)

1. **Create Account**: Sign up at [render.com](https://render.com)

2. **Create New Web Service**:
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the `backend` folder

3. **Configure Build**:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

4. **Set Environment Variables**:
   - Go to "Environment" tab
   - Add all variables from `env.example`:
     ```
     LLM_PROVIDER=openai
     OPENAI_API_KEY=your_key_here
     EMBEDDING_PROVIDER=openai
     API_PORT=8000
     CORS_ORIGINS=https://your-extension-id.chromiumapp.org
     ```

5. **Deploy**: Click "Create Web Service"

6. **Get URL**: Your backend will be at `https://your-app.onrender.com`

### Option 2: Railway

1. **Create Account**: Sign up at [railway.app](https://railway.app)

2. **New Project**:
   - Click "New Project"
   - "Deploy from GitHub repo"
   - Select your repository

3. **Configure**:
   - Railway auto-detects Python
   - Set root directory to `backend`
   - Add environment variables in "Variables" tab

4. **Deploy**: Railway automatically deploys on push

5. **Get URL**: Your backend URL will be shown in the dashboard

### Option 3: AWS EC2

1. **Launch EC2 Instance**:
   - Ubuntu 22.04 LTS
   - t2.micro (free tier) or larger
   - Configure security group: allow port 8000

2. **SSH into Instance**:
   ```bash
   ssh -i your-key.pem ubuntu@your-ec2-ip
   ```

3. **Install Dependencies**:
   ```bash
   sudo apt update
   sudo apt install python3-pip python3-venv git -y
   ```

4. **Clone and Setup**:
   ```bash
   git clone your-repo-url
   cd yt-chatbot-extension/backend
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   cp env.example .env
   nano .env  # Add your API keys
   ```

5. **Run with PM2** (recommended):
   ```bash
   sudo npm install -g pm2
   pm2 start "uvicorn main:app --host 0.0.0.0 --port 8000" --name youtube-chatbot
   pm2 save
   pm2 startup
   ```

6. **Configure Nginx** (optional but recommended):
   ```bash
   sudo apt install nginx
   # Configure nginx reverse proxy
   ```

### Option 4: Heroku

1. **Install Heroku CLI**: [heroku.com](https://devcenter.heroku.com/articles/heroku-cli)

2. **Create Procfile** in `backend/`:
   ```
   web: uvicorn main:app --host 0.0.0.0 --port $PORT
   ```

3. **Deploy**:
   ```bash
   cd backend
   heroku create your-app-name
   heroku config:set LLM_PROVIDER=openai
   heroku config:set OPENAI_API_KEY=your_key
   git push heroku main
   ```

## Chrome Extension Deployment

### Step 1: Prepare for Publishing

1. **Update API URL**:
   - Open `extension/sidepanel.js`
   - Change `API_BASE_URL` to your deployed backend URL
   - Example: `const API_BASE_URL = 'https://your-app.onrender.com';`

2. **Update CORS**:
   - In `backend/config.py` or `.env`:
   - Add your extension ID to `CORS_ORIGINS`
   - Format: `chrome-extension://YOUR_EXTENSION_ID`

3. **Create Icons**:
   - Ensure you have proper icons (16x16, 48x48, 128x128)
   - Use a professional design tool

4. **Take Screenshots**:
   - 1280x800 or 640x400 pixels
   - Show the extension in action
   - At least 1 screenshot required

### Step 2: Create ZIP File

**Windows**:
```powershell
cd extension
Compress-Archive -Path * -DestinationPath ../youtube-chatbot-extension.zip
```

**macOS/Linux**:
```bash
cd extension
zip -r ../youtube-chatbot-extension.zip . -x "*.git*" "*.DS_Store"
```

### Step 3: Submit to Chrome Web Store

1. **Go to Developer Dashboard**:
   - Visit [Chrome Web Store Developer Dashboard](https://chrome.google.com/webstore/devconsole)
   - Sign in with Google account
   - Pay one-time $5 registration fee (if not already paid)

2. **Create New Item**:
   - Click "New Item"
   - Upload your ZIP file
   - Fill in required information:

   **Store Listing**:
   - Name: YouTube Chatbot
   - Summary: Chat with YouTube videos using AI
   - Description: (Use detailed description from README)
   - Category: Productivity or Education
   - Language: English (and others if needed)

   **Privacy**:
   - Single purpose: Yes
   - Host permissions: Only YouTube
   - User data: Explain what data you collect (transcripts, queries)

3. **Upload Assets**:
   - Icons (16, 48, 128)
   - Screenshots (at least 1)
   - Promotional images (optional)

4. **Submit for Review**:
   - Review can take 1-7 days
   - You'll receive email notifications

### Step 4: Post-Publishing

1. **Monitor Reviews**: Respond to user feedback
2. **Update Regularly**: Fix bugs and add features
3. **Version Updates**: Update version in `manifest.json` before uploading new version

## Chrome Web Store Checklist

- [ ] Extension icons (16x16, 48x48, 128x128 PNG)
- [ ] Store listing screenshots (1280x800 or 640x400)
- [ ] Detailed description (at least 132 characters)
- [ ] Privacy policy URL (if collecting user data)
- [ ] Support email
- [ ] Category selected
- [ ] Language selected
- [ ] API URL updated to production backend
- [ ] CORS configured for extension ID
- [ ] Tested on multiple YouTube videos
- [ ] Error handling tested
- [ ] Rate limiting configured

## Security Checklist

- [ ] API keys stored in environment variables (never in code)
- [ ] CORS configured to only allow your extension
- [ ] Rate limiting enabled
- [ ] Input validation on all endpoints
- [ ] HTTPS enabled for backend (required for production)
- [ ] No sensitive data in extension code
- [ ] Privacy policy published (if collecting data)

## Troubleshooting Deployment

### Backend Issues

**Problem**: CORS errors
**Solution**: Update `CORS_ORIGINS` in backend config to include your extension ID

**Problem**: Rate limiting too strict
**Solution**: Adjust `RATE_LIMIT_PER_MINUTE` in config

**Problem**: Timeout errors
**Solution**: Increase timeout on hosting platform (Render: 30s, Railway: 60s)

### Extension Issues

**Problem**: Extension rejected
**Solution**: 
- Ensure privacy policy if collecting data
- Fix any security warnings
- Provide clear description

**Problem**: API calls failing
**Solution**:
- Verify backend URL is correct
- Check CORS configuration
- Ensure backend is accessible

## Production Best Practices

1. **Monitoring**: Set up error tracking (Sentry, LogRocket)
2. **Logging**: Implement proper logging
3. **Backup**: Regular backups of vector DB (if using persistent storage)
4. **Scaling**: Use load balancer for high traffic
5. **CDN**: Use CDN for static assets (if any)
6. **SSL**: Always use HTTPS in production

## Cost Estimation

### Backend Hosting:
- **Render**: Free tier available, $7/month for production
- **Railway**: $5/month minimum
- **AWS EC2**: Free tier for 12 months, then ~$10/month
- **Heroku**: Free tier discontinued, $7/month minimum

### API Costs:
- **OpenAI**: ~$0.002 per 1K tokens (varies by model)
- **Gemini**: Free tier available, then pay-as-you-go
- **Ollama**: Free (self-hosted)

### Extension:
- **Chrome Web Store**: One-time $5 registration fee

## Support

For deployment issues:
1. Check hosting platform logs
2. Test backend with curl/Postman
3. Check browser console for extension errors
4. Review Chrome Web Store review feedback

