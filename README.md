# SomaFM Scrapper

A Python-based project for scraping playlist from SomaFM for couple of ambient-based stations.

## Description

This project contains a script to scrape playlist from SomaFM and save it to MySQL. The script is designed to be run periodically using a cron job to keep the data updated. It runs every hour and basically builds a long term database of what was played in SomaFM.

It scrapes the name of author, song, album and url. 

## Installation

1. **Clone the repository**:
   ```sh
   git clone https://github.com/ExperimentalHypothesis/somafm-scrapper.git
   cd somafm-scrapper
2. **Set up a virtual environment**:
   ```sh
    python -m venv venv
    source venv/bin/activate
3. **Install dependencies**:
   ```sh
    pip install -r requirements.txt
4. **Usage**:
   ```sh
    pip install -r requirements.txt
5. **Run manually**:
   ```sh
    python main.py
6. **Run with cronjob**:
   ```sh
    59 * * * * /path/to/your//venv/bin/python /path/to/your/project/main.py >> /path/to/your/project/logs.txt 2>&1
 