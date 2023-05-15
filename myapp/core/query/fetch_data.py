import logging
import sqlite3

from cacheout import Cache

import mysql.connector as mysql

from myapp.utils.logger import setup_logger
from settings import error_log_file_path

# Use the LRU eviction strategy and limit the cache to 1000 entries
cache = Cache(maxsize=1000)

# Set up logger
log_file_path = error_log_file_path
setup_logger(log_file_path)


class DatabaseManager:
    def __init__(self):
        self.cache = Cache(maxsize=1000)

    def fetch_table_data(self, query):
        try:
            if query in self.cache:
                header, rows = self.cache.get(query)
            else:
                # Fetch credentials from SQLite database
                conn = sqlite3.connect("myapp/database/queries.db")
                cursor = conn.cursor()
                cursor.execute("SELECT username, password, host, database, port FROM user_credentials")
                result = cursor.fetchone()
                db_username = result[0]
                db_password = result[1]
                db_host = result[2]
                database = result[3]
                conn.close()

                # Connect to MySQL database using fetched credentials
                with mysql.connect(
                        host=db_host,
                        user=db_username,
                        password=db_password,
                        database=database
                ) as db, db.cursor() as cursor:
                    # Execute query and fetch header and rows
                    cursor.execute(query)
                    header = [row[0] for row in cursor.description]
                    rows = cursor.fetchall()
                    # Add query result to cache
                    self.cache.set(query, (header, rows))
            return header, rows
        except mysql.Error as e:
            # Log error message and raise custom exception
            message = f"Database Error: {e.msg}"
            logging.error(message)
            raise DatabaseError(message, query)


class DatabaseError(Exception):
    def __init__(self, message, query):
        self.message = message
        self.query = query
        super().__init__(message)
