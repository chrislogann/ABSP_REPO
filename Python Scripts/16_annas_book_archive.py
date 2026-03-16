import requests
from bs4 import BeautifulSoup
import re
from dotenv import load_dotenv
import os
import imapclient
import pyzmail
import isbnlib
import diskcache
import logging

logging.basicConfig(level=logging.DEBUG,format=' %(asctime)s %(levelname)s - %(message)s')
## Create request session
session = requests.Session()

"""
Script 16_annas_book_archive reads an email and downloads related books from Anna's Book Archive.
"""

## Access email inbox and return book content from email
def get_email_content(user_email,user_key):
    with imapclient.IMAPClient("imap.gmail.com", ssl=True) as imap_obj:
        imap_obj.login(user_email, user_key)
        imap_obj.select_folder("INBOX", readonly=True)
        UIDs = imap_obj.search(["UNSEEN","SUBJECT", "DOWNLOAD BOOKS FROM ARCHIVE"])
        raw_messages = imap_obj.fetch(UIDs, ['BODY[]', 'FLAGS'])

    return raw_messages

def process_email_content(raw_messages):

    pattern = re.compile(r"\b(?:97[89]\d{10}|\d{9}[\dX])\b")

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

    res = session.get(query_url, timeout=20)
    res.raise_for_status()

    soupReader = BeautifulSoup(res.text, "html.parser")

    bookElems = soupReader.find_all("div", {"class":"flex pt-3 pb-3 border-b last:border-b-0 border-gray-100"})
    
    download_list = []
    formats_seen = set()
    for bookElem in bookElems:

        metaElem = bookElem.select_one("div.font-semibold")
        if not metaElem:
            continue

        meta_text = metaElem.get_text().upper()

        if "ENGLISH" not in meta_text:
            continue

        if "EPUB" in meta_text:
            book_format = "EPUB"
        elif "PDF" in meta_text:
            book_format = "PDF"
        else:
            continue

        if book_format in formats_seen:
            continue

        md5_link = bookElem.select_one('a[href^="/md5/"]')

        if not md5_link:
            continue

        md5 = md5_link["href"].split("/")[-1]
        breakpoint()
        ##Add to download_list
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

    res = session.get(url, params=params, timeout=20)
    res.raise_for_status()

    try:
        data = res.json()
    except ValueError:
        return None

    download_link = data.get("download_url")

    if download_link:
        return download_link

## Returns isbn metadata
cache = diskcache.Cache("./isbn_cache")

def get_metadata(isbn):
    if isbn in cache:
        print("using cache")
        return cache[isbn]
    
    try:
        meta = isbnlib.meta(isbn, service="openl")
    except Exception:
        meta = None

    if not meta:
        meta = {
            "ISBN-13": isbn,
            "Title": "Unknown Title",
            "Authors": ["Unknown Author"]
        }

    cache.set(isbn,meta, expire=None)
    return meta

## Find book infomation from isbn
def clean_filename(filename):
        filename = re.sub(r'[\\/*?:"<>|]', "", filename)

        return filename

def generate_filename(metadata,book_format):

    isbn = metadata['ISBN-13']
    title = metadata['Title']
    authors = ", ".join(metadata["Authors"])

    filename = f"{isbn}-{title} {authors} {book_format}.{book_format.lower()}"
    filename = clean_filename(filename)

    return filename

## Create export folder
def create_folderpath():

    directory = os.getcwd()
    folderpath = os.path.join(directory,"downloaded_books")
    os.makedirs(folderpath, exist_ok = True)

    return folderpath

    # export_filepath = os.path.join(folderpath,filename)
# Download and create file
def create_file(filepath,download_link):
        
        res = session.get(download_link, stream=True, timeout=20)
        res.raise_for_status()

        with open(filepath,'wb') as bookFile:
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
    books = [book for isbn in isbn_set for book in get_book_data(isbn)]

    ## Sorted to process EPUB files first and PDF files second if necessary

    folderpath = create_folderpath()

    sorted_books = sorted(books, key=lambda x: 0 if x[2] == 'EPUB' else 1)
    seen_isbn = set()
    for book in sorted_books:
        
        isbn, md5, book_format = book

        if isbn in seen_isbn:
            continue

        book_metadata = get_metadata(isbn)
        filename = generate_filename(book_metadata,book_format)
        print(filename)

        export_filepath = os.path.join(folderpath,filename)

        if os.path.exists(export_filepath):
            print("path exists")
            seen_isbn.add(isbn)
            continue

        ## Only gets a 50 downloads a day. Use wisely
        download_link = get_download_link(md5,book_key)

        if not download_link:
            continue

        create_file(export_filepath,download_link)

        seen_isbn.add(isbn)

main()