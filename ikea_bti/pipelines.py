# -*- coding: utf-8 -*-
from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class IkeaBtiPipeline(object):
    def process_item(self, item, spider):
        return item


class KeepNameImgPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        # check if called from image_key or file_key with url as first argument
        if not isinstance(request, Request):
            url = request
        else:
            url = request.url

        return url.split('/')[-1]
