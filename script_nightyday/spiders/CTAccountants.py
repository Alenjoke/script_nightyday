# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from urllib import parse
from script_nightyday.items import CTAccountantsItem
import logging

class CtaccountantsSpider(scrapy.Spider):
    name = 'CTAccountants'
    allowed_domains = ['www.elicense.ct.gov']
    start_urls = ['https://www.elicense.ct.gov/lookup/licenselookup.aspx']
    words = [chr(x) for x in range(97, 123)]

    def parse(self, response):
        soup = BeautifulSoup(response.body, 'lxml')
        for sendkey1 in self.words:
            for sendkey2 in self.words:
                sendkey = sendkey1 + sendkey2
                logging.info('start read ' + sendkey)
                formdata = {
                    'ctl00$ScriptManager1': 'ctl00$MainContentPlaceHolder$ucLicenseLookup$UpdtPanelGridLookup|ctl00$MainContentPlaceHolder$ucLicenseLookup$UpdtPanelGridLookup',
                    'ctl00$MainContentPlaceHolder$ucLicenseLookup$ctl03$ddCredPrefix':'',
                    'ctl00$MainContentPlaceHolder$ucLicenseLookup$ctl03$tbLicenseNumber':'',
                    'ctl00$MainContentPlaceHolder$ucLicenseLookup$ctl03$ddSubCategory':'',
                    'ctl00$MainContentPlaceHolder$ucLicenseLookup$ctl03$ddStatus': '368',
                    'ctl00$MainContentPlaceHolder$ucLicenseLookup$ctl03$tbDBA_Contact':'',
                    'ctl00$MainContentPlaceHolder$ucLicenseLookup$ctl03$tbFirstName_Contact':'',
                    'ctl00$MainContentPlaceHolder$ucLicenseLookup$ctl03$tbLastName_Contact': sendkey,
                    'ctl00$MainContentPlaceHolder$ucLicenseLookup$ctl03$tbAddress2_ContactAddress':'',
                    'ctl00$MainContentPlaceHolder$ucLicenseLookup$ctl03$ddStates':'',
                    'ctl00$MainContentPlaceHolder$ucLicenseLookup$ctl03$tbCity_ContactAddress':'',
                    'ctl00$MainContentPlaceHolder$ucLicenseLookup$ctl03$tbZipCode_ContactAddress':'',
                    'ctl00$MainContentPlaceHolder$ucLicenseLookup$ctl03$ddCountry': '221',
                    'ctl00$MainContentPlaceHolder$ucLicenseLookup$ResizeLicDetailPopupID_ClientState': '0,0',
                    'ctl00$OutsidePlaceHolder$ucLicenseDetailPopup$ResizeLicDetailPopupID_ClientState': '0,0',
                    '__EVENTTARGET': 'ctl00$MainContentPlaceHolder$ucLicenseLookup$UpdtPanelGridLookup',
                    '__EVENTARGUMENT': '2~~41~~5',
                    '__VIEWSTATE': soup.select('#__VIEWSTATE')[0]['value'],
                    '__VIEWSTATEGENERATOR': '44A23853',
                    '__VIEWSTATEENCRYPTED':'',
                    '__ASYNCPOST': 'true'
                }
                yield scrapy.FormRequest(url=self.start_urls[0],meta={'formdata':formdata}, formdata=formdata, dont_filter=True, callback=self.get_info)
    def get_info(self, response):
        base_url = 'https://www.elicense.ct.gov/Lookup/licensedetail.aspx?id='
        soup = BeautifulSoup(response.body, 'lxml')
        results = soup.select('#ctl00_MainContentPlaceHolder_ucLicenseLookup_gvSearchResults > tbody > tr')
        formdata = response.meta['formdata']
        formdata['__EVENTTARGET'] = 'ctl00$MainContentPlaceHolder$ucLicenseLookup$gvSearchResults'
        for result in results:
            item = CTAccountantsItem()
            item['name'] = result.select('td:nth-of-type(2)')[0].get_text()
            item['credential'] = result.select('td:nth-of-type(3)')[0].get_text()
            item['credential_description'] = result.select('td:nth-of-type(4)')[0].get_text()
            item['state'] = result.select('td:nth-of-type(5)')[0].get_text()
            item['status'] = result.select('td:nth-of-type(6)')[0].get_text()
            item['status_reason'] = result.select('td:nth-of-type(7)')[0].get_text()
            item['city'] = result.select('td:nth-of-type(8)')[0].get_text()
            item['dba'] = result.select('td:nth-of-type(9)')[0].get_text()
            yield item
        try:
            next_page = soup.select('.CavuGridPager span')[0].parent.next_sibling
            if next_page.next_sibling is not None:
                next_page = 'Page$' + next_page.get_text()
                formdata['__EVENTARGUMENT'] = next_page
                yield scrapy.FormRequest(url=self.start_urls[0],meta={'formdata':formdata}, formdata=formdata, dont_filter=True, callback=self.get_info)
            else:
                logging.info(formdata['ctl00$MainContentPlaceHolder$ucLicenseLookup$ctl03$tbLastName_Contact'] + ' 没有下一页了...')
        except:
            logging.info(formdata['ctl00$MainContentPlaceHolder$ucLicenseLookup$ctl03$tbLastName_Contact'] + ' 只有一页...')
