import os
import requests
import bs4
import re
import threading
import logging
import time

logging.basicConfig(level=logging.DEBUG,
                    format=' %(asctime)s %(levelname)s - %(message)s')
# logging.disable()

"""
Script gathers all web comics created by Timothy Buckley.
Only new web comics are added.
Content is checked against files in folder ctrl_alt_delete_comics.
"""

# Gather comic webpages
def get_comiclist(pStartNumber, pEndNumber):

    logging.debug("Executing function get_comiclist")
    logging.debug(f"pStartNumber: {pStartNumber}")
    logging.debug(f"pEndNumber: {pEndNumber}")

    vComicList = []

    for i in range(pStartNumber, pEndNumber):

        url = f'https://cad-comic.com/category/all/page/{i}/'

        logging.debug(f"Downloading page {url}")

        res = requests.get(url)
        res.raise_for_status()

        soupReader = bs4.BeautifulSoup(res.text, "html.parser")

        comicElems = soupReader.find_all(
            "div", {"class": "comic-wrapper comic-unlocked"})

        if not comicElems:
            print("No content available. Stopping page scan.")
            return vComicList

        for comicElem in comicElems:

            imgElem = comicElem.find("img")

            if not imgElem:
                continue

            comic_url = imgElem.get("src")
            comic_name = imgElem.get("alt")

            if not comic_url or not comic_name:
                continue

            vComicList.append((comic_url, comic_name))

    logging.debug("Function get_comiclist complete")

    return vComicList


# Export webcomic to folderpath
def export_comic(pComicList):

    logging.debug("Executing Function export_comic")

    exportFolder = os.path.join(os.getcwd(), "ctrl_alt_delete_comics")
    os.makedirs(exportFolder, exist_ok=True)

    existingFiles = set(os.listdir(exportFolder))

    for comic_url, comic_name in pComicList:

        comic_filename = re.sub(r'[\/:*?"<>|]', '', comic_name).strip() + ".png"

        if comic_filename in existingFiles:
            print("Comic already exists. Skipping.")
            continue

        print(f"Adding comic file {comic_filename}")

        res = requests.get(comic_url)
        res.raise_for_status()

        imageFilepath = os.path.join(exportFolder, comic_filename)

        with open(imageFilepath, 'wb') as imageFile:
            for chunk in res.iter_content(100000):
                imageFile.write(chunk)

    logging.debug("Function export_comic complete")


def main(pStartNumber, pEndNumber):

    logging.debug("Executing Function main")
    logging.debug(f"pStartNumber: {pStartNumber}")
    logging.debug(f"pEndNumber: {pEndNumber}")

    vComicList = get_comiclist(pStartNumber, pEndNumber)

    if not vComicList:
        return

    export_comic(vComicList)

    logging.debug("Function main complete")

downloadThreads = []

for i in range(1, 250, 5):

    downloadThread = threading.Thread(
        target=main,
        args=(i, i + 100)
    )

    downloadThreads.append(downloadThread)

    downloadThread.start()

for downloadThread in downloadThreads:
    downloadThread.join()

print('Done.')