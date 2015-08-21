'''
    Checks the purchase_cache tables and removed items that are older than 30 days
    Should run it once every 24 hours (via cronjob?)
'''

import sqlite3
from datetime import date, datetime
import time
import logging
import mbcommon as mbc


homedir = mbc.set_working_path()
dbpath = "%s/mb_databases/mb_test_db.db" % (homedir)
logpath = "%s/log_files/apicall_log_%s.log" % (homedir,datetime.now().strftime("%Y_%m_%d"))


# Create daily log file
logging.basicConfig(filename=logpath,level=logging.DEBUG)



def main():

    # todays date plus 30 days
    pdate = int(time.time()-30*24*60*60)
    logging.info("mb_cacher.py -- Removing rows older than %d (%s) from purchase_cache" % (pdate,datetime.fromtimestamp(pdate).strftime('%Y-%m-%d %H:%M:%S')))


    # Connect to sql database
    mb_database = sqlite3.connect(dbpath)
    c = mb_database.cursor()

    # test entries for development
    #c.execute("insert into purchase_cache values(4,'hello@meowbucks.com','B00QJDU3KZ','','1437284338',50)")
    #c.execute("insert into purchase_cache values(4,'hello@meowbucks.com','B00QJDU3KZ','','1437384338',50)")

    t = (pdate,)
    c.execute('DELETE FROM purchase_cache WHERE purchase_date < ?',t)
    nrows = c.rowcount
    logging.info("mb_cacher.py -- Removed %d item(s) from purchase_cache" % nrows)



    # Close database
    mb_database.commit()
    mb_database.close()


if __name__ == '__main__':
    main()

