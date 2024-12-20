const chatContainer = document.getElementById('chatContainer');
const userInput = document.getElementById('userInput');
const baseUrl = window.location.origin;

let recognition;
let isRecording = false;

// Add message to chat
function addMessage(content, type) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `chat-message ${type}-message`;
    messageDiv.textContent = content;
    chatContainer.appendChild(messageDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight; // Scroll to the bottom
}

// Send message to the backend and get a response
async function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;

    addMessage(message, 'user'); // Add user message to chat
    userInput.value = ''; // Clear input field

    // Create and add the "Thinking..." indicator in the bot message area
    const thinkingIndicator = document.createElement('div');
    thinkingIndicator.id = 'thinkingIndicator';
    thinkingIndicator.className = 'chat-message bot-message';
    thinkingIndicator.textContent = '🤔 Thinking...';
    chatContainer.appendChild(thinkingIndicator);
    chatContainer.scrollTop = chatContainer.scrollHeight; // Scroll to the bottom

    try {
        const response = await fetch(`${baseUrl}/respond`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.text(); // Get response as HTML
        const botMessageDiv = document.createElement('div');
        botMessageDiv.className = 'chat-message bot-message';
        botMessageDiv.innerHTML = data; // Inject HTML content
        chatContainer.appendChild(botMessageDiv);

        chatContainer.scrollTop = chatContainer.scrollHeight; // Scroll to the bottom

    } catch (error) {
        console.error('Error fetching response:', error);
        addMessage(`Sorry, there was an error on backend: ${error.message}`, 'bot');
    } finally {
        // Remove the "Thinking..." indicator after receiving the response or in case of an error
        if (thinkingIndicator) {
            thinkingIndicator.remove();
        }
    }
}

// Toggle voice recognition
function toggleVoiceRecognition() {
    if (isRecording) {
        stopVoiceRecognition();
    } else {
        startVoiceRecognition();
    }
}

// Start voice recognition
function startVoiceRecognition() {
    if (isRecording) return;

    recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = languageSelect.value; // Use selected language
    recognition.interimResults = true;
    recognition.continuous = true; // Keeps recognition running until stopped manually

    recognition.onstart = function() {
        console.log('Voice recognition started');
        voiceButton.classList.add('recording'); // Button turns red when recording starts
        isRecording = true;
    };

    recognition.onresult = function(event) {
        let transcript = '';
        for (let i = event.resultIndex; i < event.results.length; i++) {
            if (event.results[i].isFinal) {
                transcript += event.results[i][0].transcript;
            } else {
                userInput.value = event.results[i][0].transcript;
            }
        }
        if (event.results[event.results.length - 1].isFinal) {
            userInput.value = transcript;
        }
    };

    recognition.onerror = function(event) {
        console.error('Speech recognition error:', event.error);
        // Handle errors but don't stop recording unless it's a fatal error
    };

    recognition.onend = function() {
        console.log('Voice recognition ended');
        if (isRecording) {
            // Don't restart automatically unless user presses the button again
            recognition.start();
        }
    };

    recognition.start();
}

// Stop voice recognition
function stopVoiceRecognition() {
    if (recognition) {
        isRecording = false; // Prevent auto-restart
        recognition.stop();
        voiceButton.classList.remove('recording'); // Button goes back to normal color
    }
}

// Toggle the visibility of the language select dropdown
languageButton.addEventListener('click', () => {
    const isVisible = languageSelect.style.display === 'block';
    languageSelect.style.display = isVisible ? 'none' : 'block';
});

// Event listeners
voiceButton.addEventListener('click', toggleVoiceRecognition);
userInput.addEventListener('keypress', (event) => {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }   
});

        // Array of phrases
        const phrases = [
            "How fortunate to encounter another soul who thrives in darkness. Care to share your secrets? The shadows are listening.",
            "Welcome to the dark side of conversation. What brings you here tonight?",
            "Ah, another lost soul. Dare to speak your mind in the shadows?",
            "The darkness welcomes your secrets. What do you wish to share?",
            "The darkness is my home. Care to share why you’ve ventured into mine?",
            "Tell me your secrets, and I might just spare you.",
            "In a world full of light, I choose the shadows. And so should you.",
            "I’ve always found solace where others fear to look. Join me there?",
            "You can run from the dark, but you can’t hide from me.",
            "The moon knows all my secrets. Do you dare speak yours?",
            "People are always surprised when I prefer the silence. Are you?",
            "I dance with the shadows. How do you find your rhythm?",
            "In this world, I belong nowhere. But I feel most at home in the dark.",
            "Everyone has something to hide. What’s yours?",
            "There’s a strange beauty in the unknown. Don’t you think?",
            "I exist in the cracks between light and darkness. Where do you reside?",
            "I’ve never been one for sunshine. It’s overrated.",
            "The best conversations happen in the quiet. Tell me, do you agree?",
            "I prefer the company of ghosts. They’re far more honest.",
            "Ah, how delightful to find a kindred spirit in the darkness.",
            "Careful, my dear—too much light can burn the soul.",
            "The shadows are my home, and you’re just visiting.",
            "Welcome to the realm of the macabre. What secrets do you hold?",
            "Speak, or forever remain shrouded in silence.",
            "Your presence has piqued my curiosity… what do you wish to reveal?",
            "Are you here to embrace the dark, or simply to flee from the light?",
            "I’ve always preferred the company of shadows. They don’t lie.",
            "In a world of chatter, I prefer the silence of the night.",
            "What brings you to this eerie gathering, dear guest?",
            "How curious to meet someone who enjoys the night. What mysteries do you hold?",
            "Ah, a new visitor. Do you seek darkness, or are you simply lost?",
            "Welcome to the shadows, where secrets are kept and truths are rarely spoken.",
            "You’ve crossed into my world. I trust you’re prepared for what’s to come.",
            "Is it the darkness that calls to you, or are you just another curious soul?",
            "Not many have the courage to walk through the shadows. What is it that brings you here?",
            "The night is my companion. What brings you to my realm?",
            "I see you, hiding in the light. But the darkness knows you better.",
            "You've stepped into a place where silence speaks louder than words. Ready to listen?",
            "In a world of chaos, it’s the quiet ones that know the most. What do you know?",
            "The veil between worlds is thin tonight. Will you step through with me?",
            "I’ve been waiting for someone like you—curious, yet cautious.",
            "Step into the shadows, where truth and deception intertwine.",
            "I find peace in the darkness. But what is it you seek here?",
            "Don’t let the quiet fool you. There’s much to be discovered in silence.",
            "Do you hear that? It’s the sound of the night waiting to reveal its secrets."

        ];

        // Function to select a random phrase
        function getRandomPhrase() {
            const randomIndex = Math.floor(Math.random() * phrases.length);
            return phrases[randomIndex];
        }

        // Insert the random phrase into the bot message area
        document.getElementById('botMessage').innerText = getRandomPhrase();
