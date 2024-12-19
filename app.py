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


# We run flask server on localhost:5555
# get request from the web page, check if
# request came in-English we print it back
# and translate into English and print it back otherwise
#
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from translate import  gtranslate, gtranslate_lang_detect
from render_html import render_html
from ask_llama import LlamaChat
#just for debug purpose simulate delays
import time

app = Flask(__name__, static_folder='static')
CORS(app)  # Allow cross-origin requests if needed
#initiate llamachat to store context
chat = LlamaChat()

# Route for the bot logic
@app.route('/respond', methods=['POST'])
def respond():
    user_input = request.json.get('message', '')
    try:
       
        ###### <Placeholder for return text back to bot>#####
        #debug - we just print back what user said
        #bot_response = "you said: "+user_input
            
        ### here we check if user said something
        ### in the language other that English
        ###  we translate it into english and print back
        ###  otherwise we print whatever was entered

        language=gtranslate_lang_detect(user_input)
        if 'en' in language.lower():
            response=user_input
        else:
            #bot_response="language is :"language
            #we translate user's input into English
            response = gtranslate(user_input, language, "en")
        #debug to bypass ollama
        #time.sleep(1)  
        #bot_response=response
        #let's ask llama
        bot_response = chat.ask_llama(response)    
          
                
    except Exception as e:
        bot_response = "An error occurred while processing your request. Please try again."
    
    respond_html=render_html(bot_response)
    return respond_html

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'chat_interface.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555, debug=True)
