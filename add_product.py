''' Processes user-submitted URL and inserted data into database '''

from amazon.api import AmazonAPI
import sqlite3
from datetime import date, datetime
import time
import logging
import os
import re
import mbcommon as mbc

homedir = mbc.set_working_path()
dbpath = "%s/mb_databases/mb_test_db.db" % (homedir)
logpath = "%s/log_files/applog_%s.log" % (homedir,datetime.now().strftime("%Y%m%d"))


# Create daily log file
logging.basicConfig(filename=logpath,level=logging.DEBUG)


def main():

    # todo: process POST data here
    email = "asdf@asfd.com"
    url = "http://www.amazon.com/dp/B00X4WHP5E"
    asin=re.sub('.*/dp/','',url)
    purchase_date = "1438894338"  # unix timestamp
    purchase_price = "99.99"

    logging.debug("  add_product request: email=%s ; url=%s ; purchase_date = %s ; purchase_price = %s" % (email,url,purchase_date,purchase_price))


    # safety check
    resp=mbc.call_API(asin)
    if resp:
        price, asin, title, call_date, img, url = resp
    else:
        logging.warning("  Amazon did not find asin: %s" %(asin))

    if purchase_date is '':
        purchase_date="%d" % (time.time())
        logging.warning("  No purchase_date specified... setting it to now-time (%d)" % purchase_date)
    if purchase_price is '':
        # pull price from Amazon?  pull from our product-history db?
        purchase_price = price
        logging.warning("  No purchase_price specified.... setting it to current price (%0.2f)" % purchase_price)

    # assemble the array
    item = mbc.amazonItem()
    item.email=email
    item.asin=asin
    item.purchase_date=purchase_date
    item.purchase_price=purchase_price
    

    # insert the data into the db
    mb_database = sqlite3.connect(dbpath)
    c = mb_database.cursor()
    mbc.insert_into_table(c,'purchase_history',item)
    mb_database.commit()
    mb_database.close()
    


if __name__ == '__main__':
    main()

