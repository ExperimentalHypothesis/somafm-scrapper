import mysql.connector
from mysql.connector import Error

from config import DB_NAME, DB_HOST, DB_USER, DB_PASSWORD


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
        except Error as err:
            print(f"Error {err} while connecting")

    def insert_row(self, table_name, artist, song, album, url):
        print(f"inserting row to db")

        qry = f"INSERT INTO {table_name} (artist, song, album, url) VALUES (%s, %s, %s, %s)"
        values = (artist, song, album, url)

        try:
            self.cursor.execute(qry, values)
            self.connection.commit()
        except Error as er:
            print(f"Error {er} while inserting {values}")

    def disconnect(self):
        print(f"disconnecting from db")

        if self.connection.is_connected():
            self.cursor.close()
            self.connection.close()


if __name__ == "__main__":
    try:
        mysql = MySQL()
        table = "dronezone"
        data = ["Adam Pacione", "The Channel Swimmer", "From Stills To Motion", "https://infraction.bandcamp.com"]
        mysql.insert_row(table, *data)
    except Error as err:
        print(err)
    finally:
        mysql.disconnect()