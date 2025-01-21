# Function to analyze user input and change the global MODEL variable if the input matches the format
# "model:<modelname>". If the model name is valid, return a success message and the new model name.
# If the model name is invalid, return a list of available models. If the input does not match the
# format, return the input as is.

import globals #type:ignore  here we put all global constants and variables


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

# Main function to test the model change functionality
if __name__ == "__main__":
    # Current model initialized from globals
    current_model = globals.MODEL
    
    # Example user inputs
    user_inputs = [
        "model:christian",
        "model:wednesday",
        "model:unknown",
        "Hello, how are you?"
    ]
    
    for user_input in user_inputs:
        response, current_model, changed = analyze_and_change_model(user_input, current_model)
        if changed:
            print(response)
        else:
            print(f"User input processed: {response}")