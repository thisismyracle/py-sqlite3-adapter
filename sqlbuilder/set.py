""" SQLBuilder: SET """

from typing import Any
from sqlbuilder.sqlbuilder import SQLBuilder
from sqlbuilder.where import Where


class Set:
    """
    SET SQL Builder class

    methods:
        validate() -> None
        sql() -> SQL(str)
        go() -> is SET SQL success(bool)
        where(cond) -> Where object(Where)
    """

    def __init__(self, sqlbuilder: SQLBuilder, attr: str | list[str],
                 val: Any | list[Any]):
        """
        SET SQL Builder initialization

        :param sqlbuilder: SQLBuilder object contains db connection and table info
        :param attr: table attr you want to set/update
        :param val: the value you want to update to
        """
        self.sqlbuilder = sqlbuilder
        self.attr = [attr] if isinstance(attr, str) else attr
        self.val = val if isinstance(val, list) else [val]

        self.validate()

    def validate(self):
        """
        Validating attr

        :return: raise an error if not valid
        """
        self.sqlbuilder.validate_attr(self.attr)

        len_exp = len(self.attr)
        len_diff = len(self.attr) - len(self.val)

        if len_diff != 0:
            raise IndexError(f'Expected {len_exp} values, {len_exp - len_diff} given instead.')

    def sql(self) -> str:
        """
        Get the SET SQL

        :return: SET SQL in str
        """
        table_name = self.sqlbuilder.table_name
        attr = ','.join([f'{x} = ?' for x in self.attr])
        return f'UPDATE {table_name} SET {attr}'

    def go(self) -> bool:
        """
        Running the SET SQL

        :return: is the SET SQL success(bool)
        """
        self.sqlbuilder.cur.execute(self.sql(), self.val)

        is_success = self.sqlbuilder.cur.rowcount > 0
        if is_success:
            self.sqlbuilder.con.commit()

        return is_success

    def where(self, cond: str) -> Where:
        """
        Continue to WHERE SQL statement

        :param cond: WHERE Condition
        :return: Where object
        """
        return Where(self.sqlbuilder, self.sql(), cond, set_val=self.val)
