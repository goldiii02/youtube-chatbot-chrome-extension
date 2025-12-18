/**
 * Content Script for YouTube Chatbot Extension
 * Extracts video ID and communicates with side panel
 */

let currentVideoId = null;

// Extract video ID from current page
function getVideoId() {
  const url = window.location.href;
  
  // youtube.com/watch?v=VIDEO_ID
  const watchMatch = url.match(/[?&]v=([^&]+)/);
  if (watchMatch) {
    return watchMatch[1].split('&')[0];
  }
  
  // youtu.be/VIDEO_ID
  const shortMatch = url.match(/youtu\.be\/([^?]+)/);
  if (shortMatch) {
    return shortMatch[1];
  }
  
  return null;
}

// Monitor URL changes (YouTube uses SPA navigation)
function checkVideoChange() {
  const newVideoId = getVideoId();
  
  if (newVideoId && newVideoId !== currentVideoId) {
    currentVideoId = newVideoId;
    
    // Notify side panel about video change
    chrome.runtime.sendMessage({
      type: 'VIDEO_CHANGED',
      videoId: newVideoId
    });
  }
}

// Initial check
currentVideoId = getVideoId();

// Listen for URL changes (YouTube uses pushState)
let lastUrl = location.href;
new MutationObserver(() => {
  const url = location.href;
  if (url !== lastUrl) {
    lastUrl = url;
    checkVideoChange();
  }
}).observe(document, { subtree: true, childList: true });

// Also listen for popstate events
window.addEventListener('popstate', checkVideoChange);

// Listen for messages from background script
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.type === 'VIDEO_CHANGED') {
    currentVideoId = request.videoId;
    // Forward to side panel if it exists
    window.postMessage({
      type: 'VIDEO_CHANGED',
      videoId: request.videoId
    }, '*');
  }
  
  if (request.type === 'GET_VIDEO_ID') {
    sendResponse({ videoId: currentVideoId || getVideoId() });
  }
});

// Send initial video ID to side panel
window.addEventListener('load', () => {
  const videoId = getVideoId();
  if (videoId) {
    window.postMessage({
      type: 'VIDEO_CHANGED',
      videoId: videoId
    }, '*');
  }
});

