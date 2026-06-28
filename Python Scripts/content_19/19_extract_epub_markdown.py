import os
import argparse
import ebooklib
import re
from ebooklib import epub
from markdownify import markdownify as md

"""
Script extracts text from EPUB files and converts it to formatted Markdown.
Exported .md files are outputted to the folder 'epub_markdown_output'.
Images are exported to the folder 'images' to retain working relative paths.
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

    # 2. Setup output folder for Markdown
    mdFolder = os.path.join(vDirectory, "epub_markdown_output")
    os.makedirs(mdFolder, exist_ok=True)
    
    # Setup output folder for Images
    imagesFolder = os.path.join(vDirectory, "images")
    os.makedirs(imagesFolder, exist_ok=True)
    
    # 3. Format the output filename (Removes .epub and adds _extract.md)
    base_name = os.path.splitext(vFilename)[0]
    mdFilename = f"{base_name}_extract.md"
    mdFilepath = os.path.join(mdFolder, mdFilename)

    try:
        # Load the EPUB
        book = epub.read_epub(file_path)
        
        # 4. Extract and save all images
        for item in book.get_items_of_type(ebooklib.ITEM_IMAGE):
            # Extract just the filename from the internal epub path
            img_filename = os.path.basename(item.get_name())
            img_filepath = os.path.join(imagesFolder, img_filename)
            
            with open(img_filepath, "wb") as img_file:
                img_file.write(item.get_content())
                
        print(f"Images extracted to '{imagesFolder}' directory.")

        # 5. Extract text chapters
        chapters = list(book.get_items_of_type(ebooklib.ITEM_DOCUMENT))
        
        # Open output file
        with open(mdFilepath, 'w', encoding='utf-8') as mdFile:
            for i, chapter in enumerate(chapters):
                html_content = chapter.get_body_content().decode('utf-8', errors='ignore')
                
                # Convert the HTML body to Markdown
                markdown_text = md(html_content, heading_style="ATX").strip()

                markdown_text = re.sub(r'\[(.*?)\]\([^)]*\.xhtml[^)]*\)', r'\1', markdown_text)
                markdown_text = re.sub(r'\[(.*?)\]\([^)]*\.html[^)]*\)', r'\1', markdown_text)

                # Write extracted text to file
                if markdown_text:
                    mdFile.write(f"\n\n---\n\n## Section {i + 1}\n\n")
                    mdFile.write(markdown_text)
                    
        print(f"Extraction complete! Saved to {mdFilepath}")
        
    except Exception as e:
        print(f"An error occurred during extraction: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert an EPUB file to formatted Markdown.")
    parser.add_argument(
        "filename", 
        help="The name of the EPUB file to convert (e.g., 'The Creative Act_ A Way of Being.epub')"
    )
    
    args = parser.parse_args()
    main(args.filename)