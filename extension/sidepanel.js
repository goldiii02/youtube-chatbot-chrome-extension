/**
 * Side Panel JavaScript for YouTube Chatbot Extension
 * Handles chat UI and API communication
 */

// Configuration - UPDATE THIS WITH YOUR BACKEND URL
const API_BASE_URL = 'http://localhost:8000'; // Change to your deployed backend URL

let currentVideoId = null;
let chatHistory = [];

// DOM Elements
const messagesContainer = document.getElementById('messages');
const userInput = document.getElementById('userInput');
const sendButton = document.getElementById('sendButton');
const clearButton = document.getElementById('clearButton');
const loadingIndicator = document.getElementById('loading');
const errorMessage = document.getElementById('errorMessage');
const videoIdDisplay = document.getElementById('videoId');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
  initializeExtension();
});

// Listen for video changes from content script
window.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'VIDEO_CHANGED') {
    handleVideoChange(event.data.videoId);
  }
});

// Also check video ID on load
chrome.runtime.sendMessage({ type: 'GET_VIDEO_ID' }, (response) => {
  if (response && response.videoId) {
    handleVideoChange(response.videoId);
  } else {
    // Try to extract from current tab
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      if (tabs[0] && tabs[0].url) {
        const videoId = extractVideoId(tabs[0].url);
        if (videoId) {
          handleVideoChange(videoId);
        }
      }
    });
  }
});

function extractVideoId(url) {
  const watchMatch = url.match(/[?&]v=([^&]+)/);
  if (watchMatch) return watchMatch[1].split('&')[0];
  
  const shortMatch = url.match(/youtu\.be\/([^?]+)/);
  if (shortMatch) return shortMatch[1];
  
  return null;
}

function initializeExtension() {
  // Event listeners
  sendButton.addEventListener('click', sendMessage);
  clearButton.addEventListener('click', clearChat);
  
  userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  });
  
  // Focus input on load
  userInput.focus();
}

function handleVideoChange(newVideoId) {
  if (newVideoId && newVideoId !== currentVideoId) {
    currentVideoId = newVideoId;
    videoIdDisplay.textContent = `Video ID: ${newVideoId}`;
    
    // Clear chat history for new video
    clearChat();
    
    // Show welcome message
    addBotMessage('👋 Hi! I can answer questions about the current YouTube video. What would you like to know?');
  }
}

async function sendMessage() {
  const query = userInput.value.trim();
  
  if (!query) {
    return;
  }
  
  if (!currentVideoId) {
    showError('Please navigate to a YouTube video first.');
    return;
  }
  
  // Add user message to chat
  addUserMessage(query);
  userInput.value = '';
  
  // Show loading indicator
  showLoading(true);
  hideError();
  
  try {
    // Call backend API
    const response = await fetch(`${API_BASE_URL}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        video_id: currentVideoId,
        user_query: query
      })
    });
    
    const data = await response.json();
    
    if (!response.ok) {
      throw new Error(data.error || 'Failed to get response');
    }
    
    if (data.success) {
      addBotMessage(data.answer);
    } else {
      throw new Error(data.error || 'Unknown error occurred');
    }
    
  } catch (error) {
    console.error('Error:', error);
    
    if (error.message.includes('transcript')) {
      showError('Unable to fetch transcript. The video may be private, have transcripts disabled, or be a live stream.');
    } else if (error.message.includes('Failed to fetch')) {
      showError('Cannot connect to backend server. Please ensure the backend is running and check the API_BASE_URL in sidepanel.js');
    } else {
      showError(`Error: ${error.message}`);
    }
    
    addBotMessage('Sorry, I encountered an error. Please try again or check if the video has transcripts enabled.');
  } finally {
    showLoading(false);
    userInput.focus();
  }
}

function addUserMessage(text) {
  const messageDiv = document.createElement('div');
  messageDiv.className = 'message user-message';
  messageDiv.innerHTML = `
    <div class="message-content">${escapeHtml(text)}</div>
  `;
  messagesContainer.appendChild(messageDiv);
  scrollToBottom();
}

function addBotMessage(text) {
  const messageDiv = document.createElement('div');
  messageDiv.className = 'message bot-message';
  messageDiv.innerHTML = `
    <div class="message-content">${escapeHtml(text)}</div>
  `;
  messagesContainer.appendChild(messageDiv);
  scrollToBottom();
}

function clearChat() {
  messagesContainer.innerHTML = '';
  chatHistory = [];
  addBotMessage('👋 Hi! I can answer questions about the current YouTube video. What would you like to know?');
}

function showLoading(show) {
  loadingIndicator.style.display = show ? 'flex' : 'none';
}

function showError(message) {
  errorMessage.textContent = message;
  errorMessage.style.display = 'block';
  setTimeout(() => {
    errorMessage.style.display = 'none';
  }, 5000);
}

function hideError() {
  errorMessage.style.display = 'none';
}

function scrollToBottom() {
  messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

