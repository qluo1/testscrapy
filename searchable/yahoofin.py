import os
import sys

from whoosh.index import create_in
from whoosh.fields import  Schema, TEXT,ID
from whoosh.qparser import QueryParser

schema = Schema(title=TEXT(stored=True), url=ID(stored=True), content=TEXT)

ROOT = os.path.dirname(os.path.abspath(__file__))

def write_index(title,url,content):
    ix = create_in(os.path.join(ROOT,"indexdir"), schema)
    writer = ix.writer()
    writer.add_document(title=title, url=unicode(url),
        content=content)
    writer.commit()

def search_content(phase):
    with ix.searcher() as searcher:
         query = QueryParser("content", ix.schema).parse(phase)
         results = searcher.search(query)
         return results
