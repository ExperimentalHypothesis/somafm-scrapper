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
        Row = namedtuple("Row", ["Artist", "Song", "Album", "URL"])
        for artist, song, album, url in zip(artists, songs, albums, urls, strict=True):
            self.parsed.append(Row(artist, song, album, url))
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
