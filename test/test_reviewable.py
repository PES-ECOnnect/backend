from app import app
import json


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