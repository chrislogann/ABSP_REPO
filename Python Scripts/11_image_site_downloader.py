from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
import uuid

def search_images(query):
    browser = webdriver.Edge()
    browser.get('https://images.google.com')

    wait = WebDriverWait(browser, 10)
    search_box = wait.until(EC.element_to_be_clickable((By.NAME, "q")))
    search_box.send_keys(query)
    search_box.send_keys(Keys.ENTER)

    return browser

def download_images(pSRC):
    os.makedirs('internet_images', exist_ok=True)

    res = requests.get(pSRC)
    res.raise_for_status()

    if res.status_code == 200:
        filename = f"{uuid.uuid4().hex}.jpg"

        imageFile = open(os.path.join('internet_images', filename), 'wb')

        for chunk in res.iter_content(100000):
            imageFile.write(chunk)
        imageFile.close()

def Search_and_Download_Images(pQuery):
    driver = search_images(pQuery)
    driver.execute_script("window.scrollTo(0, 0);")
    a = input("Waiting on user input...")

    page_html = driver.page_source
    pageSoup = BeautifulSoup(page_html,"html.parser")
    containers = pageSoup.find_all("div",{"class":"eA0Zlc PZPZlf WghbWd FnEtTd mkpRId m3LIae RLdvSe qyKxnc ivg-i GMCzAd"})

    len_containers = len(containers)

    print(f"Found {len_containers} image containers")

    for i in range(1, len_containers + 1):
        if i % 25 == 0: continue    

        xpath = f'//*[@id="rso"]/div/div/div[1]/div/div/div[{i}]'
        
        try:
            # 1. Click the thumbnail
            thumbnail = driver.find_element(By.XPATH, xpath)
            thumbnail.click()
            
            # 2. Wait for the preview panel image to actually exist
            time.sleep(1.5) # Short wait for the animation and URL swap
            
            # This selector targets the large image in the preview pane
            actual_images = driver.find_elements(By.CSS_SELECTOR, 'img')
            
            for img in actual_images:
                src = img.get_attribute('src')
                if src and src.startswith('https:') and not "gstatic" in src and not "google" in src:
                    print(f"Found high-res URL: {src}")
                    download_images(src)
                    break # Move to the next thumbnail once found

        except Exception as e:
            print(f"Skipping index {i} due to error: {e}")

Search_and_Download_Images("Peter Griffin")


