import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import re
import imapclient
import pyzmail
import webbrowser

"""
Script 16_auto_unsubscriber scans email inbox for unsubscribe links. Each link is opened
in a webrowser.
"""

## Acessing Email
load_dotenv()
user_email = os.getenv("personal_email")
user_passkey = os.getenv("personal_passkey")

imap_obj = imapclient.IMAPClient("imap.gmail.com",ssl = True)
imap_obj.login(user_email,user_passkey)

## Opening inbox folder
imap_obj.select_folder("INBOX",readonly=True)
UIDs = imap_obj.search(["SINCE", "01-Feb-2026"])

## Getting emails
raw_messages = imap_obj.fetch(UIDs, ['BODY[]', 'FLAGS'])

## Extracting unsubscribe links
pattern = re.compile(r"(?i)(http.*unsubscribe.*)")
unsubscribe_urls = set()
for uid, data in raw_messages.items():

    message = pyzmail.PyzMessage.factory(data[b'BODY[]'])

    if message.text_part:

        body = message.text_part.get_payload().decode(message.text_part.charset or "utf-8", errors="replace")
        
        unsubscribe_url = pattern.search(body)

        if unsubscribe_url:
            unsubscribe_urls.add(unsubscribe_url.group(1))

    elif message.html_part:

        body = message.html_part.get_payload().decode(message.html_part.charset or "utf-8", errors="replace")

        soup_reader = BeautifulSoup(body, "html.parser")
        urlElem = soup_reader.find("a", href=pattern)

        if urlElem:
            unsubscribe_url = urlElem["href"]
            unsubscribe_urls.add(unsubscribe_url)

## Opening unsubscribe links
for url in unsubscribe_urls:
    webbrowser.open(url, new=2)
