import os
import argparse
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup

"""
Script extracts text from EPUB files using the EbookLib and BeautifulSoup libraries.
Exported text files are outputted to the folder 'epub_text_output'.
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
    
    # 1. Find the EPUB file
    file_path = get_filepath(vDirectory, vFilename)
    
    if not file_path:
        print(f"Error: Could not find '{vFilename}' in {vDirectory} or its subdirectories.")
        return

    # 2. Setup output folder (Create if it doesn't exist)
    txtFolder = os.path.join(vDirectory, "epub_text_output")
    os.makedirs(txtFolder, exist_ok=True)
    
    # 3. Format the output filename (Removes .epub and adds _extract.txt)
    base_name = os.path.splitext(vFilename)[0]
    txtFilename = f"{base_name}_extract.txt"
    txtFilepath = os.path.join(txtFolder, txtFilename)
    
    print(f"Reading from: {file_path}")
    print(f"Outputting to: {txtFilepath}")

    # 4. Load EPUB and Extract Text
    try:
        # Load the EPUB file
        book = epub.read_epub(file_path)
        
        # EPUBs are structured by HTML documents rather than pages. 
        # We grab all the document items (chapters, sections, title pages, etc.)
        chapters = list(book.get_items_of_type(ebooklib.ITEM_DOCUMENT))
        print(f"Section Count: {len(chapters)}")
        
        # Open the target text file for writing
        with open(txtFilepath, 'w', encoding="utf-8") as txtFile:
            
            for i, chapter in enumerate(chapters):
                # Extract the raw HTML content from the chapter
                html_content = chapter.get_body_content()
                
                # Use BeautifulSoup to parse the HTML and extract only the plain text
                soup = BeautifulSoup(html_content, 'html.parser')
                
                # get_text() extracts text, separating blocks with newlines and stripping whitespace
                text = soup.get_text(separator='\n\n', strip=True)
                
                # Write extracted text to file (filtering out blank sections)
                if text:
                    # Write the section number identifier (analogous to page numbers)
                    txtFile.write(f"\n\n--- Section {i + 1} ---\n\n")
                    # Write the actual text
                    txtFile.write(text)
                    
        print("Extraction complete!")
        
    except Exception as e:
        print(f"An error occurred during extraction: {e}")

if __name__ == "__main__":
    # Setup argument parser
    parser = argparse.ArgumentParser(description="Extract text from an EPUB file.")
    parser.add_argument(
        "filename", 
        help="The name of the EPUB file to extract text from (e.g., 'The Creative Act_ A Way of Being.epub')"
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    # Call main with the provided filename
    main(args.filename)