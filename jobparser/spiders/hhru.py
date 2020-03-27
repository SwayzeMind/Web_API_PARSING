# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class HhruSpider(scrapy.Spider):
    name = 'hh.ru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://hh.ru/search/vacancy?area=1&st=searchVacancy&text=python&page=0']

    def parse(self, response:HtmlResponse):
        next_page = response.xpath("//a[@class='bloko-button HH-Pager-Controls-Next HH-Pager-Control']/@href").extract_first()
        yield response.follow(next_page, callback=self.parse)

        vacancies = response.xpath("//a[@class='bloko-link HH-LinkModifier']/@href").extract()
        for vacancy in vacancies:
            yield response.follow(vacancy, callback=vacancy_parse)


def vacancy_parse(response:HtmlResponse):
    result = dict()
    result['title'] = ''.join(response.xpath('//div[contains(@class, "vacancy-title")]/h1/span/text()').extract())
    if not result['title']:
        result['title'] = ''.join(response.xpath('//div[contains(@class, "vacancy-title")]/h1/text()').extract())

    result['salary'] = ''.join(response.xpath("//span[@class='bloko-header-2 bloko-header-2_lite']/text()").extract())
    result['link'] = str(response.url)[5:-1]
    yield JobparserItem(result)
