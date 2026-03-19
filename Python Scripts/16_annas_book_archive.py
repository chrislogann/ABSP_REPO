import requests
from bs4 import BeautifulSoup
import re
from dotenv import load_dotenv
import os
import imapclient
import pyzmail
import smtplib
from email.message import EmailMessage
import isbnlib
import diskcache
import logging

"""
Script 16_annas_book_archive reads an email and downloads related books from Anna's Book Archive.
"""

class EmailClient:

    """
    Manages interactions with email.
    """

    def __init__(self,email,key,subjects):
        self.email = email
        self.key = key
        self.subjects = subjects

    ## Access email inbox and return book content from email
    def get_email_content(self):

        """
        Returns isbns from emails with specific subject.

        Params:
        self: class variables for EmailClient

        Returns:
        raw_messages: data from email body

        """

        logging.info("Opening email inbox for %s",self.email)
        with imapclient.IMAPClient("imap.gmail.com", ssl=True) as imap_obj:
            imap_obj.login(self.email, self.key)
            imap_obj.select_folder("INBOX", readonly=True)

            uids = []
            for subject in self.subjects:
                logging.debug("Downloading uids with subject %s",subject)
                uids += imap_obj.search(["UNSEEN","SUBJECT",subject])

            if not uids:
                logging.info("No matching unread emails found")
                return {}

            logging.info("Found %d matching email(s)", len(uids))

            raw_messages = imap_obj.fetch(uids, ['BODY[]', 'FLAGS'])

        return raw_messages,uids

    def process_email_content(self, raw_messages):

        """
        Parses email bodies to extract isbn numbers.

        Params:
        self: class variables from EmailClient

        Returns:
        isbn_set: a unique list of isbn numbers

        """

        logging.info("Extracting ISBNs from %d email(s)", len(raw_messages))

        pattern = re.compile(r"\b(?:97[89]\d{10}|\d{9}[\dX])\b")
        isbn_set = set()

        for uid, data in raw_messages.items():

            logging.debug("Processing email UID %s", uid)

            try:
                message = pyzmail.PyzMessage.factory(data[b'BODY[]'])
            except Exception as e:
                logging.warning("Failed to parse email UID %s: %s", uid, e)
                continue

            if message.text_part:
                body = message.text_part.get_payload().decode(
                    message.text_part.charset or "utf-8",
                    errors="replace"
                )

            elif message.html_part:
                body = message.html_part.get_payload().decode(
                    message.html_part.charset or "utf-8",
                    errors="replace"
                )
                soup = BeautifulSoup(body, "html.parser")
                body = soup.get_text()

            else:
                continue

            isbn_set.update(pattern.findall(body))

        logging.info("Found %d unique ISBN(s)", len(isbn_set))

        return isbn_set
    
    ## Send reply email upon successful completion
    def send_completion_email(self, processed_isbns):

        logging.info("Sending completion email")

        msg = EmailMessage()
        msg["Subject"] = "Book Download Completed"
        msg["From"] = self.email
        msg["To"] = self.email

        body = "The following ISBNs were processed successfully:\n\n"
        body += "\n".join(processed_isbns)

        msg.set_content(body)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(self.email, self.key)
            smtp.send_message(msg)

        logging.info("Completion email sent")

    ## Moves completed request emails to inbox folder.
    def move_completed_emails(self, uids, folder_name="Processed Book Requests"):

        logging.info("Moving processed emails to folder: %s", folder_name)

        with imapclient.IMAPClient("imap.gmail.com", ssl=True) as imap_obj:
            imap_obj.login(self.email, self.key)
            imap_obj.select_folder("INBOX", readonly=False)

            # Create folder if not exists
            folders = [f[2] for f in imap_obj.list_folders()]
            if folder_name not in folders:
                imap_obj.create_folder(folder_name)

            # Mark as read
            imap_obj.add_flags(uids, [imapclient.SEEN])

            # Move emails
            imap_obj.move(uids, folder_name)

        logging.info("Emails moved successfully")

class AnnasArchiveClient:

    """
    Manages interactions with Anna's Book Archive.
    """

    def __init__(self,session,key):
        self.session = session
        self.key = key

    ## Connect to website and return download data
    def get_book_data(self, isbn):
        
        """
        Returns book content necessary for interactions with API.

        Params:

        self: class variables from AnnasArchiveClient
        isbn: unique id for a specific book.
        """

        logging.info("Searching Anna's Archive for ISBN %s", isbn)

        query_url = f"https://annas-archive.gl/search?q={isbn}"

        res = self.session.get(query_url, timeout=20)
        res.raise_for_status()

        soup = BeautifulSoup(res.text, "html.parser")

        bookElems = soup.select("div",{"class":"flex pt-3 pb-3 border-b last:border-b-0 border-gray-100"})
        logging.debug("Found %d raw result(s)", len(bookElems))

        download_list = []
        formats_seen = set()

        for bookElem in bookElems:

            metaElem = bookElem.select_one("div.font-semibold")
            if not metaElem:
                logging.debug("Skipping entry: no metadata element")
                continue

            meta_text = metaElem.get_text(strip=True).upper()

            if "ENGLISH" not in meta_text:
                continue

            book_format = None
            for fmt in ("EPUB", "PDF"):
                if fmt in meta_text:
                    book_format = fmt
                    break

            if not book_format or book_format in formats_seen:
                continue

            md5_link = bookElem.select_one('a[href^="/md5/"]')
            if not md5_link:
                logging.debug("Skipping entry: no md5 link")
                continue

            href = md5_link.get("href", "")
            parts = href.split("/")
            if len(parts) < 3:
                logging.debug("Invalid md5 href: %s", href)
                continue

            md5 = parts[-1]

            logging.debug("Adding ISBN %s with md5 %s (%s)", isbn, md5, book_format)

            download_list.append((isbn, md5, book_format))
            formats_seen.add(book_format)

            if len(formats_seen) == 2:
                break

        logging.info("Returning %d download(s) for ISBN %s", len(download_list), isbn)

        return download_list

    ## Get book download link
    def get_download_link(self, md5):
        
        """
        Utilizes API to get download link from Anna's book archive.
        Number of downloads contigent on Anna's book archive subscription.

        Params:
        md5: hash id for a specific download
        key: user API key provided by Anna's book archive.

        Returns:
        download_link: a link that allows downloading books

        """

        url = "https://annas-archive.gl/dyn/api/fast_download.json"

        params = {
            "md5": md5,
            "key": self.key
        }

        res = self.session.get(url, params=params, timeout=20)
        res.raise_for_status()

        try:
            data = res.json()
        except ValueError:
            logging.warning("Invalid JSON response for md5 %s", md5)
            return None

        download_link = data.get("download_url")

        if download_link:
            return download_link

        logging.warning("No download link found for md5 %s", md5)
        return None

class MetadataService:

    """
    Returns isbn metadata from package isbnlib.
    """

    def __init__(self):
        self.cache = diskcache.Cache("./isbn_cache")

    ## Returns isbn metadata
    def get_metadata(self,isbn):

        """
        Returns metadata from an isbn.
        Data is either cached or referenced from package isbnlib.

        Params:

        self: class variables for MetadataService
        isbn: unique id for specific book

        Returns:
        meta: metadata pertaining to a given isbn number.

        """

        logging.info("Searching for isbn metadata")

        meta = self.cache.get(isbn)
        if meta:
            logging.debug("Cache hit for ISBN %s", isbn)
            return meta
        
        try:
            meta = isbnlib.meta(isbn, service="openl")
            logging.debug("Found isbn %s metadata from package isbnlib",isbn)
        except Exception:
            meta = None
            logging.warning("isbnlib cannot find isbn %s",isbn)

        if not meta:
            meta = {
                "ISBN-13": isbn,
                "Title": "Unknown Title",
                "Authors": ["Unknown Author"]
            }
            logging.debug(f"isbn {isbn} not found neither cache or package isbnlib")

        self.cache.set(isbn,meta, expire=None)
        logging.debug("Setting cache for isbn metadata for isbn %s",isbn)
        return meta

class FileManager:

    """
    Handles operations for export file.
    """
    
    def __init__(self,directory,session):
        self.session = session
        self.folderpath = self.create_folderpath(directory)

    @staticmethod
    def _clean_filename(filename):

        """
        Removes illegal characters from filename.
        Noted as a private class for FileManager.
        """
            
        filename = re.sub(r'[\\/*?:"<>|]', "", filename)
        logging.debug("Cleaned filename %s",filename)
        return filename

    ## Find book infomation from isbn
    def generate_filename(self,metadata,book_format):

        """
        Outputs a filename from given isbn metadata.
        """

        isbn = metadata['ISBN-13']
        title = metadata['Title']
        authors = ", ".join(metadata["Authors"])

        filename = f"{isbn}-{title} {authors} {book_format}.{book_format.lower()}"
        filename = self._clean_filename(filename)
        logging.debug("Filename %s generated",filename)
        return filename

    ## Create export folder
    def create_folderpath(self,directory):

        """
        Creates export folder to house export files.
        """

        folderpath = os.path.join(directory,"downloaded_books")
        os.makedirs(folderpath, exist_ok = True)
        logging.info("Folderpath %s created/found",folderpath)
        return folderpath

    # Download and create file
    def download_file(self,filepath,download_link):
            
            """
            Downloads file from a given download_link from Anna's Book Archive API.
            """
            
            logging.info("Downloading file for path %s",filepath)
            res = self.session.get(download_link, stream=True, timeout=20)
            res.raise_for_status()

            with open(filepath,'wb') as bookFile:
                for chunk in res.iter_content(100000):
                    if chunk:
                        bookFile.write(chunk)

class LoggingManager:

    """
    Simple logging manager: writes logs to console and file (append mode).
    """

    def __init__(self, directory, log_file="book_downloader.log"):
        self.folderpath = self.create_folderpath(directory)
        self.log_file_path = os.path.join(self.folderpath, log_file)

    def create_folderpath(self,directory):

        self.folderpath = os.path.join(directory, "Log")
        os.makedirs(self.folderpath, exist_ok=True)

        return self.folderpath
    
    def start_logging(self):
        """
        Initialize logging: console + append to log file.
        """
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[
                logging.StreamHandler(),  # console
                logging.FileHandler(self.log_file_path, mode='a', encoding='utf-8')  # file append
            ]
        )
        logging.info(f"Logging started. Logs will append to {self.log_file_path}")
        
class BookDownloaderApp:

    """
    Organizes the execution defined classes and functions.
    """

    def __init__(self):

        load_dotenv()
        self.book_key = os.getenv("book_key")
        self.book_email_subject = os.getenv("book_email_subject").split(",")
        self.user_email = os.getenv("personal_email")
        self.user_passkey = os.getenv("personal_passkey")
        self.directory = os.getenv("book_directory")

        self.session = requests.Session()

        ## Start logging
        log_manager = LoggingManager(self.directory)
        log_manager.start_logging()  # configure logging for console + file

        logging.info("Initializing BookDownloaderApp")

        # Initialize services
        self.email_client = EmailClient(self.user_email, self.user_passkey, self.book_email_subject)
        self.archive_client = AnnasArchiveClient(self.session, self.book_key)
        self.metadata_service = MetadataService()
        self.file_manager = FileManager(self.directory,self.session)

    def run(self):

        """
        Executes functions to gather and export an ebook.
        """

        logging.info("Starting BookDownloaderApp")

        # Step 1: Get email content
        raw_messages, uids = self.email_client.get_email_content()
        if not raw_messages:
            return

        isbn_set = self.email_client.process_email_content(raw_messages)

        # Step 2: Get book data from Anna's Archive
        books = [
            book
            for isbn in isbn_set
            for book in self.archive_client.get_book_data(isbn)
        ]

        if not books:
            logging.info("No books found for given ISBNs")
            return

        # Step 3: Sort (EPUB first, PDF second)
        sorted_books = sorted(books, key=lambda x: 0 if x[2] == 'EPUB' else 1)

        processed_isbns = set()

        for isbn, md5, book_format in sorted_books:

            if isbn in processed_isbns:
                continue

            # Step 4: Metadata
            metadata = self.metadata_service.get_metadata(isbn)

            # Step 5: Filename
            filename = self.file_manager.generate_filename(metadata, book_format)
            filepath = os.path.join(self.file_manager.folderpath, filename)

            logging.info("Processing file %s", filename)

            if any(isbn in fname for fname in os.listdir(self.file_manager.folderpath)):
                logging.info("File already exists: %s", f"{isbn}: {metadata['Title']}")
                processed_isbns.add(f"{isbn}: {metadata['Title']}")
                continue

            # Step 6: Get download link
            download_link = self.archive_client.get_download_link(md5)

            if not download_link:
                continue

            # Step 7: Download file
            self.file_manager.download_file(filepath, download_link)

            processed_isbns.add(f"{isbn}: {metadata['Title']}")

        if processed_isbns:
            self.email_client.send_completion_email(processed_isbns)
            self.email_client.move_completed_emails(uids)

        logging.info("BookDownloaderApp finished")

app = BookDownloaderApp()
app.run()
