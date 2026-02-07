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

