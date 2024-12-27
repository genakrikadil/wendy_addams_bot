
  
    W   W     EEEEE    N   N    DDDD    Y   Y
    W   W     E        NN  N    D   D    Y Y
    W W W     EEEE     N N N    D   D     Y
    WW WW     E        N  NN    D   D     Y
    W   W     EEEEE    N   N    DDDD      Y

# Dedication

This project is dedicated to my lovely daughter, Katherine, whose enthusiasm for Wendy Addams has inspired this creation. Katherine, your love for Wendy’s unique charm and wit has brought this fun idea to life. I hope this chatbot brings you as much joy as Wendy Addams has brought to your heart.

With love,
Dad


# Project Overview

This project provides a chatbot interface for the Ollama server, simulating a conversation with Wendy Addams, a member of the Addams Family.

The chatbot supports "context-aware" conversations and allows voice input. 

A dropdown menu lets users select the language for voice input. Without the Voice Input Language selector, the voice-to-text feature assumes the input language is English and may not perform the conversion properly for another languages.

Regardless of how the user enters text, whether by typing or via voice-to-text, it is automatically translated into English if needed, and then processed by the Ollama model. The input language is detected automatically, and translation is performed on an as-needed basis.

Users do not need to select a language from the dropdown menu when entering text via the keyboard. The language selector is used exclusively for voice-to-text input.

Reloading the web page does not clear the chat "context". To clear context, you need to enter "clear history" in the chat input.

Before pressing the Mic button, make sure to select the Voice Input Language. If the Mic button is pressed, stop it, change the language, and then press the Mic again.


# Requirements:

Python 3.9.21 (This is what I used, did not test with other versions)

Docker or Python virtual environment (venv)

Ollama server with llama3.2 image (or whatever image you like)

# Project Structure:
    .
    ├── ollama_mod/
    │   ├── README.md
    │   └── wednesday
    ├── static/
    │   ├── pics/
    │   │   ├── wendy_small.png
    │   │   └── wendy.jpg
    │   ├── README.md   
    │   ├── chat_interface.htm
    │   ├── script.js
    │   └── styles.css
    ├── app.py
    ├── ask_llama.py
    ├── hallucination.py
    ├── render_html.py
    ├── translate.py
    ├── requirements.txt
    ├── Dockerfile
    ├── docker-compose.yml
    └── README.md

# How to Run:

1) Set Up Ms. Addams model:

Navigate to the ollama_mod directory and follow the instructions in the README.md to set up Wendy.

2) Start Ollama:

Ensure that the Ollama server is running.
'ollama - list' should show you that 'wednesday' model is available

3) Configure Ollama URL in ask_llama.py:
If python script runs on the same server with ollama and you use venv, no changes are needed.

If it is another server, and/or you use Docker, you need to adjust URL
Change:

    URL = "http://127.0.0.1:11434/api/generate"
    to match the server IP/hostname, where Ollama is running. 

4) Build and Run with Docker:

Make sure you're in the project root directory (where the Dockerfile is located). Then, execute the following commands to build and run the Docker container:

    #Build the Docker Image:
    docker build -t wendy_bot .

    #Verify the Image:
    docker images

    #Run the Docker Container (Detached Mode):
    docker run -d -p 5555:5555 wendy_bot

This will start the container, and you can access the chatbot via:

    http://your_server_ip:5555

You can stop the container at any time.

5) Stopping and Managing Docker Containers:

To stop the container and/or perform cleanup, use the following commands:

#Verify Running Containers:

    docker ps | grep wendy_bot

#Stop the Container:

        docker stop <container_id>

#General Docker Cleanup Commands:
    
#Remove a Stopped Container:

        docker ps -a | grep wendy
        docker stop <container_id>
        docker rm <container_id>

#Remove an Image:

        docker images | grep wendy
        docker rmi <image_name_or_id>

#Force Removal of an Image:

        docker rmi -f <image_id>

#Optional: Clean Up Unused Images:

        docker image prune

#Updates:

    Dec 27 2024: 
    -Fixed Wednesday model behaviour
    -Added a module to manage and minimize model hallucinations, ensuring they do
    not "pollute" the chat history. The issue occurred when the model responded 
    with content related to "illegal activities." That response was saved in the 
    chat history, causing the model to react in the next step with statements like,
    "I cannot provide information or guidance." A special mechanism has now been 
    implemented to prevent this behavior.

