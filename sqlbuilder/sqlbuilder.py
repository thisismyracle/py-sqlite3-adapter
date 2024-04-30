""" SQLBuilder: the data class """

from dataclasses import dataclass
from sqlite3 import Connection, Cursor


@dataclass
class SQLBuilder:
    """
    SQL Builder main class, containing essential information to run the query

    methods:
        validate_attr(input_attr) -> None
    """

    def __init__(self, con: Connection, cur: Cursor, table_name: str, table_attr: list[str]):
        """
        SQL Builder initialization

        :param con: SQLite3 database connection
        :param cur: SQLite3 database cursor
        :param table_name: the name of the table you want to take an action
        :param table_attr: the default table attr (full)
        """
        self.con = con
        self.cur = cur
        self.table_name = table_name
        self.table_attr = table_attr

    def validate_attr(self, input_attr: str | list[str]):
        """
        Validating attr

        :param input_attr: user input attr to check
        :return: raise an error if invalid
        """
        if not isinstance(input_attr, str):
            for attr in input_attr:
                if attr not in self.table_attr:
                    raise NameError(f'There is no attr named `{attr}` in table `{self.table_name}`')
        else:
            if input_attr != '*':
                raise NameError(f'Invalid attr given, `{input_attr}`.')
