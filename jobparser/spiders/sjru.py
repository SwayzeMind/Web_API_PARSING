# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem
import re

class SjruSpider(scrapy.Spider):
    name = 'sjru'
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=Python&geo%5Bc%5D%5B0%5D=1']

    def parse(self, response):
        next_page = response.xpath("//a[@class='icMQ_ _1_Cht _3ze9n f-test-button-dalshe f-test-link-Dalshe']/@href").extract_first()
        yield response.follow(next_page, callback=self.parse)

        vacancies = response.xpath('//a[contains(@class, "_1QIBo")]/@href').extract()
        for vacancy in vacancies:
            yield response.follow(vacancy, callback=self.vacancy_parse)

    @staticmethod
    def vacancy_parse(response: HtmlResponse):
        result = dict()
        result['title'] = ''.join(response.xpath('//h1[@class="_3mfro rFbjy s1nFK _2JVkc"]//text()').extract())
        salary = ''.join(response.xpath('//span[@class="_3mfro _2Wp8I ZON4b PlM3e _2JVkc"]//text()').extract())
        salary = salary.replace('\xa0—\xa0', '-')
        result['salary'] = re.sub(r'(\d+)\xa0(\d+)', r'\1\2', salary).replace('\xa0', ' ')
        result['link'] = str(response.url)[5:-1]

        yield JobparserItem(result)
