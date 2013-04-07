from pymongo import MongoClient
from flask import Flask
app = Flask(__name__)
client = MongoClient('localhost', 27017)
from pymongo import ASCENDING, DESCENDING

@app.route("/")
def list():
    ret = ""

    for i in client.scrapy.items.find():
    	item = i.items()
    	ret += "<p>%s, %s </p>" % (item[0][1],item[1][1])
    return ret

if __name__ == "__main__":
    app.run(debug=True)