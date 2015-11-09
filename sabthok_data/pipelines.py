# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os

from scrapy import signals
from scrapy.exporters import JsonItemExporter


class SabthokDataPipeline(object):
    def __init__(self):
        self.files = {}
        self.exporters = {}

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        # Setting folder to store files
        base_path = 'output/gsmarena'
        if not os.path.exists('output'):
            os.mkdir('output')
        if not os.path.exists(base_path):
            os.mkdir(base_path)

        # Open files for writing and assgin them to exporters
        for name in spider.names:
            filepath = os.path.join(base_path, name + '.json')

            self.files[name] = open(filepath, 'w')
            self.exporters[name] = JsonItemExporter(self.files[name])

            # Start exporting
            self.exporters[name].start_exporting()

    def spider_closed(self, spider):
        for name in spider.names:
            self.exporters[name].finish_exporting()
            self.files[name].close()

    def process_item(self, item, spider):
        self.exporters[item['Maker']].export_item(item)
        return item
