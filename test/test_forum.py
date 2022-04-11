from app import app
import json

import data.DBUtils as db



def test_getUsedTags():
    #response = app.test_client().get("/")
    #assert response.status_code == 200
    #assert response.data == b"PES Econnect Root!"

def test_cleanDB():
    # clean database
    # db.delete("DELETE FROM users where email in ('sign@up.test')")


