
import sqlite3
import os
from amazon.api import AmazonAPI
from datetime import date, datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class amazonItem:
    pass

def reset_db(dbpath):
    # connect to sql database
    conn = sqlite3.connect(dbpath)
    c = conn.cursor()
    
    # Uncomment below section if want to create tables purchases_tracking and product_info from scratch
    c.execute('DROP TABLE IF EXISTS user_login')
    c.execute('DROP TABLE IF EXISTS purchase_history')
    c.execute('DROP TABLE IF EXISTS purchase_cache')
    c.execute('DROP TABLE IF EXISTS product_history')
    c.execute('DROP TABLE IF EXISTS product_cache')
    
    
    c.execute('create table user_login(id integer primary key, email text, token text, ttl integer);')
    c.execute('create table purchase_history(id integer primary key, emailid integer, product_asin text, purchase_date integer, starting_price real);')
    c.execute('create table purchase_cache as select * from purchase_history where 0;')
    c.execute('create table product_history(id integer primary key, product_asin text, date integer, price real, medium_image_url text, offer_url text);')
    c.execute('create table product_cache as select * from product_history where 0;')
    
    
    
    c.execute("INSERT INTO purchase_history VALUES ('1', 'swagberry@meowbucks.com', 'B00QJDU3KY', '1438794338', '100')")
    c.execute("INSERT INTO purchase_history VALUES ('2', 'swagberry@meowbucks.com', 'B00JP7R8X6', '1438894038', '10')")
    c.execute("INSERT INTO purchase_history VALUES ('3', 'jojo@meowbucks.com', 'B00JP7R8X6', '1438892338', '10')")
    c.execute("INSERT INTO purchase_cache SELECT * FROM purchase_history")
    
    conn.commit()
    conn.close()


def db_connect(dbpath):
    mb_database = sqlite3.connect(dbpath)
    c = mb_database.cursor()
    return c


def set_working_path():
    if os.path.exists('/Users/Sherry/meowbucks/'):
        return '/Users/Sherry/meowbucks'
    else:
        return '.'



def call_API(asin):
    AMAZON_ACCESS_KEY = 'AKIAJ2MUVQ36XFWLYUEA'
    AMAZON_SECRET_KEY = '***REMOVED***z'
    AMAZON_ASSOC_TAG = 'meowbucks-20'

    amazon = AmazonAPI(AMAZON_ACCESS_KEY, AMAZON_SECRET_KEY, AMAZON_ASSOC_TAG)
    product = amazon.lookup(ItemId = asin)

    if product:
        # fields returned from Amazon
        price = product.price_and_currency[0]
        title = product.title
        call_date = date.today()
        img = product.medium_image_url
        url = product.offer_url

        return price, asin, title, call_date, img, url


def insert_into_table(c,table_name,resp):
    if table_name in ('product_history','product_cache'):
        price, asin, title, call_date, img, url = resp
        query = """INSERT INTO %s
                (product_asin, product_name, date, price, medium_image_url, offer_url)
                VALUES ('%s','%s','%s','%s','%s','%s')""" %(table_name,asin,title,call_date,price,img,url)
    elif table_name in ('purchase_history', 'purchase_cache'):
        query = """INSERT INTO %s
                (emailid,product_asin,purchase_date,starting_price)
                VALUES ('%s','%s','%s','%s')""" %(table_name,resp.email,resp.asin,resp.purchase_date,resp.purchase_price)

    c.execute(query)
    return


def send_mail(SUBJECT, BODY, TO, FROM):
    """Send out html email"""

    MESSAGE = MIMEMultipart('alternative')
    MESSAGE['subject'] = SUBJECT
    MESSAGE['To'] = TO
    MESSAGE['From'] = FROM
    MESSAGE.preamble = """
    Your mail reader does not support the report format.
    Please visit us <a href="http://www.meowbucks.com">online</a>!"""
    HTML_BODY = MIMEText(BODY, 'html')
    MESSAGE.attach(HTML_BODY)

    server = smtplib.SMTP('mail.hover.com:587')

    if __name__ == "__main__":
        server.set_debuglevel(1)

    password = "Elsasaysmeow"

    server.starttls()
    server.login(FROM,password)
    server.sendmail(FROM, TO.split(','), MESSAGE.as_string())
    server.quit()



if __name__ == '__main__':
    print "Resetting ./mb_databases/mb_test_db.db"
    reset_db('./mb_databases/mb_test_db.db')

