from app import app
import json
from domain.Reviewable import *
import data.DBUtils as dbu


# GET ALL

#def test_getProductsFromType():

def test_getinfoCompanies():
    resp = app.test_client().get("companies/1?token=93003eec-b589-11ec-a4e2-00155d3ce0fb")
    correct = ({ "imageURL": "https://cdn.shopify.com/s/files/1/0533/2089/files/placeholder-images-product-6_large.png",
                 "latitude": "10.04",
                 "longitude": "5.05",
                 "name": "TestName",
                 "questions": [],
                 "ratings": [ 0, 0, 1, 0, 0, 1 ],
                 "type": "Company" })
    response = json.loads(resp.get_data(as_text=True))
    assert (
            response["imageURL"] == correct["imageURL"] and
            response["latitude"] == correct["latitude"] and
            response["longitude"] == correct["longitude"] and
            response["name"] == correct["name"] and
            response["questions"] == correct["questions"] and
            response["ratings"] == correct["ratings"] and
            response["type"] == correct["type"]
    )

def test_getinfoProduct():
    resp = app.test_client().get("products/2?token=93003eec-b589-11ec-a4e2-00155d3ce0fb")
    correct = ({ "imageURL": "https://cdn.shopify.com/s/files/1/0533/2089/files/placeholder-images-product-6_large.png",
                 "manufacturer": "Test",
                 "name": "ProductTest",
                 "questions": [],
                 "ratings": [ 0, 0, 0, 1, 0, 0 ],
                 "type": "TestType" })
    response = json.loads(resp.get_data(as_text=True))
    assert (
        response["imageURL"]==correct["imageURL"] and
        response["manufacturer"]==correct["manufacturer"] and
        response["name"] == correct["name"] and
        response["questions"] == correct["questions"] and
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
    rev.review(id['idreviewable'],"44cab830-b668-11ec-91af-1a0e95636881,3",2)
    # Insert Answers
    rev.answerQuestion(productId=id['idreviewable'],token="44cab830-b668-11ec-91af-1a0e95636881",chosenOption=0,questionIndex=4)
    # Execute DeleteReviewable
    resp = app.test_client().delete("/products/" + str(id['idreviewable']) + "?token=44cab830-b668-11ec-91af-1a0e95636881")
    print(resp)
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