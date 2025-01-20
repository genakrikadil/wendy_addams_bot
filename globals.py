# Description: Version of the software
VERSION="Version 1.0 Rev 01202025"

# Define a list of available models
MODELS = ["christians", "wednesday", "scientist","wizard"]

# Model we use. We adjust its behaviour to match "character"
#see folder "ollama_mod" for details

#select default model
#MODEL = "wednesday"
#MODEL="christians"
#MODEL="scientist"
#MODEL="dolphin"
MODEL="wizard"


# where ollama is listening
#URL = "http://192.168.2.112:11434/api/generate"
URL = "http://127.0.0.1:11434/api/generate"
#URL ="http://10.20.187.188:11434/api/generate"
