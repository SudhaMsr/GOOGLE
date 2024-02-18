
from html import unescape
import re

def html_to_plaintext(html_text):
    # Replace HTML entities with their corresponding characters
    plaintext = unescape(html_text)

    # Remove HTML tags
    plaintext = re.sub(r'<[^>]*>', '', plaintext)
    return plaintext