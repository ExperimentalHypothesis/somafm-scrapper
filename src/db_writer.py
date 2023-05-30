from datetime import datetime

import mysql.connector
from mysql.connector import Error

from src.config import DB_NAME, DB_HOST, DB_USER, DB_PASSWORD


class MySQL:
    def __init__(self):
        self.connection = None
        self.cursor = None

        print(f"connecting to db")
        try:
            self.connection = mysql.connector.connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
            )
            self.cursor = self.connection.cursor()
        except Error as er:
            print(f"Error {er} while connecting")


    def insert_row(self, table_name, artist, song, album, url, played_at):
        print(f"inserting {artist}, {song}, {album} to table {table_name}")

        qry = f"INSERT INTO {table_name} (artist, song, album, url, played_at) VALUES (%s, %s, %s, %s, %s)"
        values = (artist, song, album, url, played_at)

        try:
            self.cursor.execute(qry, values)
            self.connection.commit()
        except Error as er:
            print(f"Error {er} while inserting {values}")

    def fetch_last_played_at(self, table_name):
        print(f"fetching last played from {table_name}")
        try:
            query = f"SELECT played_at FROM {table_name} ORDER BY played_at DESC LIMIT 1"
            self.cursor.execute(query)
            result = self.cursor.fetchone()
            return result[0] if result else datetime(2000, 1, 1, 0, 00, 0)
            # return result[0] or datetime(2000, 1, 1, 0, 00, 0)
        except Error as er:
            print(f"Error {er} while executing query: {query}")

    def close(self):
        print(f"disconnecting from db")
        if self.connection.is_connected():
            self.cursor.close()
            self.connection.close()


if __name__ == "__main__":
    try:
        mysql = MySQL()
        table = "dronezone"
        last = mysql.fetch_last_played_at(table)
        print(last)
        # data = ["Adam Pacione", "The Channel Swimmer", "From Stills To Motion", "https://infraction.bandcamp.com"]
        # mysql.insert_row(table, *data)
    except Error as err:
        print(err)
    finally:
        mysql.close()


# connecting to db
# inserting row to db
# INSERT INTO dronezone (artist, song, album, url) VALUES (%s, %s, %s, %s)
# # disconnecting from db