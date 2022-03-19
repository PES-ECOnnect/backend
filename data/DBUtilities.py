import sqlite3
class DBUtilities:
    # Function to provide query function, one = single result
    def query_db(query, args=(), one=False):
        con = sqlite3.connect('main.db')
        cur = con.execute(query, args)
        rv = cur.fetchall()
        cur.close()
        con.commit()
        return (rv[0] if rv else None) if one else rv