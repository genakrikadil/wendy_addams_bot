import globals #type:ignore  here we put all global constants

# Define a list of available models
#available_models = ["christian", "wednesday"]

# Global variable to store the currently selected model
#MODEL = globals.MODEL

# Function to analyze user input and change the global MODEL variable if the input matches the format
def analyze_and_change_model(user_input):
    # Check if the input matches the format "model:<modelname>"
    if user_input.startswith("model:"):
        model_name = user_input.split("model:")[1].strip()
        if model_name in globals.MODELS:
            globals.MODEL = model_name
            return f"Model '{model_name}' selected.", True
        else:
            return f"No such model. Available models are: {', '.join(globals.MODELS)}.",True
    return user_input, False


if __name__ == '__main__':
    # Example usage
    print(analyze_and_change_model("model:christian"))  # Output: Model 'christian' selected.
    print(analyze_and_change_model("model:unknown"))    # Output: No such model. Available models are: christian, wednesday.
    print(analyze_and_change_model("model:wednesday"))  # Output: Model 'wednesday' selected.
    print(analyze_and_change_model("How are you?"))  # no model change command found, return original text