from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, os

def get_google_links(pQuery):
    browser = webdriver.Edge()
    browser.get('https://www.google.com/')

    wait = WebDriverWait(browser, 10)
    query = wait.until(EC.element_to_be_clickable((By.NAME, "q")))

    query.send_keys(pQuery)
    time.sleep(1.5)
    query.send_keys(Keys.ENTER)

    input("input when ready")

    pages = browser.find_elements(By.CLASS_NAME,'fl')

    page_href_set = set()
    for page in pages:
        page_href = page.get_attribute("href")
        page_href_set.add(page_href)

    link_href_set = set()
    for href in page_href_set:
        browser.get(href)
        links = browser.find_elements(By.CLASS_NAME,'zReHs')

        for link in links:
            link_href = link.get_attribute("href")
            link_href_set.add(link_href)

    link_href_set_len = len(link_href_set)
    print(f"Links aquired {link_href_set_len}")
    return link_href_set

query = "PINEAPPLE"
urls = get_google_links(query)

os.makedirs('link_list', exist_ok=True)
filename = f"{query}_LINKS.txt"
file = open(os.path.join('link_list', filename),'a')
for url in urls:
    file.write(f"{url}\n")

print("Script Complete")
