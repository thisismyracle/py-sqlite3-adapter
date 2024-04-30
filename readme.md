# py-sqlite3-adapter

A basic adapter for python-sqlite3

## Installation

Clone this repo, copy the whole folder to your project, rename it to "sqlite3adapter", and import the package.
```python
from sqlite3adapter.database import Database
```

## Usage

Initialization
```python
from sqlite3adapter.database import Database

db = Database('my-database.db')
db.setup_passphrase('my-passphrase')
```
---
Create a new table*
```python
db.create_table('tbl_fruit', {
    'id': 'INTEGER PRIMARY KEY',
    'name': 'TEXT',
    'price': 'INTEGER',
    'stock': 'INTEGER'
}, passphrase='my-passphrase')
```
---
Delete an existing table*
```python
db.delete_table('table_fruit', passphrase='my-passphrase')
```
<sub>*Passphrase is required for performing administrative task such as creating and deleting tables.<sub>

***

Run an INSERT statement
```python
db.table('tbl_fruit').insert([
    (None, 'apple', 500, 5),
    (None, 'banana', 400, 150)
]).go()
```
---
Run a GET statement
```python
db.table('tbl_fruit').get().go()
```
---
Run a GET-WHERE statement
```python
db.table('tbl_fruit').get().where('price < 200').go()
```
---
Run a SET statement
```python
db.table('tbl_fruit').set('price', 100).go()
```
---
Run a SET-WHERE statement
```python
db.table('tbl_fruit').set('price', 100).where('name = "apple"').go()
```
---
For the complete example please run [main.py](https://github.com/thisismyracle/py-sqlite3-adapter/blob/main/main.py).

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)