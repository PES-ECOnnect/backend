import psycopg2
import psycopg2.extras
from configparser import ConfigParser


def config(filename='data/database.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db


def getConnection():
    params = config()
    conn = psycopg2.connect(**params)
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
        print("Successfully inserted.")
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
