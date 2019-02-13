# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from script_nightyday.items import *
import pymongo
import datetime

class ScriptNightydayPipeline(object):
    client = pymongo.MongoClient(host='localhost', port=27017)
    db = client['90days_%s' % (datetime.datetime.now().strftime('%Y-%m'))]

    def process_item(self, item, spider):
        if isinstance(item, AZPhysiciansItem):
            collection = self.db['AZPhysicians']
            collection.insert_one(item.__dict__)
        if isinstance(item, CTAccountantsItem):
            collection = self.db['CTAccountants']
            collection.insert_one(item.__dict__)
        if isinstance(item, TXBoeItem):
            collection = self.db['TXBoe']
            collection.insert_one(item.__dict__)