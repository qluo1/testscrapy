# Scrapy settings for testscrapy project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'testscrapy'

SPIDER_MODULES = ['testscrapy.spiders']
NEWSPIDER_MODULE = 'testscrapy.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.02 (KHTML, like Gecko) Chrome/25.0.1364.172 Safari/537.22'

#
LOG_FILE = "./scrapy.log"
LOG_LEVEL = "INFO"
# mongodb pipelien

ITEM_PIPELINES = [
  'testscrapy.pipelines.DuplicatesPipeline',
  'testscrapy.pipelines.YahooMarketNewsClassifierPipeline',
  'testscrapy.pipelines.MongoDBPipeline',
  'testscrapy.pipelines.WhooshIindexPipeline',
]

MONGODB_SERVER = 'localhost'
MONGODB_PORT = 27017
MONGODB_DB = 'scrapy'
MONGODB_COLLECTION = 'items'
MONGODB_UNIQ_KEY = 'url'
MONGODB_ITEM_ID_FIELD = '_id'
MONGODB_SAFE = True
REPLACE_ITEM = True

# 
NUM_TOP_WORDS = 30
from local_settings import *