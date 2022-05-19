import psycopg2
import psycopg2.extras
from configparser import ConfigParser
import os

def getConnection():
    params = {}
    '''
    params['host'] = os.environ.get('ECONNECT_DATABASE_HOST')
    params['database'] = os.environ.get('ECONNECT_DATABASE_NAME')
    params['password'] = os.environ.get('ECONNECT_DATABASE_PASSWORD')
    params['user'] = os.environ.get('ECONNECT_DATABASE_USER')
    '''
    conn = psycopg2.connect(
        database=os.environ.get('ECONNECT_DATABASE_NAME'),
        user=os.environ.get('ECONNECT_DATABASE_USER'),
        host=os.environ.get('ECONNECT_DATABASE_HOST'),
        password=os.environ.get('ECONNECT_DATABASE_PASSWORD')
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
        print("Successfully inserted.")

        return True

    except psycopg2.Error:
        return False

    finally:
        cur.close()
        conn.close()


def insertAndReturnLastRowId(query, args=()):
    conn = getConnection()
    cur = conn.cursor()

    try:
        cur.execute(query, args)
        conn.commit()
        print("Successfully inserted.")

        return True

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
