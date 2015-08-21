'''
    Takes in a POST or GET string with an email address, generates a login token, and emails it to the user
'''

import sqlite3
from datetime import date, datetime
import time
import logging
import mbcommon as mbc
import hashlib
import re


homedir = mbc.set_working_path()
dbpath = "%s/mb_databases/mb_test_db.db" % (homedir)
logpath = "%s/log_files/apicall_log_%s.log" % (homedir,datetime.now().strftime("%Y%m%d"))


# Create daily log file
logging.basicConfig(filename=logpath,level=logging.DEBUG)



def main():

    # how many minutes should the token be valid for
    expmin = 15

    # TODO: get form data for this variable (what other variables can we append here)
    email = "albert.liang@gmail.com"
    nowtime = int(time.time())
    exptime = nowtime+expmin*60

    # generate the login token
    m = hashlib.md5()
    m.update(email)
    m.update(str(nowtime))
    token = m.hexdigest()


    # Connect to sql database
    mb_database = sqlite3.connect(dbpath)
    c = mb_database.cursor()

    t=(email,token,exptime)
    c.execute("INSERT INTO user_login (email,token,ttl) values(?,?,?)",t)

    # Close database
    mb_database.commit()
    mb_database.close()



    # send email to user
    url = "http://www.meowbucks.com/login/%s" % token
    f = open('login_template.html','r')
    tmp = f.read()
    f.close()
    tmp = re.sub('!LOGINURL',url,tmp)
    tmp = re.sub('!EXPMIN',str(expmin),tmp)
   
    FROM ='hello@meowbucks.com'
    mbc.send_mail("Meowbucks - Login Link", tmp, email, FROM)
    # temporary debug
    #print token


if __name__ == '__main__':
    main()

