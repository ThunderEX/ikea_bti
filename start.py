import locale
import argparse
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from ikea_bti.spiders.bti import BtiSpider
import jsonline2md

parser = argparse.ArgumentParser()
parser.add_argument('-l', dest='locale',
                    default=locale.getdefaultlocale()[0],
                    help='your locale, such as en_US, should be available in %s' % BtiSpider.sitemap_urls)
args = parser.parse_args()

BtiSpider.sitemap_follow = ['/sitemap/%s/' % args.locale]
if args.locale == 'zh_CN':
    from itertools import count
    from urllib import request, error

    BtiSpider.sitemap_urls = [
        'https://www.ikea.cn/robots.txt',
        'https://www.ikea.cn/sitemap/zh_CN/siteMap_Category_zh_CN.xml',
        ]
    try:
        for i in count(1):
            url = 'https://www.ikea.cn/sitemap/zh_CN/siteMap_Product_zh_CN_{}.xml'.format(i)
            req = request.Request(url, method='HEAD')
            res = request.urlopen(req)
            BtiSpider.sitemap_urls.append(url)
    except error.HTTPError:
        pass
print(BtiSpider.sitemap_urls[-1])

process = CrawlerProcess(get_project_settings())
process.crawl(BtiSpider)
process.start()  # the script will block here until the crawling is finished
jsonline2md.process()
