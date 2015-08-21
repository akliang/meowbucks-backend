
import mbcommon as mbc

if __name__ == "__main__": 
    f = open('pricedrop_template.html','r')
    email_content = f.read()
    f.close()
 
    #TO = "sonic_down@yahoo.com ; albert.liang@gmail.com, sherry415@gmail.com, kevin.cheng76@gmail.com"
    TO = 'sonic_down@yahoo.com, albert.liang@gmail.com'
    FROM ='hello@meowbucks.com'
 
    mbc.send_mail("Your Amazon Item Reduced in Price!", email_content, TO, FROM)
