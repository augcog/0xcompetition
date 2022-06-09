import pandas as pd
import json
from sqlalchemy import create_engine, inspect


class CompetitionSQLWrapper:

    def __init__(self, file_path: str):
        """
        Takes a file path, validate whether this file path is correct or not, and connect to the database

        raise file not found error if file path is wrong
        raise Connection\error if connection fails.
        Args:
            file_path:

        Returns:

        """
        try:
            with open(file_path) as f:
                data = json.load(f)
                f.close()
                print("File path has been accepted.")
        except OSError:
            raise OSError("File not found. Check the name of the file.")

        username = data['username']
        password = data['password']
        ip_address = data['ip_address']
        port = data['port']
        database = data['database']

        self.alchemy_engine = create_engine(
            f"postgresql+pg8000://{username}:{password}@{ip_address}:{port}/{database}",
            pool_recycle=3600,
            pool_pre_ping=True
        )
        self.inspector = inspect(self.alchemy_engine)

        try:
            self.db_connection = self.alchemy_engine.connect()
            print("Connection successful.")
        except ConnectionError:
            raise ConnectionError("Failed to connect!!!")

    def query(self, query: str) -> pd.DataFrame:
        """
        Using a user SQL statement input, this function will use the database
        connection to execute the statement and return a pandas dataframe
        Args:
            query:

        Returns:

        """
        results = pd.read_sql_query(query, self.db_connection)
        # TODO: implement column name parsing
        df = pd.DataFrame(results, columns=None)

        return df

    def list_tables(self):
        """
        Creates and prints out a list of tables in the database
        Args:
            None

        Returns:
            tables: a list of the table names in the database

        """
        tables = self.inspector.get_table_names()
        return tables

    def list_columns(self, table_name: str):
        """
        Creates and prints out a list of columns in a specific table
        Args:
            table_name:

        Returns:
            cols

        """
        try:
            cols = []
            for results in self.inspector.get_columns(table_name):
                cols.append(results.get('name'))
        except NameError:
            raise NameError("Table name, " + table_name + " is not valid!")

        return cols

    def list_indexes(self, table_name: str):
        """
        Creates and prints out a list of indices in a specific table
        Args:
            table_name:

        Returns:
            indexes:

        """
        try:
            indexes = []
            for results in self.inspector.get_indexes(table_name):
                indexes.append(results.get('name'))
        except NameError:
            raise NameError("Table name, " + table_name + " is not valid!")

        return indexes

    def get_primary_key_info(self, table_name: str):
        """
        Creates and prints out a list of indices in a specific table
        Args:
            table_name:

        Returns:
            pk:

        """
        try:
            pk = []
            for results in self.inspector.get_pk_constraint(table_name):
                pk.append(results)
        except NameError:
            raise NameError("Table name, " + table_name + " is not valid!")

        return pk

    def get_foreign_keys_info(self, table_name: str):
        """
        Creates and prints out a list of indices in a specific table
        Args:
            table_name:

        Returns:
            fk:

        """
        try:
            fk = []
            for results in self.inspector.get_foreign_keys(table_name):
                fk.append(results)
            print(fk)
        except NameError:
            raise NameError("Table name, " + table_name + " is not valid!")

        return fk
