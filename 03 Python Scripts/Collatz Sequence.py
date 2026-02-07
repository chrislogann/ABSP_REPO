import sys


## Generate Collatz sequence

class CollatzLogic:
    @staticmethod
    def collatz_calc(number):
        if number % 2 == 0:
            print('EVEN')
            return 3 * number + 1

        elif number % 2 == 1:
            print('ODD')

class EntryType:
    @staticmethod
    def input_method():

        input_value = "A"

        while True:

            input_value = input().strip()
            print(input_value)
            if input_value.upper() == "Q":
                print("Exiting Program")
                sys.exit()
                #quit()

            try:
                print("Enter 'Q' to Quit Program")
                print("or input value:")

                input_value = int(input_value)

            except ValueError:
                print("ValueError: Not Integer type")
                continue

            RetVal = str(CollatzLogic.collatz_calc(input_value))
            print("Return number is " + RetVal)

EntryType.input_method()
## Generate Collatz sequence

def collatz(number):

    if number % 2 == 0:
        print('EVEN')
        return 3 * number + 1

    elif number % 2 == 1:
        print('ODD')


input_value = 0
try:
    print("input value:")
    input_value = int(input())
except ValueError:
    print("ValueError: Not Integer type")
    quit()

    return_val = str(collatz(input_value))
    print("Return number is " + return_val)

