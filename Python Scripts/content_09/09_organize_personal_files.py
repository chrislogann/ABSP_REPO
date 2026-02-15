import os
import re
import shutil

"""
This script cleans up the folder Python Scripts.
Files are renamed and moved into their respective
"""

def copy_files(pSourceFolder,pLandingFolder,pFileName):
    """
    Copies files from source folder to Landing Folder
    """  
    SourceFile = os.path.join(pSourceFolder, pFileName)
    shutil.copy(SourceFile,pLandingFolder)
    print(f"Copying file {pFileName} to folder {os.path.basename(pLandingFolder)}")

def rename_files(pSourceFolder,pFileName):
    """
    Renames files in source folder.
    Filenames are set to lower and replaces spaces with underscores.
    """
    SourceFile = os.path.join(pSourceFolder,pFileName)
    new_filename = pFileName.lower().replace(" ","_")
    RenameSourceFile = os.path.join(pSourceFolder,new_filename)

    if SourceFile == RenameSourceFile:
        print(f"Skipping rename (already normalized): {pFileName}")
        return pFileName   # return unchanged name

    shutil.move(SourceFile,RenameSourceFile)
    print(f"Renaming file {pFileName} in folder {os.path.basename(pSourceFolder)}")
    return new_filename

def create_subfolders(pSourceFolder,pFileName,pIndex):  

    """
    Creates subfolders according to index patterns and
    moves files with coorsponding index to respective subfolder.
    """

    SubFolderName = f"content_{pIndex}"
    LandingSubFolder = os.path.join(pSourceFolder,SubFolderName)

    if not os.path.exists(LandingSubFolder):
        os.makedirs(LandingSubFolder)
        print(f"Created folder: {SubFolderName}")
    
    SourceFile = os.path.join(pSourceFolder,pFileName)
    LandingFile = os.path.join(LandingSubFolder,pFileName)
    shutil.move(SourceFile,LandingFile)

def organize_files(pSourcePath,pLandingPath,pFilePattern):
    """
    Takes a source path and landing path to organize the landing spot folder.
    pFilePattern identifies index patterns within a filename.
    """

    os.makedirs(pLandingPath, exist_ok=True)

     
    for folderName, _, filenames in os.walk(pSourcePath):
        print('')
        for filename in filenames:

            match = pFilePattern.search(filename)

            if match:
                copy_files(folderName,pLandingPath,filename)
                
    files = list(os.listdir(pLandingPath))

    for filename in files:

        match = pFilePattern.search(filename)

        if match:

            rIndex = match.group(1)

            NewFilename = rename_files(pLandingPath,filename)
            create_subfolders(pLandingPath,NewFilename,rIndex)
        
filepath = os.getcwd()
SourceFolderPath = os.path.join(filepath, "Python Scripts")
LandingFolderPath = os.path.join(filepath, "Python Scripts Copy")

FilePattern = re.compile(r"""
                          ^(\d{2}) ##Index
                          (.+) ## Name
                          (\.\w+)$ # file extension     
                          """,re.VERBOSE)

organize_files(SourceFolderPath,LandingFolderPath,FilePattern)
