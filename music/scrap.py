from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import csv

BASE_URL = "https://www.versuri.ro"
START_URL = "https://www.versuri.ro/artist/lidia-buble/"

def scroll_and_collect_links(driver, pause=1):
    last_height = driver.execute_script("return document.body.scrollHeight")
    links_set = set()

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(pause)

        elems = driver.find_elements(By.CSS_SELECTOR, 'a[href^="/versuri/"]')
        for el in elems:
            title = el.text.strip()
            href = el.get_attribute("href")
            if href and title:
                links_set.add((title, href))

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    return list(links_set)

def main():
    options = Options()
    options.add_argument("--headless")  
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=options)

    try:
        print(f"🔎 Se încarcă pagina: {START_URL}")
        driver.get(START_URL)
        time.sleep(3)

        print("🔄 Derulez pagina și colectez linkuri...")
        song_links = scroll_and_collect_links(driver)

        print(f"✅ Găsite {len(song_links)} melodii.")
        with open("melodii_links.csv", "+a", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(song_links)

        print("📁 Salvate în melodii_links.csv")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
