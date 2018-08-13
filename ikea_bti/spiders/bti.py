from scrapy.spiders import SitemapSpider

from ikea_bti.items import IkeaBtiItem


class BtiSpider(SitemapSpider):
    name = "bti"
    sitemap_urls = ['http://www.ikea.com/sitemap.xml']
    sitemap_follow = ['/sitemap/zh_CN/']
    sitemap_rules = [
        (r'.*/products/', 'parse_product_page'),
    ]

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
