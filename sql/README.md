# Assignment SQL

The accepted implementation uses persistent SQLite storage in `data/cardio_train.sqlite`.

- `03_create_table_sqlite.sql`: SQLite schema, primary key and category constraints. Notebook 01 creates and imports the database when the table does not exist.
- `04_queries_sqlite.sql`: 13 queries ready to execute directly in SQLite.
- `01_create_table.sql` and `02_queries.sql`: optional Db2 reference versions.
- `queries.json`: Db2 query definitions; notebook 01 converts the row-limit syntax when executing with SQLite.

SQLite and local notebook execution replace IBM Cloud under the instructor-approved alternative. Db2 Cloud was not executed.
