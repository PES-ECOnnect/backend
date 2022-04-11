from app import app

import json

import data.DBUtils as db
import domain.Reviewable as rev

def test_initDB():
    db.insert("INSERT INTO sessiontoken VALUES ('93003eec-b589-11ec-a4e2-00155d3ce0fb',1)")

def test_getProductTypes():
    response = app.test_client().get("/products/types?token=93003eec-b589-11ec-a4e2-00155d3ce0fb")
    assert response.status_code == 200

def test_createProductType():
    response = app.test_client().post("/products/types?token=93003eec-b589-11ec-a4e2-00155d3ce0fb&name=newTypeXXX", data=json.dumps({'questions':['q1', 'q2']}), content_type='application/json')
    assert response.status_code == 200
    assert response.data == b'{"status":"success"}\n'

def test_cleanDB():
    id = rev.getReviewableTypeIdByName('newTypeXXX')
    db.delete("DELETE FROM question where typeid = %s", (id,))
    db.delete("DELETE FROM reviewableType where name = 'newTypeXXX'")
    db.delete("DELETE FROM sessiontoken where token = '93003eec-b589-11ec-a4e2-00155d3ce0fb'")

'''
def test_getProductTypes():

def test_createProductType():
'''