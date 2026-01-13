const API_BASE_URL = 'https://onboardai-d0dab4frh4hhffaq.centralindia-01.azurewebsites.net';

function getSessionId() {
  let sessionId = localStorage.getItem("session_id");
  if (!sessionId) {
    sessionId = crypto.randomUUID();
    localStorage.setItem("session_id", sessionId);
  }
  return sessionId;
}

const chatMessages = document.getElementById('chatMessages');
const messageInput = document.getElementById('messageInput');
const sendButton = document.getElementById('sendButton');
const charCount = document.getElementById('charCount');
const typingIndicator = document.getElementById('typingIndicator');
const errorModal = document.getElementById('errorModal');
const errorMessage = document.getElementById('errorMessage');

let isLoading = false;

document.addEventListener('DOMContentLoaded', () => {
  sendButton.addEventListener('click', sendMessage);
  messageInput.addEventListener('keypress', handleKeyPress);
  messageInput.addEventListener('input', updateCharCount);
  messageInput.focus();
});

function handleKeyPress(e) {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
}

function updateCharCount() {
  const length = messageInput.value.length;
  charCount.textContent = length;

  if (length > 900) {
    charCount.style.color = 'var(--warning-color)';
  } else if (length >= 1000) {
    charCount.style.color = 'var(--error-color)';
  } else {
    charCount.style.color = 'var(--secondary-text)';
  }
}

async function sendMessage() {
  const message = messageInput.value.trim();

  if (!message || isLoading) return;

  addMessage(message, 'user');

  messageInput.value = '';
  updateCharCount();

  showTypingIndicator();
  isLoading = true;
  sendButton.disabled = true;

  try {
    const response = await fetch(`${API_BASE_URL}/ask`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        query: message,
        session_id: getSessionId()
      })
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();

    addMessage(data.answer, 'bot', data.source);

  } catch (error) {
    console.error('Error:', error);
    showError('Failed to connect to the server. Please check your connection and try again.');
  } finally {
    hideTypingIndicator();
    isLoading = false;
    sendButton.disabled = false;
    messageInput.focus();
  }
}

function addMessage(content, sender, sources = []) {
  const messageDiv = document.createElement('div');
  messageDiv.className = `message ${sender}-message`;

  const avatarDiv = document.createElement('div');
  avatarDiv.className = 'message-avatar';
  avatarDiv.innerHTML = sender === 'user' ?
    '<i class="fas fa-user"></i>' :
    '<i class="fas fa-robot"></i>';

  const contentDiv = document.createElement('div');
  contentDiv.className = 'message-content';

  const formattedContent = renderMarkdown(content);

  contentDiv.innerHTML = formattedContent;

  if (sources && sources.length > 0) {
    const sourceDiv = document.createElement('div');
    sourceDiv.className = 'source-attribution';

    const sourceIcon = document.createElement('i');
    sourceIcon.className = 'fas fa-link';

    const sourceText = document.createElement('span');
    sourceText.textContent = `Sources: ${sources.join(', ')}`;

    sourceDiv.appendChild(sourceIcon);
    sourceDiv.appendChild(sourceText);
    contentDiv.appendChild(sourceDiv);
  }

  messageDiv.appendChild(avatarDiv);
  messageDiv.appendChild(contentDiv);

  chatMessages.appendChild(messageDiv);

  Prism.highlightAllUnder(contentDiv);

  scrollToBottom();
}

function renderMarkdown(text) {
  marked.setOptions({
    breaks: true,
    gfm: true,
    sanitize: false,
    highlight: function (code, lang) {
      if (Prism.languages[lang]) {
        return Prism.highlight(code, Prism.languages[lang], lang);
      }
      return code;
    }
  });

  let html = marked.parse(text);

  html = html
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&amp;/g, '&');

  return html;
}

function showTypingIndicator() {
  typingIndicator.style.display = 'flex';
  scrollToBottom();
}

function hideTypingIndicator() {
  typingIndicator.style.display = 'none';
}

function scrollToBottom() {
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

function showError(message) {
  errorMessage.textContent = message;
  errorModal.style.display = 'block';
}

function closeErrorModal() {
  errorModal.style.display = 'none';
}

window.addEventListener('click', (e) => {
  if (e.target === errorModal) {
    closeErrorModal();
  }
});

document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape' && errorModal.style.display === 'block') {
    closeErrorModal();
  }
});

function autoResize() {
  messageInput.style.height = 'auto';
  messageInput.style.height = Math.min(messageInput.scrollHeight, 120) + 'px';
}

document.addEventListener('keydown', (e) => {
  // Ctrl/Cmd + K to clear chat
  if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
    e.preventDefault();
    if (confirm('Clear all messages?')) {
      chatMessages.innerHTML = '';
      addMessage('Hello! I\'m your AI assistant. How can I help you today?', 'bot');
    }
  }

  // Ctrl/Cmd + / to focus input
  if ((e.ctrlKey || e.metaKey) && e.key === '/') {
    e.preventDefault();
    messageInput.focus();
  }
});

async function checkConnection() {
  try {
    const response = await fetch(`${API_BASE_URL}/`);
    const data = await response.json();

    if (data.status === 'running') {
      document.querySelector('.status-text').textContent = 'Online';
      document.querySelector('.status-dot').style.background = 'var(--success-color)';
    }
  } catch (error) {
    document.querySelector('.status-text').textContent = 'Offline';
    document.querySelector('.status-dot').style.background = 'var(--error-color)';
  }
}

checkConnection();

setInterval(checkConnection, 30000);
