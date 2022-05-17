from app import app
import data.DBUtils as db

def test_iniBD():
    token = '93003eec-b589-11ec-a4e2-00155d3ce0fa'
    db.insert("INSERT INTO sessiontoken VALUES (%s, 4)", (token,))
    type = 'testAddQuest'
    db.insert("INSERT INTO reviewableType (name) VALUES (%s)", (type,))

def test_addQuestion():
    name = 'testAddQuest'
    query = db.select("SELECT typeid FROM reviewableType WHERE name = %s", (name, ), True)
    typeId = query['typeid']
    response = app.test_client().post("/questions?token=93003eec-b589-11ec-a4e2-00155d3ce0fa&statement=newTestQuestion&type=testAddQuest")
    assert response.status_code == 200
    query = db.select("SELECT statement FROM question WHERE typeId  = %s AND statement = 'newTestQuestion'", (typeId,), True)
    assert query['statement'] is not None

def test_addCompanyQuestion():
    response = app.test_client().post("/companies/questions?token=93003eec-b589-11ec-a4e2-00155d3ce0fa&statement=newTestQuestion")
    assert response.status_code == 200
    query = db.select("SELECT statement FROM question WHERE typeId  = 1 AND statement = 'newTestQuestion'", None, True)
    assert query['statement'] is not None

def test_cleanDB():
    name = 'testAddQuest'
    query = db.select("SELECT typeid FROM reviewableType WHERE name = %s", (name,), True)
    typeId = query['typeid']
    db.delete("DELETE FROM sessiontoken WHERE token = '93003eec-b589-11ec-a4e2-00155d3ce0fa'")
    db.delete("DELETE FROM reviewableType WHERE typeid = %s", (typeId,))
    db.delete("DELETE FROM question WHERE statement = 'testAddQuest'")

import data.DBUtils as db


import data.DBUtils as db


import data.DBUtils as db


'''

# GET QUESTIONS

def test_getCompanyQuestions():

# ANSWER QUESTIONS

def test_answerProductQuestion():

def test_answerCompanyQuestion():
'''


def test_initDB():
    db.insert("INSERT INTO sessiontoken VALUES ('93003eec-b589-11ec-a4e2-00155d3ce0fb',1)")
    db.insert("INSERT INTO question VALUES (1, 1, 'test')")


def test_modifyQuestion():
    response = app.test_client().put("questions/1?token=93003eec-b589-11ec-a4e2-00155d3ce0fb&newQuestion=haha")
    assert response.status_code == 200
    assert response.data == b'{"status":"success"}\n'


def test_deleteQuestion():
    response = app.test_client().delete("questions/1?token=93003eec-b589-11ec-a4e2-00155d3ce0fb")
    assert response.status_code == 200
    assert response.data == b'{"status":"success"}\n'


def test_cleanDB():
    db.delete("DELETE FROM sessiontoken where token = '93003eec-b589-11ec-a4e2-00155d3ce0fb'")