# SQL-Based Equipment Checkout System

This project is a small command-line application that interacts with a relational SQL database (SQLite). It models a simple equipment checkout workflow using three related tables: `users`, `items`, and `loans`. The software demonstrates full CRUD functionality by creating the database tables, querying data (including JOIN queries), inserting new records, updating existing records, and deleting records when allowed.

## Instructions for Build and Use

[Software Demo] https://youtu.be/6WbaLqQ4ApI

Steps to build and/or run the software:

1. Make sure Python 3 is installed.
2. Place `app.py`, `db.py`, and `ops.py` in the same folder.
3. In a terminal, navigate to that folder and run:
   - `python app.py`
4. The program will automatically create `checkout.db` (SQLite database) the first time it runs.

Instructions for using the software:

1. Run the program with `python app.py`.
2. Choose option **2** to seed the database with sample users/items (recommended for demo/testing).
3. Use the menu to perform operations such as:
   - **Query (SELECT):** List items, search items, list active loans
   - **Add (INSERT):** Add user, add item, checkout item
   - **Update (UPDATE):** Return loan, update item name
   - **Delete (DELETE):** Delete loan, delete item, delete user

## Development Environment

To recreate the development environment, you need the following software and/or libraries with the specified versions:

* Python 3.10+ (any recent Python 3 version should work)
* SQLite (included with Python via the built-in `sqlite3` module)
* No external Python libraries required

## Useful Websites to Learn More

I found these websites useful in developing this software:

* [Python sqlite3 documentation](https://docs.python.org/3/library/sqlite3.html)
* [SQLite Foreign Key Support](https://www.sqlite.org/foreignkeys.html)
* [SQLite SQL Language Reference](https://www.sqlite.org/lang.html)

## Future Work

The following items I plan to fix, improve, and/or add to this project in the future:

* [ ] Add reporting queries (ex: overdue loans, most borrowed items)
* [ ] Add aggregate summaries (ex: COUNT of active loans per user, COUNT of items per category)
* [ ] Improve validation and add more edit options (ex: update due date, update categories)
