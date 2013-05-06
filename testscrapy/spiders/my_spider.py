from scrapy.spider import BaseSpider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
from datetime import datetime as dt, timedelta
from dateutil import parser
from random import randint
from scrapy import log
from scrapy.conf import settings
# from crawler.settings import settings
from scrapy.crawler.Crawler import settings
from scrapy.http import Request
##
from pprint import pprint
import string
import codecs
import re
import time
import pytz
import feedparser
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
from testscrapy.items import YahooNewsItem , WantTimesItem, RealestateAuctionItem

class YahooFinSpider(BaseSpider):
    name = "yahoofin"
    allowed_domains = ['au.finance.yahoo.com']
    start_urls = ["http://au.finance.yahoo.com/news/topic-top-stories/"]
    pipelines = set(['yahoo', 'mongo', 'whoosh'])

    p = re.compile("/news/.*\.html")

    def parse(self,response):
        print response.url
        if settings['LOCAL_ENV'] == 'HOME':
            from pyvirtualdisplay import Display
            display = Display(visible=0, size=(800, 600))
            display.start()
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
        # close virtual display
        if 'display' in locals() and display.is_started:
            display.stop()

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
        # item['timestamp'] = item['timestamp'].astimezone(pytz.utc)
        # print "%sT%s" % (extra[1],extra[2].replace("(",'').replace(")","")), item['timestamp'],item['timestamp'].astimezone(pytz.utc), item['timestamp'].tzinfo
        return item


########## realestateView property data
def chunks(l, n):
    """ Yield successive n-sized chunks from l.
    """
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

cleanup = lambda x: x.replace('\n','').replace('\t','').replace(u'\xa0','').strip()

class RealestateViewSpider(BaseSpider):
    name = "realestateView"
    allowed_domains = ['realestateview.com.au']
    start_urls = [
                'http://www.realestateview.com.au/propertydata/auction-results/victoria/',
                'http://www.realestateview.com.au/propertydata/auction-results/nsw/',
                'http://www.realestateview.com.au/propertydata/auction-results/tasmania/',
                'http://www.realestateview.com.au/propertydata/auction-results/south-australia/'
                ]
    pipelines = set(['mongo',])


    def parse(self,response):
        log.msg(response.url,level=log.INFO)
        hxs = HtmlXPathSelector(response)
        title = hxs.select("//div[@class='pd-content-heading-inner']/h2/text()").extract()[0]
        _date = title.split("-")
        print parser.parse(_date[1].strip()), parser.parse(_date[2].strip())

        # # pprint(hxs.select("//div[@class='pd-content-medium-inner']").extract()[-5:-4])
        # f =  codecs.open("out.html","w",encoding="utf-8")
        item = hxs.select("/html/body/div[6]/div[4]/div/div/div/div/div/div[5]/div/div[2]/div")
        # print item
        for idx, i in  enumerate(item.select(".//tr/td/text()").extract()):
            print idx, cleanup(i)
        # f.write(item[0])
        # f.close()

        # urls = [Request("%s%s" % (self.start_urls[0],i), self.parse_suburb) for i in string.uppercase]
        # return urls
        # print urls
        for j in self.start_urls:
            for i in string.uppercase:
                yield Request("%s%s" % (j,i), self.parse_suburb)

    def parse_suburb(self,response):
        """ """
        print response.url
        state = response.url.split("/")[-2]
        hxs = HtmlXPathSelector(response)

        title = hxs.select("//div[@class='pd-content-heading-inner']/h2/text()").extract()[0]
        _date = title.split("-")
        print parser.parse(_date[1].strip()), parser.parse(_date[2].strip())
        week_start, week_end = parser.parse(_date[1].strip()), parser.parse(_date[2].strip())
        suburbs = hxs.select("//div[@class='pd-content-heading-dark-inner']/h2/text()").extract()
        # pprint(suburbs)
        tbls = hxs.select("//div[@class='pd-table-inner']/table")
        
        ret = []

        for idx, tbl in enumerate(tbls):
            """ each suburb """
            suburb = suburbs[idx].split(" Sales ")[0]
            
            lst = [cleanup(i) for i in tbl.select(".//tr/td/text()").extract()]
            for i in chunks(lst,7):
                item = RealestateAuctionItem()
                item['state'] = state
                item['suburb'] = suburb
                item['week_start'] = week_start
                item['address'] = i[0]
                item['room'] = i[1]
                item['price'] = i[2]
                item['category'] = i[3]
                item['method'] = i[4]
                item['sales_date'] = parser.parse(i[5])
                item['agency'] = i[6]
                # id
                item['url'] = "%s-%s-%s-%s-%s-%s" % \
                    (state,week_start.strftime("%Y%m%d"),suburb,item['address'],item['room'],item['price'])
                # print item
                log.msg(item['url'], level=log.INFO)
                ret.append(item)

        return ret

        
