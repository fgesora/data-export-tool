import logging
import sqlite3

import mysql.connector as mysql
from colorama import Fore
from prompt_toolkit import prompt


class QueryManager:
    def __init__(self) -> None:
        # Create a connection pool to manage SQLite connections
        self.connection_pool = sqlite3.connect("myapp/database/queries.db", check_same_thread=False)
        self.setup_database()

    def setup_database(self) -> None:
        """
        Create queries and user_credentials in the sqlite database if they don't exit

        :return: None
        """
        # Create the queries table if it doesn't exist
        with self.connection_pool as conn:
            cursor = conn.cursor()

            # Create queries table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS queries (
                    id INTEGER PRIMARY KEY,
                    table_name TEXT,
                    query TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Create user_credentials table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_credentials (
                    host TEXT,
                    database TEXT,
                    port INTEGER,
                    username TEXT,
                    password TEXT
                )
            """)

    def save_query_to_db(self, table_name: str, query_text: str):
        """
        Save a query to the database.

        Args:
            table_name (str): The name of the table associated with the query.
            query_text (str): The text of the query to be saved.
        :return: None
        """
        with self.connection_pool as conn:
            cursor = conn.cursor()
            query = "INSERT INTO queries (table_name, query) VALUES (?, ?)"
            values = (table_name, query_text)
            cursor.execute(query, values)

    def update_query_in_database(self, query_name: str, new_query: str):
        """
        Update a query in the database.

        Args:
            query_name (str): The name of the query to be updated.
            new_query (str): The new query text.

        :returns:
            any: updates the query in the database
        """
        try:
            with self.connection_pool as conn:
                cursor = conn.cursor()
                update_query_sql = "UPDATE queries SET query = ? WHERE table_name = ?"
                values = (new_query, query_name)
                cursor.execute(update_query_sql, values)
        except sqlite3.Error as error:
            raise Exception("An error occurred while updating the query: " + str(error))

    def retrieve_preset_queries(self) -> list:
        """
        Retrieve the list of preset queries from the database.

        Returns:
            list: A list of query tuples containing table names and query texts.
        """
        with self.connection_pool as conn:
            cursor = conn.cursor()
            select_query = "SELECT table_name, query FROM queries"
            cursor.execute(select_query)
            return cursor.fetchall()

    def store_credentials(self, host: str, database: str, port: str, username: str, password: str) -> None:
        """
        Store the database credentials in the database.

        Args:
            host (str): The database host.
            database (str): The name of the database.
            port (int): The port number.
            username (str): The username.
            password (str): The password.
        """
        with self.connection_pool as conn:
            cursor = conn.cursor()
            insert_query = "INSERT INTO user_credentials (host, database, port, username, password) VALUES (?, ?, ?, " \
                           "?, ?)"
            values = (host, database, port, username, password)
            cursor.execute(insert_query, values)

    def credentials_exist(self) -> bool:
        """
        Check if database credentials exist.

        Returns:
            bool: True if credentials exist, False otherwise.
        """
        with self.connection_pool as conn:
            cursor = conn.cursor()
            select_query = "SELECT * FROM user_credentials"
            cursor.execute(select_query)
            return cursor.fetchone() is not None

    @staticmethod
    def test_database_connection(host: str, database: str, port: str, username: str, password: str) -> bool:
        """
        Test the database connection with the provided credentials.

        Args:
            host (str): The database host.
            database (str): The name of the database.
            port (int): The port number.
            username (str): The username.
            password (str): The password.

        Returns:
            bool: True if the connection is successful, False otherwise.
        """
        try:
            conn = mysql.connect(
                host=host,
                port=port,
                user=username,
                password=password,
                db=database,
                connect_timeout=5
            )
            conn.close()
            return True
        except mysql.errors.DatabaseError as e:
            logging.error(f"Failed to connect to the database: {e}")
            return False

    @staticmethod
    def get_database_credentials() -> tuple:
        """
        Prompt the user to enter the database credentials.

        Returns:
            tuple: A tuple containing the host, database, port, username, and password.
        """
        host = input(Fore.CYAN + "HOST: ")
        database = input(Fore.CYAN + "DATABASE: ")
        port = int(input(Fore.CYAN + "PORT: "))
        username = input(Fore.CYAN + "USERNAME: ")
        password = prompt("PASSWORD: ", is_password=True)

        return host, database, port, username, password

    def setup_database_credentials(self) -> None:
        """
        Set up the database credentials.
        """
        while True:
            host, database, port, username, password = self.get_database_credentials()

            if self.test_database_connection(host, database, port, username, password):
                self.store_credentials(host, database, port, username, password)
                print(Fore.GREEN, "Database credentials saved successfully!")
                break
            else:
                print(Fore.LIGHTRED_EX, "Failed to connect to the database. Please check your credentials.")
                while True:
                    retry = input(Fore.LIGHTBLUE_EX + "Do you want to retry? (Y/N): ").upper()
                    if retry == "Y":
                        break
                    elif retry == "N":
                        exit()
                    else:
                        print(Fore.LIGHTRED_EX, "Invalid input. Please enter 'Y' or 'N'.")
