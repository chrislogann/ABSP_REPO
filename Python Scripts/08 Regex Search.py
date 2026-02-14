import os
import re

'''
08 Regeax Search.py returns a regular expression pattern from a text file.
Users may define the pattern.
'''

filepath = os.getcwd()+"\\search_input.txt"

def return_file_match(pFile,pPattern):
    ## Reading file
    search_file = open(pFile,"r")
    file_string = search_file.read()
    search_file.close()

    ## Regex
    pattern = pPattern
    matches = re.findall(pPattern, file_string)

    print("Regex Pattern: " + pPattern)
    print("Match Count: " + str(len(matches)))
    pattern_count = {}

    for match in matches:
        if match in pattern_count:
            pattern_count[match] += 1
        elif match not in pattern_count:
            pattern_count.setdefault(match,1)

    sorted_dict = dict(sorted(pattern_count.items(), key=lambda item: item[1]))

    for k,v in sorted_dict.items():
        print(f"Pattern: {k}, Count: {v}")

print("Input Regex Pattern")
pattern = input()
return_file_match(filepath,pattern)

