import os
import sys

from whoosh.index import create_in, open_dir
from whoosh.fields import  Schema, TEXT,ID,DATETIME
from whoosh.qparser import QueryParser

schema = Schema(title=TEXT(stored=True), url=ID(stored=True), date=DATETIME, content=TEXT)

ROOT = os.path.dirname(os.path.abspath(__file__))

def write_index(title,url,content,date):
    """ """
    if not os.path.exists(os.path.join(ROOT,"indexdir")):
        os.mkdir(os.path.join(ROOT,"indexdir"))
        ix = create_in(os.path.join(ROOT,"indexdir"),schema)
    else:
        ix = open_dir(os.path.join(ROOT,"indexdir"))
    
    writer = ix.writer()
    writer.add_document(title=title, url=unicode(url),content=content,date=date)
    writer.commit()

def search_content(phase):
    ix = open_dir(os.path.join(ROOT,"indexdir"))
    ret = []
    with ix.searcher() as searcher:
        query = QueryParser("content", ix.schema).parse(phase)
        results = searcher.search(query)
        for i in results:
            ret.append(dict(title=i['title'],url=i['url']))
        return ret
