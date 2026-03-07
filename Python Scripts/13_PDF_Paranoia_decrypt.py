import os
import PyPDF2
import re

"""
Script 13_PDF_Paranoia_decrypt unlocks an encrypted pdf and create decrypted copy.
Users provide a directory and password to access PDFs.
Outputted files land in the given directory, and filenames end with suffix _decrypted.pdf.
"""

##Gather encrypted pdf files in directory
def gather_encrypted_pdfs(pDirectory):
    filepath_list = []
    for path, subfolder, filenames in os.walk(pDirectory):

        for file in filenames:

            if not file.endswith(".pdf"):
                continue
            
            filepath = os.path.join(path,file)
            pdfReader = PyPDF2.PdfReader(open(filepath,'rb'))

            if pdfReader.is_encrypted == True:
                filepath_list.append(filepath)
    
    return filepath_list

##Create unlocked copy of encrypted file and add decrypted to filename
def create_decrypted_pdfs(pFilePathList,pPassword):
    
    for original_filepath in pFilePathList:
            
        ## Current PDF File
            original_filename = os.path.basename(original_filepath)

            original_pdf_file = open(original_filepath,'rb')

            ##Gather PDF Pages
            pdfReader = PyPDF2.PdfReader(original_pdf_file)

            retval = pdfReader.decrypt(pPassword)
            
            if retval == 0:
                print(f"Password not accepted for file {original_filename}")
                print("Continue to next file \n")
                continue

            print(f"Password accepted for file {original_filename}. Copying pdf content.")

            page_count = len(pdfReader.pages)
            pdfWriter = PyPDF2.PdfWriter()
            
            for pageNum in range(page_count):
                
                pageObj = pdfReader.pages[pageNum]
                pdfWriter.add_page(pageObj)

            ## New PDF File
            pattern = r"^(.+?)\.(.+?)$"
            match = re.match(pattern,original_filename)
            filename_no_extension = match.group(1).replace("_encrypted","")
            file_extension = match.group(2)
            new_filename = f"{filename_no_extension}_decrypted.{file_extension}"
            new_filepath = str(original_filepath).replace(original_filename,new_filename)

            new_pdf_file = open(new_filepath,'wb')

            pdfWriter.write(new_pdf_file)

            original_pdf_file.close()
            new_pdf_file.close()

            print(f"Created file {new_filename}")

directory = os.getcwd()
vFilepath_List = gather_encrypted_pdfs(directory)
vPassword = "TEST"

create_decrypted_pdfs(vFilepath_List,vPassword)

