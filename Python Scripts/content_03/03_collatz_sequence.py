import re

class CollatzLogic:
    @staticmethod
    def collatz_calc(number):

        ## Generate Collatz sequence

        if number % 2 == 0:
            print('EVEN')
            return 3 * number + 1

        elif number % 2 == 1:
            print('ODD')

class EntryType:
    @staticmethod
    def input_method():

        input_value = None

        while True:
            
            print("Enter 'Q' to Quit Program")
            print("or input value:")
            input_value = input()

            if re.search(r"(?i)Q",input_value.upper()):
                print("Exiting Program")
                quit()

            try:
                input_value = int(input_value)

            except ValueError:
                print("ValueError: Not Integer type")

            RetVal = str(CollatzLogic.collatz_calc(input_value))
            print("Return number is " + RetVal)

EntryType.input_method()

