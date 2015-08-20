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
 
    server = smtplib.SMTP('smtp.gmail.com:587')
 
    if __name__ == "__main__":
        server.set_debuglevel(1)
 
    password = "mbpowercat"
 
    server.starttls()
    server.login(FROM,password)
    server.sendmail(FROM, [TO], MESSAGE.as_string())
    server.quit()
 
if __name__ == "__main__": 
    email_content = """
<html>
  <!-- Top menu -->
  <table style="margin-top:15px" width="610" cellpadding="0" cellspacing="3">
    <tbody>
      <tr>
        <td valign="bottom" align="left" style="color:#999999;font-family:Arial,Helvetica,sans-serif;font-size:11px;text-decoration:none">Meowbucks Price Drop Message
        </td>
        <td valign="bottom" align="right" style="color:#999999;font-family:Arial,Helvetica,sans-serif;font-size:11px;text-decoration:none">
        <a href="http://www.meowbucks.com" style="text-align:center;color:#999999;font-family:Arial,Helvetica,sans-serif;font-size:11px" target="_blank">View on our site</a>
        </td>
      </tr>
    </tbody>
  </table>

  <!-- Title and logo -->
  <table width="610" cellpadding="0" cellspacing="10px" style="background-color:#fff">
    <tbody>
      <tr width="590">
        <td colspan="3" align="center" valign="middle">
          <table cellpadding="0" cellspacing="0">
            <tbody>
              <tr>
                <td valign="middle">
                  <h1>Meowbucks</h1>
                </td>
              </tr>
            </tbody>
          </table>
        </td>
      </tr>

  <!-- Items with price drop -->
  <tr width="590">
    <td>
      <table cellpadding="0" cellspacing="20px" style="line-height:0">
        <tbody>


          <tr>
            <td valign="top">
              <a href="http://www.amazon.com" style="color:#333333;text-decoration:none" target="_blank">
              <img width="160" height="120" style="margin-bottom:0px;line-height:0" alt="" src="" class="CToWUd">
              </a>
            </td>
            <td valign="top" style="padding-left:20px;font-family:Arial,sans-serif;font-size:12px;color:#333333">
              <table cellspacing="20px">
                <tbody>
                  <tr><td><h3>Name of the Amazon Item</h3></td></tr>
                  <tr><td><b>Original Price:</b> $100</td></tr>
                  <tr><td><b>Current Price:</b> $50</td></tr>
                </tbody>
              </table>
            </td>
          </tr>

          <tr>
            <td valign="top">
              <a href="http://www.amazon.com" style="color:#333333;text-decoration:none" target="_blank">
              <img width="160" height="120" style="margin-bottom:0px;line-height:0" alt="" src="" class="CToWUd">
              </a>
            </td>
            <td valign="top" style="padding-left:20px;font-family:Arial,sans-serif;font-size:12px;color:#333333">
              <table cellspacing="20px">
                <tbody>
                  <tr><td><h3>Name of the Amazon Item</h3></td></tr>
                  <tr><td><b>Original Price:</b> $100</td></tr>
                  <tr><td><b>Current Price:</b> $50</td></tr>
                </tbody>
              </table>
            </td>
          </tr>
        

        </tbody>
      </table>
    </td>
  </tr>      

  <!-- Footer and disclaimer -->
  <table width="610" cellpadding="0" cellspacing="0">
    <tbody>
      <tr>
        <td align="center" valign="top"><span>
          <p style="text-align:center;font-size:11px;font-family:Arial,sans-serif">
            Don't miss out on latest Amazon price drops! Make sure to add <a href="mailto:meowbucks.sherry@gmail.com" target="_blank">meowbucks.sherry@gmail.com</a> to your <br> address book to ensure that you receive our emails.
          </p></span>
          <p style="text-align:center;font-size:11px;font-family:Arial,sans-serif;color:#ababab">
            This email was sent to <a href="mailto:meowbucks.sherry%40gmail.com" target="_blank">meowbucks.sherry@gmail.com</a>.<span><br> You received this message because you have recently visited Meowbucks.com.<br> If you would like to manage your email preferences, please <a href="http://www.meowbucks.com" style="color:#333333" target="_blank">click here</a>.
          </span></p>
          <span>
          <p style="text-align:center;font-size:11px;font-family:Arial,sans-serif;color:#ababab">2015 <a href="http://www.meowbucks.com" style="color:#333333" target="_blank">Meowbucks.com</a> All Rights Reserved.</p>
          <p style="font-size:10px;font-family:Verdana,Arial,Helvetica,sans-serif;line-height:150%;color:#666666;margin:8px 0;padding:0">
          </p>
          </span>
        </td>
      </tr>
    </tbody>
  </table>

</html>
    """
 
    TO = 'sherry415@gmail.com; albert.liang@gmail.com; kevin.cheng76@gmail.com'
    FROM ='sherry.meowbucks@gmail.com'
 
    send_mail("Your Amazon Item Reduced in Price!", email_content, TO, FROM)
