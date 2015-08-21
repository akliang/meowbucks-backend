''' This python module interacts with the purchase_cache and product_info tables. 
    1. select unique product_asin from the purchase_cache table
    2. call amazon API using asin to get product information
    3. populate the product_info page with data returned from the API
'''

import sqlite3
from datetime import date, datetime
import logging
import mbcommon as mbc


homedir = mbc.set_working_path()
dbpath = "%s/mb_databases/mb_test_db.db" % (homedir)
logpath = "%s/log_files/apicall_log_%s.log" % (homedir,datetime.now().strftime("%Y%m%d"))


# Create daily log file
logging.basicConfig(filename=logpath,level=logging.DEBUG)


# Get a list of asins to send to api
def get_asin_list(c):
    asin_list = []

    for row in c.execute('SELECT DISTINCT product_asin FROM purchase_cache'):
        row = row[0].encode('utf-8')
        asin_list.append(row)

    return asin_list




def main():
    mbc.reset_db(dbpath)

    # Connect to sql database
    mb_database = sqlite3.connect(dbpath)
    c = mb_database.cursor()

    # Get a list of asins from purchase_cache table
    asin_list = get_asin_list(c)
    successfully_updated= 0

    # Call api and update table
    if len(asin_list) > 0:
        for asin in asin_list:

            resp = mbc.call_API(asin)
            if resp:
                mbc.insert_into_table(c,'product_history',resp)
                mbc.insert_into_table(c,'product_cache',resp)
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

