""" SQLBuilder: INSERT """

from sqlbuilder.sqlbuilder import SQLBuilder


class Insert:
    """
    INSERT SQL Builder class

    methods:
        validate() -> None
        sql() -> SQL(str)
        go() -> is INSERT SQL success(bool)
    """

    def __init__(self, sqlbuilder: SQLBuilder, rows: list[tuple]):
        """
        INSERT SQL Builder initialization

        :param sqlbuilder: SQLBuilder object contains db connection and table info
        :param rows: the rows want to be inserted to the table in list of tuples
        """
        self.sqlbuilder = sqlbuilder
        self.rows = rows

        self.validate()

    def validate(self):
        """
        Validating attr

        :return: raise an error if not valid
        """
        attr = self.sqlbuilder.table_attr
        len_exp = len(attr)  # expected len
        for row in self.rows:
            len_diff = len_exp - len(row)
            if len_diff != 0:
                raise IndexError(f'Expected {len_exp} values, {len_exp - len_diff} given instead.')

    def sql(self) -> str:
        """
        Get the INSERT SQL

        :return: INSERT SQL in str
        """
        table_name = self.sqlbuilder.table_name
        attr = self.sqlbuilder.table_attr
        attr_str = ','.join(list(self.sqlbuilder.table_attr))
        q_marks = ','.join(['?' for _ in range(len(attr))])
        sql = f'INSERT INTO {table_name}({attr_str}) VALUES ({q_marks})'

        return sql

    def go(self) -> bool:
        """
        Running the INSERT SQL

        :return: is the INSERT SQL success(bool)
        """
        self.sqlbuilder.cur.executemany(self.sql(), self.rows)

        is_success = self.sqlbuilder.cur.rowcount > 0
        if is_success:
            self.sqlbuilder.con.commit()

        return is_success
