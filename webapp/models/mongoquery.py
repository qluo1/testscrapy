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
db = client.scrapy

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
        # print i
        return dict(title=i['title'],source=i['source'],
                   date=i['timestamp'].isoformat(),url=i['url'],
                   content=i['content'])
    return i

def query_items(items):
    """ """
    filter = {'url': {'$in': items}}
    cur = db.items.find(filter).sort([('timestamp',DESCENDING)])
    print cur.count()
    return [dict(title=i['title'],oid=str(i['_id']),date=timesince(i['timestamp'])) for i in cur]


def query_property(state = None,suburb = None):
    """ """
    filter = {}
    if state:
        filter.update({'state':state})
    if suburb:
        filter.update({'suburb': suburb})

    cur = db.propertyData.find(filter)
    for i in cur:
        print i['suburb'],i['address'],i['category'],i['price'],i['method'],i['week_start']


from bson.code import Code
def query_state_suburb(date,state='victoria'):
    """ """

    maper = Code(""" 
        function() {
                emit(this.suburb, 1);
        }
    """)
    
    reducer = Code(""" 
        function(key,values) {
            var count = 0;
            for (var i = 0; i < values.length; i++) {
                count += values[i];
            }
            return count;
        }
        """)

    filter = {'state':state,'week_start': dt.strptime(date,'%Y%m%d')}
    result = db.propertyData.map_reduce(maper,reducer,"myresults",query=filter)
    
    return [i['_id'] for i in result.find()]

def query_summary(date,state='victoria'):
    """ """

    maper = Code(""" 
        function() {
                emit(this.method, 1);
        }
    """)
    
    reducer = Code(""" 
        function(key,values) {
            var count = 0;
            for (var i = 0; i < values.length; i++) {
                count += values[i];
            }
            return count;
        }
        """)

    filter = {'state':state,'week_start': dt.strptime(date,'%Y%m%d')}
    result = db.propertyData.map_reduce(maper,reducer,"myresults",query=filter)
    
    return [{i['_id']: i['value']} for i in result.find()]
