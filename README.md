[![GitHub stars](https://img.shields.io/github/stars/Sajjal/SQLite_As_JSON)](https://github.com/Sajjal/SQLite_As_JSON/stargazers)
[![GitHub issues](https://img.shields.io/github/issues/Sajjal/SQLite_As_JSON)](https://github.com/Sajjal/SQLite_As_JSON/issues)
![GitHub language count](https://img.shields.io/github/languages/count/Sajjal/SQLite_As_JSON)
![GitHub top language](https://img.shields.io/github/languages/top/Sajjal/SQLite_As_JSON)
![GitHub repo size](https://img.shields.io/github/repo-size/Sajjal/SQLite_As_JSON)

# SQLite As JSON

A Python helper package to do SQLite CRUD operation via JSON object. This package is developed using Python 3 with no external dependencies.

---

## Background (_Why this package was developed?_)

I'm working on another Python project that requires me to store a very minimal amount of data so I decided to use SQLite as a database. I feel that it is very easy to make typos and errors while creating multiple tables and doing some CRUD operations. Therefore, I created a separate helper Class that takes in a JSON object and parses it to create tables and do CRUD operations according to the instruction defined in that JSON object. It significantly helped to minimize errors. I thought it could be useful to others too and here it is.

## Installation:

### Download Package:

- `pip install SQLiteAsJSON`

### Setup

- Create table schema on **db_config.json** file as:

```JSON
[{
        "table_name": "my_table",
        "fields": [
            { "name": "id", "type": "char", "length": "50", "null": 0 },
            { "name": "timestamp", "type": "char", "length": "20", "null": 0 },
            { "name": "email", "type": "char", "length": "50", "null": 0 },
            { "name": "password", "type": "char", "length": "50", "null": 0 },
            { "name": "personID", "type": "char", "length": "50", "null": 0 }
        ],
        "config": {
            "primary_key": "id",
            "foreign_key": {
                "field": "personID",
                "reference_table": "persons",
                "reference_table_field": "id" }
                }
        },

    {
        "table_name": "persons",
        "fields": [
            { "name": "id", "type": "char", "length": "50", "null": 0 },
            { "name": "timestamp", "type": "char", "length": "20", "null": 0 },
            { "name": "first_name", "type": "char", "length": "20", "null": 0 },
            { "name": "last_name", "type": "char", "length": "20", "null": 1 },
            { "name": "address", "type": "char", "length": "100", "null": 1 }
        ],
        "config": {
            "primary_key": "id"
        }
    }]
```

- You can add more than one table
- You must have `id` and `timestamp` fields in each table, these will be auto-populated
- Each table should have at most one `primary_key`, you may have one optional `foreign_key` per table
- If you want the field to be `NOT NULL` pass `"null" : 0` else pass `"null" : 1`

---

#### Initialize:

- Instantiate Class object as: `db = ManageDB(<database name>, <path to db_config.json>)`
- Example:

  ```python
  from SQLiteAsJSON import ManageDB

  db = ManageDB('my_databse.db', 'db_config.json')
  ```

- The default `check_same_thread` option for `SQLite` is `True`. You can set it `False` as:

  ```python
  db = ManageDB('my_databse.db', 'db_config.json', False)
  ```

#### Create table

- Table can be created by calling `db.create_table()`
- Example:
  ```python
  db.create_table()
  ```
- Returns: Success message(dict): If the table creation was successful else none

#### Insert data

- Pass **table name** and **data to insert** as: `db.insert_data(<table_name>, <data_to_insert>)`
- Example:

  ```python
  db.insert_data('my_table', {"email": 'a@b.com', "password": 'password', "personID":'1'})
  ```

- Returns: Success message(dict): If the insertion was successful else none
- SQLite does not supports boolean data types, it is recommended to use 1 for True and 0 for False
- To insert **_Array (List)_** or **Object (dict)**, first stringify it using `json.dumps([List])` or `json.dumps({dict})`

#### Search data

- Pass **table name** w/ **optional search condition** as: `db.search_data(<table_name>, <optional_search_condition>)`
- Example:

  ```python
  db.search_data('my_table')
  db.search_data('my_table', {"id":"55bd5301b331439fae2ba8572942ded5"})
  ```

- Multiple search conditions can be passed as:

  ```python
  db.search_data('my_table', {"email":"a@b.com", "personID":"1"})
  ```

- Multiple search conditions will be joined by `AND` operator by default. It can be changed to `OR` as:

  ```python
    db.search_data('my_table', {"email":"a@b.com", "personID":"1"}, 'OR')
  ```

- Returns: Search results (dict): Search results as a JSON object

#### Update data

- Pass **table name**, **row id** and **data to update** as: `db.update_data(<table_name>, <row_id>, <data_to_update>)`
- Example:

  ```python
  db.update_data('my_table', '55bd5301b331439fae2ba8572942ded5', {
        "email:abc@example.com","password":"hello_world"
      })
  ```

- Returns: Success message(dict): If the update was successful else none

#### Delete data

- Pass **table name** and **row id** as: `db.delete_data(<table_name>, <row_id>)`
- Example:

  ```python
  db.delete_data('my_table', '55bd5301b331439fae2ba8572942ded5')
  ```

- Returns: Success message(dict): If the delete operation was successful else none

---

With Love,

**Sajjal**
