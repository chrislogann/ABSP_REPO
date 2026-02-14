import os 
import shutil
import re

"""
09 Selective Copy.py takes a regular expression pattern to identify target file extensions.
Selected files then copy over to folder 09_Copy_Folder.
"""

filepath = os.getcwd()

try:
    os.makedirs(filepath+"\\09_Copy_Folder")
    FolderPath = filepath+"\\09_Copy_Folder"
except FileExistsError:
    FolderPath = filepath+"\\09_Copy_Folder"

FilePattern = re.compile(r"(.+\.py$)")

for folderName, subfolders, filenames in os.walk(filepath):
    for filename in filenames:

        match = FilePattern.search(filename)

        if match != None:
            filepath = folderName +'\\'+ filename
            try:
                shutil.copy(filepath,FolderPath)
                print(f"Copying file {filename} to folder {FolderPath.split("\\")[-1]}")
            except shutil.SameFileError:
                print(f"Deleting file {filename} in folder {FolderPath.split("\\")[-1]}")
                os.unlink(FolderPath+"\\"+filename)
                

print('Script Complete')
