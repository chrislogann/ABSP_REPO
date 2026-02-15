import os
import operator

"""
09 Deleting Uneeded File.py prints files over a certain limit
"""
def convert_byte(pFileSize,pMetric):
    """
    convert_byte converts byte values
    """
    metric_dict={
        "BYTES": pFileSize,
        "KB": pFileSize/(1024*1),
        "MB": pFileSize/(1024*2)
    }

    return metric_dict[pMetric]

def compare_values(a, b, op_symbol):
    """
    Compare two values dynamically based on the operator symbol.
    """

    comparison_ops = {
        ">": operator.gt,   # greater than
        "<": operator.lt,   # less than
        ">=": operator.ge,  # greater than or equal
        "<=": operator.le,  # less than or equal
        "==": operator.eq,  # equal
        "!=": operator.ne   # not equal
    }

    if op_symbol not in comparison_ops:
        raise ValueError(f"Invalid operator: {op_symbol}")
    return comparison_ops[op_symbol](a, b)

def print_filesize(pFolderPath,pLimit,pMetric,pSign):

    for foldername, subfolders, filenames in os.walk(pFolderPath):
        for filename in filenames:
            filepath = foldername+"\\"+filename

            filesize = os.path.getsize(filepath)

            convert_val = convert_byte(filesize,pMetric)
            success = compare_values(convert_val,pLimit,pSign)

            if success == True:
                print(f"File Name: {filename},file size in KBs {round(convert_val,2)}")
                print(filepath)
                print('\n')

FolderPath = os.getcwd()

print_filesize(FolderPath,10,"KB",">")
