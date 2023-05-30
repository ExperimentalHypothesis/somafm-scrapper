import bs4
import requests
from bs4 import BeautifulSoup
from collections import namedtuple

urls = [
    "https://somafm.com/dronezone/songhistory.html",
    "https://somafm.com/darkzone/songhistory.html",
    "https://somafm.com/deepspaceone/songhistory.html",
    "https://somafm.com/missioncontrol/songhistory.html"
]


# def fetch_site():
#     soup = BeautifulSoup()
#     url = "https://somafm.com/dronezone/songhistory.html"

def is_valid_row(row: bs4.element.Tag):
    return not ("Played At" in row.text or "Break / Station ID" in row.text)


def get_playlist_rows() -> list:
    """ Gets list of tuples"""
    ans = []
    response = requests.get(urls[0])
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find("div", id="playinc")
    rows = table.find_all("tr")

    for row in rows:
        if is_valid_row(row):
            cells = row.find_all("td")
            one_row = []
            for cell in cells:
                if not cell.text:
                    continue
                one_row.append(cell.text)
            if one_row:
                ans.append(one_row)
    return ans


class ParsedRow:
    def __init__(self, page):
        self.soup = BeautifulSoup(page, "html.parser")
        self.parsed = []

    @property
    def artists(self):
        locator = "td:nth-child(2)"
        artists = self.soup.select(locator)
        return artists

    @property
    def songs(self):
        locator = "td:nth-child(3)"
        songs = self.soup.select(locator)
        return songs

    @property
    def albums(self):
        locator = "td:nth-child(4)"
        albums = self.soup.select(locator)
        return albums

    # @property
    # def urls(self):
    #     locator = "td:nth-child(4)"
    #     urls = self.soup.select(locator)
    #     return urls

    def parse(self):
        artists = [a.text for a in self.artists[1:]]
        albums = [a.text for a in self.albums[1:]]
        songs = [s.text.strip() for s in self.songs[1:]]
        # urls = [u.attrs["href"] for u in self.urls]
        print(artists)
        print(albums)
        print(songs)
        # print(urls)
        # for album, artist, song in zip(albums, artists, songs, strict=True):
        #     self.parsed.append((album, artist, song))



def main():
    # print(get_playlist_rows())

    page = requests.get(urls[0]).text
    # print(page)
    pr = ParsedRow(page)
    pr.parse()
    print(pr.parsed)


    # for artists, songs in zip(pr.artists(), pr.songs()):
    #     print(artists, songs)

if __name__ == "__main__":
    main()