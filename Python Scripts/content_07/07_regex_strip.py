import re

def StripString(inputString,StripPattern):
    
    ## Default if StriPattern empty
    if StripPattern == "":
        pattern = r'^\s*(.+?)\s*$'
        replace_method = r"\1"
        
    else:
        pattern = '(?i)['+StripPattern+']'
        replace_method = ""
    
    result = re.sub(pattern,replace_method,inputString)

    return result

target_string = "  Hello World!    "

RetVal = StripString(target_string,"")

print(RetVal)
