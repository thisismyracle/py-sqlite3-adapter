""" SQLBuilder: GET """

from sqlbuilder.sqlbuilder import SQLBuilder
from sqlbuilder.where import Where


class Get:
    """
    GET SQL builder class

    methods:
        validate() -> None
        sql() -> SQL(str)
        go() -> result of SQL GET(list)
        where(cond) -> Where object(Where)
    """

    def __init__(self, sqlbuilder: SQLBuilder, attr: str | list[str] | None):
        """
        GET SQL Builder initialization

        :param sqlbuilder: SQLBuilder object contains db connection and table info
        :param attr: Table attr you want to get
        """
        self.sqlbuilder = sqlbuilder
        self.attr = self.sqlbuilder.table_attr if attr is None else attr
        self.attr = [self.attr] if isinstance(attr, str) else self.attr

        self.validate()

    def validate(self):
        """
        Validating attr

        :return: raise an error if not valid
        """
        self.sqlbuilder.validate_attr(self.attr)

    def sql(self) -> str:
        """
        Get the GET SQL

        :return: GET sql in str
        """
        table_name = self.sqlbuilder.table_name
        attr_str = ','.join(list(self.attr))

        return f'SELECT {attr_str} FROM {table_name}'

    def go(self) -> list:
        """
        Running the GET SQL

        :return: the result of GET SQL
        """
        self.sqlbuilder.cur.execute(self.sql())

        is_success = self.sqlbuilder.cur.rowcount > 0
        if is_success:
            self.sqlbuilder.con.commit()

        temp_res = self.sqlbuilder.cur.fetchall()
        attr_len = len(self.attr)
        res = []

        for tr in temp_res:
            res.append({self.attr[i]: tr[i] for i in range(attr_len)})

        return res

    def where(self, cond: str) -> Where:
        """
        Continue to WHERE SQL statement

        :param cond: WHERE Condition
        :return: Where object
        """
        return Where(self.sqlbuilder, self.sql(), cond, get_attr=self.attr)
