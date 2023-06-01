import os
from os.path import join, dirname
from dotenv import load_dotenv


load_dotenv(join(dirname(__file__), '../.env'))

DB_HOST = os.environ.get("DB_HOST")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")



if __name__ == "__main__":
    print(DB_HOST)