import requests
from src.parsed_row import ParsedRow

urls = [
    "https://somafm.com/dronezone/songhistory.html",
    "https://somafm.com/darkzone/songhistory.html",
    "https://somafm.com/deepspaceone/songhistory.html",
    "https://somafm.com/missioncontrol/songhistory.html"
]

def main():
    page = requests.get(urls[0]).text
    row = ParsedRow(page)
    row.parse()


if __name__ == "__main__":
    main()
