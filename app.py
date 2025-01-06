import uuid
from flask import Flask, request, jsonify, send_from_directory, session
from flask_cors import CORS
from translate import gtranslate, gtranslate_lang_detect
from render_html import render_html
from ask_llama import LlamaChat
from datetime import timedelta


app = Flask(__name__, static_folder='static')
CORS(app)

# Set a secret key for session management
app.secret_key = 'my_very_secret_key_is_here'

# Set the session timeout duration
app.permanent_session_lifetime = timedelta(minutes=30)

# Store chat instances associated with sessions
chat_instances = {}


@app.route('/respond', methods=['POST'])
def respond():
    user_input = request.json.get('message', '')

    try:
        # Make the session permanent to apply the timeout
        session.permanent = True

        # Generate a unique session ID for the chat instance if not already set
        if 'session_id' not in session:
            session['session_id'] = str(uuid.uuid4())  # Generate a unique UUID
            chat_instances[session['session_id']] = LlamaChat()

        # Retrieve the chat instance for the session
        chat = chat_instances[session['session_id']]

        # Detect language of the input and translate if necessary
        language = gtranslate_lang_detect(user_input)
        if 'en' in language.lower():
            response = user_input
        else:
            response = gtranslate(user_input, language, "en")
   
        # Get a response from LlamaChat
        bot_response = chat.ask_llama(response)

        # optional /* BETA */ we translate ollama response (en) to 
        # pre-defined language, russian (ru) for example 
        #response = gtranslate(bot_response, "en", "ru")
        #un-comment line below.
        #bot_response=response
        ######

        # Render the response in HTML format
        respond_html = render_html(bot_response)

    except Exception as e:
        print(f"Error: {e}")  # Debugging
        bot_response = f"An error occurred while processing your request. Please try again.{e}"
        respond_html = render_html(bot_response)

    return respond_html


@app.route('/')
def index():
    #return send_from_directory(app.static_folder, 'chat_interface.html')
    return send_from_directory(app.static_folder, 'index.html')

@app.before_request
def before_request():
    # Check if the session has expired
    if 'session_id' in session and session['session_id'] in chat_instances:
        session.modified = True
    else:
        # Clear session and associated chat instance if expired
        if 'session_id' in session:
            chat_instances.pop(session['session_id'], None)
        session.clear()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555, debug=True)
