# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field

class ScriptNightydayItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
class AZPhysiciansItem(scrapy.Item):
    name = Field()
    address = Field()
    phone = Field()
    license_number = Field()
    license_status = Field()
    license_date = Field()
    license_renewed = Field()
    due_to_renew = Field()
    license_expires = Field()
class COMarijuanaItem(scrapy.Item):
    name = Field()
    type = Field()
    lic = Field()
    status = Field()
    expiration_date = Field()
class CTAccountantsItem(scrapy.Item):
    #Name|Credential|Credential Description|Status|Status Reason|City|State|Zip|DBA
    name = Field()
    credential = Field()
    credential_description = Field()
    state = Field()
    status = Field()
    status_reason = Field()
    city = Field()
    dba = Field()
class TXBoeItem(scrapy.Item):
    license = Field()
    exp_date = Field()
    name = Field()
    city = Field()
    zip = Field()
    county = Field()
    phone = Field()