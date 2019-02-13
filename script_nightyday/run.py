from scrapy import cmdline

spider = 'TXBoi'
cmd = 'scrapy crawl %s ' % (spider)
cmdline.execute(cmd.split())