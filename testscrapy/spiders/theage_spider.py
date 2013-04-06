from scrapy.spider import BaseSpider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
from datetime import datetime as dt, timedelta

from scrapy import log

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

import re
import time
from scrapy.http import Request
from random import randint
import codecs
class YahooFinSpider(BaseSpider):
	name = "yahoofin"
	allowed_domains = ['au.finance.yahoo.com']
	start_urls = ["http://au.finance.yahoo.com/news/topic-top-stories/"]
	p = re.compile("/news/.*\.html")
	def parse(self,response):
		print response.url
		browser = webdriver.Remote("http://localhost:4445",{}) 
		# browser = webdriver.Firefox() 
		browser.get(response.url)
		# for i in range(0,5):
		# 	browser.find_element_by_xpath("//a[@class='more-link']").click()
		# 	time.sleep(3)
		hxs = HtmlXPathSelector(text=browser.page_source)
		links = hxs.select("//a/@href").extract()
		browser.close()
		return [Request("http://au.finance.yahoo.com"+i,callback=self.parse_article) for i in links if self.p.search(i)]

	def parse_article(self,response):
		print response.url
		hxs = HtmlXPathSelector(response)
		print hxs.select("//h1[@class='headline']/text()")
		with codecs.open("%d.html" % randint(0,100),"w", encoding='utf-8') as f:
			f.write(hxs.select("//div[@id='mediaarticlebody']").extract()[0])
