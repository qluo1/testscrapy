import os
import sys
from datetime import datetime as dt, timedelta
# mongo db
from pymongo import MongoClient
from pymongo import ASCENDING, DESCENDING
import bson
from bson import json_util
from bson.code import Code
from utils.timesince import timesince

# mongo db
client =  MongoClient('localhost', 27017)

## default config
PARENT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PARENT not in sys.path:
    sys.path.insert(0,PARENT)

import default_cfg

def query_yahoo(index,numOfDays=3):
    """ query yahoo index content"""
    num_days = dt.now() - timedelta(days = numOfDays)

    filter = {'yahoo_market_news':0} if index == 'business' else {'yahoo_market_news':1}
    filter.update({'timestamp': {"$gt": num_days}})

    coll = default_cfg.MONGODB_COLLECTIONS['yahoofin']
    rets = []
    for i in client.scrapy[coll].find(filter).sort([('timestamp',DESCENDING)]):
        rets.append(dict(title=i['title'],source=i['source'],
                         date=timesince(i['timestamp']),url=i['url'],
                         oid=str(i['_id'])))
    return rets

def query_wantTimes(numOfDays=3):
    """ query wantTimes index content """
    num_days = dt.now() - timedelta(days=numOfDays)

    filter = {'timestamp': {"$gt": num_days}}
    
    coll = default_cfg.MONGODB_COLLECTIONS['wantTimes']
    # print coll
    # print client.scrapy[coll].count()
    rets = []
    for i in client.scrapy[coll].find(filter).sort([('timestamp',DESCENDING)]):
        rets.append(dict(title=i['title'],source=i['source'],
                         date=timesince(i['timestamp']),url=i['url'],
                         oid=str(i['_id'])))
    return rets
def query_news_by_oid(oid):
    i = None
    for key,val in default_cfg.MONGODB_COLLECTIONS.items():
        i =  client.scrapy[val].find_one({"_id": bson.ObjectId(oid)})
        if i: break

    if i:
        print i
        return dict(title=i['title'],source=i['source'],
                   date=i['timestamp'].isoformat(),url=i['url'],
                   content=i['content'])
    return i

def query_items(items):
    """ """
    filter = {'url': {'$in': items}}
    cur = client.scrapy.items.find(filter).sort([('timestamp',DESCENDING)])
    print cur.count()
    return [dict(title=i['title'],oid=str(i['_id']),date=timesince(i['timestamp'])) for i in cur]
