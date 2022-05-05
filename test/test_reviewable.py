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

def test_deleteReviewable():
    # Insert reviewables
    rev = Reviewable(id = 99,name='ProvaEliminat',type='Solar panel',imageURL='https://xd',manufacturer='jo',lat="null",lon="null")
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
    resp = app.test_client().delete("/products/" + str(id['idreviewable']) + "?token=78801988-cbb5-11ec-8824-1eb137071756")
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