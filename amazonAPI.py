from amazon.api import AmazonAPI
import sqlite3
from datetime import date

# get prices for a list of product asins
items = []

#connect to sql database
mb_database = sqlite3.connect('/Users/Sherry/meowbucks/mb_databases/mb_test_db.db')
c = mb_database.cursor()

# Uncomment below section if want to create tables purchases_tracking and product_info from scratch
# c.execute('''DROP TABLE purchases_tracking''')
# c.execute('''DROP TABLE product_info''')

# c.execute('''CREATE TABLE purchases_tracking
#              (date tid integer primary key, emailid integer, product_asin text, product_name text, purchase_date integer, starting_price real)''')
# c.execute("INSERT INTO purchases_tracking VALUES ('1', 'swagberry@meowbucks.com', 'B00QJDU3KY', 'Kindle', '3', '100')")
# c.execute("INSERT INTO purchases_tracking VALUES ('2', 'swagberry@meowbucks.com', 'B00JP7R8X6', 'Kindle Cover', '2', '10')")

# c.execute('''CREATE TABLE product_info
#              (product_asin text, product_name text, date integer, price real, medium_image_url text, offer_url text, PRIMARY KEY (product_asin, date)
# )''')


for row in c.execute('SELECT product_asin FROM purchases_tracking'):
	row = row[0].encode('utf-8')
	items.append(row)


# call Amazon API
AMAZON_ACCESS_KEY = 'AKIAJ2MUVQ36XFWLYUEA'
AMAZON_SECRET_KEY = '***REMOVED***z'
AMAZON_ASSOC_TAG = 'meowbucks-20'

amazon = AmazonAPI(AMAZON_ACCESS_KEY, AMAZON_SECRET_KEY, AMAZON_ASSOC_TAG)

for item in items:
	product = amazon.lookup(ItemId = item)
	# resulting fields
	price = product.price_and_currency[0]
	asin = product.asin
	title = product.title
	call_date = date.today()
	img = product.medium_image_url
	url = product.offer_url

	# print price
	# print asin
	# print title
	# print call_date
	# print img
	# print url

 	query = "INSERT INTO product_info (product_asin, product_name, date, price, medium_image_url, offer_url) VALUES ('%s','%s','%s','%s','%s','%s')" %(asin,title,call_date,price,img,url)
 	c.execute(query)

mb_database.commit()
mb_database.close()