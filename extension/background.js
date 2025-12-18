/**
 * Background Service Worker for YouTube Chatbot Extension
 * Handles side panel opening and video ID tracking
 */

// Open side panel when extension icon is clicked
chrome.action.onClicked.addListener((tab) => {
  if (tab.url && (tab.url.includes('youtube.com/watch') || tab.url.includes('youtu.be/'))) {
    chrome.sidePanel.open({ windowId: tab.windowId });
  }
});

// Listen for tab updates to detect video changes
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status === 'complete' && tab.url) {
    if (tab.url.includes('youtube.com/watch') || tab.url.includes('youtu.be/')) {
      // Extract video ID and notify content script
      const videoId = extractVideoId(tab.url);
      if (videoId) {
        chrome.tabs.sendMessage(tabId, {
          type: 'VIDEO_CHANGED',
          videoId: videoId
        }).catch(() => {
          // Content script might not be ready yet
        });
      }
    }
  }
});

// Listen for messages from content script
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.type === 'GET_VIDEO_ID') {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      if (tabs[0] && tabs[0].url) {
        const videoId = extractVideoId(tabs[0].url);
        sendResponse({ videoId: videoId });
      } else {
        sendResponse({ videoId: null });
      }
    });
    return true; // Keep channel open for async response
  }
  
  if (request.type === 'OPEN_SIDE_PANEL') {
    chrome.sidePanel.open({ windowId: sender.tab.windowId });
    sendResponse({ success: true });
  }
});

/**
 * Extract YouTube video ID from URL
 * Supports both youtube.com/watch?v= and youtu.be/ formats
 */
function extractVideoId(url) {
  if (!url) return null;
  
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

// Set up side panel for YouTube tabs
chrome.tabs.onUpdated.addListener((tabId, info, tab) => {
  if (tab.url && (tab.url.includes('youtube.com/watch') || tab.url.includes('youtu.be/'))) {
    chrome.sidePanel.setOptions({
      tabId: tabId,
      path: 'sidepanel.html',
      enabled: true
    });
  }
});

