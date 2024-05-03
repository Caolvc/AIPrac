import json
from dbserver import DbServer
db = DbServer()
chars = db.query_characters()
print(type(chars))