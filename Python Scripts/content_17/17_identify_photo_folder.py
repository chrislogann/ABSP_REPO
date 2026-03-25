import os 
from PIL import Image
import logging

logging.basicConfig(level=logging.INFO,format=' %(asctime)s %(levelname)s - %(message)s')
# logging.disable()

"""
Script 17_identify_photo_folder finds a computer's photo folder.
A photo folder is a folder containing large (greater than 500x500) images
as well as a file extension ending with ".png" or ".jpg".
Results will output the absolute photo folder.
"""

def get_photo_folderpath(drive):

    """
    Searches a computer drive for folder containing more than half of image files.
    Photos are defined as having a dimension greather than 500x500 and
    file extensions ending with '.jpg' or '.png'.
    Potential photo folders are printed on the console.

    Params:
    drive: a directory containing a drive

    Returns:
    None
    """

    ## Walk entire computer drive.
    for folderpath,subfolder,filenames in os.walk(drive):

        acceptable_photo_count = 0
        total_file_count = 0
        for filename in filenames:

            total_file_count += 1

            ## Analyze if file ends with .png or .jpg
            valid_exts = ('.jpg','.png')
            if not filename.lower().endswith(valid_exts):
                logging.debug("File extension not in valid_exts tuple")
                continue

            photo_filepath = os.path.join(folderpath,filename)
            
            try:

                with Image.open(photo_filepath) as photoIm:
                    photo_width, photo_length = photoIm.size
                    logging.debug("Image file pixel dimensions %sx%s",photo_length,photo_width)

            except (Image.UnidentifiedImageError, OSError):
                logging.debug("Image not in acceptable format")
                continue
            
            ## Assess if image file's height and width are greater than 500 pixels
            if not (photo_length > 500 and photo_width > 500):
                logging.debug("Image dimension not greater than 500x500")
                continue
            
            ##Count number of photos meeting criteria from folder
            acceptable_photo_count +=1

        if total_file_count == 0:
            logging.debug("No content found.")
            continue
        
        ## Return absolute folderpath if photo criteria is greater than 50% of all files
        if (acceptable_photo_count/total_file_count) > 0.50:
            logging.info("Found folder meeting image criteria")
            print(folderpath)

drives = ('C:\\','G:\\')

for drive in drives:
    get_photo_folderpath(drive)

