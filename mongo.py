from pymongo import MongoClient
from bson.objectid import ObjectId
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
import pandas as pd
import time

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
    c.close()

def monthPass(m):
    conn = MongoClient('192.168.0.11:27017')
    db = conn['1521900003T0']
    collection=db.T1_Log
    result = collection.find({'Time':{'$gte': datetime(2018,m,1),'$lt': datetime(2018,m,1)+relativedelta(months=1)}}).count()
    conn.close()
    return result

def getErrorCount(stDate,edDate):
    conn = MongoClient('192.168.0.11:27017')
    db = conn['1521900003T0']
    collection=db.T1_Log
    ErrorCount = {}
    r = [{'ErrorCode':i['ErrorCode']} for i in collection.find({'Time':{'$gt': stDate,'$lt': edDate},'Result':'FAIL'}) if 'ErrorCode' in i.keys()]
    print('-------FAIL:{}'.format(len(r)))
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

def cpkinitalTable(stDate,edDate,db_,coll_):
    print(stDate,edDate)
    sstime = time.time()
    conn = MongoClient('192.168.0.11:27017')
    db = conn[db_]
    colls = db.collection_names()
    collection=db[coll_]

    avgList,stdList,minList,maxList = [],[],[],[]
    specMin = ['specMin']
    specMax = ['specMax']
    cpkLlist = ['Cpk-L']
    cpkHlist = ['Cpk-H']
    cpklist = ['Cpk']
    levellist = ['Level']
    calist = ['Ca']
    cplist = ['Cp']
    # getPass = [i for i in collection.find({'Time':{'$gt': stDate,'$lt': edDate},"Result":"PASS"})]
    # getPass = [i for i in wholeData if i['Result']=='PASS' and (stDate < i['Time'] < edDate)]
    # print(getPass[0]['Frequency'])
    # print('--------------------{}'.format(len(getPass)))
    df = pd.DataFrame([i for i in collection.find({'Time':{'$gt': stDate,'$lt': edDate},"Result":"PASS"})])
    if coll_ == 'DsQAM' or coll_ == 'UsQAM':
        spec = df['MeasurePwr'][0]
        df = df.drop(['Frequency','ChResult','MeasurePwr','Result','ReportPwr','Time','Station-id','TestTime'], axis=1)
        for v in [i-2 for i in spec]:specMin.append(round(v,2))
        for v in [i+2 for i in spec]:specMax.append(round(v,2))
    elif coll_ == 'DsMER' or coll_ == 'UsSNR':
        if coll_ == 'DsMER':
            spec = [df['Criteria'][0]]*len(df['RxMer'][0])
            df = df.drop(['Frequency','ChResult','RxMer','Result','Time','Station-id','TestTime','Criteria'], axis=1)
        else:
            spec = [df['Criteria'][0]]*len(df['UsSnr'][0])
            df = df.drop(['Frequency','ChResult','UsSnr','Result','Time','Station-id','TestTime','Criteria'], axis=1)
        for v in spec:
            specMin.append(round(v,2))
            specMax.append(round(v+15,2))

    cols = df.columns.tolist()
    colSorted = [cols[-1]]+cols[:-1]
    # a = df[colSorted].head(10)
    a = df[colSorted]
    alen = len(a)
    # spec = [round(sum(i)/len(i),2) for i in zip(*[i['MeasurePwr'] for i in getPass])]

    conn.close()    
    print('Query MongoDB During Time: {}'.format(time.time()-sstime))
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
        else:
            avgList.append(avg[c])
            stdList.append(std[c])
            minList.append(amin[c])
            maxList.append(amax[c])

    cpkL = [i for i in map(lambda x, y, z: (x-y)/(3*z) , avgList[1:], specMin[1:], stdList[1:])]

    cpkH = [i for i in map(lambda x, y, z: (y-x)/(3*z) , avgList[1:], specMax[1:], stdList[1:])]

    cpk = [i for i in map(lambda x, y: min(x,y) , cpkL, cpkH)]

    ca = [i for i in map(lambda x, y, z: abs(x-(y+z)/2)/((z-y)/2), avgList[1:], specMin[1:], specMax[1:])]

    cp = [i for i in map(lambda x, y, z: (z-y)/(x*6), stdList[1:], specMin[1:], specMax[1:])]

    for c in cpkL: cpkLlist.append(round(c,2))

    for c in cpkH: cpkHlist.append(round(c,2))

    for c in cpk: cpklist.append(round(c,2))

    for c in cpkLevel(cpk): levellist.append(c)

    for c in ca: calist.append('{}%'.format(round(c*100)))

    for c in cp: cplist.append(round(c,2))
    #.loc[row_indexer,col_indexer] = value instead , a.loc[0].keys()
    # allList = [specMin,specMax,avgList,stdList,minList,maxList,cpkLlist,cpkHlist,cpklist,levellist,calist,cplist]
    # for k in a.keys():
    #     for i,l in enumerate(allList):
    #         a.loc[i][k] = l[i]
    # a.loc[alen] = a.loc[0]
    # a.loc[alen+1] = a.loc[1]
    # a.loc[alen+2] = a.loc[2]
    # a.loc[alen+3] = a.loc[3]
    # a.loc[alen+4] = a.loc[4]
    # a.loc[alen+5] = a.loc[5]
    # a.loc[alen+6] = a.loc[6]
    # a.loc[alen+7] = a.loc[7]
    # a.loc[alen+8] = a.loc[8]
    # a.loc[alen+9] = a.loc[9]
    # a.loc[alen+10] = a.loc[10]
    # a.loc[alen+11] = a.loc[11]
    for i,k in enumerate(a.keys()):
        a.loc[0,k] = specMin[i]
        a.loc[1,k] = specMax[i]
        a.loc[2,k] = avgList[i]
        a.loc[3,k] = stdList[i]
        a.loc[4,k] = minList[i]
        a.loc[5,k] = maxList[i]
        a.loc[6,k] = cpkLlist[i]
        a.loc[7,k] = cpkHlist[i]
        a.loc[8,k] = cpklist[i]
        a.loc[9,k] = levellist[i]
        a.loc[10,k] = calist[i]
        a.loc[11,k] = cplist[i]
    # print(a[:12])
    print('Table During Time: {}'.format(time.time()-sstime))
    return a[:12]

def batchProcessing(stDate,edDate):
    startTime = time.time()
    # stDate = date
    # edDate = date+relativedelta(days=1)
    conn = MongoClient('192.168.0.11:27017')
    db = conn['1521900003T0']
    colls = db.collection_names()
    collection=db.DsQAM
    combinData = pd.DataFrame()
    for day in range((edDate-stDate).days):
        getPass = [i for i in collection.find({'Time':{'$gt': stDate+timedelta(day),'$lt': edDate+timedelta(day)},"Result":"PASS"})]
        # getPass = [i for i in wholeData if i['Result']=='PASS' and (stDate < i['Time'] < edDate)]
        # print(getPass[0]['Frequency'])
        # print('--------------------{}'.format(len(getPass)))
        # conn.close()
        df = pd.DataFrame(getPass)
        df = df.drop(['Frequency','ChResult','MeasurePwr','Result','ReportPwr'], axis=1)
        cols = df.columns.tolist()
        colSorted = [cols[-1]]+[cols[-2]]+[cols[-4]]+cols[:-4]
        # a = df[colSorted].head(10)
        a = df[colSorted]
        alen = len(a)
        spec = [round(sum(i)/len(i),2) for i in zip(*[i['MeasurePwr'] for i in getPass])]
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
        if day == 0:
            combinData = a[a.columns[3:]][:9]
        else:
            combinData = (combinData+a[a.columns[3:]][:9])/2
        print('Days---{}---\n{}'.format(day,combinData))
    print('Total Time: {}'.format(time.time()-startTime))
    return combinData
    # (a[a.columns[3:]][:9]+b[b.columns[3:]][:9])/2
    # return a[:12]

def abatchProcessing(stDate,edDate):
    startTime = time.time()
    # stDate = date
    # edDate = date+relativedelta(days=1)
    conn = MongoClient('192.168.0.11:27017')
    db = conn['1521900003T0']
    colls = db.collection_names()
    collection=db.DsQAM
    combinData = pd.DataFrame()
    getPass = [i for i in collection.find({'Time':{'$gt': stDate,'$lt': edDate},"Result":"PASS"})]
    # getPass = [i for i in wholeData if i['Result']=='PASS' and (stDate < i['Time'] < edDate)]
    # print(getPass[0]['Frequency'])
    print('--------------------{}'.format(len(getPass)))
    # conn.close()
    df = pd.DataFrame(getPass)
    df = df.drop(['Frequency','ChResult','MeasurePwr','Result','ReportPwr'], axis=1)
    cols = df.columns.tolist()
    colSorted = [cols[-1]]+[cols[-2]]+[cols[-4]]+cols[:-4]
    # a = df[colSorted].head(10)
    a = df[colSorted]
    alen = len(a)
    spec = [round(sum(i)/len(i),2) for i in zip(*[i['MeasurePwr'] for i in getPass])]
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
    print('Total Time: {}'.format(time.time()-startTime))
    # return combinData
    # (a[a.columns[3:]][:9]+b[b.columns[3:]][:9])/2
    return a[:12]

def getdbList():
    conn = MongoClient('192.168.0.11:27017')
    dblist = conn.list_database_names()
    dbDicList = []
    for db in dblist:
        dbDicList.append({"label": db, "value": db})
    return dbDicList

def getcollectionList():
    conn = MongoClient('192.168.0.11:27017')
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
