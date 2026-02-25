from bs4 import BeautifulSoup
import requests,os,re

"""
Script 11_link_verification seeks to validate working urls.
It collects broken url links that return 404.
"""

def link_verification(pURL):
    res = requests.get(url)
    res.raise_for_status()
    soup = BeautifulSoup(res.text,"html.parser")

    linkElem = soup.find_all('a')

    link_set = set()
    for link in linkElem:

        href = link.get('href')

        if not href:
            continue
        if href.startswith("/"):
            new_url = url.rsplit("/", 1)[0] + "/" + href
            link_set.add(new_url)
        if href.startswith("http"):
            link_set.add(href)

    link_set_len = len(link_set)

    print(f"Links found: {link_set_len}")

    broken_links = set()
    for link in link_set:
        res = requests.get(link)

        if res.status_code == 404:
            broken_links.add(link)

    return broken_links

def generate_file(pURL,pSet):
    os.makedirs('broken_links', exist_ok=True)

    pattern = r"\/\/(.+)"
    match = re.search(pattern, url)
    filename = match.group(1).replace("/","_")
    filename = f"{filename}_broken_links.txt"

    file = open(os.path.join('broken_links', filename),'w')
    for link in broken_links:
        file.write(f"{link}\n")

    print(f"File: {filename} created")


url = "https://stardewvalleywiki.com/Pineapple"

broken_links = link_verification(url)
generate_file(url,broken_links)






