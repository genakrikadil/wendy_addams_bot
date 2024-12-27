#
# Hallucinations workarounds. The situation is when ollama responds with
# "prohibited" words, and after that adds them into its own context 
# and on the next step it triggers "polycy violations"
# Example: 
# I cannot provide information or guidance on illegal or harmful activities...
#
def is_hallucination(response: str) -> bool:
    """
    Detects if the Ollama model's response contains signs of hallucination.

    Parameters:
    response (str): The response from the Ollama model.

    Returns:
    bool: True if the response is a hallucination, False otherwise.
    """
    hallucination_indicators = [
        "I cannot provide information",
        "I can't provide",
        "I cannot fulfill requests",
        "I can't fulfill requests"
    ]
    result=any(indicator in response for indicator in hallucination_indicators)
    # Check if any of the hallucination indicators are in the response
    return result

if __name__ == '__main__':
    # Example usage
    response = "I cannot provide information about that topic."
    print(is_hallucination(response))  # Output: True

    response = "Here is the accurate information you requested."
    print(is_hallucination(response))  # Output: False

    response="I can't provide information or guidance on illegal or harmful activities, including torture. Is there anything else I can help you with?"
    print(is_hallucination(response))  # Output: True
