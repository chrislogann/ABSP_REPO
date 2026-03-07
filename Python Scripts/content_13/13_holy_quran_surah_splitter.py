import os
import PyPDF2
import re

"""
Script 13_Holy_Quran_Surah_Splitter breaks down the Quran down by Surah.
It utilizes the table of contents to create a pdf and txt files for each surah.
An output file is created for each Surah with the file suffix _<Surah Name>.pdf.
"""

def find_holy_quran(pDirectory,pFilename):

    """
    Function find_holy_quran searches for a quran from a given filename.
    The Holy Quran must come from the Bridges translation.

    Params:
    pDirectory: folder location for the Holy Quran
    pFileName: Name of file with extension (.pdf)

    Returns:
    file_path_list: contains filepath for the given filename

    """

    filepath_list = []
    # Find Holy Quran PDF
    for path, subfolder, filenames in os.walk(pDirectory):

        for file in filenames:

            if not file.endswith(".pdf"):
                continue
            
            if file != pFilename:
                continue
            
            filepath = os.path.join(path,file)
            filepath_list.append(filepath)
    
    return filepath_list

def get_surah_pages(pFilePathList):

    """
    Function get_surah_pages parses a table of contents. It gathers Surah name and starting page.
    The PDF begins the holy Quran on page 46, so each page is increased by 45.
    The table of contents is between pages 41 and 44, so the for loop range is defined.

    Params:
    pFilePathList: A list that contains the filepath to the Holy Quran

    Returns:
    table_of_contents: exports a nested list with surah name and starting page.

    """

    table_of_contents = []
    for original_filepath in pFilePathList:
                
        ## Current PDF File
        pdf_file = open(original_filepath,'rb')

        ## Open PDF
        pdfReader = PyPDF2.PdfReader(pdf_file)
        
        ## Table of contents
        for i in range(41,44):
            pageObj = pdfReader.pages[i] 
            text = pageObj.extract_text()

            pattern = re.compile(r"""
                                 (?P<surah>\d+?.+?) ## Surah Name
                                 (\s{1,2}) ##Surah Name may end with one or two spaces
                                 ([.\s]+) ## long break of periods that may interject with spaces
                                 (?P<page>[\d\s]+) ## Page Number could be split by whitespace
                                 ([\nA-Za-z]+) ## Ends with either new line or word
                                  """,re.VERBOSE)
            
            match = re.findall(pattern,text)

            for surah,_,_,page,_ in match:
                surah_renamed = "_surah_"+str(surah).lower().replace('.',"").replace(" ","_")
                page_cleaned = re.sub(r"\s","",page)
                content_list = [surah_renamed,int(page_cleaned)+45]
                table_of_contents.append(content_list)
                    
        pdf_file.close()

    return table_of_contents

def gather_pages(pPDFReader,pPDFWriter,pStartPage,pEndPage):

    """
    Function gather_pages returns a PDFWriter with page content from a start and end range.
    Note that indexing begins at zero, so pStartPage - 1 needed.

    Params:
    pPDFReader: PyPDF2 object containing page content
    pPDFWriter: PyPDF2 object that gathers page content
    pStartPage: Starting page
    pEndPage: Ending page

    Returns:
    pPDFWriter: outputs page content from given range

    """

    print("Getting surah pages")
    for pageNum in range(pStartPage-1,pEndPage):
            pageObj = pPDFReader.pages[pageNum]
            pPDFWriter.add_page(pageObj)
    return pPDFWriter

def generate_pdf(pDirectory,pFilename,pPdfWriter):
        """
        Generates and exports PDF files. Creates folder called pdf_folder.

        Params:
        pDirectory: File landing location
        pFilename: Name for generated file
        pPdfWriter: Holds content for writing file

        Returns:
        pdf_filepath: location of new pdf file

        """
        ## Create PDF folder and filepath
        pdf_folder = re.sub(r"[^\\]+$","pdf_folder",pDirectory)
        pdf_filename = re.sub(r"^(.+)",r"\1.pdf",pFilename)
        pdf_filepath = os.path.join(pdf_folder,pdf_filename)
        os.makedirs(pdf_folder,exist_ok=True)

         ## Generate PDF File
        new_pdf_file = open(pdf_filepath,'wb')

        pPdfWriter.write(new_pdf_file)

        new_pdf_file.close()

        return pdf_filepath

def generate_txt(pDirectory,pPdfFilepath,pFilename):

    """
    Generates text file from pdf file. Exports content to folder txt_folder.

    Params:
    pDirectory: Location to export text file
    pPdfFilepath: Location of pdf file to gather data from
    pFilename: Name of export file

    returns:
    txtFilepath: Location of new txt file.
    """

    ## Create TXT Folder and filepath
    txtFolder = re.sub(r"[^\\]+$","text_folder",pDirectory)
    os.makedirs(txtFolder,exist_ok=True)
    txtFilename = re.sub(r"^(.+)",r"\1.txt",pFilename)
    txtFilepath = os.path.join(txtFolder,txtFilename)

    ## Reading PDF File
    pdfFile = open(pPdfFilepath,'rb')
    pdfReader = PyPDF2.PdfReader(pdfFile)
    pageCount = len(pdfReader.pages)
    print(f"Page Count: {pageCount}")

    ## Write file content
    txtFile = open(txtFilepath,'w',encoding="utf-8")
    for i in range(pageCount):
        pageObj = pdfReader.pages[i] 
        text = pageObj.extract_text()
        txtFile.write(text)
    txtFile.close()
    pdfFile.close()

    return txtFilepath

def get_page_range(pTableOfContents):
        """
        Gathers a list of tuples containg surah,start page, and end page.

        Params:
        pTableOfContents: A nested list variable containing surah and starting page

        Returns:
        vPageRangeList:
        A nested tuple list containing surah, start page, and end page
        """

        vTableOfContents_len = len(pTableOfContents)
        vPageRangeList = []
        for i in range(vTableOfContents_len):
                        
            try:

                vSurah = pTableOfContents[i][0]
                vStartPage = pTableOfContents[i][1]
                vEndPage = pTableOfContents[i+1][1]

            except IndexError:

                print("End of list")
                vSurah = pTableOfContents[i][0]
                vStartPage = pTableOfContents[i][1]
                vEndPage = pTableOfContents[i][1]

            vPageRange = (vSurah,vStartPage,vEndPage)
            print(vPageRange)
            vPageRangeList.append(vPageRange)
        
        return vPageRangeList

def create_export_surah(pFilePathList,pTableOfContents):

    """
    Takes in filepath list and table of contents containing surah name and page count.
    A pdf and text files are created and outputted for each surah.
    Calls function gather_pages to return pages from the holy Quran.

    Params: 

    pFilePathList: Contains filepath to the holy Quran
    pTableOfContents: Contains Surah name and Starting Page

    returns:
    None

    """

    vPageRangeList = get_page_range(pTableOfContents)

    for original_filepath in pFilePathList:

        original_pdf_file = open(original_filepath,'rb')
        
        pdfReader = PyPDF2.PdfReader(original_pdf_file)
        
        for PageRange in vPageRangeList:
        
            vSurah = PageRange[0]
            vStartPage = PageRange[1]
            vEndPage = PageRange[2]

            print(f"Surah: {vSurah}\nStart Page {vStartPage}: End Page {vEndPage}")

            pdfWriter = PyPDF2.PdfWriter()
            pdfWriter = gather_pages(pdfReader,pdfWriter,vStartPage,vEndPage)

            ##Create new filename
            original_filename = os.path.basename(original_filepath)
            pattern = r"^(.+?)\.(\w+)$"
            match = re.match(pattern,original_filename)
            original_filename_no_extension = match.group(1)
            
            new_filename = f"{original_filename_no_extension}{vSurah}"

            vNewPdfFilepath = generate_pdf(original_filepath,new_filename,pdfWriter)
            vNewTxtFilepath = generate_txt(original_filepath,vNewPdfFilepath,new_filename)

        original_pdf_file.close()

directory = os.getcwd()
vFilename = "Bridges_Translation_of_quran.pdf"
vFilePathList = find_holy_quran(directory,vFilename)
vTableOfContents = get_surah_pages(vFilePathList)
create_export_surah(vFilePathList,vTableOfContents)


    