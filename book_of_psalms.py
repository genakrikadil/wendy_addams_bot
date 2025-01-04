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
#
# I want the bot when I ask to read me some specific psalm
# from King Solomon's Psalms book just quote it.
#

import json
import re
import os

# Load and preprocess the JSON data for quick access
def load_psalms(json_file):
    with open(json_file, 'r', encoding='utf-8') as file:
        psalms_data = json.load(file)
        # Preprocess chapters into a dictionary for O(1) lookup
        chapter_dict = {
            chapter["chapter"]: chapter["verses"]  # Store verses as a list
            for chapter in psalms_data["chapters"]
        }
        return chapter_dict

# Get the text of a specific Psalm by chapter number, formatted as HTML
def get_psalm_text_html(preprocessed_data, chapter_number):
    verses = preprocessed_data.get(str(chapter_number))
    if not verses:
        return "<b>Psalm not found.</b>"

    # Construct the HTML
    html = [f"<h1>Psalm {chapter_number}</h1><br>"]
    for verse in verses:
        line_number = verse["verse"]
        line_text = verse["text"]
        html.append(f"<b>{line_number}</b> {line_text}<br>")
    return "\n".join(html)

# Main function to handle queries
def psalms(query):
    current_path = os.getcwd()
    psalms_file = current_path+'/Psalms.json'

    #check if file exists
    if not os.path.exists(psalms_file):
        return "Psalms.json file not found.", True

    preprocessed_data = load_psalms(psalms_file)
    # Extract the Psalm number from the query using regex
    match = re.search(r"Psalm (\d+)", query, re.IGNORECASE)
    if match:
        psalm_number = int(match.group(1))
        psalm_html = get_psalm_text_html(preprocessed_data, psalm_number)
        return psalm_html, True
    else:
        return query, False


##### Example how you call it #########
if __name__ == "__main__":
    
    query = "What is Psalm 13 about?"

    #call the function
    reply_text, reply_bool = psalms(query)

    #print the result
    if reply_bool:
        print(reply_text)
    else:
        print("No Psalm number found in the query.")
