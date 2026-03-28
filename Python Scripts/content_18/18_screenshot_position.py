import pyautogui
import time

print("Move your mouse to the top-left corner of the desired region...")
time.sleep(3) # Give yourself 3 seconds to move the mouse
pos1 = pyautogui.position()
print(f"Top-left corner (x1, y1): {pos1}")

print("Now move your mouse to the bottom-right corner of the desired region...")
time.sleep(3) # Give yourself 3 seconds to move the mouse
pos2 = pyautogui.position()
print(f"Bottom-right corner (x2, y2): {pos2}")

# Calculate width and height
width = pos2[0] - pos1[0]
height = pos2[1] - pos1[1]

print(f"Calculated region tuple: region=({pos1[0]}, {pos1[1]}, {width}, {height})")
