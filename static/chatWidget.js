(function () {
  // Create the chat widget HTML structure
  const widgetHTML = `
    <div class="chat-widget">
      <div class="chat-header" id="chatHeader">
        Nevermore Academy
        <select id="languageSelect">
          <option value="en-US" selected>English</option>
          <option value="es-ES">Spanish</option>
          <option value="fr-FR">French</option>
          <option value="de-DE">German</option>
          <option value="ru-RU">Russian</option>
        </select>
      </div>
      <div class="chat-body" id="chatBody">
        <p>Agent online. What brings you here?</p>
      </div>
      <div class="chat-footer">
        <input type="text" id="chatInput" placeholder="Type a message or 'clear history'... " />
        <button id="voiceButton" aria-label="Start voice input">
          <img src="/static/icons/mic.png" />
        </button>
      </div>
    </div>
    <div class="chat-icon" id="chatIcon">
      <img src="/static/icons/wendy.png" alt="Chat Icon" />
    </div>
  `;

  // Inject chat widget into the body of the page
  const body = document.body;
  const widgetContainer = document.createElement("div");
  widgetContainer.innerHTML = widgetHTML;
  body.appendChild(widgetContainer);

  // Add chat widget styles dynamically
  const style = document.createElement("style");
  style.innerHTML = `
    body {
      font-family: Arial, sans-serif;
      margin: 0;
      padding: 0;
      background: #f4f4f4;
    }
    .chat-widget {
      position: fixed;
      top: 10px;
      left: 10px;
      width: 300px;
      height: 400px;
      background: white;
      border-radius: 8px;
      box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
      z-index: 1000;
      display: none;
      flex-direction: column;
      min-width: 300px;  
      min-height: 400px;
      max-width: 1200px;
      max-height: 700px;
      resize: both;
      overflow: auto;
    }
    .chat-header {
      background: #007bff;
      color: white;
      padding: 10px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      cursor: grab;
    }
    .chat-header select {
      background: white;
      color: black;
      border: none;
      border-radius: 4px;
      padding: 5px;
      font-size: 14px;
      outline: none;
    }
    .chat-body {
      height: calc(100% - 100px);
      padding: 10px;
      overflow-y: auto;
    }    
    .chat-footer {
      display: flex;
      align-items: center;
      padding: 10px;
      border-top: 1px solid #ddd;
    }
    .chat-footer input {
      border: none;
      flex: 1;
      padding: 5px;
      font-size: 16px;
      outline: none;
    }
    .chat-footer button {
      background: none;
      border: none;
      cursor: pointer;
      padding: 5px;
    }
    .chat-footer button.recording {
      color: red;
    }
    .chat-footer button:hover {
      color: #007BFF;
    }
    .chat-icon {
      position: fixed;
      bottom: 20px;
      right: 20px;
      width: 100px;
      height: auto;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
    }
    .chat-icon img {
      width: 100%;
      height: 100%;
      border-radius: 50%;
    }

  .chat-message {
      margin: 5px 0;
      padding: 10px;
      border-radius: 5px;
  }

  .bot-message {
      background: #e9ecef;
      align-self: flex-start;
      color: black;
  }

  .corner-image {
    float: left; /* Positions the image to the left */
    margin-right: 15px; /* Adds spacing between image and text */
    width: 40px; /* Adjust the size of the image */
    height: auto; /* Maintains aspect ratio */
  }
  .clearfix::after {
    content: "";
    clear: both;
    display: table;
  }
  `;
  document.head.appendChild(style);

  // Get references to DOM elements
  const chatWidget = document.querySelector(".chat-widget");
  const chatHeader = document.querySelector("#chatHeader");
  const chatBody = document.querySelector("#chatBody");
  const chatInput = document.querySelector("#chatInput");
  const voiceButton = document.querySelector("#voiceButton");
  const chatIcon = document.querySelector("#chatIcon");
  const languageSelect = document.querySelector("#languageSelect");

  let offsetX = 0;
  let offsetY = 0;
  let isDragging = false;

  // Toggle chat widget visibility when clicking the chat icon
  chatIcon.addEventListener("click", () => {
    if (chatWidget.style.display === "none" || chatWidget.style.display === "") {
      chatWidget.style.display = "flex"; // Show the chat widget
    } else {
      chatWidget.style.display = "none"; // Hide the chat widget
    }
  });

  // Update language for speech recognition
  languageSelect.addEventListener("change", () => {
    if (recognition) {
      recognition.lang = languageSelect.value;
    }
  });

  // Dragging functionality for the chat widget
  chatHeader.addEventListener("mousedown", (e) => {
    if (e.target.tagName === "SELECT") return;

    isDragging = true;
    offsetX = e.clientX - chatWidget.offsetLeft;
    offsetY = e.clientY - chatWidget.offsetTop;
    chatHeader.style.cursor = "grabbing";
  });

  document.addEventListener("mousemove", (e) => {
    if (isDragging) {
      let newLeft = e.clientX - offsetX;
      let newTop = e.clientY - offsetY;

      newLeft = Math.max(0, newLeft);
      newTop = Math.max(0, newTop);

      chatWidget.style.left = `${newLeft}px`;
      chatWidget.style.top = `${newTop}px`;
    }
  });

  document.addEventListener("mouseup", () => {
    isDragging = false;
    chatHeader.style.cursor = "grab";
  });

  // Add message to chat body
  function addMessage(message, role = "user") {
    if (role == "user") {
    const messageElement = document.createElement("p");
    messageElement.textContent = message;
    messageElement.style.color = role === "user" ? "blue" : "black";
    chatBody.appendChild(messageElement);
    chatBody.scrollTop = chatBody.scrollHeight;
    }
    if (role == "bot") {
      const messageElement = document.createElement("div");
      messageElement.className = 'chat-message bot-message';
      messageElement.innerHTML = message; // Use innerHTML instead of textContent
      chatBody.appendChild(messageElement);
      chatBody.scrollTop = chatBody.scrollHeight;
    }
  }
  // Send message to the backend and get a response
  async function sendMessage() {
  const message = chatInput.value.trim();
  if (!message) return;
  
  // Print user's message on the body of chat
  addMessage(message, "user");
  chatInput.value = "";

  // Add "thinking" indicator
  const thinkingIndicator = document.createElement("div");
  thinkingIndicator.id = "thinkingIndicator";
  thinkingIndicator.innerHTML = '<img src="/static/icons/thinking.gif" style="width: 50px; height: 50px;">';
  
  chatBody.appendChild(thinkingIndicator);
  chatBody.scrollTop = chatBody.scrollHeight;

    
    //      * * * BACKEND CALL * * *
    // Insert code to interact with backend
    //
    let backend_response = 'bot says hi!'; // Declare backend_response variable
    //this is where we will call the backend
    const baseUrl = window.location.origin;
  
  
    // call backend *******************
    try {
    const response = await fetch(`${baseUrl}/respond`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message })
    });

    if (!response.ok) {
        backend_response = `HTTP error! status: ${response.status}`;
    } else {
        const data = await response.text(); // Get response as HTML
        backend_response = data;
    }
} catch (error) {
    console.error('Error fetching response:', error);
    backend_response = `Can not reach backend ${baseUrl} error: ${error.message}`;
}
    // ********************************
    // end of * * * BACKEDND CALL * * *  
    // print backend response on chat window
    
    // Remove the thinking indicator after the delay
    thinkingIndicator.remove();
    addMessage(backend_response, "bot");
  
  
}

  chatInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter" && chatInput.value.trim() !== "") {
      sendMessage();
    }
  });

  let recognition;
  if ("webkitSpeechRecognition" in window || "SpeechRecognition" in window) {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    recognition = new SpeechRecognition();
    recognition.lang = "en-US";
    recognition.interimResults = true;
    recognition.continuous = true;

    voiceButton.addEventListener("click", () => {
      if (voiceButton.classList.contains("recording")) {
        recognition.stop();
      } else {
        recognition.start();
      }
    });

    recognition.addEventListener("start", () => {
      voiceButton.innerHTML = '<img src="/static/icons/mic-record.png" />';
      voiceButton.classList.add("recording");
    });

    recognition.addEventListener("end", () => {
      voiceButton.innerHTML = '<img src="/static/icons/mic.png" />';
      voiceButton.classList.remove("recording");
    });

    recognition.addEventListener("result", (event) => {
      chatInput.value = event.results[0][0].transcript;
    });
  } else {
    voiceButton.disabled = true;
    alert("Speech Recognition is not supported in your browser.");
  }
})();
