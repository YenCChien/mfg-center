from pymongo import MongoClient
from bson.objectid import ObjectId
from dateutil.relativedelta import relativedelta
from datetime import datetime
import pandas as pd

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
    conn = MongoClient('192.168.45.38:27017')
    db = conn['1521900003T0']
    collection=db.T1_Log
    result = collection.find({'Time':{'$gte': datetime(2018,m,1),'$lt': datetime(2018,m,1)+relativedelta(months=1)}}).count()
    return result

def getErrorCount(stDate,edDate):
    conn = MongoClient('192.168.45.38:27017')
    db = conn['1521900003T0']
    collection=db.T1_Log
    ErrorCount = {}
    r = [i for i in collection.find({'Time':{'$gt': stDate,'$lt': edDate},'Result':'FAIL'})]
    for s in r:
        try:
            if len(s['ErrorCode']) > 5:
                ErrorCount.update({'Others':0})
            else:
                ErrorCount.update({s['ErrorCode']:0})
        except:continue
    for s in r:
        try:
            if len(s['ErrorCode']) > 5:
                ErrorCount['Others'] += 1
            else:
                ErrorCount[s['ErrorCode']] += 1
        except:continue
    print(ErrorCount)
    return ErrorCount

def cpkLevel(cpkList):
    levelList = []
    for cpk in cpkList:
        if cpk < 0.67:
            levelList.append('D')
        elif 0.67 <= cpk < 1:
            levelList.append('C')
        elif 1 <= cpk < 1.33:
            levelList.append('B')
        elif 1.33 <= cpk < 1.67:
            levelList.append('A')
        else:
            levelList.append('A+')
    return levelList

def cpkinitalTable(stDate,edDate):
    conn = MongoClient('192.168.45.38:27017')
    db = conn['1521900003T0']
    colls = db.collection_names()
    collection=db.DsQAM
    getPass = [i for i in collection.find({'Time':{'$gt': stDate,'$lt': edDate},"Result":"PASS"})]
    # getPass = [i for i in wholeData if i['Result']=='PASS' and (stDate < i['Time'] < edDate)]
    # print(getPass[0]['Frequency'])
    conn.close()
    df = pd.DataFrame(getPass)
    df = df.drop(['Frequency','ChResult','MeasurePwr','Result','ReportPwr'], axis=1)
    cols = df.columns.tolist()
    colSorted = [cols[-1]]+[cols[-2]]+[cols[-4]]+cols[:-4]
    # a = df[colSorted].head(10)
    a = df[colSorted]
    alen = len(a)
    spec = getPass[0]['MeasurePwr']
    avgList,stdList,minList,maxList = [],[],[],[]
    specMin = ['specMin',None,None]
    specMax = ['specMax',None,None]
    cpkLlist = ['Cpk-L',None,None]
    cpkHlist = ['Cpk-H',None,None]
    cpklist = ['Cpk',None,None]
    levellist = ['Level',None,None]
    calist = ['Ca',None,None]
    cplist = ['Cp',None,None]
    for v in [i-2 for i in spec]:specMin.append(round(v,2))
    for v in [i+2 for i in spec]:specMax.append(round(v,2))
    avg = a.mean().round(2)
    std = a.std().round(2)
    amin = a.min()
    amax = a.max()
    for c in a.columns:
        if c == '_id':
            avgList.append('Avg')
            stdList.append('Std')
            minList.append('Min')
            maxList.append('Max')
        elif c == 'Time':
            avgList.append(None)
            stdList.append(None)
            minList.append(None)
            maxList.append(None)
        elif c == 'Station-id':
            avgList.append(None)
            stdList.append(None)
            minList.append(None)
            maxList.append(None)
        else:
            avgList.append(avg[c])
            stdList.append(std[c])
            minList.append(amin[c])
            maxList.append(amax[c])
    cpkL = [i for i in map(lambda x, y, z: (x-y)/(3*z) , avgList[3:], specMin[3:], stdList[3:])]
    cpkH = [i for i in map(lambda x, y, z: (y-x)/(3*z) , avgList[3:], specMax[3:], stdList[3:])]
    cpk = [i for i in map(lambda x, y: min(x,y) , cpkL, cpkH)]
    ca = [i for i in map(lambda x, y, z: abs(x-(y+z)/2)/((z-y)/2), avgList[3:], specMin[3:], specMax[3:])]
    cp = [i for i in map(lambda x, y, z: (z-y)/(x*6), stdList[3:], specMin[3:], specMax[3:])]
    for c in cpkL: cpkLlist.append(round(c,2))
    for c in cpkH: cpkHlist.append(round(c,2))
    for c in cpk: cpklist.append(round(c,2))
    for c in cpkLevel(cpk): levellist.append(c)
    for c in ca: calist.append('{}%'.format(round(c*100)))
    for c in cp: cplist.append(round(c,2))
    a.loc[alen] = a.loc[0]
    a.loc[alen+1] = a.loc[1]
    a.loc[alen+2] = a.loc[2]
    a.loc[alen+3] = a.loc[3]
    a.loc[alen+4] = a.loc[4]
    a.loc[alen+5] = a.loc[5]
    a.loc[alen+6] = a.loc[6]
    a.loc[alen+7] = a.loc[7]
    a.loc[alen+8] = a.loc[8]
    a.loc[alen+9] = a.loc[9]
    a.loc[alen+10] = a.loc[10]
    a.loc[alen+11] = a.loc[11]
    a.loc[0] = specMin
    a.loc[1] = specMax
    a.loc[2] = avgList
    a.loc[3] = stdList
    a.loc[4] = minList
    a.loc[5] = maxList
    a.loc[6] = cpkLlist
    a.loc[7] = cpkHlist
    a.loc[8] = cpklist
    a.loc[9] = levellist
    a.loc[10] = calist
    a.loc[11] = cplist
    return a[:12]

def getdbList():
    conn = MongoClient('192.168.45.38:27017')
    dblist = conn.list_database_names()
    dbDicList = []
    for db in dblist:
        dbDicList.append({"label": db, "value": db})
    return dbDicList

def getcollectionList():
    conn = MongoClient('192.168.45.38:27017')
    db = conn['1521900003T0']
    collList = db.list_collection_names()
    collDicList = []
    for col in collList:
        collDicList.append({"label": col, "value": col})
    return collDicList


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
