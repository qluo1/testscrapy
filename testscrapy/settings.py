# Scrapy settings for testscrapy project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'qiscrapy'

SPIDER_MODULES = ['testscrapy.spiders']
NEWSPIDER_MODULE = 'testscrapy.spiders'

# Crawl user-agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.02 (KHTML, like Gecko) Chrome/25.0.1364.172 Safari/537.22'

#
LOG_FILE = "./logs/scrapy.log"
LOG_LEVEL = "INFO"
# pipelien

ITEM_PIPELINES = [
  'testscrapy.pipelines.DuplicatesPipeline',
  'testscrapy.pipelines.YahooMarketNewsClassifierPipeline',
  'testscrapy.pipelines.MongoDBPipeline',
  'testscrapy.pipelines.WhooshIindexPipeline',
]

EXTENSIONS = {
    'scrapy.contrib.feedexport.FeedExporter': None,
}

MONGODB_SERVER = 'localhost'
MONGODB_PORT = 27017
MONGODB_DB = 'scrapy'
MONGODB_UNIQ_KEY = 'url'
MONGODB_ITEM_ID_FIELD = '_id'
MONGODB_SAFE = True

# map crawl name to mongodb collection
MONGODB_COLLECTIONS = {
	'yahoofin': 'items',
	'wantTimes': 'wantTimes',
}

# 
NUM_TOP_WORDS = 30
# import local settings to override default
try:
	from local_settings import *
except ImportError:
	pass
