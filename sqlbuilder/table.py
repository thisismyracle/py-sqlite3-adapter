""" Table SQLBuilder initial class """

from typing import Any
from sqlbuilder.sqlbuilder import SQLBuilder
from sqlbuilder.get import Get
from sqlbuilder.set import Set
from sqlbuilder.insert import Insert


class Table:
    """
    Table SQLBuilder initial class, where all the SQL query begin

    methods:
        get(attr) -> Get object(Get)
        set(attr, val) -> Set object(Set)
        insert(rows) -> Insert object(Insert)
    """

    def __init__(self, sqlbuilder: SQLBuilder):
        """
        SQL Builder initialization

        :param sqlbuilder: SQLBuilder object contains db connection and table info
        """
        self.sqlbuilder = sqlbuilder

    def get(self, attr: str | list[str] | None = None) -> Get:
        """
        Continue to the GET statement

        :param attr: table attr you want to get the values
        :return: Get object
        """
        return Get(self.sqlbuilder, attr)

    def set(self, attr: str | list[str], val: Any | list[Any]) -> Set:
        """
        Continue to the SET statement

        :param attr: table attr you want to set/update
        :param val: the new values
        :return: Set object
        """
        return Set(self.sqlbuilder, attr, val)

    def insert(self, rows: list[tuple]) -> Insert:
        """
        Continue to the INSERT statement

        :param rows: the rows you want to insert to the table
        :return: Insert object
        """
        return Insert(self.sqlbuilder, rows)
