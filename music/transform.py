from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

import pandas as pd

import time

import csv

INPUT_FILE = "melodii_links.csv"
OUTPUT_FILE = "melodii_versuri.csv"

def setup_driver():
    options = Options()
    options.add_argument("--headless=new")  
    options.add_argument("--window-size=1920,1080")
    service = Service("music/chromedriver.exe")  
    return webdriver.Chrome(service=service, options=options)

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def extrage_versuri(driver, url):
    try:
        driver.get(url)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@id="textdiv"]/p'))
        )

        p_tags = driver.find_elements(By.XPATH, '//div[@id="textdiv"]/p')
        versuri = "\n".join([p.text.strip() for p in p_tags if p.text.strip()])
        return versuri

    except Exception as e:
        print(f"Eroare la {url}: {e}")
        return ""

def get_versuri(driver, url):
    driver.get(url)
    time.sleep(2)  

    try:
        title_text = driver.title
        if "versuri" in title_text.lower() and " - " in title_text:
            parts = title_text.lower().replace(" versuri", "").split(" - ", 1)
            artist = parts[0].strip().title()
            titlu = parts[1].strip().title()
        else:
            artist = ""
            titlu = title_text

        versuri = extrage_versuri(driver, url)
        return artist, titlu, versuri

    except Exception as e:
        print(f"Eroare la {url}: {e}")
        return "", "", ""

def main():
    driver = setup_driver()
    results = []

    with open(INPUT_FILE, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader) 
        for i, (titlu_original, link) in enumerate(reader, 1):
            print(f"[{i}]  Accesez: {link}")
            artist, titlu, versuri = get_versuri(driver, link)
            if versuri:
                for vers in versuri.split("\n"):
                    if vers.strip(): 
                        results.append([artist, titlu, vers.strip()])
            else:
                print(f"   Versuri goale.")
            time.sleep(1)  

    driver.quit()

    with open(OUTPUT_FILE, "w", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Artist", "Titlu", "Versuri"])
        writer.writerows(results)

    print(f" Salvate {len(results)} melodii în {OUTPUT_FILE}")


if __name__ == "__main__":
    main()