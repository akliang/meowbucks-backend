
import sqlite3


def start():
  # connect to sql database
  #mb_database = sqlite3.connect('/Users/Sherry/meowbucks/mb_databases/meow1.sqlite')
  conn = sqlite3.connect('./meow1.sqlite')
  c = conn.cursor()
  
  # Uncomment below section if want to create tables purchases_tracking and product_info from scratch
  #c.execute('DELETE FROM user_info;')
  #c.execute('DELETE FROM purchase_tracking;')
  #c.execute('DELETE FROM purchase_archives;')
  #c.execute('DELETE FROM product_info;')
  #c.execute('DELETE FROM product_history;')
  c.execute('DROP TABLE IF EXISTS user_info')
  c.execute('DROP TABLE IF EXISTS purchase_tracking')
  c.execute('DROP TABLE IF EXISTS purchase_archives')
  c.execute('DROP TABLE IF EXISTS product_info')
  c.execute('DROP TABLE IF EXISTS product_history')
  
  
  c.execute('create table user_info(id integer primary key, email text, name text, password text);')
  c.execute('create table purchase_tracking(id integer primary key, emailid integer, product_asin text, product_name text, purchase_date integer, starting_price real);')
  c.execute('create table purchase_archives as select * from purchase_tracking where 0;')
  c.execute('create table product_info(id integer primary key, product_asin text, product_name text, date integer, price real, medium_image_url text, offer_url text);')
  c.execute('create table product_history as select * from product_info where 0;')
  
  
  
  c.execute('INSERT INTO user_info VALUES(1,"asdf@asdf.com","asdf","asdf")')
  c.execute("INSERT INTO purchase_tracking VALUES ('1', 'swagberry@meowbucks.com', 'B00QJDU3KY', 'Kindle', '3', '100')")
  c.execute("INSERT INTO purchase_tracking VALUES ('2', 'swagberry@meowbucks.com', 'B00JP7R8X6', 'Kindle Cover', '2', '10')")
  conn.commit()
  conn.close()


if __name__ == '__main__':
  start()

