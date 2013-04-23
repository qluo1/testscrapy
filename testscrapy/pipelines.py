# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

class TestscrapyPipeline(object):
    def process_item(self, item, spider):
        return item

from scrapy import signals
from scrapy.exceptions import DropItem

class DuplicatesPipeline(object):

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        if item['url'] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(item['url'])
            return item


#### 
from searchable.yahooClassifier import YahooClassifier

class YahooMarketNewsClassifierPipeline(object):
    """
    """
    def __init__(self):
        self.classifier = YahooClassifier()

    def process_item(self, item, spider):
        if 'yahoo' not in getattr(spider,"pipelines",[]):
            return item
        # pipeline
        if item['source'] in ['ABC']:
            item['yahoo_market_news'] = 0
            return item
        # using classifier here for other source
        cat = self.clasifier.classify(item['content'])
        item['yahoo_market_news'] = cat
        log.msg("category: %s as %d" % (item['title'],cat), level=log.INFO)
        return item

"""MongoDB Pipeline for scrapy"""
import pymongo
from scrapy.conf import settings
from scrapy import log

MONGODB_SAFE = True
MONGODB_ITEM_ID_FIELD = "_id"

class MongoDBPipeline(object):
    def __init__(self):
        connection = pymongo.Connection(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        self.db = connection[settings['MONGODB_DB']]
        # self.collection = self.db[settings['MONGODB_COLLECTION']]
        self.collections = settings['MONGODB_COLLECTIONS']
        self.uniq_key = settings.get('MONGODB_UNIQ_KEY', None)
        self.itemid = settings.get('MONGODB_ITEM_ID_FIELD',MONGODB_ITEM_ID_FIELD)
        self.safe = settings.get('MONGODB_SAFE', MONGODB_SAFE)
        self.replace = settings.get('REPLACE_ITEM', MONGODB_SAFE)
        if isinstance(self.uniq_key, basestring) and self.uniq_key == "":
            self.uniq_key = None
            
        if self.uniq_key:
            for name, coll in self.collections.items():
                self.db[coll].ensure_index(self.uniq_key,unique=True)

    def process_item(self, item, spider):
        if 'mongo' not in getattr(spider,"pipelines",[]):
            return item
        
        name = spider.name
        assert(name in self.collections.keys())
        # mongo collection
        coll = self.db[self.collections[name]]
        # pipeline
        if self.uniq_key is None:
            result = coll.insert(dict(item), safe=self.safe)
        else:
            # check duplicaiton based on url
            if not self.replace and coll.find({'url':item['url']}).count() > 0 :
                raise DropItem("Duplicate item found: %s" % item['url'])

            result = coll.update(
                            {self.uniq_key: item[self.uniq_key]},
                            dict(item),
                            upsert=True, safe=self.safe)

        # If item has _id field and is None
        if self.itemid in item.fields and not item.get(self.itemid, None):
            item[self.itemid] = result

        log.msg("Item %s wrote to MongoDB database %s/%s" %
                    (result, settings['MONGODB_DB'], name),
                    level=log.DEBUG, spider=spider)
        return item

### 
from searchable.yahoofin import write_index

class WhooshIindexPipeline(object):

    def process_item(self, item, spider):
        if 'whoosh' not in getattr(spider,"pipelines",[]):
            return item
        # process
        log.msg("write index :%s" % item, level=log.DEBUG)
        write_index(item['title'],item['url'],item['content'],item['timestamp'])
