import logging
import sqlite3


class Database:
    """ Database class which handes the SDLite database,
        using just one main table """
    log = logging.getLogger(__name__)

    def __init__(self, filePath: str) -> None:
        """ Initiates the database """
        self.log.info(f"Initiating database at {filePath}")

        self.connect(filePath)

    def connect(self, filePath: str) -> None:
        """ Create the sqlite connection to the file """
        self.filePath: str = filePath
        self.con: sqlite3.Connection = sqlite3.connect(self.filePath)
        self.cur: sqlite3.Cursor = self.con.cursor()

    def save(self) -> None:
        """ Commits changes """
        self.con.commit()

    def saveAndClose(self) -> None:
        """ Commits and closes the connection """
        self.log.info(f"Closing database connection to {self.filePath}")
        self.con.close()

    def makeTable(self, table: str, columns: str) -> None:
        """ Loads (or creates) the given table """
        # Get table names
        tables = self.cur.execute("SELECT name FROM sqlite_master").fetchall()

        # Get list of table names using list comprehension to turn
        # the list of tuples into one consolidated list
        tableNames: list[str] = [table[0] for table in tables]

        if table not in tableNames:
            self.log.info(f"Creating table {table}")
            self.cur.execute(f"CREATE TABLE {table} ({columns})")

        self.save()

    # Inserting and fetching:
    def insert(self, table: str, key: str, value: str) -> None:
        """ Inserts the given key and value into the table """
        self.log.info(f"Inserting into {table}: ({key}, {value})")
        self.cur.execute(f"INSERT INTO {table} VALUES (?, ?)", (key, value))
        self.save()

    def fetch(self, table: str, keyColumn: str, key: str, valueColumn: str):
        """ Gets the value of the valueColumn column where
            the keyColumn column is equal to the given key """
        self.log.info(
            f"In {table}, finding the value of "
            f"{valueColumn} where {keyColumn} = {key}"
        )
        value = self.cur.execute(f"SELECT {valueColumn} FROM {table} \
                                 WHERE {keyColumn} = ?", (key,)).fetchone()

        # Turn tuple into one value
        if value is None:
            return None
        return value[0]

    def update(self, table: str, keyColumn: str, key: str,
               valueColumn: str, value: str) -> None:
        """ Sets valueColumn to value where keyColumn is equal to key """
        self.log.info(
            f"In {table}, changing {valueColumn} to {value} "
            f"where {keyColumn} = {key}"
        )
        self.cur.execute(f"UPDATE {table} SET {valueColumn} = ? \
                           WHERE {keyColumn} = ?", (value, key))
        self.save()

    def set(self, table: str, key: str, value: str) -> None:
        """ Inserts the data if it doesn't exist, otherwise updates it """
        if self.fetch(table, key, value):
            self.update(table, key, value)
        else:
            self.insert(table, key, value)

    def setIfNone(self, table: str, keyColumn: str, key: str,
                  valueColumn: str, defaultValue: str):
        """ Inserts the data if it doesn't exist,
            otherwise returns the current value """
        getValue = self.fetch(table, keyColumn, key, valueColumn)
        if getValue is None:  # Insert if it does not exist
            self.insert(table, key, defaultValue)
            return defaultValue
        return getValue
