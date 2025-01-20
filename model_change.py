import globals #type:ignore  here we put all global constants

# Define a list of available models
#available_models = ["christian", "wednesday"]

# Global variable to store the currently selected model
#MODEL = globals.MODEL

# Function to analyze user input and change the global MODEL variable if the input matches the format
#prompt,self.model,changed=analyze_and_change_model(prompt,self.model)
def analyze_and_change_model(user_input,model_name):
    # Check if the input matches the format "model:<modelname>"
    if user_input.startswith("model:"):
        model_name = user_input.split("model:")[1].strip()
        if model_name in globals.MODELS:
            #globals.MODEL = model_name
            return f"Model '{model_name}' selected.", model_name,True
        else:
            return f"Available models are: {', '.join(globals.MODELS)}.", model_name, True
    return user_input, model_name,False

