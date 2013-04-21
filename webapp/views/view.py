import json
from datetime import datetime as dt, timedelta
# flask
from flask import Flask, current_app,request
from flask import render_template, jsonify, abort
# mongo db
from pymongo import MongoClient
from pymongo import ASCENDING, DESCENDING
import bson
from bson import json_util

import logging 
log = logging.getLogger(__name__)
# mongo db
client =  MongoClient('localhost', 27017)


## index page
def home():
    return render_template("home.html")

## flight demo
def demo():
    return render_template("demo.html")

############ API call ##########
from timesince import timesince
def get_index(index):
    """ """
    # print index
    three_days = dt.now() - timedelta(days = 2)
    filter = {'yahoo_market_news':0} if index == 'business' else {'yahoo_market_news':1}
    filter.update({'timestamp': {"$gt": three_days}})

    rets = []
    for i in client.scrapy.items.find(filter).sort([('timestamp',DESCENDING)]):
        rets.append(dict(title=i['title'],source=i['source'],
                         date=timesince(i['timestamp']),url=i['url'],
                         _id=str(i['_id'])))

    # print rets
    return  current_app.response_class(json.dumps(rets,indent=None if request.is_xhr else 2), mimetype='application/json')


#@app.route("/query/<_id>")
def get_news(oid):
    i = client.scrapy.items.find_one({"_id": bson.ObjectId(oid)})
    # print i
    if i:
        ret = dict(title=i['title'],source=i['source'],
                   date=i['timestamp'].isoformat(),url=i['url'],
                   content=i['content'])
        return current_app.response_class(json.dumps(ret,indent=None if request.is_xhr else 2), mimetype='application/json')
    abort(404)

############ search items ###############
def search():
    """  handle post method """
    print request.method
    print request
    from searchable import yahoofin
    #
    if request.method == 'POST':
        terms = request.form.get('terms')
        print terms
        rets = yahoofin.search_content(unicode(terms))
        # build json here
        print rets
        return current_app.response_class(json.dumps(rets,indent=None if request.is_xhr else 2), mimetype='application/json')

# get item 
def get(ref):
    item = client.scrapy.items.find_one({'url':ref})
    if item:
        item['timestamp'] = item['timestamp'].isoformat()
        item['id'] = str(item.pop("_id"))
        return jsonify(item)
    abort(404)
