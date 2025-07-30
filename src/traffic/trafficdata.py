import sqlite3
from pathlib import Path

import pandas as pd


def create_database():
    """ Creates a SQLite database with traffic data.

    The database is intentionally not normalised to avoid you from using this for coursework 01.

    The data is saved to a file named traffic.db with two tables named 'uk' and 'london'

    Returns:
            str: A message indicating whether the database was created successfully.

    Raises:
            ValueError: If there is an issue with the data values.
            sqlite3.OperationalError: If there is an operational error with SQLite.
            sqlite3.IntegrityError: If there is a database integrity error.
            Exception: For any other unexpected errors.
    """
    # Create a connection to an SQLite database
    database_filepath = Path(__file__).parent.joinpath("traffic.db")
    conn = sqlite3.connect(database_filepath)

    # Load the data files using Pandas dataframe
    data_file_uk = Path(__file__).parent.joinpath("traffic-flow-uk.xls")
    data_file_london = Path(__file__).parent.joinpath("traffic-flow-borough.xls")
    df_uk = pd.read_excel(data_file_uk)
    df_lon_cars = pd.read_excel(data_file_london, sheet_name="Traffic Flows Cars")
    df_lon_all = pd.read_excel(data_file_london, sheet_name="Traffic Flows All vehicles")

    # Add the data to the database
    try:
        df_uk.to_sql('uk', conn, if_exists='replace', index=False)
        df_lon_cars.to_sql('london_cars', conn, if_exists='replace', index=False)
        df_lon_all.to_sql('london_all', conn, if_exists='replace', index=False)
        return "Database created successfully"
    except ValueError as ve:
        print("ValueError:", ve)
    except sqlite3.OperationalError as oe:
        print("OperationalError:", oe)
    except sqlite3.IntegrityError as ie:
        print("IntegrityError:", ie)
    except Exception as e:
        print("Unexpected error:", e)


class TrafficData:
    """
    A class to interact with the traffic.db SQLite database.

        Attributes:
            conn (sqlite3.Connection): The connection object to the SQLite database.
            cursor (sqlite3.Cursor): The cursor object to execute SQL commands.
    """

    def __init__(self, db_location):
        """
        Initializes the TrafficData class with a connection to the specified SQLite database.

        Args:
            db_location (str): The filepath to the SQLite database file.

        """
        try:
            self.conn = sqlite3.connect(db_location)
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")

    def get_columns(self, table_name):
        """
        Retrieves the column names from the specified table.

        Args:
            table_name (str): The name of the table to retrieve column names from.

        Returns:
            list: A list of column names from the table.
        """
        try:
            self.cursor.execute(f"PRAGMA table_info({table_name})")
            return [col[1] for col in self.cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"Error retrieving column names from {table_name}: {e}")
            return []

    def get_rows(self, table_name):
        """
        Retrieves all rows from the specified table.

        Args:
            table_name (str): The name of the table to retrieve rows from.

        Returns:
            list: A list of tuples containing the rows from the table.
        """
        try:
            self.cursor.execute(f"SELECT * FROM {table_name}")
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error retrieving data from {table_name}: {e}")
            return []

    def add_row(self, table_name, columns, values):
        """Adds a new row to the specified table with the given columns and values.

            Args:
                table_name (str): The name of the table to add the row to.
                columns (list): A list of column names to insert values into.
                values (list): A list of values to insert into the columns.

        """
        try:
            columns_str = ', '.join(columns)
            placeholders = ', '.join(['?'] * len(values))
            self.cursor.execute(f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})", values)
            self.conn.commit()
        except (sqlite3.Error, ValueError) as e:
            print(f"Error adding data to {table_name}: {e}")

    def update_row(self, table_name, set_clause, condition):
        """ Updates rows in the specified table based on the given condition.

            Args:
                table_name (str): The name of the table to update rows in.
                set_clause (str): The SET clause specifying the columns and values to update.
                condition (str): The condition to determine which rows to update.
        """
        try:
            self.cursor.execute(f"UPDATE {table_name} SET {set_clause} WHERE {condition}")
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error updating data in {table_name}: {e}")

    def delete_row(self, table_name, condition):
        """
        Deletes rows from the specified table based on the given condition.

        Args:
        table_name (str): The name of the table to delete rows from.
        condition (str): The condition to determine which rows to delete.
        """
        try:
            self.cursor.execute(f"DELETE FROM {table_name} WHERE {condition}")
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error deleting data from {table_name}: {e}")

    def close(self):
        """
        Closes the connection to the SQLite database.
        """
        try:
            self.conn.close()
        except sqlite3.Error as e:
            print(f"Error closing the database connection: {e}")


def say_hello():
    """ Returns a string that says hello world.

    Do not use this for writing your own tests.
    This is a simple function that is included so you can check that your environment is set up correctly for running tests.

    """
    return "Hello world"
