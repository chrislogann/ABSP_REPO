#! python3
# multidownloadXkcd.py - Downloads XKCD comics using multiple threads.

"""
Script 15_multidownloadXkcd.py downloads new web comics not stored in the xkcd folder.
This script runs once a day.
"""

import requests, os, bs4, threading, time, datetime

os.makedirs('xkcd', exist_ok=True)

def downloadXkcd(startComic, endComic):

    for urlNumber in range(startComic, endComic):

        print('Downloading page http://xkcd.com/%s...' % (urlNumber))

        res = requests.get('https://xkcd.com/%s' % (urlNumber))
        res.raise_for_status()

        soup = bs4.BeautifulSoup(res.text, "lxml")

        comicElem = soup.select('#comic img')

        if comicElem == []:
            print('Could not find comic image.')
        else:

            comicUrl = 'https:' + comicElem[0].get('src')

            print('Downloading image %s...' % comicUrl)

            res = requests.get(comicUrl)
            res.raise_for_status()

            xkcd_folderpath = os.path.join(os.getcwd(),'xkcd')
            folder_content = os.listdir(xkcd_folderpath)
            if os.path.basename(comicUrl) in folder_content:
                print("Content already exists in folder")
                continue

            print("Adding new comic")

            imageFile = open(os.path.join('xkcd', os.path.basename(comicUrl)), 'wb')

            for chunk in res.iter_content(100000):
                imageFile.write(chunk)

            imageFile.close()

while True:

    downloadThreads = []

    for i in range(1, 1400, 100):

        downloadThread = threading.Thread(target=downloadXkcd, args=(i, i + 99))

        downloadThreads.append(downloadThread)

        downloadThread.start()

    for downloadThread in downloadThreads:
        downloadThread.join()

    print('Done.')

    print("Waiting one day until next execution.")
    time.sleep(24*60*60)

