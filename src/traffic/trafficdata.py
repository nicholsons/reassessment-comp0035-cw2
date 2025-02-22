import sqlite3


class TrafficData:
    """
    A class to interact with the traffic.db SQLite database.

    Attributes:
    ----------
    conn : sqlite3.Connection
        The connection object to the SQLite database.
    cursor : sqlite3.Cursor
        The cursor object to execute SQL commands.
    """

    def __init__(self, db_location):
        """
        Initializes the TrafficData class with a connection to the specified SQLite database.

        Parameters:
        ----------
        db_location : str
            The filepat to the SQLite database file.
        """
        try:
            self.conn = sqlite3.connect(db_location)
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")

    def get_columns(self, table_name):
        """
        Retrieves the column names from the specified table.

        Parameters:
        ----------
        table_name : str
            The name of the table to retrieve column names from.

        Returns:
        -------
        list
            A list of column names from the table.
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

        Parameters:
        ----------
        table_name : str
            The name of the table to retrieve rows from.

        Returns:
        -------
        list
            A list of tuples containing the rows from the table.
        """
        try:
            self.cursor.execute(f"SELECT * FROM {table_name}")
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error retrieving data from {table_name}: {e}")
            return []

    def add_row(self, table_name, columns, values):
        """
        Adds a new row to the specified table with the given columns and values.

        Parameters:
        ----------
        table_name : str
            The name of the table to add the row to.
        columns : list
            A list of column names to insert values into.
        values : list
            A list of values to insert into the columns.

        Raises:
        ------
        ValueError
            If the data type of any value does not match the expected data type for the column.
        """
        try:
            # Validate data types
            for col, val in zip(columns, values):
                if col in ["year", "year_id", "borough_id", "flow_id"]:
                    if not isinstance(val, int):
                        raise ValueError(f"Invalid data type for column {col}. Expected int.")
                elif col in ["million_vehicle_km", "cars", "light_commercial_vehicles", "heavy_goods_vehicles",
                             "motorcycles", "buses_and_coaches", "all_motor_vehicles"]:
                    if not isinstance(val, (int, float)):
                        raise ValueError(f"Invalid data type for column {col}. Expected float.")
                elif col in ["borough_name", "la_code"]:
                    if not isinstance(val, str):
                        raise ValueError(f"Invalid data type for column {col}. Expected str.")

            columns_str = ', '.join(columns)
            placeholders = ', '.join(['?'] * len(values))
            self.cursor.execute(f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})", values)
            self.conn.commit()
        except (sqlite3.Error, ValueError) as e:
            print(f"Error adding data to {table_name}: {e}")

    def update_row(self, table_name, set_clause, condition):
        """
        Updates rows in the specified table based on the given condition.

        Parameters:
        ----------
        table_name : str
            The name of the table to update rows in.
        set_clause : str
            The SET clause specifying the columns and values to update.
        condition : str
            The condition to determine which rows to update.
        """
        try:
            self.cursor.execute(f"UPDATE {table_name} SET {set_clause} WHERE {condition}")
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error updating data in {table_name}: {e}")

    def delete_row(self, table_name, condition):
        """
        Deletes rows from the specified table based on the given condition.

        Parameters:
        ----------
        table_name : str
            The name of the table to delete rows from.
        condition : str
            The condition to determine which rows to delete.
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
    This is a test function that is included so you can check that your environment is set-up correctly for running tests.

    """
    return "Hello world"
