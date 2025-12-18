# Chrome Extension - Setup Instructions

## Required Files

Make sure you have all these files in the `extension` directory:

- `manifest.json` ✅
- `background.js` ✅
- `content.js` ✅
- `sidepanel.html` ✅
- `sidepanel.js` ✅
- `styles.css` ✅
- `icons/` folder with:
  - `icon16.png`
  - `icon48.png`
  - `icon128.png`

## Creating Icons

If you don't have icons yet, you can:

1. **Use an online generator**: Search for "Chrome extension icon generator"
2. **Create simple icons**: Use any image editor (Paint, GIMP, Photoshop)
3. **Use placeholder images**: For testing, any 16x16, 48x48, and 128x128 PNG files will work

## Loading the Extension

1. Open Chrome
2. Go to `chrome://extensions/`
3. Enable "Developer mode" (top right toggle)
4. Click "Load unpacked"
5. Select the `extension` folder
6. The extension should appear in your list

## Configuration

Before using, update `sidepanel.js`:

```javascript
const API_BASE_URL = 'http://localhost:8000'; // Your backend URL
```

For production, use your deployed backend URL (e.g., `https://your-backend.railway.app`).

## Testing

1. Navigate to any YouTube video
2. Click the extension icon
3. Side panel should open
4. Try asking a question!

## Troubleshooting

- **Extension not loading**: Check browser console for errors
- **Side panel not opening**: Make sure you're on a YouTube video page
- **API errors**: Verify backend is running and URL is correct

