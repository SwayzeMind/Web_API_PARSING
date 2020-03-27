# -*- coding: utf-8 -*-

from jobparser.items import JobparserItem
from typing import Dict
import re
from pymongo import MongoClient
from pymongo import errors

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class JobparserPipeline(object):
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_db = client['scrapyDB']


    def process_item(self, item, spider):
        salary = self.parse_compensation(comp=item['salary'])
        result = {}
        result.update(item)
        del result['salary']
        result.update(salary)
        result['source'] = spider.name

        collection = self.mongo_db[spider.name]
        collection.insert_one(result)

        return item


    def parse_compensation(self, comp: str) -> Dict:
        salary_from = salary_to = units = ''
        comp_search = re.search('(от)?([0-9 ]+)?(до|-)?([0-9 ]+)? (.*)$', comp.lower().replace('\xa0', ''))
        if comp_search:
            if comp_search.group(2):
                salary_from = int(comp_search.group(2))
            if comp_search.group(3) and '-' in comp_search.group(3) or comp_search.group(
                    3) and 'до' in comp_search.group(3):
                salary_to = int(comp_search.group(4))
            elif comp_search.group(1) and 'до' in comp_search.group(1):
                salary_to = int(comp_search.group(2))
            if salary_to or salary_from:
                units = comp_search.group(5)

        return {'salary_from': salary_from, 'salary_to': salary_to, 'units': units}
