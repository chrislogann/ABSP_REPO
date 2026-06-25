import os
import pypdf
import argparse

"""
Script extracts text from PDF files using the pypdf library.
Exported text files are outputted to the folder 'pdf_text_19'.
Export filename is {book_title}_extract.txt
"""

def get_filepath(directory, target_filename):
    """Recursively search for a file in a directory."""
    for folderpath, subfolder, filenames in os.walk(directory):
        if target_filename in filenames:
            return os.path.join(folderpath, target_filename)
    return None

def main(vFilename):
    vDirectory = os.getcwd()
    
    # 1. Find the PDF file
    file_path = get_filepath(vDirectory, vFilename)
    
    if not file_path:
        print(f"Error: Could not find '{vFilename}' in {vDirectory} or its subdirectories.")
        return

    # 2. Setup output folder (Create if it doesn't exist)
    txtFolder = os.path.join(vDirectory, "pdf_text_19")
    os.makedirs(txtFolder, exist_ok=True)
    
    # 3. Format the output filename (Removes .pdf and adds _extract.txt)
    base_name = os.path.splitext(vFilename)[0]
    txtFilename = f"{base_name}_extract.txt"
    txtFilepath = os.path.join(txtFolder, txtFilename)
    
    print(f"Reading from: {file_path}")
    print(f"Outputting to: {txtFilepath}")

    # 4. Load PDF and Extract Text
    try:
        # Use context managers for both reading and writing
        with open(file_path, 'rb') as pdfFile, open(txtFilepath, 'w', encoding="utf-8") as txtFile:
            pdfReader = pypdf.PdfReader(pdfFile)
            pageCount = len(pdfReader.pages)
            print(f"Page Count: {pageCount}")
            
            for i in range(pageCount):
                pageObj = pdfReader.pages[i] 
                text = pageObj.extract_text()
                
                # Write extracted text to file (filtering out None types if a page is blank)
                if text:
                    # Write the page number identifier
                    txtFile.write(f"\n\n--- Page {i + 1} ---\n\n")
                    # Write the actual text
                    txtFile.write(text)
                    
        print("Extraction complete!")
        
    except Exception as e:
        print(f"An error occurred during extraction: {e}")

if __name__ == "__main__":
    # Setup argument parser
    parser = argparse.ArgumentParser(description="Extract text from a PDF file.")
    parser.add_argument(
        "filename", 
        help="The name of the PDF file to extract text from (e.g., 'The Creative Act_ A Way of Being.pdf')"
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    # Call main with the provided filename
    main(args.filename)