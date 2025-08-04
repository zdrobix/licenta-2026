import requests

from run_model import run_model_verse

url_base = f"https://api.lyrics.ovh/v1/"

def search(search_query):
    url = f"https://itunes.apple.com/search?term={search_query}&entity=song&limit=5"
    response = requests.get(url)

    if response.status_code == 200:
        results = response.json().get("results", [])
        if not results:
            print("No results found.")
            return None
        return results
    else:
        print("Error fetching search results.")
        return None

def get_lyrics(artist, title):
    url = url_base + f"{artist}/{title}"
    response = requests.get(url)
    if response.status_code == 200:
        lyrics = response.json().get("lyrics", "Lyrics not found.")
        return lyrics
    else:
        return "Lyrics not found."


def run_api():
    query = input("Enter a song name or artist: ")
    search_result = search(query)

    if search_result:
        print("\nResults: ")
        for i, song in enumerate(search_result):
            print(f"{i + 1}) {song['trackName']} - {song['artistName']}")

        option = int(input("Enter the song number: ")) - 1
        if 0 <= option < len(search_result):
            selected = search_result[option]
            artist = selected["artistName"]
            title = selected["trackName"]

            lyrics = get_lyrics(artist, title)
            print(f"{selected['trackName']} - {selected['artistName']}\n")
            print(lyrics.strip())
            run_model_verse(lyrics)
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    while True:
        run_api()