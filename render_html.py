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



# ollama resond in well formatted text
# we want to preserve that formatting
# but we will convirt it into HTML nicelly

from flask import render_template_string
import markdown

def render_html(bot_response):
    # Convert Markdown to HTML
    html_response = markdown.markdown(bot_response, extensions=['fenced_code', 'tables'])
    # Render the response in Wendy-style
    html_template = f"""
                <body class="clearfix">
                        <img src="\static\pics\wendy_small.png" alt="Description" class="corner-image">
                        <p>
                        {html_response}
                        </p>
                </body>
        """
    return render_template_string(html_template)
