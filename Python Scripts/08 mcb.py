#! python3
# mcb.py - Saves and loads pieces of text to the clipboard.
# Usage:
#   python mcb.py save <keyword>  - Saves clipboard to keyword.
#   python mcb.py <keyword>       - Loads keyword to clipboard.
#   python mcb.py list            - Loads all keywords to clipboard.

import shelve
import pyperclip
import sys

mcbShelf = shelve.open('08 mcb')

# Save clipboard content
if len(sys.argv) == 3 and sys.argv[1].lower() == 'save':
    mcbShelf[sys.argv[2]] = pyperclip.paste()

elif len(sys.argv) == 2 and sys.argv[1].lower() == 'delete':
    mcbShelf.clear()
elif len(sys.argv) == 3 and sys.argv[1].lower() == 'delete':
    mcbShelf.pop(sys.argv[2])

elif len(sys.argv) == 2:
    # List keywords and load content
    if sys.argv[1].lower() == 'list':
        pyperclip.copy(str(list(mcbShelf.keys())))
    elif sys.argv[1] in mcbShelf:
        pyperclip.copy(mcbShelf[sys.argv[1]])

mcbShelf.close()