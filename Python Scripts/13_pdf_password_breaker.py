import os
import PyPDF2
import logging

logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s %(levelname)s - %(message)s')
logging.disable()

"""
Script 13_pdf_password_breaker.py opens an encrypted pdf by searching an english dictionary.
"""

##Import an encrypted pdf and english dictionary
def get_filepath(pDirectory,pFilename):

    """
    Returns filepath from given filename.

    Params:
    pDirectory: Folder location
    pFilename: target filename

    Returns:
    TargetFilepath: filepath from given filename
    """
    logging.debug(f"Searching pDirectory for pFilename")
    for folderpath,subfolder,filenames in os.walk(pDirectory):

        for filename in filenames:
            
            TargetFilepath = ""
            if filename != pFilename:
                continue

            TargetFilepath = os.path.join(folderpath,filename)
            logging.debug(f"File {filename} found!")

            return TargetFilepath
    
    logging.debug(f"File {pFilename} not found")
    return None

## open dictionary and attempt password with every english word
def crack_password(pPdfReader,pPasswordFilepath):

    """
    Cracks password by running an english dictionary.
    Password attempts are in all uppercase or all lowercase.

    Params:
    pPdfReader: PDF object containing password
    pPasswordFilepath: filepath where dictionary data is stored

    Returns:
    vUpperPassword: An all uppercased password
    VLowerPassword: An all lowercased password
    None: No password found
    """

    vPasswordFile = open(pPasswordFilepath,'r')
    logging.debug(f"Opened vPasswordFile")
    vPasswordFileContent = vPasswordFile.readlines()
    logging.debug(f"Password content loaded")
    vPasswordFile.close()
    logging.debug(f"Closed vPasswordFile")

    logging.debug(f"Running vPasswordFileContent loop")
    for password in vPasswordFileContent:

        vUpperPassword = password.upper().strip()
        vLowerPassword = password.lower().strip()
        # logging.debug(password)

        retval = pPdfReader.decrypt(vUpperPassword)
        # logging.debug(retval)

        if retval != 0:
            logging.debug(f"Returning password from vUpperPassword")
            return vUpperPassword
        
        retval = pPdfReader.decrypt(vLowerPassword)
        # logging.debug(retval)


        if retval != 0:
            logging.debug(f"Returning password from vLowerPassword")
            return vLowerPassword

        continue

    logging.debug(f"No password found")
    return None

def main():
    """
    Executed defined functions and opens PDF. Prints password if found or not found.


    Params:
    None

    Returns:
    None

    """
    ## Get Files
    vDirectory = os.getcwd()
    vFilename = "13_english_dictionary.txt"
    vDictionaryFilepath = get_filepath(vDirectory,vFilename)
    logging.debug(f"vDictionaryFilepath: {vDictionaryFilepath}")

    vFilename = "ATA-2024-Unclassified-Report_encrypted.pdf"
    vEncrytpedFilepath = get_filepath(vDirectory,vFilename)
    logging.debug(f"vEncrytpedFilepath: {vEncrytpedFilepath}")

    ##Open PDF
    vEncryptedPdf = open(vEncrytpedFilepath,'rb')
    logging.debug(f"vEncryptedPdf opened")

    vPDFReader = PyPDF2.PdfReader(vEncryptedPdf)

    if vPDFReader.is_encrypted == True:
        logging.debug(f"PDF file is encrypted")
    elif vPDFReader.is_encrypted == False:
        print("PDF file not encrypted. Quitting script")
        quit()

    ## Cracking password
    vPassword = crack_password(vPDFReader,vDictionaryFilepath) or "No password found"

    print(f"PDF file '{os.path.basename(vEncrytpedFilepath)}' password is {vPassword}")

    ## Close PDF
    vEncryptedPdf.close()
    logging.debug(f"vEncryptedPdf closed")
    print("Script complete. Quitting.")

main()
