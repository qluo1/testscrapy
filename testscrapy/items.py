# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class MongoItem(Item):
    """ _id will be populated by mongodb pipeline """
    _id = Field()

class YahooNewsItem(MongoItem):
    """ """
    url = Field()
    title = Field()
    source = Field()
    timestamp = Field()
    content = Field()
    yahoo_market_news = Field()

class WantTimesItem(MongoItem):
    """ """
    url = Field()
    title = Field()
    source = Field()
    content = Field()
    timestamp = Field()

