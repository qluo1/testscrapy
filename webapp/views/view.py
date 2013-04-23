import json
# flask
from flask import Flask, current_app,request
from flask import render_template, jsonify, abort
# mongo db
from models import query_index,query_news_by_oid,query_items

import logging 
log = logging.getLogger(__name__)


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
    rets = query_index(index)
    return  current_app.response_class(json.dumps(rets,indent=None if request.is_xhr else 2), 
                        mimetype='application/json')

def get_news(oid):
    """ """
    ret = query_news_by_oid(oid)
    if ret:
        return current_app.response_class(json.dumps(ret,indent=None if request.is_xhr else 2),
                    mimetype='application/json')
    abort(404)

############ search items ###############
def search():
    """  handle post method """
    # print request.method
    # print request
    from searchable import yahoofin
    #
    if request.method == 'POST':
        terms = request.form.get('terms')
        # print terms
        rets = yahoofin.search_content(unicode(terms))
        # build json here
        # print rets
        query = [i['url'] for i in rets]
        # print query
        items = query_items(query)
        return current_app.response_class(json.dumps(items,indent=None if request.is_xhr else 2),
                mimetype='application/json')

# get item 
def get(ref):
    item = client.scrapy.items.find_one({'url':ref})
    if item:
        item['timestamp'] = item['timestamp'].isoformat()
        item['id'] = str(item.pop("_id"))
        return jsonify(item)
    abort(404)
