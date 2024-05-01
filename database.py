""" The main file to using Database """

import sqlite3
from sqlbuilder.sqlbuilder import SQLBuilder
from sqlbuilder.table import Table


class Database:
    """
    Database class

    methods:
        setup_passphrase(new_passphrase) -> None
        update_blueprint() -> None
        is_table_exists(table_name) -> is_exists(bool)
        is_admin(passphrase) -> is_admin(bool)
        create_table(table_name,contents,passphrase) -> is_success(bool)
        delete_table(table_name,passphrase) -> is_success(bool)
        get_table_names() -> table_names(list of str)
        get_table_info(table_name) -> table_info(list)
        table(table_name) -> table(Table)
    """

    def __init__(self, db_name: str):
        """
        Database initialization

        :param db_name: database name in string (e.g. 'database.db')
        """
        self.con = sqlite3.connect(db_name)
        self.cur = self.con.cursor()
        self.blueprint = {}
        self.update_blueprint()
        self.passphrase = None

    def setup_passphrase(self, new_passphrase: str):
        """
        Set up a new passphrase to perform an administrative task

        :param new_passphrase: a new passphrase(str)
        :return: None
        """
        self.passphrase = new_passphrase
        print('New passphrase has been set.')

    def update_blueprint(self):
        """
        Update all table blueprints (table names and contents)
        """
        self.blueprint = {}
        table_names = self.get_table_names()
        for table_name in table_names:
            table_info = self.get_table_info(table_name)
            self.blueprint[table_name] = [info[1] for info in table_info]

    def is_table_exists(self, table_name: str) -> bool:
        """
        Check if the specified table is already exists

        :param table_name: table name in str
        :return: is_exists(bool)
        """
        self.update_blueprint()

        try:
            self.table(table_name).get().go()
        except NameError:
            return False

        return True

    def is_admin(self, passphrase: str) -> bool:
        """
        Check if you can perform administrative task or not

        :param passphrase: passphrase for administrative level methods
        :return: is_admin(bool)
        """
        if self.passphrase is None:
            err_msg = 'Passphrase is not set. Please call "setup_passphrase(new_passphrase)".'
            raise ValueError(err_msg)

        if passphrase == self.passphrase:
            return True
        return False

    def create_table(self, table_name: str, contents: dict, passphrase: str | None = None) -> bool:
        """
        Creates new table in the database

        :param table_name: table name in str
        :param contents: dict of field name and its field attributes
        :param passphrase: passphrase for administrative level methods
        :return: is_success(bool)
        """
        if passphrase is None:
            err_msg = 'Please provide "passphrase" in the args to perform administrative methods.'
            raise ValueError(err_msg)
        if not self.is_admin(passphrase):
            raise ValueError('The given passphrase is not match, table creation failed.')

        is_exists = self.is_table_exists(table_name)

        val_attr = ','.join(str(key + ' ' + val) for key, val in contents.items())
        sql = f'CREATE TABLE IF NOT EXISTS {table_name} ({val_attr})'
        self.cur.execute(sql)

        is_success = (not is_exists) and self.is_table_exists(table_name)

        if is_success:
            self.con.commit()
            print(f'Table `{table_name}` has been created.')
            print(contents)
        else:
            print('Table creation failed.')

        return is_success

    def delete_table(self, table_name: str, passphrase: str | None = None) -> bool:
        """
        Delete existing table from database

        :param table_name: table name in str
        :param passphrase: passphrase for administrative level methods
        :return: is_success(bool)
        """
        if passphrase is None:
            err_msg = 'Please provide "passphrase" in the args to perform administrative methods.'
            raise ValueError(err_msg)
        if not self.is_admin(passphrase):
            raise ValueError('The given passphrase is not match, table deletion failed.')

        is_exists = self.is_table_exists(table_name)

        if not is_exists:
            print(f'There is no table named `{table_name}`. Table deletion failed.')
            return False

        sql = f'DROP TABLE {table_name}'
        self.cur.execute(sql)

        is_success = is_exists and (not self.is_table_exists(table_name))
        if is_success:
            self.con.commit()
            print(f'Table `{table_name}` has been deleted.')
        else:
            print('Table deletion failed. No table has been deleted.')

        return is_success

    def get_table_names(self) -> list[str]:
        """
        Get table names in the database

        :return: table names(list of str)
        """
        sql = 'SELECT name FROM sqlite_master WHERE type="table"'
        self.cur.execute(sql)
        res = self.cur.fetchall()
        table_names = [ele[0] for ele in res]

        return table_names

    def get_table_info(self, table_name: str) -> list:
        """
        Get specified table info

        :param table_name: table name you want to know about
        :return: table information using PRAGMA(list)
        """
        sql = f'PRAGMA table_info({table_name})'
        self.cur.execute(sql)
        table_info = self.cur.fetchall()

        return table_info

    def table(self, table_name: str) -> Table:
        """
        The sql builder starts here, get the specified table to starts query

        :param table_name: table name you want to take action
        :return: Table object
        """

        # validation
        if table_name not in self.blueprint:
            raise NameError(f'There is no table named `{table_name}`')

        sqlbuilder = SQLBuilder(self.con, self.cur, table_name, self.blueprint[table_name])

        return Table(sqlbuilder)
