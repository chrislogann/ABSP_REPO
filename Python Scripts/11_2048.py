from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

"""
Script 11_2048 sends keys to play 2048.
"""

browser = webdriver.Edge()
browser.get('https://www.2048.org/')

game_board = browser.find_element(By.TAG_NAME,'html')

while True:

    try:
        game_board.send_keys(Keys.UP)
        game_board.send_keys(Keys.RIGHT)
        game_board.send_keys(Keys.DOWN)
        game_board.send_keys(Keys.LEFT)
    except:
        print("Game Over")
        quit()


