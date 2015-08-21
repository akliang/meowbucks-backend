import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
 
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
 
    #server = smtplib.SMTP('smtp.gmail.com:587')
    server = smtplib.SMTP('mail.hover.com:587')
 
    if __name__ == "__main__":
        server.set_debuglevel(1)
 
    #password = "mbpowercat"
    password = "Elsasaysmeow"
 
    server.starttls()
    server.login(FROM,password)
    server.sendmail(FROM, TO2, MESSAGE.as_string())
    server.quit()
 
if __name__ == "__main__": 
    f = open('pricedrop_template.html','r')
    email_content = f.read()
    f.close()
 
    #TO = 'sherry415@gmail.com; albert.liang@gmail.com; kevin.cheng76@gmail.com'
    TO = "sonic_down@yahoo.com ; albert.liang@gmail.com, sherry415@gmail.com, kevin.cheng76@gmail.com"
    TO2 = ['sonic_down@yahoo.com', 'albert.liang@gmail.com','sherry415@gmail.com','kevin.cheng76@gmail.com']
    #FROM ='sherry.meowbucks@gmail.com'
    FROM ='hello@meowbucks.com'
 
    send_mail("Your Amazon Item Reduced in Price!", email_content, TO, FROM)
