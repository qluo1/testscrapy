from scrapy.spider import BaseSpider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
from datetime import datetime as dt, timedelta
from dateutil import parser
from scrapy import log
from scrapy.conf import settings

from selenium import webdriver

class TheAgeSpider(CrawlSpider):
	name = 'theage'
	allowed_domains = ['theage.com.au']
	start_urls = ["http://www.theage.com.au/business"]
	today = dt.strftime(dt.now(),"%Y%m%d")
	log.msg( 'www.theage.com.au/business/.*-%s-.*html$' % today, level=log.DEBUG)
	rules = [Rule(SgmlLinkExtractor(allow=['www.theage.com.au/business/.*-%s-.*html$' % today ,]), 'parse_article', follow=True)]

	def parse_article(self, response):
		hxs = HtmlXPathSelector(response)
		print response.url
		print hxs.select("//div[@class='articleBody']/p").extract()

########### Yahoo Finance News
import re
import time
from scrapy.http import Request
from random import randint
import codecs
import feedparser
from testscrapy.items import YahooNewsItem , WantTimesItem

class YahooFinSpider(BaseSpider):
	name = "yahoofin"
	allowed_domains = ['au.finance.yahoo.com']
	start_urls = ["http://au.finance.yahoo.com/news/topic-top-stories/"]
	pipelines = set(['yahoo', 'mongo', 'whoosh'])

	p = re.compile("/news/.*\.html")

	def parse(self,response):
		print response.url
		if settings['LOCAL_ENV'] == 'HOME':
			browser = webdriver.Firefox() 
		else:
			browser = webdriver.Remote("http://localhost:4444",{}) 

		browser.get(response.url)
		for i in range(0,3):
			browser.find_element_by_xpath("//a[@class='more-link']").click()
			time.sleep(3)
		hxs = HtmlXPathSelector(text=browser.page_source)
		links = hxs.select("//a/@href").extract()
		browser.close()
		return [Request("http://au.finance.yahoo.com"+i,callback=self.parse_article) for i in links if self.p.search(i)]

	def parse_article(self,response):
		# print response.url
		hxs = HtmlXPathSelector(response)
		item = YahooNewsItem()
		item['url'] = response.url.split(";_")[0].split("/")[-1]
		item['title'] =  hxs.select("//h1[@class='headline']/text()").extract()[0]
		item['timestamp'] = parser.parse(hxs.select("//cite/abbr/@title").extract()[0])
		item['source'] = hxs.select("//span[@class='provider org']/text()").extract()[0]
		item['content'] = hxs.select("//div[@id='mediaarticlebody']").extract()[0]
		return item

from dateutil import parser
class WantTimesChinaSpider(BaseSpider):
	name = "wantTimes"
	allowed_domains = ['wantchinatimes.com']
	start_urls = ["http://www.wantchinatimes.com/Rss.aspx?MainCatID=12"]
	pipelines = set(['mongo'])

	def parse(self,response):
		feed = feedparser.parse(response.url)
		links = [Request(i.link,self.parse_article) for i in feed.entries ]
		return links

	def parse_article(self, response):
		""" """
		log.msg(response.url,level=log.INFO)
		hxs = HtmlXPathSelector(response)
		item = WantTimesItem()
		item['url'] = response.url
		item['title'] = hxs.select("//div[@class='article-header']/h1/text()").extract()[0]
		item['content'] = hxs.select("//div[@class='article-content']").extract()[0]
		extra = hxs.select("//div[@class='article-header']/ul/li/text()").extract()
		
		log.msg(extra,level=log.DEBUG)
		item['source'] = extra[0]
		item['timestamp'] = parser.parse("%sT%s" % (extra[1],extra[2].replace("(",'').replace(")","")))
		return item