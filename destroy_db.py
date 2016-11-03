"""
Destroy the database for the specified user
(who must not be siteUserAdmin)
"""

import pymongo
from pymongo import MongoClient
import sys

import secrets.admin_secrets
import secrets.client_secrets

MONGO_ADMIN_URL = "mongodb://{}:{}@{}:{}/admin".format(
    secrets.admin_secrets.admin_user,
    secrets.admin_secrets.admin_pw,
    secrets.admin_secrets.host, 
    secrets.admin_secrets.port)

try: 
    dbclient = MongoClient(MONGO_ADMIN_URL)
    db = getattr(dbclient, secrets.client_secrets.db)
    print("Got database")
    print("Attempting drop users")
    # db.command( {"dropAllUsersFromDatabase": 1 } )
    #db.remove_user(secrets.client_secrets.db_user)
    print("Dropped database users for {}".format(secrets.client_secrets.db))
    db.command( {"dropDatabase": 1 } )
    print("Dropped database {}".format(secrets.client_secrets.db))
except Exception as err:
    print("Failed")
    print(err)



        
