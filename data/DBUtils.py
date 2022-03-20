import sqlite3


# Make Query results associative.
# - Source: https://stackoverflow.com/questions/3300464/how-can-i-get-dict-from-sqlite-query
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def getCon():
    con = sqlite3.connect('data/main.db')
    con.row_factory = dict_factory
    return con
