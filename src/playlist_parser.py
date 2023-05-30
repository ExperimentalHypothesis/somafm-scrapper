from collections import namedtuple
from typing import List, Optional
from datetime import datetime, timedelta


import requests
from bs4 import BeautifulSoup


class PlaylistParser:
    """
    Returns parsed playlist as list of tuples.
    Artist, Album, Song, URL, PlayedAt
    """

    def __init__(self, url):
        self.page = requests.get(url).text
        self.soup = BeautifulSoup(self.page, "html.parser")
        self.parsed = []

    def parse(self) -> List[namedtuple]:
        played_at = self.played_at
        artists = self.artists
        albums = self.albums
        songs = self.songs
        urls = self.urls
        channel = self.channel

        if len(played_at) != len(albums):
            self.delete_break_station(played_at, artists)

        Row = namedtuple("Row", ["channel", "artist", "song", "album", "url", "played_at"])
        for artist, song, album, url, played_at in zip(artists, songs, albums, urls, played_at, strict=True):
            row = Row(channel, artist, song, album, url, played_at)
            self.parsed.append(row)

        return self.parsed

    @property
    def played_at(self):
        locator = "td:nth-child(1)"
        played_at = [a.text for a in self.soup.select(locator)[1:] if a.text]

        if last_idx := self.last_before_midnight(played_at) is None:
            times = [self.convert_time(time) for time in played_at]
        else:
            times = [self.convert_time(time) - timedelta(days=1) for time in played_at if i <= last_idx]

        return times


    @property
    def artists(self):
        locator = "td:nth-child(2)"
        artists = [a.text for a in self.soup.select(locator)[1:]]
        return artists

    @property
    def songs(self):
        locator = "td:nth-child(3)"
        songs = [s.text.strip() for s in self.soup.select(locator)[1:]]
        return songs

    @property
    def albums(self):
        locator = "td:nth-child(4)"
        albums = [a.text for a in  self.soup.select(locator)[1:]]
        return albums

    @property
    def urls(self):
        locator = "td:nth-child(4)"
        urls = [x.find("a")["href"] for x in self.soup.select(locator)[1:]]
        return urls

    @property
    def channel(self):
        locator = "div#channelblock h1"
        channel = self.soup.select_one(locator).get_text(strip=True)
        return channel

    @staticmethod
    def delete_break_station(played_at, artists):
        idx_to_delete = []
        for idx, artist in enumerate(artists):
            if artist == "Break / Station ID":
                idx_to_delete.append(idx)

        # needs to be done backwards to avoid out of range err
        for idx in reversed(idx_to_delete):
            del artists[idx]
            del played_at[idx]

    @staticmethod
    def convert_time(scrapped_time: str) -> datetime:
        scrapped_time = scrapped_time.replace("\xa0 (Now)", "").strip()
        current_date = datetime.now().date()
        current_datetime = f"{current_date} {scrapped_time}"
        return datetime.strptime(current_datetime, "%Y-%m-%d %H:%M:%S")

    @staticmethod
    def last_before_midnight(times: list) -> Optional[int]:
        for idx in range(len(times)-1):
            if times[idx].startswith("0") and times[idx+1].startswith("2"):
                return idx+1
        return None


if __name__ == "__main__":
    p = PlaylistParser("https://somafm.com/dronezone/songhistory.html")
    p.parse()
    for i in p.parsed:
        print(i)