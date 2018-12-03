from pymongo import MongoClient
from bson.objectid import ObjectId
from dateutil.relativedelta import relativedelta
from datetime import datetime

class Mongodb:
    def __init__(self, ip, port):
        self.conn = MongoClient("{0}:{1}".format(ip,port))
        try:
            info = self.conn.server_info()
        except Exception as err:
            raise Exception(err)
        else:
            for msg in info:
                print('{0}:{1}'.format(msg,info[msg]))
    def login_db(self, name):
        self.db = eval('self.conn.'+name)
        return self.db
    def logout_db(self):
        self.db.logout()
    def collection(self, name):
        self.tb = eval('self.db.'+name)
    def find(self, key=None, value=None):
        return self.tb.find_one({key: value})
    def filter(self,dic=None):
        return [i for i in self.tb.find(dic)]
    def count(self,dic=None):
        return self.tb.find(dic).count()
    def insert(self, dic):
        if self.find('_id',dic['_id']):
            i = 0
            while True:
                i+=1
                if not self.find('_id',dic['_id']+'-{}'.format(i)):
                    dic['_id'] = dic['_id']+'-{}'.format(i)
                    self.tb.insert_one(dict([(k,dic[k]) for k in sorted(dic.keys())]))
                    break
        else:
            print(dict([(k,dic[k]) for k in sorted(dic.keys())]))
            self.tb.insert_one(dict([(k,dic[k]) for k in sorted(dic.keys())]))
    def close(self):
        self.conn.close()

def saveDB(db, table, data, server, port=27017):
    c = Mongodb(server,port)
    c.login_db(AFI)
    c.collection(table)
    c.insert(data)
    c.close

def monthPass(m):
    conn = MongoClient('127.0.0.1:27017')
    db = conn['1521900003T0']
    collection=db.T1_Log
    result = collection.find({'Time':{'$gte': datetime(2018,m,1),'$lt': datetime(2018,m,1)+relativedelta(months=1)}}).count()
    return result
# conn = MongoClient('192.168.45.68:27017')

# db = conn.AFI
# collection = db.LED
# collection.stats

# ## filter db from defined time to currnt 
# result = [i for i in collection.find({'Time':{'$gt': datetime(2018,1,1)}})]

# >>> for c in result: print(c)
# {'Station-id': '1', 'Result': 'PASS', '_id': 'F81D0FDA6863', 'Time': datetime.datetime(2018, 9, 18, 11, 49, 3, 403000)}
# {'Station-id': '1', 'Result': 'PASS', '_id': 'F81D0FDA6863-1', 'Time': datetime.datetime(2018, 9, 18, 11, 51, 57, 46000)}
# {'Station-id': '1', 'Result': 'PASS', '_id': 'F81D0FDA6863-2', 'Time': datetime.datetime(2018, 9, 18, 11, 53, 22, 439000)}
# {'Station-id': '1', 'Result': 'FAIL', '_id': 'F81D0FDA6863-3', 'Time': datetime.datetime(2018, 9, 18, 13, 1, 58, 719000)}

# collection.find({"Result":"PASS","_id":{'$regex':'^F81D0FDA6863.*'}}).count()
