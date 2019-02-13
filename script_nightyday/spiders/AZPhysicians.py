# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from script_nightyday.items import AZPhysiciansItem
import logging

class AzphysiciansSpider(scrapy.Spider):
    name = 'AZPhysicians'
    allowed_domains = ['www.azmd.gov']
    words = [chr(x) for x in range(97, 123)]
    base_url = 'https://gls.azmd.gov/glsuiteweb/clients/azbom/public/webverificationsearch.aspx'

    def start_requests(self):
        for sendkey1 in self.words:
            for sendkey2 in self.words:
                for sendkey3 in self.words:
                    sendkey = sendkey1 + sendkey2 + sendkey3
                    logging.info('开始搜索%s...' % (sendkey))
                    form_data = {
                        '__EVENTTARGET':'',
                        '__EVENTARGUMENT':'',
                        '__VIEWSTATE': 'Lo93Xrbb1D/R1o7gZxA42QoCvAOgBwxP4HNciQn0j6fH5tFeBQ7HKiawJ9b+aiKnN3qJ7P89y05N8xJ3i5sKuEZcM8LUBjaTfLYi7usm01axg2wBiZGsXCSe7utT0qgNdqn5q7253mNwFOs7LpdRKKraDsChi5tjpAWoVW6yHVIfH7qI4XVruRPOxGpx0ZzHpqUkcAmBY0BrilXEz3KemBw1cnlC2CtTevVaSgt3FLtudM9bwFGoSPVfxaY0glHJGpEeIFRdN3mqzGloEExyZ5icAVLbEVX2AhejmjYlm4EN4Q73y37VZth4hQGNlD3lFGfWKhKLMo0hGPFv/QjXd9ViLn3KCNgI5XqFc2uU1emRsdguQWPFTSIOg/h1YAYMLUUXCjz+TJQ331jT7xgkO8j4GtfkGl6eHelCOFHvh6oal8t/2FvM+fnTzqWQlKaYi77snm5kq9ZMsxo9UWJv+V1zUmWGucUj1+OTXBuqADDP4aZCjEbJiWJRk2B7HxDqjM8Btj65RmHm63f1Xp2tSaL/M6OfDsaSvNc/AOfnOBIgqNMJUDlqYz6vzpLq9ZcdFf3mCh5ky6jqusHS0GfUAlKH/ga17I0XyWpjmUr6v2X1QVqhCIegr5ocezVh4CgAKISI+/c9aXgsXiKSRKKkgIAZ81+x3BDFXPeduRZxt0VIPK2UU4BXCpyey9x4D42ag1cdsbwMMorIW0fR4LqeswskI6G8iusTr7OC/2Mal6IxAX4Z',
                        '__VIEWSTATEGENERATOR': 'C402AD49',
                        '__VIEWSTATEENCRYPTED':'',
                        '__EVENTVALIDATION': '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',
                        'Name': 'rbName1',
                        'tbLastName': sendkey,
                        'tbFirstName':'',
                        'btnName': 'Name Search',
                        'tbErrorName': 'No doctors found with those specifications.',
                        'License': 'rbLicense1',
                        'tbFileNumber':'',
                        'Specialty': 'rbSpecialty1',
                        'ObjectTypeID': '2954',
                        'ObjectID': '40',
                        'PrimaryField': '14217',
                        'County1': '15910',
                        'City1':''
                    }
                    yield scrapy.FormRequest(self.base_url, formdata=form_data, callback=self.parse, dont_filter=True)
    def parse(self, response):
        if not str(response.body).__contains__('No doctors found with those specifications.'):
            soup = BeautifulSoup(response.body, 'lxml')
            lines = soup.select('table table tr')
            try:
                last_line = lines.pop()
            except Exception as e:
                logging.info('该页无记录')
            for line in lines:
                try:
                    link = line.select('a')[0]['href']
                    yield scrapy.Request(link, callback=self.get_info, dont_filter=True)
                except IndexError as e:
                    logging.info('该页无记录')
            try:
                href = last_line.select('span')[0].next_sibling.next_sibling['href']
                EVENTTARGET = href[25:44]
                form_data = {
                    '__EVENTTARGET': EVENTTARGET,
                    '__EVENTARGUMENT':'',
                    '__VIEWSTATE': soup.select('#__VIEWSTATE')[0]['value'],
                    '__VIEWSTATEGENERATOR': soup.select('#__VIEWSTATEGENERATOR')[0]['value'],
                    '__VIEWSTATEENCRYPTED':'',
                    '__EVENTVALIDATION': soup.select('#__EVENTVALIDATION')[0]['value'],
                     'txtDum':''
                }
                url = 'https://gls.azmd.gov/glsuiteweb/clients/azbom/Public/Results.aspx'
                yield scrapy.FormRequest(url=url, formdata=form_data, method='POST', dont_filter=True, callback=self.parse)
            except Exception as e:
                logging.info('没有下一页了...')
    def get_info(self, response):
        soup = BeautifulSoup(response.body, 'lxml')
        item = AZPhysiciansItem()
        item['name'] = ''
        item['address'] = ''
        item['phone'] = ''
        item['license_number'] = ''
        item['license_status'] = ''
        item['license_date'] = ''
        item['license_renewed'] = ''
        item['due_to_renew'] = ''
        item['license_expires'] = ''

        item['name'] = soup.select('#dtgGeneral_ctl02_lblLeftColumnEntName')[0].get_text()
        address_phone = soup.select('#dtgGeneral_ctl02_lblLeftColumnPracAddr')[0].get_text()
        if address_phone is not None:
            address_phone = address_phone.split('Phone:')
            if len(address_phone) == 2:
                item['address'] = address_phone[0]
                item['phone'] = address_phone[1]
            else:
                item['address'] = address_phone[0]
        license = str(soup.select('#dtgGeneral td:nth-of-type(2)')[0]).replace('\n','').strip('<td>').strip('</td>').strip('<br').split('<br/>')
        for content in license:
            if content.__contains__('License Number'):
                item['license_number'] = content.split(':')[1]
            elif content.__contains__('License Status'):
                item['license_status'] = content.split(':')[1]
            elif content.__contains__('Licensed Date'):
                item['license_date'] = content.split(':')[1]
            elif content.__contains__('License Renewed'):
                item['license_renewed'] = content.split(':')[1]
            elif content.__contains__('Due to Renew By'):
                item['due_to_renew'] = content.split(':')[1]
            elif content.__contains__('Expires'):
                item['license_expires'] = content.split(':')[1]
        yield item