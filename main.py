import time

from src.writer import write_to_file

URLS = [
    "https://somafm.com/dronezone/songhistory.html",
    "https://somafm.com/darkzone/songhistory.html",
    "https://somafm.com/deepspaceone/songhistory.html",
    "https://somafm.com/missioncontrol/songhistory.html"
]


def main():
    while True:
        try:
            write_to_file(URLS)
        except Exception as e:
            print(e)
        time.sleep(3600)



if __name__ == "__main__":
    main()