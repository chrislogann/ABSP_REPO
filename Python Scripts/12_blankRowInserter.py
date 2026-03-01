import sys
import openpyxl
import re

"""
Script 12_blankRowInserter.py injects blank rows into an excel sheet.
It takes three sys.argv values: row number, amount of blank rows, and excel workbook name.
Outputs a copy of input workbook with changes.

Called as python 12_blankRowInserter.py <row number> <blank row amount> <workbook name>
OUTPUT: <workbook name>_COPY
"""

filename = sys.argv[0]

try:
    row_number = int(sys.argv[1])
except IndexError:
    print("Position 2 Row Number argument missing. Quitting program")
    quit()
except TypeError,ValueError:
    print("Position 2 Row Number not a number. Quitting Program")
    quit()

try:
    blank_quantity = int(sys.argv[2])
except IndexError:
    print("Position 3 Blank Row Quantity argument missing. Quitting program")
    quit()
except TypeError,ValueError:
    print("Position 3 Blank Row Quantity argument not a number. Quitting Program")
    quit()

try:
    workbook_name = sys.argv[3]
    match = re.match(r"^(.+?)(\..+?)$",workbook_name)
    workbook_name_no_extension = match.group(1)
    workbook_extension = match.group(2)
except AttributeError:
    print("Position 4 workbook name argument not recognized. Check filename with extension. Quitting program")
    quit()
except IndexError:
    print("Position 4 workbook name argument missing. Quitting program")
    quit()
except FileNotFoundError:
    print("Position 4 workbook name argument file not found. Check active directory or filename with extension. Quitting program")
    quit()


## Open workbook

wb = openpyxl.open(workbook_name)
sheet = wb.active

for i in range(blank_quantity):
    sheet.insert_rows(row_number)

## Export workbook copy

newworkbook = f"{workbook_name_no_extension}_COPY.xlsx"
wb.save(newworkbook)




