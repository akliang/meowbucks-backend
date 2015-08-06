''' This python module interacts with the purchase_tracking and product_info tables. 
    1. select unique product_asin from the purchase_tracking table
    2. call amazon API using asin to get product information
    3. populate the product_info page with data returned from the API
'''

from amazon.api import AmazonAPI
import sqlite3
from datetime import date, datetime
import logging

# Create daily log file
logging.basicConfig(filename='/Users/Sherry/meowbucks/log_files/apicall_log_%s.log' %(datetime.now().strftime("%Y_%m_%d_%H_%M")),
                    level=logging.DEBUG)


# Get a list of asins to send to api
def get_asin_list(c):
    asin_list = []

    for row in c.execute('SELECT product_asin FROM purchase_tracking'):
        row = row[0].encode('utf-8')
        asin_list.append(row)

    return asin_list


# Call amazon api
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


# Updated table using data returned from api
def update_product_table(c, asin, title, call_date, price, img, url):

    query = """INSERT INTO product_info 
            (product_asin, product_name, date, price, medium_image_url, offer_url) 
            VALUES ('%s','%s','%s','%s','%s','%s')""" %(asin,title,call_date,price,img,url)
    c.execute(query)


def main():

    # Connect to sql database
    mb_database = sqlite3.connect('/Users/Sherry/meowbucks/mb_databases/mb_test_db.db')
    c = mb_database.cursor()

    # Uncomment below section if want to create tables purchase_tracking and product_info from scratch
    c.execute('''DROP TABLE IF EXISTS purchase_tracking''')
    c.execute('''DROP TABLE IF EXISTS purchases_tracking''')
    c.execute('''DROP TABLE IF EXISTS product_info''')

    c.execute('''CREATE TABLE purchase_tracking
                 (date tid integer primary key, emailid integer, product_asin text, product_name text, purchase_date integer, starting_price real)''')
    c.execute("INSERT INTO purchase_tracking VALUES ('1', 'swagberry@meowbucks.com', 'B00QJDU3KY', 'Kindle', '3', '100')")
    c.execute("INSERT INTO purchase_tracking VALUES ('2', 'swagberry@meowbucks.com', 'B00JP7R8X6', 'Kindle Cover', '2', '10')")

    c.execute('''CREATE TABLE product_info
                 (product_asin text, product_name text, date integer, price real, medium_image_url text, offer_url text, PRIMARY KEY (product_asin, date)
    )''')

    # Get a list of asins from purchase_tracking table
    asin_list = get_asin_list(c)
    successfully_updated= 0

    # Call api and update table
    if len(asin_list) > 0:
        for asin in asin_list:

            resp = call_API(asin)
            if resp:
                price, asin, title, call_date, img, url = resp
                update_product_table(c, asin, title, call_date, price, img, url)
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