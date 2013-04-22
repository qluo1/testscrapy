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


def query_index(index,numOfDays=3):
    # print index
    three_days = dt.now() - timedelta(days = numOfDays)
    filter = {'yahoo_market_news':0} if index == 'business' else {'yahoo_market_news':1}
    filter.update({'timestamp': {"$gt": three_days}})

    rets = []
    for i in client.scrapy.items.find(filter).sort([('timestamp',DESCENDING)]):
        rets.append(dict(title=i['title'],source=i['source'],
                         date=timesince(i['timestamp']),url=i['url'],
                         oid=str(i['_id'])))
    return rets

def query_news_by_oid(oid):
    i = client.scrapy.items.find_one({"_id": bson.ObjectId(oid)})
    if i:
        return dict(title=i['title'],source=i['source'],
                   date=i['timestamp'].isoformat(),url=i['url'],
                   content=i['content'])
    else:
        return None

def query_items(items):
    """ """
    filter = {'url': {'$in': items}}
    cur = client.scrapy.items.find(filter).sort([('timestamp',DESCENDING)])
    print cur.count()
    return [dict(title=i['title'],oid=str(i['_id']),date=timesince(i['timestamp'])) for i in cur]
