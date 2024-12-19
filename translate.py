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
# translates the text from one language into another
# pip install googletrans==4.0.0-rc1
#
#to see list of supported languages:
# from googletrans import LANGUAGES
# print(LANGUAGES)
#
#  see usage in _main_ below
#
#
from googletrans import Translator

def gtranslate_lang_detect(input_text):
# Detect the language of the text
# Initialize the translator
    translator = Translator()
 # Handle errors gracefully:
    try:
        result = translator.detect(input_text)
        return result.lang

    except Exception as e:
        return f"Language detection failed: {e}"  # Corrected exception handling

    


def gtranslate(input_text, lang_src, lang_dst):
    # Initialize the translator
    translator = Translator()

    # Handle errors gracefully:
    try:
        translation = translator.translate(input_text, src=lang_src, dest=lang_dst)
        return translation.text  # Fixed closing parenthesis

    except Exception as e:
        return f"Translation failed: {e}"  # Corrected exception handling


if __name__ == '__main__':

    # Example how to call the functions above
    # translate from one language to another 
    out = gtranslate("Здравствуйте уважаемые", "ru", "en")
    print('Translation:',out)

    #auto detect language
    out=gtranslate_lang_detect("Como Estas?")
    print ('Languge Detected:',out)

