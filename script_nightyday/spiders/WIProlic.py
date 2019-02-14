# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from script_nightyday.items import WIProlicItem

class WiprolicSpider(scrapy.Spider):
    name = 'WIProlic'
    allowed_domains = ['app.wi.gov']
    words = [chr(x) for x in range(97, 123)]

    def start_requests(self):
        url = 'https://app.wi.gov/LicenseSearch/'
        for sendkey in self.words:
            formdata = {
                'CredentialViewModel.CredentialType.CredNameCode': '-1',
                'CredentialViewModel.CredentialStatusCode': '2',
                'CredentialViewModel.Zip': '',
                'CredentialViewModel.Name': sendkey,
                'Command': 'TradeCredAdvSearch'
            }
            yield scrapy.FormRequest(url=url, formdata=formdata, callback=self.parse)

    def parse(self, response):
        soup = BeautifulSoup(response.body, 'lxml')
        lines = soup.select('table tr')
        print(len(lines))
        if len(lines) > 0:
            lines.pop(0)
        for line in lines:
            item = WIProlicItem()
            item['id'] = ''
            item['name'] = ''
            item['city'] = ''
            item['state'] = ''
            item['zip'] = ''
            item['profession'] = ''
            item['expiration'] = ''

            item['id'] = line.select('td:nth-of-type(1)')[0].get_text()
            item['name'] = line.select('td:nth-of-type(2)')[0].get_text()
            city_state_zip = line.select('td:nth-of-type(3)')[0].get_text()
            arr = city_state_zip.split(' ')
            arr.remove('')
            item['city'] = arr[0]
            item['state'] = arr[1]
            item['zip'] = arr[2]
            item['profession'] = line.select('td:nth-of-type(4)')[0].get_text()
            item['expiration'] = line.select('td:nth-of-type(5)')[0].get_text()
            yield item
