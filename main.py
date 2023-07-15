from datetime import time

from src.db_writer import MySQL
from src.playlist_parser import PlaylistParser

URLS = [
    "https://somafm.com/dronezone/songhistory.html",
    "https://somafm.com/darkzone/songhistory.html",
    "https://somafm.com/deepspaceone/songhistory.html",
    "https://somafm.com/missioncontrol/songhistory.html"
]


# TODO move this to parser
def get_parsed_rows(urls: list) -> list:
    rows = []
    for url in URLS:
        parser = PlaylistParser(url)
        playlist = parser.parse()
        for row in playlist:
            channel = (lambda ch: ch.lower().replace(" ", ""))(row[0])  # Drone Zone -> dronezone
            rows.append(tuple([channel, row.artist, row.song, row.album, row.url, row.played_at]))
    return rows


def main():
    mysql = MySQL()

    rows = get_parsed_rows(urls=URLS)
    for row in rows:
        mysql.insert_row(*row)


if __name__ == "__main__":
    while True:
        main()
        time.sleep(36000)
