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
