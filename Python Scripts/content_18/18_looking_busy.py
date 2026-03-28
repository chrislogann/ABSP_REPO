import pyautogui
import time

"""
Script 18_looking_busy.py jiggles mouse every 10 seconds. This prevents computer from going to sleep.
"""

print('Press Ctrl-C to quit.')


try:
    while True:

        pyautogui.moveRel(10, 0, duration=0.2)
        time.sleep(10)
        pyautogui.moveRel(-10, 0, duration=0.2)


except KeyboardInterrupt:
    print('Done.')


