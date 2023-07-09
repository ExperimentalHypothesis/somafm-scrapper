from src.playlist_parser import PlaylistParser


def write_to_file(urls: list) -> None:
    for url in urls:
        print(f"scrapping {url}")
        channel_name = url.split("/")[-2]
        with open(channel_name, "a", encoding="utf-8") as fw:
            parser = PlaylistParser(url)
            playlist = parser.parse()
            for row in playlist:
                fw.write(", ".join([row.Artist, row.Song, row.Album, row.URL]) + "\n")


