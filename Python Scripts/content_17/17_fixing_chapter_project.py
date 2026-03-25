from PIL import Image
import os
import re

"""
Script 17_fixing_chapter_project revises script resizeAndAddLogo.py. It lowers the file extension
and scales an image two times its logo size.
"""

def lower_extension(match):
    return match.group(1)+match.group(2).lower()

def get_filepath(directory,target_filename):

    for folderpath,subfolder,filenames in os.walk(directory):

        for filename in filenames:

            if filename.upper() != target_filename.upper():
                continue
            
            filename = re.sub(r"^(.+?)(\.\w+)$",lower_extension,filename)

            filepath = os.path.join(folderpath,filename)
            return filepath

## Getting Logo
square_fit_size = 300
logo_filename = 'logo.PNG'

directory = os.getcwd()

logo_filepath = get_filepath(directory,logo_filename)
logoIm = Image.open(logo_filepath)
logo_width, logo_height = logoIm.size

## Getting Photo
os.makedirs('withLogo', exist_ok=True)
photo_filename = 'richard.png'
photo_filepath = get_filepath(directory,photo_filename)

pictureIm = Image.open(photo_filepath)

photo_width, photo_height = logo_width*2,logo_height*2
pictureIm = pictureIm.resize((photo_width,photo_height))

##Resize image

# if photo_width > square_fit_size and photo_height > square_fit_size:

#     if photo_width > photo_height:

#         photo_height = int((square_fit_size/photo_width)*photo_height)
#         photo_width = square_fit_size

#     else:

#         photo_width = int((square_fit_size/photo_width)*photo_height)
#         photo_height = square_fit_size

#     print('Resizing %s...' % (photo_filename))
#     pictureIm = pictureIm.resize((photo_width,photo_height))

## Add Logo
logoIm = logoIm.convert("RGBA")
logoIm = logoIm.resize((logo_height,logo_width))
pictureIm = pictureIm.convert("RGBA")

print('Adding logo to %s...' % (photo_filename))
pictureIm.paste(logoIm, (photo_width - logo_width, photo_height - logo_height), logoIm)
# Save changes.
pictureIm.save(os.path.join('withLogo', photo_filename))

