from pymongo import MongoClient
import bson
from bson import json_util
from flask import Flask, current_app,request
from flask import render_template, jsonify, abort


app = Flask(__name__)
client = MongoClient('localhost', 27017)
from pymongo import ASCENDING, DESCENDING

from datetime import datetime as dt, timedelta

# url
@app.route("/")
def home():
    three_days = dt.now() - timedelta(days = 2)
    ret = ''
    for i in client.scrapy.items.find({'timestamp':{"$gt": three_days}, 'yahoo_market_news': 0}).sort([('timestamp',DESCENDING)]):
    	item = i.items()
    	ret += "<p> <a href='/item/%s'> %s</a> at %s </p>" % (item[1][1].split("/")[-1],item[0][1],item[2][1])
    return ret

@app.route("/item/<ref>")
def item(ref):
    print ref
    item = client.scrapy.items.find_one({'url':ref})
    print item
    if item:
        return render_template("item.html",item=item)

    return "not found: %s" % ref

@app.route("/test")
def test():
    return render_template("home.html")

@app.route("/news")
def news():
    return render_template("news.html")


# api
@app.route("/get/<ref>")
def get(ref):
    item = client.scrapy.items.find_one({'url':ref})
    if item:
        item['timestamp'] = item['timestamp'].isoformat()
        item['id'] = str(item.pop("_id"))
        return jsonify(item)
    abort(404)


import json
@app.route("/get/business")
def get_business_index():
    """ """
    three_days = dt.now() - timedelta(days = 2)
    
    rets = []
    for i in client.scrapy.items.find({'yahoo_market_news':0}).sort([('timestamp',DESCENDING)]):
        rets.append(dict(title=i['title'],source=i['source'],date=i['timestamp'].isoformat(),url=i['url'],_id=str(i['_id'])))

    print rets
    return  current_app.response_class(json.dumps(rets,indent=None if request.is_xhr else 2), mimetype='application/json')

@app.route("/query/<_id>")
def get_news(_id):
    i = client.scrapy.items.find_one({"_id": bson.ObjectId(_id)})
    # print i
    if i:
        ret = dict(title=i['title'],source=i['source'],date=i['timestamp'].isoformat(),url=i['url'],content=i['content'])
        return current_app.response_class(json.dumps(ret,indent=None if request.is_xhr else 2), mimetype='application/json')
    abort(404)

if __name__ == "__main__":
    app.run(debug=True,port=9003)
