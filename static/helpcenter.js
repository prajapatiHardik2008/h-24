/**
 * H-24 Portal - AI Help Center
 * Modern JavaScript with error handling, local storage, and animations
 */

// ============================================
// DOM Elements
// ============================================
const DOM = {
    queryInput: document.getElementById('queryInput'),
    submitBtn: document.getElementById('submitBtn'),
    loading: document.getElementById('loading'),
    resultCard: document.getElementById('resultCard'),
    aiResponse: document.getElementById('aiResponse'),
    statusMsg: document.getElementById('statusMsg'),
    copyBtn: document.getElementById('copyBtn'),
    clearHistoryBtn: document.getElementById('clearHistoryBtn'),
    statsSection: document.getElementById('statsSection'),
    queryCount: document.getElementById('queryCount'),
    avgTime: document.getElementById('avgTime')
};

// ============================================
// App State
// ============================================
const AppState = {
    queryHistory: [],
    dailyQueries: 0,
    responseTimes: [],
    currentQuery: ''
};

// ============================================
// Initialize App
// ============================================
function init() {
    loadFromLocalStorage();
    setupEventListeners();
    updateStatsDisplay();
    animateInElements();
}

// ============================================
// Load saved data from localStorage
// ============================================
function loadFromLocalStorage() {
    try {
        const savedHistory = localStorage.getItem('h24_query_history');
        if (savedHistory) {
            AppState.queryHistory = JSON.parse(savedHistory);
        }
        
        const savedDate = localStorage.getItem('h24_last_date');
        const today = new Date().toDateString();
        
        if (savedDate === today) {
            const savedCount = localStorage.getItem('h24_daily_queries');
            AppState.dailyQueries = savedCount ? parseInt(savedCount) : 0;
        } else {
            AppState.dailyQueries = 0;
            localStorage.setItem('h24_last_date', today);
            localStorage.setItem('h24_daily_queries', '0');
        }
    } catch (e) {
        console.error('Failed to load from localStorage:', e);
    }
}

// ============================================
// Save to localStorage
// ============================================
function saveToLocalStorage() {
    try {
        localStorage.setItem('h24_query_history', JSON.stringify(AppState.queryHistory.slice(-20)));
        localStorage.setItem('h24_daily_queries', AppState.dailyQueries.toString());
    } catch (e) {
        console.error('Failed to save to localStorage:', e);
    }
}

// ============================================
// Update daily query count
// ============================================
function incrementDailyQueries() {
    AppState.dailyQueries++;
    localStorage.setItem('h24_daily_queries', AppState.dailyQueries.toString());
    updateStatsDisplay();
}

// ============================================
// Add response time tracking
// ============================================
function addResponseTime(timeMs) {
    AppState.responseTimes.push(timeMs);
    // Keep only last 10 response times
    if (AppState.responseTimes.length > 10) {
        AppState.responseTimes.shift();
    }
    updateStatsDisplay();
}

// ============================================
// Calculate average response time
// ============================================
function getAverageResponseTime() {
    if (AppState.responseTimes.length === 0) return 0;
    const sum = AppState.responseTimes.reduce((a, b) => a + b, 0);
    return Math.round(sum / AppState.responseTimes.length);
}

// ============================================
// Update stats display
// ============================================
function updateStatsDisplay() {
    if (DOM.queryCount) {
        DOM.queryCount.textContent = AppState.dailyQueries;
    }
    if (DOM.avgTime) {
        DOM.avgTime.textContent = getAverageResponseTime();
    }
    
    // Show stats section if there's data
    if (DOM.statsSection && (AppState.dailyQueries > 0 || AppState.responseTimes.length > 0)) {
        DOM.statsSection.style.display = 'block';
    }
}

// ============================================
// Setup all event listeners
// ============================================
function setupEventListeners() {
    // Submit button click
    if (DOM.submitBtn) {
        DOM.submitBtn.addEventListener('click', handleSubmit);
    }
    
    // Enter key press
    if (DOM.queryInput) {
        DOM.queryInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                handleSubmit();
            }
        });
        
        // Auto-resize? Not needed but add focus effect
        DOM.queryInput.addEventListener('focus', () => {
            DOM.queryInput.parentElement.style.transform = 'scale(1.01)';
        });
        
        DOM.queryInput.addEventListener('blur', () => {
            DOM.queryInput.parentElement.style.transform = 'scale(1)';
        });
    }
    
    // Copy button
    if (DOM.copyBtn) {
        DOM.copyBtn.addEventListener('click', copyResponseToClipboard);
    }
    
    // Clear history button
    if (DOM.clearHistoryBtn) {
        DOM.clearHistoryBtn.addEventListener('click', clearHistory);
    }
    
    // Example chips - event delegation
    const examplesGrid = document.getElementById('examplesGrid');
    if (examplesGrid) {
        examplesGrid.addEventListener('click', (e) => {
            const chip = e.target.closest('.example-chip');
            if (chip && chip.dataset.query) {
                DOM.queryInput.value = chip.dataset.query;
                handleSubmit();
            }
        });
    }
}

// ============================================
// Handle form submission
// ============================================
async function handleSubmit() {
    const query = DOM.queryInput.value.trim();
    
    if (!query) {
        showStatus('Please enter a question!', 'error');
        shakeElement(DOM.queryInput);
        return;
    }
    
    // Rate limiting check (client-side)
    if (AppState.dailyQueries >= 50) {
        showStatus('Daily limit reached (50 queries). Come back tomorrow!', 'error');
        return;
    }
    
    // Save current query
    AppState.currentQuery = query;
    
    // Hide previous result and show loading
    hideResult();
    showLoading(true);
    showStatus('');
    
    const startTime = performance.now();
    
    try {
        const response = await fetch('/getaians', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: JSON.stringify({ command: query }),
            signal: AbortSignal.timeout(30000) // 30 second timeout
        });
        
        const endTime = performance.now();
        const responseTime = Math.round(endTime - startTime);
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        const data = await response.json();
        
        if (data.ans) {
            displayResponse(data.ans);
            addToHistory(query, data.ans);
            incrementDailyQueries();
            addResponseTime(responseTime);
            showStatus(`✅ Response generated in ${responseTime}ms`, 'success');
            setTimeout(() => {
                if (DOM.statusMsg) DOM.statusMsg.style.display = 'none';
            }, 3000);
        } else {
            throw new Error('No response from AI');
        }
        
    } catch (error) {
        console.error('Error:', error);
        
        let errorMessage = 'Connection error. Please try again.';
        if (error.name === 'TimeoutError') {
            errorMessage = 'Request timeout. AI is taking too long. Please try again.';
        } else if (error.message.includes('429')) {
            errorMessage = 'Too many requests. Please wait a moment.';
        } else if (error.message.includes('500')) {
            errorMessage = 'Server error. Our team has been notified.';
        }
        
        showStatus(errorMessage, 'error');
        displayFallbackResponse(query);
        
    } finally {
        showLoading(false);
    }
}

// ============================================
// Display AI response with formatting
// ============================================
function displayResponse(text) {
    if (!DOM.aiResponse || !DOM.resultCard) return;
    
    let formattedText = text || 'No response received.';
    
    // Format code blocks
    formattedText = formattedText.replace(/```(\w*)\n([\s\S]*?)```/g, (match, lang, code) => {
        return `<pre><code class="language-${lang || 'text'}">${escapeHtml(code.trim())}</code></pre>`;
    });
    
    // Format inline code
    formattedText = formattedText.replace(/`([^`]+)`/g, '<code>$1</code>');
    
    // Format bullet points
    formattedText = formattedText.replace(/^[\*\-]\s(.+)$/gm, '• $1');
    
    // Format numbered lists
    formattedText = formattedText.replace(/^\d+\.\s(.+)$/gm, '<span class="list-num">$&</span>');
    
    // Convert line breaks to <br> tags
    formattedText = formattedText.replace(/\n/g, '<br>');
    
    // Highlight security keywords
    const keywords = ['SQL', 'XSS', 'CSRF', 'DDoS', 'injection', 'vulnerability', 'exploit', 'patch', 'firewall'];
    keywords.forEach(keyword => {
        const regex = new RegExp(`\\b(${keyword})\\b`, 'gi');
        formattedText = formattedText.replace(regex, '<span class="highlight-keyword">$1</span>');
    });
    
    DOM.aiResponse.innerHTML = formattedText;
    DOM.resultCard.style.display = 'block';
    
    // Animate result card
    DOM.resultCard.style.animation = 'fadeInUp 0.5s ease';
    setTimeout(() => {
        if (DOM.resultCard) DOM.resultCard.style.animation = '';
    }, 500);
}

// ============================================
// Display fallback response when AI fails
// ============================================
function displayFallbackResponse(query) {
    const fallbackResponses = {
        default: "I'm having trouble connecting to my AI brain. Please try again in a moment. Meanwhile, you can check our <a href='/help'>documentation</a>.",
        security: "For security-related queries, please check our <a href='/certificates'>certification guides</a> or try again later.",
        tool: "Our AI service is temporarily unavailable. You can still use our <a href='/base64_tool'>manual tools</a>."
    };
    
    let response = fallbackResponses.default;
    if (query.toLowerCase().includes('security') || query.toLowerCase().includes('hack')) {
        response = fallbackResponses.security;
    } else if (query.toLowerCase().includes('tool') || query.toLowerCase().includes('encode')) {
        response = fallbackResponses.tool;
    }
    
    displayResponse(`⚠️ **AI Service Temporarily Unavailable**\n\n${response}\n\nPlease try again in a few seconds.`);
}

// ============================================
// Add query to history
// ============================================
function addToHistory(query, response) {
    AppState.queryHistory.unshift({
        query: query.substring(0, 100),
        timestamp: new Date().toISOString(),
        responsePreview: response.substring(0, 100)
    });
    
    // Keep only last 20
    if (AppState.queryHistory.length > 20) {
        AppState.queryHistory.pop();
    }
    
    saveToLocalStorage();
}

// ============================================
// Clear history
// ============================================
function clearHistory() {
    if (confirm('Are you sure you want to clear your query history?')) {
        AppState.queryHistory = [];
        AppState.responseTimes = [];
        saveToLocalStorage();
        showStatus('History cleared!', 'success');
        setTimeout(() => {
            if (DOM.statusMsg) DOM.statusMsg.style.display = 'none';
        }, 2000);
        updateStatsDisplay();
    }
}

// ============================================
// Copy response to clipboard
// ============================================
async function copyResponseToClipboard() {
    const responseText = DOM.aiResponse.innerText || DOM.aiResponse.textContent;
    
    if (!responseText || responseText.trim() === '') {
        showStatus('Nothing to copy!', 'error');
        return;
    }
    
    try {
        await navigator.clipboard.writeText(responseText);
        showStatus('📋 Copied to clipboard!', 'success');
        
        // Change copy button text temporarily
        const originalText = DOM.copyBtn.innerHTML;
        DOM.copyBtn.innerHTML = '✅ COPIED!';
        setTimeout(() => {
            DOM.copyBtn.innerHTML = originalText;
        }, 2000);
        
    } catch (err) {
        console.error('Failed to copy:', err);
        showStatus('Failed to copy. Manual copy required.', 'error');
    }
}

// ============================================
// UI Helper Functions
// ============================================
function showLoading(show) {
    if (DOM.loading) {
        DOM.loading.classList.toggle('active', show);
    }
    if (DOM.submitBtn) {
        DOM.submitBtn.disabled = show;
        if (show) {
            DOM.submitBtn.style.opacity = '0.7';
        } else {
            DOM.submitBtn.style.opacity = '1';
        }
    }
}

function showStatus(message, type = '') {
    if (!DOM.statusMsg) return;
    
    DOM.statusMsg.textContent = message;
    DOM.statusMsg.className = 'status-message';
    if (type) {
        DOM.statusMsg.classList.add(type);
        DOM.statusMsg.style.display = 'block';
        
        if (type !== 'error') {
            setTimeout(() => {
                if (DOM.statusMsg) {
                    DOM.statusMsg.style.opacity = '0';
                    setTimeout(() => {
                        if (DOM.statusMsg) DOM.statusMsg.style.display = 'none';
                        if (DOM.statusMsg) DOM.statusMsg.style.opacity = '1';
                    }, 500);
                }
            }, 4000);
        }
    } else {
        DOM.statusMsg.style.display = 'none';
    }
}

function hideResult() {
    if (DOM.resultCard) {
        DOM.resultCard.style.display = 'none';
    }
    if (DOM.aiResponse) {
        DOM.aiResponse.innerHTML = '';
    }
}

function shakeElement(element) {
    if (!element) return;
    element.style.transform = 'translateX(0)';
    element.style.animation = 'shake 0.3s ease-in-out';
    setTimeout(() => {
        element.style.animation = '';
    }, 300);
}

function animateInElements() {
    const elements = document.querySelectorAll('.input-card, .help-header, .examples-section');
    elements.forEach((el, index) => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        setTimeout(() => {
            el.style.transition = 'all 0.5s ease';
            el.style.opacity = '1';
            el.style.transform = 'translateY(0)';
        }, index * 100);
    });
}

// ============================================
// Escape HTML to prevent XSS
// ============================================
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// ============================================
// Add CSS animations dynamically
// ============================================
function addAnimations() {
    const style = document.createElement('style');
    style.textContent = `
        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            25% { transform: translateX(-5px); }
            75% { transform: translateX(5px); }
        }
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        .highlight-keyword {
            color: #00ff88;
            font-weight: bold;
            background: rgba(0, 255, 136, 0.1);
            padding: 0 2px;
            border-radius: 3px;
        }
        .list-num {
            color: #00b4ff;
        }
        code {
            background: rgba(0, 0, 0, 0.5);
            padding: 2px 6px;
            border-radius: 4px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.85em;
        }
        pre {
            background: #0a0a0f;
            padding: 12px;
            border-radius: 8px;
            overflow-x: auto;
            border-left: 3px solid #00ff88;
        }
        pre code {
            background: none;
            padding: 0;
        }
    `;
    document.head.appendChild(style);
}

// ============================================
// Start the app
// ============================================
document.addEventListener('DOMContentLoaded', () => {
    init();
    addAnimations();
    
    // Focus on input on page load
    if (DOM.queryInput) {
        DOM.queryInput.focus();
    }
});