import requests
from bs4 import BeautifulSoup
import re
from dotenv import load_dotenv
import os
import imapclient
import pyzmail
import isbnlib

"""
Script 16_annas_book_archive reads an email and downloads related books from Anna's Book Archive.
"""

## Access email inbox and return book content from email
def get_email_content(user_email,user_key):
    imap_obj = imapclient.IMAPClient("imap.gmail.com",ssl = True)
    imap_obj.login(user_email,user_key)

    ## Opening inbox folder
    imap_obj.select_folder("INBOX",readonly=True)
    UIDs = imap_obj.search(["UNSEEN","SUBJECT", "DOWNLOAD BOOKS FROM ARCHIVE"])

    ## Getting email content
    raw_messages = imap_obj.fetch(UIDs, ['BODY[]', 'FLAGS'])

    return raw_messages

def process_email_content(raw_messages):

    pattern = re.compile(r"\d{10,13}")

    isbn_set = set()
    for uid, data in raw_messages.items():

        message = pyzmail.PyzMessage.factory(data[b'BODY[]'])

        if message.text_part:

            body = message.text_part.get_payload().decode(message.text_part.charset or "utf-8", errors="replace")

            isbn_set.update(pattern.findall(body))

        elif message.html_part:

            body = message.html_part.get_payload().decode(message.html_part.charset or "utf-8", errors="replace")
            soup_reader = BeautifulSoup(body, "html.parser")
            text = soup_reader.get_text()
            isbns = pattern.findall(text)
            isbn_set.update(isbns)
        
    return isbn_set

## Connect to website and return download data
def get_book_data(isbn):

    query_url = f"https://annas-archive.gl/search?q={isbn}"

    res = requests.get(query_url)
    res.raise_for_status()

    soupReader = BeautifulSoup(res.text, "html.parser")

    bookElems = soupReader.find_all("div", {"class":"flex pt-3 pb-3 border-b last:border-b-0 border-gray-100"})

    download_list = []
    formats_seen = set()
    for bookElem in bookElems:

        ##Getting metadata
        metaElem = bookElem.find("div",{"class":"text-gray-800 dark:text-slate-400 font-semibold text-sm leading-[1.2] mt-2"})
        meta_text = metaElem.get_text()

        ##Only English books
        if "ENGLISH" not in meta_text.upper():
            continue
        
        ##Only PDF or EPUB formats
        if "PDF" in meta_text.upper():
            book_format = "PDF"
        
        elif "EPUB" in meta_text.upper():
            book_format = "EPUB"

        else:
            continue

        ##One book format type per download
        if book_format in formats_seen:
            continue

        md5_href = bookElem.find("a")["href"]
        match = re.search(r"([^\/]+$)",md5_href)

        ##Only Matches
        if not match:
            continue
        
        ##Add to download_list
        md5 = match.group(1)
        download_list.append((isbn,md5,book_format))
        formats_seen.add(book_format)

        ## Break loop once list is populated with PDF and EPUB
        if len(formats_seen) == 2:
            break

    return download_list

## Get book download link
def get_download_link(md5,key):

    url = "https://annas-archive.gl/dyn/api/fast_download.json"

    params = {
        "md5": md5,
        "key": key
    }

    res = requests.get(url, params=params)

    data = res.json()

    if data["download_url"]:
        download_link = data["download_url"]
        print("Download link:", download_link)
        return download_link
    else:
        print("Error:", data["error"])
        return None

## Returns isbn metadata
def get_metadata(isbn):

    metadata = isbnlib.meta(isbn, service='default')

    if not metadata:
        return {
            "isbn": isbn,
            "title": "Unknown Title",
            "authors": ["Unknown Author"]
        }

    return {
        "isbn": metadata.get("ISBN-13", isbn),
        "title": metadata.get("Title", "Unknown Title"),
        "authors": metadata.get("Authors", ["Unknown Author"])
    }

## Find book infomation from isbn
def generate_filename(metadata,book_format):

    def clean_filename(filename):
        filename = re.sub(r'[\\/*?:"<>|]', "", filename)

        return filename

    isbn = metadata['isbn']
    title = metadata['title']
    authors = ", ".join(metadata["authors"])
    file_format = book_format.lower()

    filename = f"{isbn}-{title} {authors} {book_format}.{file_format}"

    filename = clean_filename(filename)

    return filename
	
# Download and create file
def create_file(filename,download_link):
        
        res = requests.get(download_link)
        res.raise_for_status()

        ## Create export folder and filepath
        directory = os.getcwd()
        folderpath = os.path.join(directory,"downloaded_books")
        os.makedirs(folderpath, exist_ok = True)

        export_filepath = os.path.join(folderpath,filename)

        with open(export_filepath,'wb') as bookFile:
            for chunk in res.iter_content(100000):
                bookFile.write(chunk)

## central execution
def main():

    ## Load environment variables
    load_dotenv()
    book_key = os.getenv("book_key")
    user_email = os.getenv("personal_email")
    user_passkey = os.getenv("personal_passkey")

    ## Access
    raw_messages = get_email_content(user_email,user_passkey)
    isbn_set = process_email_content(raw_messages)

    ## Get md5 and file format for each ISBN
    books = []
    for isbn in isbn_set:

        books.extend(get_book_data(isbn))

    ## Sorted to process EPUB files first and PDF files second if necessary
    sorted_books = sorted(books, key=lambda x: 0 if x[2] == 'EPUB' else 1)
    seen_isbn = set()
    for book in sorted_books:
        
        isbn, md5, book_format = book

        if isbn in seen_isbn:
            continue

        download_link = get_download_link(md5,book_key)

        if not download_link:
            continue
        
        metadata = get_metadata(isbn)
        filename = generate_filename(metadata,book_format)
        print(filename)

        create_file(filename,download_link)

        seen_isbn.add(isbn)

main()