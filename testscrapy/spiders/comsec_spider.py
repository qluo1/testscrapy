from scrapy.spider import BaseSpider
from scrapy.http import FormRequest


class Comsec_spider(BaseSpider):
    name = "comsec"
    allowed_domains = ["comsec.com.au"]
    start_urls = (
        'https://www.comsec.com.au/default.aspx',
        )

    def parse(self, response):
        print "parsing"
        print response.url
        return [FormRequest.from_response(response, formname = "fmLogin",
            formdata={'UcHeader1_LoginName': 'john', 'UcHeader1_Password': 'secret'},
            callback=self.after_login)]
    
    def after_login(self,response):
        # check login succeed before going on
        print response.url
        print  response.body
        return {}
