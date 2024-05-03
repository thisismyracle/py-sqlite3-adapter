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
                 set_val: list[Any] | None = None,
                 get_attr: list[str] | None = None, *values: Any):
        """
        Where SQL Builder initialization

        :param sqlbuilder: SQLBuilder object contains db connection and table info
        :param prev_sql: previous SQL
        :param cond: WHERE SQL condition
        :param set_val: new values if needed (e.g. for SET SQL)
        :param get_attr: attr you want to GET
        :param values: WHERE values
        """
        self.sqlbuilder = sqlbuilder
        self.prev_sql = prev_sql
        self.cond = cond
        self.set_val = set_val
        self.get_attr = get_attr
        self.values = values

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
        if self.set_val is None:
            # GET-WHERE
            self.sqlbuilder.cur.execute(self.sql(), self.values)
        else:
            # SET-WHERE
            set_where_val = self.set_val + list(self.values)
            self.sqlbuilder.cur.execute(self.sql(), set_where_val)

        is_success = self.sqlbuilder.cur.rowcount > 0
        if is_success:
            self.sqlbuilder.con.commit()

        if self.set_val is None:
            # GET-WHERE
            temp_res = self.sqlbuilder.cur.fetchall()
            attr_len = len(self.get_attr)
            res = []

            for tr in temp_res:
                res.append({self.get_attr[i]: tr[i] for i in range(attr_len)})

            return res
        return is_success
