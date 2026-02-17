def delimited_string(InputList,InputDelimiter):
    print('Returning delimited String')
    return InputDelimiter.join(InputList)

spam = []

while True:

    print('Enter input value')
    print('or type DONE when finished')
    InputValue = str(input())

    if InputValue.upper() == 'DONE':
        break
    elif InputValue.upper() == '':
        print('Value cannot be empty. Try Again.\n')
        continue

    spam.append(InputValue)
    print('Input added to list. Next.')


delimiter = ', '
retval = delimited_string(spam,delimiter)

print(retval)
