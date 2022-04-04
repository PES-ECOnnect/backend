import psycopg2
import psycopg2.extras


def getConnection():
    conn = psycopg2.connect(
        host="localhost",
        database="econnect",
        user="pol",
        password="111111"
    )

    return conn


def select(query, args=(), one=False):
    conn = getConnection()

    # result rows represented by a list of python dicts
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute(query, args)
    rv = cur.fetchall()

    cur.close()
    conn.close()

    return (rv[0] if rv else None) if one else rv


def insert(query, args=()):
    conn = getConnection()
    cur = conn.cursor()

    try:
        cur.execute(query, args)
        conn.commit()
        return cur.lastrowid

    except psycopg2.Error:
        return False

    finally:
        cur.close()
        conn.close()


def update(query, args=()):
    conn = getConnection()
    cur = conn.cursor()
    try:
        cur.execute(query, args)
        conn.commit()
        return True

    except psycopg2.Error:
        return False

    finally:
        cur.close()
        conn.close()


def delete(query, args=()):
    conn = getConnection()
    cur = conn.cursor()
    try:
        cur.execute(query, args)
        conn.commit()
        return True

    except psycopg2.Error:
        return False

    finally:
        cur.close()
        conn.close()
