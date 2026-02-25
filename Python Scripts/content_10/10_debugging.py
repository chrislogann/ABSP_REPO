import random
import logging

logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s %(levelname)s - %(message)s')
logging.disable()


"""
This program seeks to debug the given coin flip script.
One will test their capabilities to debug and log issues.
"""

logging.debug("Program Begin")

toss_lib = {
    "HEADS":1,
    "TAILS":0
}

toss = random.randint(0, 1) # 0 is tails, 1 is heads
logging.debug(f"Toss: {toss}")

i = 0
logging.debug("while True loop begins")
while True:
    print('Guess the coin toss! Enter heads or tails:')
    guess = input()

    try:
        guess = toss_lib[guess.upper()]
    except KeyError:
        print("Input not recognized. Try again.")
        continue

    logging.debug(f"Guess: {guess}")

    i += 1
    logging.debug(f"increment i to {i}")

    if toss == guess:
        print('You got it!')
        logging.debug("Program end")
        quit()
    elif i == 2:
        print("YOU'RE A LOSER!!!")
        logging.debug(f"i = 2. Breaking loop.")
        break
    else:
        print('Nope! Guess again!')
logging.debug("while True loop ended")
    
logging.debug("Program end")

