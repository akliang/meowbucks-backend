'''
    Checks the *_cache tables to make sure the items are in the right place
    Should run it once every 24 hours
'''

import sqlite3
from datetime import date, datetime
import logging
import mbcommon as mbc


homedir = mbc.set_working_path()
dbpath = "%s/mb_databases/mb_test_db.db" % (homedir)
logpath = "%s/log_files/apicall_log_%s.log" % (homedir,datetime.now().strftime("%Y_%m_%d_%H_%M"))


# Create daily log file
logging.basicConfig(filename=logpath,level=logging.DEBUG)

# Get a list of asins to send to api
def query_cache(c,table):
    cachelist = []

    #for row in c.execute('SELECT id,date FROM %s' % table):
    for row in c.execute('SELECT * FROM %s' % table):
        row = row[0].encode('utf-8')
        cachelist.append(row)

    return cachelist





def main():
    # Connect to sql database
    mb_database = sqlite3.connect(dbpath)
    c = mb_database.cursor()

    # check product_cache first
    icache = query_cache(c,'product_cache')
    if len(icache) > 0:
        for C in icache:
            print "hello %s %s" % (C[0],C[1])
 



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

