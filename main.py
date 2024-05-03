""" The main file to test the basic case of using Database module """

from database import Database


if __name__ == '__main__':

    # Create a database connection
    db = Database('my_database.db')
    db.setup_passphrase('lorem-ipsum')

    # Check if table exists
    print('Is tbl_fruit exists?')
    is_exists = db.is_table_exists('tbl_fruit')
    print(is_exists)

    # ADMINISTRATIVE: Delete the table if exists
    if is_exists:
        print('\nDeleting table if exists')
        print(db.delete_table('tbl_fruit', passphrase='lorem-ipsum'))

    # ADMINISTRATIVE: Create new table
    print('\nCreate new table called tbl_fruit')
    print(db.create_table('tbl_fruit', {
        'id': 'INTEGER PRIMARY KEY',
        'name': 'TEXT',
        'price': 'INTEGER',
        'stock': 'INTEGER'
    }, passphrase='lorem-ipsum'))

    # TIPS: Always include passphrase in function args to perform administrative task
    #       such as create_table and delete_table.
    #       This passphrase is not secret, but is always needed to perform administrative task.

    # Check if table exists (again)
    print('\nIs tbl_fruit exists? (2)')
    print(db.is_table_exists('tbl_fruit'))

    # GET statement
    print('\nLets see the tbl_fruit contains')
    print(db.table('tbl_fruit').get().go())

    # INSERT statement
    print('\nLets insert some fruits')
    print(db.table('tbl_fruit').insert([
        (None, 'apple', 500, 5),
        (None, 'banana', 400, 150)
    ]).go())
    print(db.table('tbl_fruit').get().go())

    # GET-WHERE statement
    print('\nHow about we check the running out fruits?')
    print(db.table('tbl_fruit').get().where('stock < ?', 50).go())

    # SET-WHERE statement
    print('\nStocks are cominggg! renewing stock count!')
    print(db.table('tbl_fruit').set('stock', 105).where('name = ?', 'apple').go())
    print(db.table('tbl_fruit').get().go())

    # SET statement
    print('\nHere we comes! lowering the PRICE!')
    print(db.table('tbl_fruit').set('price', 100).go())
    print(db.table('tbl_fruit').get().go())
