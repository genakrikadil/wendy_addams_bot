#
# Querry Lama server and remembers converstaion 
# history to follow context.
# 'clear history' will start new converstion
#
# you can NOT change tokens and temperature dynamically
# https://genai.stackexchange.com/questions/699/how-to-set-ollama-temperature-from-command-line
#
# use modefile instead:
# https://github.com/ollama/ollama/blob/main/docs/modelfile.md
# Model Params
#       max_tokens=80,           # Limit to short answers
#       temperature=0.8,         # Balance creativity and precision
#       top_k=150,               # Broader token pool for intelligent phrasing
#       top_p=0.85,              # Increase diversity slightly
#       frequency_penalty=0.3,   # Avoid repetition
#       stop=[".", "?", "!"],    # Stop at logical sentence boundaries
#  
#  Copyright 2024 Dmitriy Ivanov
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import requests  # Add this import statement
import json

#URL = "http://192.168.2.112:11434/api/generate"
URL = "http://127.0.0.1:11434/api/generate"
#URL ="http://10.20.187.188:11434/api/generate"

#see folder "ollama_mod"
MODEL = "wednesday"

class LlamaChat:
    def __init__(self, history_limit=10):
        self.url = URL  # Use the constant for the URL
        self.headers = {"Content-Type": "application/json"}
        self.history = []  # Store conversation history
        self.history_limit = history_limit  # Set a maximum history limit

    def clear_history(self):
        """Clears the conversation history."""
        self.history = []

    def ask_llama(self, prompt):
        # Check for a manual clear command
        if prompt.lower() == "clear history":
            self.clear_history()
            return "Let's start new conversation."

        # Add the user's prompt to the history
        self.history.append({"role": "user", "content": prompt})

        # Maintain the history length within the limit
        if len(self.history) > self.history_limit:
            self.history.pop(0)

        # Format the full conversation for the model
        full_prompt = "\n".join(
            f"{msg['role'].capitalize()}: {msg['content']}" for msg in self.history
        )

        # Data payload for the API
        data = {
            "model": MODEL,  # Use the constant for the model
            "prompt": full_prompt,
            "stream": False,
            "max_tokens":80,           # Limit to short answers
            "temperature":0.8,         # Balance creativity and precision
            "top_k":150,               # Broader token pool for intelligent phrasing
            "top_p":0.85,              # Increase diversity slightly
            "frequency_penalty":0.3,   # Avoid repetition
            "stop":[".", "?", "!"]    # Stop at logical sentence boundaries
        }

        try:
            response = requests.post(self.url, headers=self.headers, data=json.dumps(data))
            if response.status_code == 200:
                # Get the model's response and add it to the history
                model_response = response.json().get("response", "No response received from the model.")
                self.history.append({"role": "assistant", "content": model_response})

                # Maintain the history length within the limit
                if len(self.history) > self.history_limit:
                    self.history.pop(0)

                return model_response
            else:
                return f"Something is not right with Ollama Server. Here is what she sad:<br><br>\n {response.status_code}: {response.text}"
        except Exception as e:
            return f"Is Ollama server running? Here is Error I received:<br><br> \n {str(e)}"

if __name__ == '__main__':
    chat = LlamaChat()
    print("Welcome to Llama Chat!")
    while True:
        user_input = input("You (type 'exit' to quit): ").strip()
        if user_input.lower() == "exit":
            print("Exiting Llama Chat. Goodbye!")
            break
        response = chat.ask_llama(user_input)
        print(f"Llama: {response}")
