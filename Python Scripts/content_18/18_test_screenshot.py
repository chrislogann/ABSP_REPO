import os
import pyautogui
import time

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
        
directory = os.getcwd()

## Prepare hotdogs
# screenshot = get_filepath(directory,'ready_hotdog.png')
# pos = locate_position(screenshot)
# x, y = pyautogui.center(pos)

# pyautogui.click(x, y, duration=0.2,clicks=4)
# time.sleep(1)

# screenshot = get_filepath(directory,'ready_bun.png')
# pos = locate_position(screenshot)
# x, y = pyautogui.center(pos)

# pyautogui.click(x, y, duration=0.2,clicks=4)
# time.sleep(1)

## deliver order

