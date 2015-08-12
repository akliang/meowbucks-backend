''' Processes user-submitted URL and inserted data into database '''

from amazon.api import AmazonAPI
import sqlite3
from datetime import date, datetime
import time
import logging
import os
import init_db
import re
import mbcommon as mbc

homedir = mbc.set_working_path()
dbpath = "%s/mb_databases/mb_test_db.db" % (homedir)
logpath = "%s/log_files/apicall_log_%s.log" % (homedir,datetime.now().strftime("%Y_%m_%d_%H_%M"))


# Create daily log file
logging.basicConfig(filename=logpath,level=logging.DEBUG)


def main():

    # todo: process POST data here
    email = "asdf@asfd.com"
    url = "http://www.amazon.com/dp/B00X4WHP5E"
    asin=re.sub('.*/dp/','',url)
    purchase_date = "1438894338"  # unix timestamp
    purchase_price = "99.99"


    # safety check
    resp=call_API(asin)
    if resp:
        price, asin, title, call_date, img, url = resp
    else:
        logging.warning("Amazon did not find asin: %s" %(asin))

    if purchase_date is '':
        purchase_date="%d" % (time.time())
        logging.warning("No purchase_date specified... setting it to now-time (%d)" % purchase_date)
    if purchase_price is '':
        # pull price from Amazon?  pull from our product-history db?
        purchase_price = price
        logging.warning("No purchase_price specified.... setting it to current price (%0.2f)" % purchase_price

    # assemble the array
    


    # insert the data into the db
    mb_database = sqlite3.connect(dbpath)
    c = mb_database.cursor()
    %insert_into_table(c,'purchase_history',
    


    init_db.start(dbpath)

    # Connect to sql database

    # Get a list of asins from purchase_cache table
    asin_list = get_asin_list(c)
    successfully_updated= 0

    # Call api and update table
    if len(asin_list) > 0:
        for asin in asin_list:

            resp = call_API(asin)
            if resp:
                #price, asin, title, call_date, img, url = resp
                #update_product_table(c, asin, title, call_date, price, img, url)
                insert_into_table(c,'product_history',resp)
                insert_into_table(c,'product_cache',resp)
                successfully_updated += 1
            else:
                logging.warning("Amazon did not find asin: %s" %(asin))
                

    logging.info('%s asins were sent to api. %s asins successfully updated product table.' 
                %((len(asin_list)), successfully_updated))

    # Close database
    mb_database.commit()
    mb_database.close()


if __name__ == '__main__':
    main()

