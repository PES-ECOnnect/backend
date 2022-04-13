from app import app


# GET ALL

#def test_getProductsFromType():

def test_getinfoCompanies():
    response = app.test_client().get("companies/1?token=93003eec-b589-11ec-a4e2-00155d3ce0fb")
    correct = (b'{"imageURL":"https://cdn.shopify.com/s/files/1/0533/2089/files/placeholder-i'\
                b'mages-product-6_large.png","latitude":"10.04","longitude":"5.05","name":"Tes'\
               b'tName","questions":[],"ratings":[0,0,1,0,0,1],"type":"Company"}\n')
    assert response.data == correct
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