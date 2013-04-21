import os
import sys
## webapp folder
PARENT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PARENT not in sys.path:
    sys.path.insert(0,PARENT)

#
from flask import Flask

app = Flask(__name__)

# url
@app.route("/test")
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


from urls import build_url
build_url(app)
# load configuration
import default_cfg
app.config.from_object(default_cfg)

if __name__ == "__main__":
    app.run(debug=True,port=9003)

