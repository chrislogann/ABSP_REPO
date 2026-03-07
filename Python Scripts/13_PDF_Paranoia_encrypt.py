import os
import PyPDF2
import re

"""
Script 13_PDF_Paranoia_encrypt encrypts all unencrytped PDF files in a given directory by setting a password.
All encrypted files with end with the suffix _encrypted.pdf.
All set passwords will be tested before delete the original PDF file.
Note that original files will be removed upon successful script execution.
"""

##Locate and gather PDFs in directory
def gather_unencrypted_pdfs(pDirectory):
    filepath_list = []
    for path, subfolder, filenames in os.walk(pDirectory):

        for file in filenames:

            if not file.endswith(".pdf"):
                continue
            
            filepath = os.path.join(path,file)
            pdfReader = PyPDF2.PdfReader(open(filepath,'rb'))

            if pdfReader.is_encrypted == False:
                filepath_list.append(filepath)
    
    return filepath_list

##Create copy of PDF with password and filename suffix _encrypted.pdf
def encrypt_pdfs(pPDFList,pPassword):

    for original_filepath in pPDFList:

        ## Current PDF File
        original_filename = os.path.basename(original_filepath)

        original_pdf_file = open(original_filepath,'rb')

        ##Gather PDF Pages
        pdfReader = PyPDF2.PdfReader(original_pdf_file)
        page_count = len(pdfReader.pages)
        pdfWriter = PyPDF2.PdfWriter()
        
        for pageNum in range(page_count):
            
            pageObj = pdfReader.pages[pageNum]
            pdfWriter.add_page(pageObj)


        ## New PDF File
        pattern = r"^(.+?)\.(.+?)$"
        match = re.match(pattern,original_filename)
        filename_no_extension = match.group(1)
        file_extension = match.group(2)
        new_filename = f"{filename_no_extension}_encrypted.{file_extension}"
        new_filepath = str(original_filepath).replace(original_filename,new_filename)

        new_pdf_file = open(new_filepath,'wb')

        ##Set encrypted password
        pdfWriter.encrypt(pPassword)
        pdfWriter.write(new_pdf_file)

        original_pdf_file.close()
        new_pdf_file.close()

        ##Test encryption password
        if os.path.exists(new_filepath):
            print("Testing encryption password")
            pdfReader = PyPDF2.PdfReader(new_filepath)
            pdfReader.decrypt(pPassword)
            print("password successful")
            print(f"File {new_filename} added")
        
        ##Delete original file
        if os.path.exists(original_filepath):
            print(f"Removing file {original_filename}")
            os.remove(original_filepath)

directory = os.getcwd()
vFilepath_List = gather_unencrypted_pdfs(directory)
vPassword = "TEST"
encrypt_pdfs(vFilepath_List,vPassword)
