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
process = CrawlerProcess(get_project_settings())
process.crawl(BtiSpider)
process.start()  # the script will block here until the crawling is finished
jsonline2md.process()
