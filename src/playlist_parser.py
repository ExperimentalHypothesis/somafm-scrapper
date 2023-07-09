from collections import namedtuple
from typing import List

import requests
from bs4 import BeautifulSoup


class PlaylistParser:
    """
    Returns parsed playlist as list of tuples.
    Artist, Album, Song, URL
    """

    def __init__(self, url):
        self.page = requests.get(url).text
        self.soup = BeautifulSoup(self.page, "html.parser")
        self.parsed = []

    def parse(self) -> List[namedtuple]:
        artists = [a.text for a in self.artists[1:] if a.text != "Break / Station ID"]
        albums = [a.text for a in self.albums[1:]]
        songs = [s.text.strip() for s in self.songs[1:]]
        urls = [x.find("a")["href"] for x in self.urls[1:]]
        Row = namedtuple("Row", ["channel", "artist", "song", "album", "url"])
        for artist, song, album, url in zip(artists, songs, albums, urls, strict=True):
            row = Row(self.channel, artist, song, album, url)
            self.parsed.append(row)
        return self.parsed

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

    @property
    def urls(self):
        locator = "td:nth-child(4)"
        urls = self.soup.select(locator)
        return urls

    @property
    def channel(self):
        locator = "div#channelblock h1"
        channel = self.soup.select_one(locator).get_text(strip=True)
        return channel


if __name__ == "__main__":
    p = PlaylistParser("https://somafm.com/dronezone/songhistory.html")
    p.parse()