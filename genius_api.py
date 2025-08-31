import csv
import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import pandas as pd

load_dotenv()
GENIUS_TOKEN = os.getenv("GENIUS_TOKEN")
BASE_URL = "https://api.genius.com"


def search_song(query):
    headers = {"Authorization": f"Bearer {GENIUS_TOKEN}"}
    response = requests.get(BASE_URL + "/search", params={"q": query}, headers=headers)
    data = response.json()

    if not data["response"]["hits"]:
        return None

    song_info = data["response"]["hits"][0]["result"]
    return song_info

def get_lyrics(url):
    response = requests.get(url)
    response.raise_for_status()
        
    soup = BeautifulSoup(response.text, "html.parser")
        
    lyrics_divs = soup.find_all("div", attrs={"data-lyrics-container": "true"})
    if not lyrics_divs:
        print("Lyrics div not found.")
        return None
    
    lyrics = []
    for div in lyrics_divs:
        text = div.get_text(separator="\n").strip()
        if text:
            lyrics.extend(text.split("\n"))
    
    return [l for l in lyrics if "[" not in l 
            and "]" not in l 
            and "This Is" not in l
            and "Read More" not in l
            and "Lyrics" not in l
            and l.strip() != ""
            and "Contributors" not in l]

def save_lyrics_to_csv(title, lyrics, filename="melodii_versuri_genius.csv"):
    with open(filename, "a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        for line in lyrics:
            writer.writerow([title, line])


def process_song(search_query):
    song = search_song(search_query)
    if song:
        print("Title:", song["full_title"])
        print("URL:", song["url"])

        lyrics = get_lyrics(song["url"])
        if lyrics:
            print("Lyrics fetched successfully.")
            save_lyrics_to_csv(song["title"], lyrics)
        else:
            print("Failed to fetch lyrics.")

def get_artist_songs(artist_id, per_page=50):
    songs = []
    page = 1
    headers = {"Authorization": f"Bearer {GENIUS_TOKEN}"}

    while True:
        params = {"per_page": per_page, "page": page}
        response = requests.get(f"{BASE_URL}/artists/{artist_id}/songs", headers=headers, params=params)
        data = response.json()
        
        hits = data["response"]["songs"]
        if not hits:
            break
        
        songs.extend(hits)
        page += 1

    return songs

def search_artist(name):
    headers = {"Authorization": f"Bearer {GENIUS_TOKEN}"}
    response = requests.get(BASE_URL + "/search", params={"q": name}, headers=headers)
    data = response.json()
    for hit in data["response"]["hits"]:
        if hit["result"]["primary_artist"]["name"].lower() == name.lower():
            return hit["result"]["primary_artist"]["id"]
    return None

if __name__== "__main__":
    names = ["Ian (ROU)"]
    for name in names:
        artist_id = search_artist(name)
        all_songs = get_artist_songs(artist_id)
        for song in all_songs:
            process_song(song["full_title"])
    