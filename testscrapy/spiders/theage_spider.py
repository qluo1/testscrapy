
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



class YahooAuNewsSpider(CrawlSpider):
	name = "YahooAuNews"
	allowed_domains = ['theage.com.au']
	start_urls = ["http://au.finance.yahoo.com/news/topic-top-stories/"]
	
	rules = [Rule(SgmlLinkExtractor(allow=['/news/.*html;.*',]), 'parse_article', follow=True)]

	def parse_article(self, response):
		hxs = HtmlXPathSelector(response)
		print response.url
		print hxs.select("//div[@class='bd']/p").extract()


class TheAge_Spider(BaseSpider):
	name = "basic_debug"
	allowed_domains = ['au.finance.yahoo.com']
	start_urls = ["http://au.finance.yahoo.com/news/topic-top-stories/"]
	
	def parse(self,response):
		print response.url
		with open("out.html","w") as f:
			f.write(response.body)
		browser = webdriver.Remote("http://localhost:4445",{}) 
		browser.get(response.url)
		browser.get_screenshot_as_file("out2.png")
		with open("out2.html","w") as f:
			f.write(browser.page_source)
		hxs = HtmlXPathSelector(text=browser.page_source)
		print hxs.select("//a/text()").extract()
