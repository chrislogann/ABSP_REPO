import os
import pyautogui
import keyboard
import time
import logging

logging.basicConfig(level=logging.DEBUG,format=' %(asctime)s %(levelname)s - %(message)s')
# logging.disable()

def get_filepath(directory,target_filename):

    for folderpath,subfolder,filenames in os.walk(directory):

        for filename in filenames:

            if target_filename != filename:
                continue

            return os.path.join(folderpath,filename)

def locate_position(screenshot_name,interval=0.95):
    pos = pyautogui.locate(
    screenshot_name,
    pyautogui.screenshot(allScreens=True),
    confidence=interval
    )

    return pos

class food_prep:

    def __init__(self,directory):
        self.directory = directory
    
    def __stock_buns(self):

        try:
            screenshot = get_filepath(self.directory,'buns.png')
            pos = locate_position(screenshot)
            x, y = pyautogui.center(pos)

            logging.info("Stocking buns")

            pyautogui.click(x, y, duration=0.2,clicks=4)
            # time.sleep(0.25)
        except:
            pass
            
    def __stock_hotdogs(self):

        try:
            screenshot = get_filepath(self.directory,'hotdogs.png')
            pos = locate_position(screenshot)
            x, y = pyautogui.center(pos)

            logging.info("Stocking hotdogs")

            pyautogui.click(x, y, duration=0.2,clicks=4)
            # time.sleep(1)
        except:
            pass
            

    def __make_hotdog(self):
        
        try:
            screenshot = get_filepath(self.directory,'ready_hotdog.png')
            pos = locate_position(screenshot,0.75)
            x, y = pyautogui.center(pos)

            logging.info("Hotdog ready")

            pyautogui.click(x, y, duration=0.2)
            time.sleep(1)
        except:
            logging.info("Not hotdogs ready")
            return None

        try:
            screenshot = get_filepath(self.directory,'ready_bun.png')
            pos = locate_position(screenshot,0.95)
            x, y = pyautogui.center(pos)

            logging.info("preparing hotdog")

            pyautogui.click(x, y, duration=0.2)
            time.sleep(1)
        except:
            logging.info("No buns ready")
            return None

    def prepare_food(self):

        self.__stock_buns()
        self.__stock_hotdogs()
        self.__make_hotdog()


class deliver_order:

    def __init__(self,directory):
        self.directory = directory
    
    def deliver_order(self):

        try:
            screenshot = get_filepath(self.directory,'order_1.png')
            pos = locate_position(screenshot)
            x, y = pyautogui.center(pos)

            pyautogui.click(x, y, duration=0.2)
            time.sleep(0.5)
        except:
            pass

        try:
            screenshot = get_filepath(self.directory,'order_2.png')
            pos = locate_position(screenshot)
            x, y = pyautogui.center(pos)

            pyautogui.moveTo(x, y, duration=0.2)
            time.sleep(0.5)
        except:
            pass

class operate:

    def __init__(self):
        self.directory = os.getcwd()

        self.food_prep = food_prep(self.directory)
        self.deliver_order = deliver_order(self.directory)

    def run(self):

        pyautogui.FAILSAFE = True
        
        try:
            while True:

                if keyboard.is_pressed('esc'):
                    print('Quitting...')
                    break

                self.food_prep.prepare_food()
                # self.deliver_order.deliver_order()
                time.sleep(0.5)
        except KeyboardInterrupt:
            print("Stopped by user")

app = operate()
app.run()

# directory = os.getcwd()
# ## add buns
# screenshot = get_filepath(directory,'empty_counter.png')
# pos = locate_position(screenshot)
# x, y = pyautogui.center(pos)

# pyautogui.moveTo(x, y, duration=0.2)
# time.sleep(1)

# ## add hotdogs
# screenshot = get_filepath(directory,'empty_grill.png')
# pos = locate_position(screenshot)
# x, y = pyautogui.center(pos)

# pyautogui.moveTo(x, y, duration=0.2)
# time.sleep(1)

# screenshot = get_filepath(directory,'hotdogs.png')
# pos = locate_position(screenshot)
# x, y = pyautogui.center(pos)

# pyautogui.click(x, y, duration=0.2,clicks=4)
# time.sleep(1)
