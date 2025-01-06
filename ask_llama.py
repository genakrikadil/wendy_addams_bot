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
from hallucination import is_hallucination
from model_change import analyze_and_change_model
from book_of_psalms import psalms
from render_html import render_html
import re
import globals #type:ignore  here we put all global constants

#clean ollama nonsence 

def clean_ollama_response(response):
    # Set of words or phrases to remove from ollama response
    words_to_remove = {"User:", "System:", "Assistant:"}

    # Iterate through the set of words and remove them from the response
    for word in words_to_remove:
        # Using regular expression to remove each word or phrase from the text
        response = re.sub(rf"\b{re.escape(word)}\b", "", response, flags=re.IGNORECASE)
    return response.strip()

class LlamaChat:
    def __init__(self, history_limit=10):
        self.url = globals.URL  # Use the constant for the URL
        self.headers = {"Content-Type": "application/json"}
        self.history = []  # Store conversation history
        self.history_limit = history_limit  # Set a maximum history limit

    def clear_history(self):
        """Clears the conversation history."""
        self.history = []

    def ask_llama(self, prompt):
        #######################################
        # Check if it is command for backend
        #######################################

        # "psalm <psalm number>" command
        reply_text, reply_bool = psalms(prompt)
        if reply_bool:
            # Add psalm to the history
            self.history.append({"role": "user", "content": reply_text}) 
            return reply_text
                
        # "clear history" command
        if prompt.lower() == "clear history":
            self.clear_history()
            return "Let's start new conversation."
        
        # "version" command
        if prompt.lower() == "version":
            return globals.VERSION+" Model:"+globals.MODEL
        
        # "model:" command
        prompt,changed=analyze_and_change_model(prompt)
        if changed:
            return prompt
        
        # "?" command
        if prompt.lower() == "?":
            return """ <h1>Available Commands</h1><br>
            <b>psalm psalm_number</b>: Displays a Psalm from the Book of Psalms.<br>
            <b>clear history</b>: Clears the chat history.<br>
            <b>version</b>: Shows the code version and the name of the model in use.<br>
            <b>model:name_of_the_model</b>: Switches to a specified AI model or lists available models.<br>
            <br>
            <b>Note:</b> The language selector dropdown affects only the Speech-to-Text functions. You can enter 
            your question or statement in any supported language. Input will be recognized automatically, and 
            the model will always respond in English."""
        #######################################
        # End of command processing
        #######################################

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
            "model": globals.MODEL,  # Use the constant for the model
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
            #print (data)
            response = requests.post(self.url, headers=self.headers, data=json.dumps(data))
            if response.status_code == 200:
                # Get the model's response and add it to the history
                model_response = response.json().get("response", "No response received from the model.")
                #clean response from Rubbish words
                model_response = clean_ollama_response(model_response)
                #check if the model hallucinated with "Prohibited conversations"
                #if so- remove 2 last records from the history- the last user request and previous
                #ollama response, otherwise add the message to the history This will insure
                #the history is not poisoned with "banned" theme and we will be able to continue
                #our dialogue
                if is_hallucination(model_response):
                    model_response="I do not want to talk about this."
                    if len(self.history) > 2:
                        self.history = self.history[:-2]
                    else:
                        self.history=[]
                else:
                    self.history.append({"role": "assistant", "content": model_response})

                # Maintain the history length within the limit
                if len(self.history) > self.history_limit:
                    self.history.pop(0)

                return model_response
            else:
                return f"Something is not right with Ollama Server. Here is what she sad:<br><br>\n {response.status_code}: {response.text}"
        except Exception as e:
            return f"<h1>Is Ollama server running?</h1> <br><br> Here is Error I received:<br><br> \n {str(e)}"

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
