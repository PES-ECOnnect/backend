from app import app
import json
from domain.Reviewable import *
import data.DBUtils as dbu


# GET ALL

def test_iniDB():
    dbu.insert("INSERT INTO sessiontoken VALUES ('test_token', 1)")

def test_getinfoCompanies():
    insert = app.test_client().post("companies?token=TEST_POL&name=testpytestcompany&imageURL=xd&lat=0&lon=0")
    q = "SELECT idreviewable from reviewable WHERE name = 'testpytestcompany'"
    result = dbu.select(q, args=(), one=True)
    uri = "companies/"+ str(result["idreviewable"]) + "?token=TEST_POL"
    resp = app.test_client().get(uri)
    correct = ({ "imageurl": "xd",
                 "latitude": "0.00",
                 "longitude": "0.00",
                 "name": "testpytestcompany",
                 #"questions": [],
                 "ratings": [0,0,0,0,0,0],
                 "type": "Company" })
    response = json.loads(resp.get_data(as_text=True))
    q = "DELETE FROM reviewable WHERE name = 'testpytestcompany'"
    result = dbu.delete(q, args=())
    assert (
            response["imageURL"] == correct["imageurl"] and
            response["latitude"] == correct["latitude"] and
            response["longitude"] == correct["longitude"] and
            response["name"] == correct["name"] and
            #response["questions"] == correct["questions"] and
            response["ratings"] == correct["ratings"] and
            response["type"] == correct["type"]
    )

def test_getinfoProduct():
    insert = app.test_client().post("products?token=TEST_POL&name=testpytestproduct&imageURL=xd&manufacturer=jo&type=Generadors")
    q = "SELECT idreviewable from reviewable WHERE name = 'testpytestproduct'"
    result = dbu.select(q, args=(), one=True)
    uri = "products/" + str(result["idreviewable"]) + "?token=TEST_POL"
    resp = app.test_client().get(uri)
    correct = ({ "imageURL": "xd",
                 "manufacturer": "jo",
                 "name": "testpytestproduct",
                 #"questions": [],
                 "ratings": [ 0, 0, 0, 0, 0, 0 ],
                 "type": "Generadors" })
    response = json.loads(resp.get_data(as_text=True))
    q = "DELETE FROM reviewable WHERE name = 'testpytestproduct'"
    result = dbu.delete(q, args=())
    assert (
        response["imageURL"]==correct["imageURL"] and
        response["manufacturer"]==correct["manufacturer"] and
        response["name"] == correct["name"] and
        #response["questions"] == correct["questions"] and
        response["ratings"] == correct["ratings"] and
        response["type"]==correct["type"]
    )


from app import app
import json
from domain.Reviewable import *
import data.DBUtils as dbu


# GET ALL

#def test_getProductsFromType():

def test_getinfoCompanies():
    insert = app.test_client().post("companies?token=TEST_POL&name=testpytestcompany&imageURL=xd&lat=0&lon=0")
    q = "SELECT idreviewable from reviewable WHERE name = 'testpytestcompany'"
    result = dbu.select(q, args=(), one=True)
    uri = "companies/"+ str(result["idreviewable"]) + "?token=TEST_POL"
    resp = app.test_client().get(uri)
    correct = ({ "imageurl": "xd",
                 "latitude": 0.0,
                 "longitude": 0.0,
                 "name": "testpytestcompany",
                 #"questions": [],
                 "ratings": [0,0,0,0,0,0],
                 "type": "Company" })
    response = json.loads(resp.get_data(as_text=True))
    #q = "DELETE FROM reviewable WHERE name = 'testpytestcompany'"
    #result = dbu.delete(q, args=())
    assert (
            response["imageURL"] == correct["imageurl"] and
            float(response["latitude"]) == float(correct["latitude"]) and
            float(response["longitude"]) == float(correct["longitude"]) and
            response["name"] == correct["name"] and
            #response["questions"] == correct["questions"] and
            response["ratings"] == correct["ratings"] and
            response["type"] == correct["type"]
    )

def test_getinfoProduct():
    insert = app.test_client().post("products?token=TEST_POL&name=testpytestproduct&imageURL=xd&manufacturer=jo&type=Generadors")
    q = "SELECT idreviewable from reviewable WHERE name = 'testpytestproduct'"
    result = dbu.select(q, args=(), one=True)
    uri = "products/" + str(result["idreviewable"]) + "?token=TEST_POL"
    resp = app.test_client().get(uri)
    correct = ({ "imageURL": "xd",
                 "manufacturer": "jo",
                 "name": "testpytestproduct",
                 #"questions": [],
                 "ratings": [ 0, 0, 0, 0, 0, 0 ],
                 "type": "Generadors" })
    response = json.loads(resp.get_data(as_text=True))
    #q = "DELETE FROM reviewable WHERE name = 'testpytestproduct'"
    #result = dbu.delete(q, args=())
    assert (
        response["imageURL"]==correct["imageURL"] and
        response["manufacturer"]==correct["manufacturer"] and
        response["name"] == correct["name"] and
        #response["questions"] == correct["questions"] and
        response["ratings"] == correct["ratings"] and
        response["type"]==correct["type"]
    )

def test_deleteReviewable():
    # Insert reviewables
    rev = Reviewable(id = 91243123412341234123,name='ProvaEliminat',type='Solar panel',imageURL='https://xd',manufacturer='jo',lat="null",lon="null")
    rev.insert()
    #getproductid
    q = "SELECT idreviewable FROM reviewable where name = 'ProvaEliminat'"
    id = dbu.select(q,(),True)
    print(id["idreviewable"])
    # Insert Valorations
    rev.review(id['idreviewable'],"TEST_POL",2)
    # Insert Answers
    rev.answerQuestion(productId=id['idreviewable'],token="TEST_POL",chosenOption=0,questionIndex=4)
    # Execute DeleteReviewable
    resp = app.test_client().delete("/products/" + str(id['idreviewable']) + "?token=test_token")
    # Check valorations, answers, equip/installers and reviewable are not in the database
    q = "SELECT * FROM reviewable WHERE idreviewable = %s"
    select = dbu.select(q,(id['idreviewable'],),True)
    print(select)
    assert select is None
    q = "SELECT * FROM valoration WHERE idreviewable = %s"
    select = dbu.select(q, (id['idreviewable'],), True)
    assert select is None
    q = "SELECT * FROM equipmentproduct WHERE idreviewable = %s"
    select = dbu.select(q, (id['idreviewable'],), True)
    assert select is None
    q = "SELECT * FROM answer WHERE idreviewable = %s"
    select = dbu.select(q, (id['idreviewable'],), True)
    assert select is None


def test_editProduct():
    #insert token
    token = 'test_token'
    dbu.insert("INSERT INTO sessiontoken VALUES (%s, 4)", (token, ))
    type = 'test'
    dbu.insert("INSERT INTO reviewableType (name) VALUES (%s)", (type,))
    # insert product
    prod = Reviewable(id= 7777, name = 'testEdit', type = 'Generadors', imageURL = 'image', manufacturer='testMan', lat = 'null', lon = 'null')
    prod.insert()
    name = 'testEdit'
    query = dbu.select("SELECT idreviewable FROM reviewable WHERE name = %s", (name, ), True)
    prodId = query['idreviewable']
    req = "/products/"+str(prodId)+"?token=test_token&name=newNameEdit&manufacturer=newMan&imageURL=newImage&type=test"
    print(req)
    response = app.test_client().post(req)
    assert response.status_code == 200

    product = dbu.select("SELECT name FROM reviewable WHERE idreviewable = %s", (prodId, ), True)
    info = dbu.select("SELECT * FROM equipmentproduct WHERE idreviewable = %s", (prodId, ), True)
    assert product['name'] == 'newNameEdit'
    assert info['manufacturer'] == 'newMan'

    #dbu.delete("DELETE FROM reviewableType WHERE name = 'test'")
    #dbu.delete("DELETE FROM reviewable WHERE idreviewable = %s", (prodId,))

def test_editCompany():
    # insert product
    comp = Reviewable(id=7777, name='testEdit', type='Company', imageURL='image', manufacturer=None, lat=0.0,
                      lon=0.0)
    comp.insert()
    name = 'testEdit'
    query = dbu.select("SELECT idreviewable FROM reviewable WHERE name = %s", (name,), True)
    compId = query['idreviewable']
    req = "/companies/" + str(
        compId) + "?token=test_token&name=newNameEdit2&lat=1.1&lon=1.1&imageURL=newImage"
    print(req)
    response = app.test_client().post(req)
    assert response.status_code == 200

    company = dbu.select("SELECT name FROM reviewable WHERE idreviewable = %s", (compId,), True)
    info = dbu.select("SELECT * FROM installercompany WHERE idreviewable = %s", (compId,), True)
    assert company['name'] == 'newNameEdit2'
    assert float(info['lat']) == 1.1
    assert float(info['lon']) == 1.10

    #dbu.delete("DELETE FROM sessiontoken WHERE token = 'test_token'")
    #dbu.delete("DELETE FROM reviewable WHERE idreviewable = %s", (compId,))

def test_cleanDB():
    dbu.delete("DELETE FROM sessiontoken WHERE token = 'test_token'")
    dbu.delete("DELETE FROM reviewableType WHERE name = 'test'")


    dbu.delete("DELETE FROM reviewable WHERE name = 'newNameEdit2'")


    dbu.delete("DELETE FROM reviewable WHERE name = 'newNameEdit'")

    q = "DELETE FROM reviewable WHERE name = 'testpytestproduct'"
    result = dbu.delete(q, args=())
    q = "DELETE FROM reviewable WHERE name = 'testpytestcompany'"
    result = dbu.delete(q, args=())

    '''
# CREATE

def test_createProduct():   

def test_createCompany():

# GET INFO 

def test_getInfoProduct():

def test_getInfoCompany():

# REVIEW

def test_reviewProduct():

def test_reviewCompany():
'''