import logging
import os
import json
import sqlite3
import traceback
from filelock import FileLock
from pathlib import Path

logging.basicConfig(
    level = logging.INFO,
    format = '%(asctime)s | %(process)d | %(levelname)s | %(message)s'
)

class DB(object):
    def __init__(self, db_path):
        self.db_path = Path(db_path)
        self.process_lock_path = f'{self.db_path}.lock'
        self.process_lock = FileLock(self.process_lock_path, timeout = -1)
        self.create_db()

    def create_db(self):
        with self.process_lock:
            if not os.path.exists(self.db_path):
                connection = sqlite3.connect(self.db_path)
                cursor = connection.cursor()
                cursor.execute('CREATE TABLE IF NOT EXISTS data (key TEXT PRIMARY KEY, value TEXT)')
                connection.commit()
                connection.close()


    def retrieve_db(self):
        with self.process_lock:
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()
            cursor.execute('SELECT key, value FROM data')
            rows = cursor.fetchall()
            database = {row[0]: row[1] for row in rows}
            connection.close()
            return database
        
    def set(self, key, val):
        try:
            database = self.retrieve_db()
            database[key] = val
            self.flush_database(database)
        except Exception:
            logging.error(traceback.format_exc())
            return False
        return True

    def get(self, key):
        key = str(key)
        database = self.retrieve_db()
        if key in database:
            return database[key]
        return None

    def remove(self, key):
        key = str(key)
        database = self.retrieve_db()
        if key not in database:
            raise KeyError(
                f"{key} Does Not Exist in Database"
            )
        del database[key]

        try:
            self.flush_database(database)
        except Exception:
            logging.error(traceback.format_exc())
            return False
        return True
    
    def keys(self):
        return self.retrieve_db().keys()

    def values(self):
        return self.retrieve_db().values()

    def items(self):
        return self.retrieve_db().items()

    def dumps(self):
        return json.dumps(self.retrieve_db(), sort_keys=True)

    def truncate_db(self):
        self._flush_database({})
        return True


    def __repr__(self):
        return str(self.retrieve_db())

    def __len__(self):
        return len(self.retrieve_db())

    def flush_database(self, database):
        with self.process_lock:
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()
            cursor.execute('DELETE FROM data')
            for key, value in database.items():
                cursor.execute('INSERT INTO data (key, value) VALUES (?, ?)', (key, value))
            connection.commit()
            connection.close()

