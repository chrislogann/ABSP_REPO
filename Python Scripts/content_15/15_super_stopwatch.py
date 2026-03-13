import time
import pyperclip

"""
Script 15_super_stopwatch.py measures the time between hitting the enter key.
The stopwatch takes laps whenever the enter key is selected.
"""

# Display the program's instructions.
print('Press ENTER to begin. Afterwards, press ENTER to "click" the stopwatch.Press Ctrl-C to quit.')
input()                    
print('Started.')
startTime = time.time()    
lastTime = startTime
lapNum = 1
copyOutput = ""
# Start tracking the lap times.

try:
   while True:
            input()
            lapTime = round(time.time() - lastTime, 2)
            totalTime = round(time.time() - startTime, 2)

            adj_lapnum = str(lapNum).ljust(1," ").rjust(2," ")
            adj_totalTime = str(totalTime).rjust(5," ")
            adj_lapTime = str(lapTime).rjust(6," ")
            
            print_line = 'Lap #%s: %s (%s)' % (adj_lapnum, adj_totalTime, adj_lapTime)
            print(print_line, end = "")
            copyOutput = f"{copyOutput}\n{print_line}"

            lapNum += 1
            lastTime = time.time() # reset the last lap time
except KeyboardInterrupt:
       # Handle the Ctrl-C exception to keep its error message from displaying.
       print("\nCopying output to user clipboard")
       pyperclip.copy(copyOutput)
       print('\nDone.')
