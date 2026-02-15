import os

'''
Madlib.py intakes a Madlib file with the key identifiers ADJECTIVE,NOUN, and VERB.
Users input the desired word which replaces the identifier.
This script outputs the modified phrase to madlib_output.
'''

path = os.getcwd()

madlib_text = open(path+"\\madlib_input.txt","r")

madlib_content = madlib_text.read()

madlib_list = madlib_content.split()

madlib_text.close()

for i in range(len(madlib_list)):
    
    if "ADJECTIVE" in madlib_list[i]:
        print("Input a adjective: ")
        input_value = input()
        madlib_list[i] = madlib_list[i].replace("ADJECTIVE",input_value)

    elif "NOUN" in madlib_list[i]:
        print("Input a noun: ")
        input_value = input()
        madlib_list[i] = madlib_list[i].replace("NOUN",input_value)

    elif "VERB" in madlib_list[i]:
        print("Input a verb: ")
        input_value = input()
        madlib_list[i] = madlib_list[i].replace("VERB",input_value)


madlib_mod = " ".join(madlib_list)    
madlib_output = open(path+"\\madlib_output.txt","w")
madlib_output.write(madlib_mod+'\n')
madlib_output.close()






