# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from script_nightyday.items import TXBoeItem
import re

class TxboeSpider(scrapy.Spider):
    name = 'TXBoe'
    allowed_domains = ['www.tdlr.texas.gov']
    words = [chr(x) for x in range(97, 123)]

    def start_requests(self):
        url = 'https://www.tdlr.texas.gov/licensesearch/SearchResultsListBrowse.asp?from=search'
        for sendkey1 in self.words:
            for sendkey2 in self.words:
                sendkey = sendkey1 + sendkey2
                formdata = {
                    'tdlr_status': '-1',
                    'pht_lic':'',
                    'pht_expdt':'',
                    'pht_oth_name': sendkey,
                    'phy_city': '-1',
                    'phy_cnty': '-1',
                    'phy_zip':'',
                    'B1': 'Search'
                }
                yield scrapy.FormRequest(url=url, formdata=formdata, callback=self.parse, dont_filter=True)

    def parse(self, response):
        if not str(response.body).__contains__('No Records Found'):
            soup = BeautifulSoup(response.body, 'lxml')
            lines = soup.select('#content > table table tr')
            if lines is not None and len(lines) > 1:
                lines.pop(0)
            for line in lines:
                item = TXBoeItem()
                item['license'] = ''
                item['exp_date'] = ''
                item['name'] = ''
                item['city'] = ''
                item['zip'] = ''
                item['county'] = ''
                item['phone'] = ''
                item['license'] = line.select('td:nth-of-type(1)')[0].get_text()
                item['exp_date'] = line.select('td:nth-of-type(2)')[0].get_text()
                item['name'] = line.select('td:nth-of-type(3)')[0].get_text()
                item['city'] = line.select('td:nth-of-type(4)')[0].get_text()
                item['zip'] = line.select('td:nth-of-type(5)')[0].get_text()
                item['county'] = line.select('td:nth-of-type(6)')[0].get_text()
                item['phone'] = line.select('td:nth-of-type(7)')[0].get_text()
                yield item
            try:
                next = soup.find(text=re.compile('Next')).find_parent()
                url = 'https://www.tdlr.texas.gov/licensesearch/' + next['href']
                yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)
            except:
                print('没有下一页了')