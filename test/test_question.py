from app import app

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