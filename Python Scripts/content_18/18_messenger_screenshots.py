import pyautogui
import os

# pyautogui.screenshot('start_chat.png',allScreens=True,region=(2243, 608, 115, 34))

pos = pyautogui.locate(
    'G:\\My Drive\\GIT_REPO\\ABSP_REPO\\hangout_screenshots\\new_chat.png',
    pyautogui.screenshot(allScreens=True),
    confidence=0.95
)

x, y = pyautogui.center(pos)
pyautogui.moveTo(x, y, duration=0.2)

pass