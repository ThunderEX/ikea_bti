# -*- coding: utf-8 -*-
from urllib.parse import urlparse, urlunparse

from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request
from scrapy.exceptions import DropItem
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class IkeaBtiPipeline(object):
    def __init__(self):
        super(IkeaBtiPipeline, self).__init__()
        self.urls_seen = set()

    def process_item(self, item, spider):
        # clear query in url in case there are any vertical bar "|" which break markdown table delimiter
        item['url'] = urlunparse(urlparse(item['url'])._replace(query=''))

        if item['url'] in self.urls_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.urls_seen.add(item['url'])
            return item


class KeepNameImgPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        # check if called from image_key or file_key with url as first argument
        if not isinstance(request, Request):
            url = request
        else:
            url = request.url

        return url.split('/')[-1]
