import os
import re
import shutil

"""
This script cleans up the folder Python Scripts.
Files are renamed and moved into their respective
"""

filepath = os.getcwd()

FilePattern = re.compile(r"""
                          ^(\d{2})
                          (.+)
                          (.\w)$         
                          """,re.VERBOSE)

source_filepath = filepath+"\\Python Scripts"
for folderName, subfolders, filenames in os.walk(source_filepath):
    for filename in filenames:

        match = FilePattern.search(filename)

        if match != None:

            rIndex = match.group(1)
            rName = match.group(2)
            rExtension = match.group(3)

            SubFolderPath = f"{folderName}\\{rIndex}_content"
            
            try:
                os.makedirs(SubFolderPath)
            except FileExistsError:
                None
            
            SourceFile = folderName+"\\"+filename
            SubFolderFile = SubFolderPath+"\\"+filename
            RenameSubFolderFile = SubFolderPath+"\\"+filename.replace(" ","_")

            try:
                shutil.move(SourceFile,SubFolderPath)
                shutil.move(SubFolderFile,RenameSubFolderFile)
                print(f"Copying file {filename} to folder {SubFolderPath.split("\\")[-1]}")
            except shutil.SameFileError:
                print(f"Deleting file {filename} in folder {SubFolderPath.split("\\")[-1]}")
                os.unlink(SubFolderPath+"\\"+filename)

