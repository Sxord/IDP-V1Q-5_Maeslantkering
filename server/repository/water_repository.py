import sqlite3
import time


class WaterRepository:
    connection: sqlite3.Connection

    def __init__(self, connection):
        self.connection = connection
        self.create_table()

    def create_table(self):
        self.connection.execute(
            'CREATE TABLE IF NOT EXISTS water ('
            'id INTEGER PRIMARY KEY AUTOINCREMENT,'
            'average_height REAL,'
            'epoch REAL'
            ');'
        )
        self.connection.commit()

    def add_data(self, water_height):
        self.connection.execute('INSERT INTO water (average_height, epoch)'
                                'VALUES({}, {});'.format(water_height,
                                                         time.time()
                                                         )
                                )
        self.connection.commit()

    def fetch_all(self):
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM water ORDER BY id DESC LIMIT 42')
        return cursor.fetchall()
