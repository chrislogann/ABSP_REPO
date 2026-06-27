import os
import argparse
import ebooklib
from ebooklib import epub
from markdownify import markdownify as md

"""
Script extracts text from EPUB files and converts it to formatted Markdown.
Exported .md files are outputted to the folder 'epub_markdown_output'.
Export filename is {book_title}_extract.md
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
    mdFolder = os.path.join(vDirectory, "epub_markdown_output")
    os.makedirs(mdFolder, exist_ok=True)
    
    # 3. Format the output filename (Removes .epub and adds _extract.md)
    base_name = os.path.splitext(vFilename)[0]
    mdFilename = f"{base_name}_extract.md"
    mdFilepath = os.path.join(mdFolder, mdFilename)
    
    print(f"Reading from: {file_path}")
    print(f"Outputting to: {mdFilepath}")

    # 4. Load EPUB and Convert to Markdown
    try:
        book = epub.read_epub(file_path)
        chapters = list(book.get_items_of_type(ebooklib.ITEM_DOCUMENT))
        print(f"Section Count: {len(chapters)}")
        
        # Open the target Markdown file for writing
        with open(mdFilepath, 'w', encoding="utf-8") as mdFile:
            
            for i, chapter in enumerate(chapters):
                # EPUB body content is stored as bytes, so we decode it to a UTF-8 string
                html_content = chapter.get_body_content().decode('utf-8', errors='ignore')
                
                # Convert the HTML body to Markdown
                # heading_style="ATX" forces headers to use the '#' syntax instead of underlining
                markdown_text = md(html_content, heading_style="ATX").strip()
                
                # Write extracted text to file (filtering out blank sections)
                if markdown_text:
                    # Write a Markdown horizontal rule and Section header
                    mdFile.write(f"\n\n---\n\n## Section {i + 1}\n\n")
                    
                    # Write the converted markdown text
                    mdFile.write(markdown_text)
                    
        print(f"Extraction complete! Saved to {mdFilename}")
        
    except Exception as e:
        print(f"An error occurred during extraction: {e}")

if __name__ == "__main__":
    # Setup argument parser
    parser = argparse.ArgumentParser(description="Convert an EPUB file to formatted Markdown.")
    parser.add_argument(
        "filename", 
        help="The name of the EPUB file to convert (e.g., 'The Creative Act_ A Way of Being.epub')"
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    # Call main with the provided filename
    main(args.filename)