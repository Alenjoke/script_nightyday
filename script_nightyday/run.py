from scrapy import cmdline

spider = 'WIProlic'
cmd = 'scrapy crawl %s ' % (spider)
cmdline.execute(cmd.split())