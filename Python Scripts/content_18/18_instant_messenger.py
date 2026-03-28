import pyautogui
import os
from dotenv import load_dotenv
import time

"""
Script 18_instant_messenger.py sends automated messages to select users using Google Hangouts.
"""

def locate_position(screenshot_name):
    pos = pyautogui.locate(
    screenshot_name,
    pyautogui.screenshot(allScreens=True),
    confidence=0.95
    )

    return pos

def get_filepath(directory,target_filename):

    for folderpath,subfolder,filenames in os.walk(directory):

        for filename in filenames:

            if target_filename != filename:
                continue

            return os.path.join(folderpath,filename)

load_dotenv()
message_recipients = os.getenv('message_recipients').split(',')
directory = os.getcwd()

## Loop through recipients
for recipient in message_recipients:

    ## locate new message button
    new_chat_screenshot = get_filepath(directory,'new_chat.png')
    pos = locate_position(new_chat_screenshot)
    x, y = pyautogui.center(pos)

    pyautogui.click(x, y, duration=0.2)
    time.sleep(1)
    pyautogui.typewrite(recipient.strip(), 0.25)
    pyautogui.press('enter')

    ## Locate start chat button
    start_chat_screenshot = get_filepath(directory,'start_chat.png')
    pos = locate_position(start_chat_screenshot)
    x, y = pyautogui.center(pos)
    pyautogui.click(x, y, duration=0.2)

    ## Enter and send message
    message = 'HELLO WORLD!!!'
    time.sleep(1)
    pyautogui.typewrite(message, 0.25)
    pyautogui.press('enter')

print("script complete")