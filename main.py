import requests
from src.parsed_table import ParsedTable

urls = [
    "https://somafm.com/dronezone/songhistory.html",
    "https://somafm.com/darkzone/songhistory.html",
    "https://somafm.com/deepspaceone/songhistory.html",
    "https://somafm.com/missioncontrol/songhistory.html"
]

def main():
    for url in urls:
        print(f"--------- {url} -----------")
        page = requests.get(url).text
        table = ParsedTable(page)
        table.parse()
        print(table.parsed)


if __name__ == "__main__":
    main()
