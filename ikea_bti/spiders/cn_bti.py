import re
from scrapy import Request
from scrapy.utils.response import get_base_url
from scrapy.utils.python import unique as unique_list
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from ikea_bti.items import IkeaBtiItem

class RmDupliLinkExtractor(LinkExtractor):
    """
    Sometimes
    https://www.ikea.cn/cn/zh/ideas/201542_iden01a/cn/zh/catalog/categories/departments/eating/18869/
    generates link to
    https://www.ikea.cn/cn/zh/ideas/201542_iden01a/cn/zh/catalog/categories/departments/eating/18869/cn/zh/catalog/categories/departments/eating/18869/
    """
    def extract_links(self, response):
        links = super(RmDupliLinkExtractor, self).extract_links(response)
        base_url = get_base_url(response)
        return unique_list([link for link in links if not (link.url.startswith(base_url) and base_url.endswith(link.url[len(base_url):]))])

class CNBtiSpider(CrawlSpider):
    name = "cn_bti"
    allowed_domains = ['ikea.cn']
    start_urls = ['https://www.ikea.cn/cn/zh/']
    rules = (
        # Extract links matching r'.*/products/' and parse them with the spider's method parse_product_page
        Rule(RmDupliLinkExtractor(allow=(r'.*/cn/zh.*/products/', )), callback='parse_product_page', follow=True),

        # Extract links matching r'.*/catalog/'
        # and follow links from them (since no callback means follow=True by default).
        Rule(RmDupliLinkExtractor(allow=(r'', ), deny=(r'\bcn/en\b', r'\ben_CN\b', r'/webapp/wcs/stores/servlet/'))),
        # Rule(RmDupliLinkExtractor(allow=(r'.*/cn/zh.*/catalog/', ))),
    )

    def parse_product_page(self, response):
        div = response.xpath('//div[contains(@class, "productBtiFront")]')
        if div:
            div = div[0]
            yield IkeaBtiItem(
                name=div.xpath('.//span[contains(@class, "productName")]/text()').extract_first().strip(),
                type=div.xpath('.//span[contains(@class, "productType")]/text()').extract_first().strip(),
                family_price=''.join(e for e in div.xpath('.//span[contains(@class, "ikeaFamilyPrice")]/text()').extract()).strip().replace(u'\xa0', u' '),
                package_price=''.join(e for e in div.xpath('.//span[contains(@class, "packagePrice")]/text()').extract()).strip().replace(u'\xa0', u' '),
                image_urls=[response.urljoin(response.xpath('//img[contains(@id, "productImg")]/@src').extract_first())],
                url=response.url,
            )
        for option in response.xpath('//option').re(r'\"http[^"]*\"'):
            if re.search(r'.*/cn/zh.*/products/', option):
                yield Request(option.strip('"'), callback=self.parse_product_page)
            else:
                yield Request(option.strip('"'), callback=self.parse)
