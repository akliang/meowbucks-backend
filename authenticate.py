'''
    Takes in a POST or GET string with the login token, and tries to match it against an existing one
'''

import sqlite3
from datetime import date, datetime
import time
import logging
import mbcommon as mbc


homedir = mbc.set_working_path()
dbpath = "%s/mb_databases/mb_test_db.db" % (homedir)
logpath = "%s/log_files/apicall_log_%s.log" % (homedir,datetime.now().strftime("%Y%m%d"))


# Create daily log file
logging.basicConfig(filename=logpath,level=logging.DEBUG)



def main():

    token = "77f1faed9a11fb38d261061380751cbb"
    nowtime = int(time.time())

    # Connect to sql database
    mb_database = sqlite3.connect(dbpath)
    c = mb_database.cursor()

    t=(token,nowtime)
    c.execute("SELECT email FROM user_login WHERE token = ? AND ttl > ?",t)
    ret = c.fetchall()


    if len(ret)>1:
        print "Error -- something went wrong."
    elif len(ret)==0:
        print "No login found, or token has expired."
    else:
        print "Welcome %s!" % ret[0][0]
        # remove the token from the table
        t=(token,)
        c.execute("DELETE FROM user_login WHERE token = ?",t)



    mb_database.commit()
    mb_database.close()





if __name__ == '__main__':
    main()

