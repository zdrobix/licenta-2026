import requests
import csv
import time
import re

from bs4 import BeautifulSoup

BASE_URL = "https://www.poezii.org"
START_URL = "https://www.poezii.org/"

def get_soup(url):
    r = requests.get(url)
    return BeautifulSoup(r.text, "html.parser")

def get_autori_links():
    soup = get_soup(START_URL)
    links = []
    for a in soup.select('a[href^="/poezii/"]'):
        href = a.get('href')
        text = a.text.strip()
        if re.match(r'^/poezii/.+-\d+\.html$', href):
            links.append((text, BASE_URL + href))

    print(f"Găsiți {len(links)} autori.")
    return links

def get_poezii_links(autor_url):
    soup = get_soup(autor_url)
    poezii_links = []

    for a in soup.select('a[href^="/poezie/"]'):
        href = a.get('href')
        titlu = a.text.strip()
        poezii_links.append((titlu, BASE_URL + href))

    print(f"  → {len(poezii_links)} poezii găsite pentru autorul la {autor_url}")
    return poezii_links

def get_poezie(poem_url):
    soup = get_soup(poem_url)
    title_tag = soup.find('h3', class_='clr-title-main')
    if title_tag is None:
        raise ValueError(f"Nu s-a găsit titlul la {poem_url}")
    title = title_tag.text.strip()

    content_tag = soup.find('div', style=lambda value: value and 'white-space: pre-wrap' in value)
    if content_tag is None:
        raise ValueError(f"Nu s-au găsit versuri la {poem_url}")
    content = content_tag.text.strip()
    return title, content

def main():
    autori = get_autori_links()
    
    for autor, autor_url in autori:
        print(f"\nAutor: {autor}")
        poezii_autor = []

        try:
            poezii_links = get_poezii_links(autor_url)
        except Exception as e:
            print(f" Eroare la {autor_url}: {e}")
            continue

        for titlu, link in poezii_links:
            try:
                _, text = get_poezie(link)
                poezii_autor.append([autor, titlu, text])
                print(f"  ↳ {titlu}")
                time.sleep(1)
            except Exception as e:
                print(f"   Eroare poezie: {e}")
                continue

        filename = f"./data_web/poezii_{re.sub(r'[^\w\-]', '_', autor)}.csv"
        with open(filename, "w", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Autor", "Titlu", "Versuri"])
            writer.writerows(poezii_autor)

        print(f"✔ Salvate {len(poezii_autor)} poezii în {filename}")


if __name__ == "__main__":
    main()