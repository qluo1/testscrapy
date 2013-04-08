from pymongo import MongoClient
from bson import json_util
from flask import Flask
from flask import render_template, jsonify, abort


app = Flask(__name__)
client = MongoClient('localhost', 27017)
from pymongo import ASCENDING, DESCENDING

from datetime import datetime as dt, timedelta

# url
@app.route("/")
def home():
    one_days = dt.now() - timedelta(days = 0)
    two_days = dt.now() - timedelta(days = 20)
    ret = ''
    for i in client.scrapy.items.find({'timestamp':{"$gt": two_days, '$lt': one_days}}).sort([('timestamp',DESCENDING)]):
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
    return render_template("index.html")

@app.route("/news")
def news():
    return render_template("news.html")


# api
@app.route("/get/<ref>")
def get(ref):
    item = client.scrapy.items.find_one({'url':ref})
    if item:
        item['timestamp'] = item['timestamp'].isoformat()
        item.pop("_id")
        return jsonify(item)
    abort(404)

if __name__ == "__main__":
    app.run(debug=True,port=9009)
