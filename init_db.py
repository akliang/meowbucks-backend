
import sqlite3


def start(dbpath):
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


if __name__ == '__main__':
  start()

