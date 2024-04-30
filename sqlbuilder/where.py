""" SQLBuilder: WHERE """

from typing import Any
from sqlbuilder.sqlbuilder import SQLBuilder


class Where:
    """
    WHERE SQL Builder class

    methods:
        sql() -> SQL(str)
        go() -> the SQL result(list) or is SQL success(bool)
    """

    def __init__(self, sqlbuilder: SQLBuilder, prev_sql: str, cond: str,
                 val: list[Any] | None = None):
        """
        Where SQL Builder initialization

        :param sqlbuilder: SQLBuilder object contains db connection and table info
        :param prev_sql: previous SQL
        :param cond: WHERE SQL condition
        :param val: new values if needed (e.g. for SET SQL)
        """
        self.sqlbuilder = sqlbuilder
        self.prev_sql = prev_sql
        self.cond = cond
        self.val = val

    def sql(self) -> str:
        """
        Get the SET SQL

        :return: SET SQL in str
        """
        sql = f'{self.prev_sql} WHERE {self.cond}'
        return sql

    def go(self) -> list | bool:
        """
        Running the X-WHERE SQL

        :return: the result of X-WHERE SQL(list) or is X-WHERE SQL success(bool)
        """
        if self.val is None:
            self.sqlbuilder.cur.execute(self.sql())
        else:
            self.sqlbuilder.cur.execute(self.sql(), self.val)

        is_success = self.sqlbuilder.cur.rowcount > 0
        if is_success:
            self.sqlbuilder.con.commit()

        if self.val is None:
            return self.sqlbuilder.cur.fetchall()
        return is_success
