from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime

conn = MongoClient('192.168.45.68:27017')

db = conn.AFI
collection = db.LED
collection.stats

## filter db from defined time to currnt 
result = [i for i in collection.find({'Time':{'$gt': datetime(2018,1,1)}})]

>>> for c in result:
...     print(c)
... 
{'Station-id': '1', 'Result': 'PASS', '_id': 'F81D0FDA6863', 'Time': datetime.datetime(2018, 9, 18, 11, 49, 3, 403000)}
{'Station-id': '1', 'Result': 'PASS', '_id': 'F81D0FDA6863-1', 'Time': datetime.datetime(2018, 9, 18, 11, 51, 57, 46000)}
{'Station-id': '1', 'Result': 'PASS', '_id': 'F81D0FDA6863-2', 'Time': datetime.datetime(2018, 9, 18, 11, 53, 22, 439000)}
{'Station-id': '1', 'Result': 'FAIL', '_id': 'F81D0FDA6863-3', 'Time': datetime.datetime(2018, 9, 18, 13, 1, 58, 719000)}

