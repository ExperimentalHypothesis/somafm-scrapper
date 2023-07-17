import time

from src.db_writer import MySQL
from src.playlist_parser import PlaylistParser

URLS = [
    "https://somafm.com/dronezone/songhistory.html",
    "https://somafm.com/darkzone/songhistory.html",
    "https://somafm.com/deepspaceone/songhistory.html",
    "https://somafm.com/missioncontrol/songhistory.html"
]

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
    rows = get_parsed_rows(urls=URLS)
    channels = {row[0]: None for row in rows}
    for channel, last_played_at in channels.items():
        channels[channel] = mysql.fetch_last_played_at(channel)

    for row in reversed(rows):  # ID increment fits with time increment
        channel = row[0]
        played_at = row[-1]
        artist = row[1]
        song = row[2]
        album = row[3]
        if played_at <= channels[channel]:
            print(f"kanal: {channel}, last DT: {channels[channel]} | {played_at}, {artist}, {song}, {album}")
            continue
        mysql.insert_row(*row)


if __name__ == "__main__":
    while True:
        mysql = MySQL()
        try:
            main()
        finally:
            mysql.close()
        time.sleep(3600)