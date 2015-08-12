
import sqlite3


def reset_db(dbpath):
    # connect to sql database
    conn = sqlite3.connect(dbpath)
    c = conn.cursor()
    
    # Uncomment below section if want to create tables purchases_tracking and product_info from scratch
    c.execute('DROP TABLE IF EXISTS user_info')
    c.execute('DROP TABLE IF EXISTS purchase_history')
    c.execute('DROP TABLE IF EXISTS purchase_cache')
    c.execute('DROP TABLE IF EXISTS product_history')
    c.execute('DROP TABLE IF EXISTS product_cache')
    
    
    c.execute('create table user_info(id integer primary key, email text, name text, password text);')
    c.execute('create table purchase_history(id integer primary key, emailid integer, product_asin text, product_name text, purchase_date integer, starting_price real);')
    c.execute('create table purchase_cache as select * from purchase_history where 0;')
    c.execute('create table product_history(id integer primary key, product_asin text, product_name text, date integer, price real, medium_image_url text, offer_url text);')
    c.execute('create table product_cache as select * from product_history where 0;')
    
    
    
    c.execute('INSERT INTO user_info VALUES(1,"asdf@asdf.com","asdf","asdf")')
    c.execute("INSERT INTO purchase_history VALUES ('1', 'swagberry@meowbucks.com', 'B00QJDU3KY', 'Kindle', '1438894338', '100')")
    c.execute("INSERT INTO purchase_history VALUES ('2', 'swagberry@meowbucks.com', 'B00JP7R8X6', 'Kindle Cover', '1438894038', '10')")
    c.execute("INSERT INTO purchase_history VALUES ('3', 'jojo@meowbucks.com', 'B00JP7R8X6', 'Kindle Cover', '1438892338', '10')")
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
        query = """INSERT INTO product_cache
                (product_asin, product_name, date, price, medium_image_url, offer_url)
                VALUES ('%s','%s','%s','%s','%s','%s')""" %(asin,title,call_date,price,img,url)
    #elseif table_name in ('purchase_history', 'purchase_cache'):

    c.execute(query)
    return




