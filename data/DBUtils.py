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


def query_db(query, args=(), one=False):
    con = sqlite3.connect('data/main.db')
    con.row_factory = dict_factory
    cur = con.execute(query, args)
    rv = cur.fetchall()
    cur.close()
    con.commit()
    return (rv[0] if rv else None) if one else rv
