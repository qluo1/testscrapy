from pymongo import MongoClient
from flask import Flask
app = Flask(__name__)
client = MongoClient('localhost', 27017)
from pymongo import ASCENDING, DESCENDING

@app.route("/")
def list():
    ret = ""

    for i in client.scrapy.items.find().sort([('timestamp',DESCENDING)]):
    	item = i.items()
    	ret += "<p> <a href='/item/%s'> %s</a> at %s </p>" % (item[1][1].split("/")[-1],item[0][1],item[2][1])
    return ret

@app.route("/item/<ref>")
def item(ref):
    print ref
    item = client.scrapy.items.find_one({'url':'http://au.finance.yahoo.com/news/' + ref})
    print item
    if item:
        return item['content']
    else:
        return "not found: %s" % ref

if __name__ == "__main__":
    app.run(debug=True)
