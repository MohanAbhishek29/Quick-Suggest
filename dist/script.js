const searchBar = document.getElementById('search-bar');
const suggestionsBox = document.getElementById('suggestions-box');

// Debounce function to limit API calls
function debounce(func, wait) {
    let timeout;
    return function (...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, args), wait);
    };
}

// Function to fetch suggestions from C++ backend
async function fetchSuggestions(query) {
    if (!query) {
        suggestionsBox.innerHTML = '';
        suggestionsBox.classList.add('hidden');
        return;
    }

    try {
        // Try C++ Server first
        const response = await fetch(`http://localhost:8080/search?q=${query}`);
        if (!response.ok) throw new Error('C++ Server not reachable');
        
        const data = await response.json();
        renderSuggestions(data, query);
    } catch (error) {
        console.warn('Backend offline, using Static Engine.');
        
        // Fallback to JS-powered Trie Engine
        if (typeof trieEngine !== 'undefined') {
            await trieEngine.init();
            const results = trieEngine.trie.getSuggestions(query);
            renderSuggestions(results, query);
        }
    }
}

// Function to handle search (Navigate to definition page)
function performSearch(word) {
    if (!word) return;

    saveToHistory(word); // Save to history before navigating

    // Redirect to the definition page with the query param
    window.location.href = `definition.html?q=${encodeURIComponent(word)}`;
}

// --- History Management (LocalStorage) ---
function saveToHistory(term) {
    let history = JSON.parse(localStorage.getItem('qs_history')) || [];
    // Remove if exists to push to top
    history = history.filter(item => item.toLowerCase() !== term.toLowerCase());
    // Add to beginning
    history.unshift(term);
    // Keep max 5
    if (history.length > 5) history.pop();

    localStorage.setItem('qs_history', JSON.stringify(history));
}

function loadHistory() {
    return JSON.parse(localStorage.getItem('qs_history')) || [];
}

function renderHistory() {
    const history = loadHistory();
    if (history.length === 0) return;

    const html = `
        <div class="suggestions-label">Recent Searches</div>
        ${history.map((word, index) =>
        `<div class="suggestion-item history-item" data-index="${index}" data-word="${word}">${word}</div>`
    ).join('')}
    `;

    suggestionsBox.innerHTML = html;
    suggestionsBox.classList.remove('hidden');

    // Add click listeners
    document.querySelectorAll('.suggestion-item').forEach(item => {
        item.addEventListener('click', (e) => {
            const word = e.currentTarget.dataset.word;
            performSearch(word);
        });
    });
}


// Function to fetch and display definition (Modified for Multi-page approach)
// Note: This is now mainly skipped in favor of navigation, but we keep the fetchSuggestions logic.

// --- Keyboard Navigation Variables ---
let currentFocus = -1;

// --- Function to render suggestions (Updated) ---
function renderSuggestions(suggestions, query) {
    if (suggestions.length === 0) {
        suggestionsBox.classList.add('hidden');
        return;
    }

    currentFocus = -1; // Reset focus on new search

    const html = suggestions.map((word, index) => {
        // Highlight logic
        const regex = new RegExp(`^(${query})`, 'i');
        const highlightedWord = word.replace(regex, `<span class="highlight">$1</span>`);
        return `<div class="suggestion-item" data-index="${index}" data-word="${word}">${highlightedWord}</div>`;
    }).join('');

    suggestionsBox.innerHTML = html;
    suggestionsBox.classList.remove('hidden');

    // Add click listeners
    document.querySelectorAll('.suggestion-item').forEach(item => {
        item.addEventListener('click', (e) => {
            const word = e.currentTarget.dataset.word;
            performSearch(word);
        });
    });
}

// --- Keyboard Navigation Logic ---
searchBar.addEventListener('keydown', (e) => {
    const items = document.querySelectorAll('.suggestion-item');
    if (e.key === 'ArrowDown') {
        currentFocus++;
        addActive(items);
        e.preventDefault(); // Stop cursor moving
    } else if (e.key === 'ArrowUp') {
        currentFocus--;
        addActive(items);
        e.preventDefault();
    } else if (e.key === 'Enter') {
        e.preventDefault();
        if (currentFocus > -1) {
            // Simulate click on active item
            if (items) items[currentFocus].click();
        } else {
            // Standard search
            performSearch(searchBar.value.trim());
        }
    }
});

function addActive(items) {
    if (!items) return false;
    removeActive(items);
    if (currentFocus >= items.length) currentFocus = 0;
    if (currentFocus < 0) currentFocus = items.length - 1;

    // Add class active
    items[currentFocus].classList.add('active');

    // Auto-fill input (optional cool feature)
    // searchBar.value = items[currentFocus].dataset.word; 

    // Scroll into view if needed
    items[currentFocus].scrollIntoView({ block: 'nearest' });
}

function removeActive(items) {
    for (let i = 0; i < items.length; i++) {
        items[i].classList.remove('active');
    }
}

// --- Voice Search Logic (Fast & Auto-Search) ---
const micIcon = document.querySelector('.mic-icon');
if (micIcon) {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
        const recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.lang = 'en-US';
        recognition.interimResults = true;

        micIcon.addEventListener('click', () => {
            if (micIcon.classList.contains('listening')) {
                recognition.stop();
            } else {
                recognition.start();
                micIcon.classList.add('listening');
                searchBar.placeholder = "Listening...";
                searchBar.value = "";
            }
        });

        recognition.onresult = (event) => {
            let interim = '';
            for (let i = event.resultIndex; i < event.results.length; ++i) {
                if (event.results[i].isFinal) {
                    const final = event.results[i][0].transcript.trim();
                    searchBar.value = final;
                    setTimeout(() => performSearch(final), 500);
                } else {
                    interim += event.results[i][0].transcript;
                    searchBar.value = interim;
                }
            }
        };

        recognition.onend = () => {
            micIcon.classList.remove('listening');
            if (!searchBar.value) searchBar.placeholder = "Search (e.g., 'algorithm')...";
        };

        recognition.onerror = () => {
            micIcon.classList.remove('listening');
            searchBar.placeholder = "Error! Try again.";
        };
    } else {
        micIcon.style.display = 'none';
    }
}


// Event Listener for Input
searchBar.addEventListener('input', debounce((e) => {
    const query = e.target.value.trim();
    if (query.length === 0) {
        renderHistory();
    } else {
        fetchSuggestions(query);
    }
}, 200));

// Show History on Focus
searchBar.addEventListener('focus', () => {
    if (searchBar.value.trim().length === 0) {
        renderHistory();
    }
});


// Hide suggestions when clicking outside
document.addEventListener('click', (e) => {
    if (!searchBar.contains(e.target) && !suggestionsBox.contains(e.target) && !e.target.closest('.mic-icon')) {
        suggestionsBox.classList.add('hidden');
    }
});
