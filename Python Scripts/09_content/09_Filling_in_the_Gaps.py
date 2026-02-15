import os
import re
import shutil

"""
09 Filling in the Gaps.py organizes files by indicies. 
It can either rename a file to adjust index or
create new files to fill in gaps.
"""

def organize_files(pFolderPath,pFilePattern,pMode):
    for foldername, subfolders, filenames in os.walk(pFolderPath):

        i = 0
        for filename in filenames:
            match = pFilePattern.search(filename)

            if match != None:
                i += 1

                rName = match.group(1)
                rIndex = match.group(2)
                rExtension = match.group(3)

                new_index = str(i).rjust(3,"0")
                new_filename = rName+new_index+rExtension

                filepath = foldername+"\\"+filename
                new_filepath = foldername+"\\"+new_filename

                if pMode.upper() == "CREATE" and new_index != rIndex:
                    create_file = open(new_filepath,'a')
                elif pMode.upper() == "RENAME":
                    shutil.move(filepath,new_filepath)

    print("organize_files is complete")

FolderPath = os.getcwd()
FilePattern = re.compile(r"""
                        ^(spam)
                         (\d{3})
                         (.\w+)$
                         """,re.VERBOSE)

organize_files(FolderPath,FilePattern,"CREATE")



            

    
