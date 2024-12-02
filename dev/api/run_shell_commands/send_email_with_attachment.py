#!/home/bgroves@BUSCHE-CNC.COM/anaconda3/envs/etl/bin/python
# https://medium.com/@neonforge/how-to-send-emails-with-attachments-with-python-by-using-microsoft-outlook-or-office365-smtp-b20405c9e63a
# https://realpython.com/python-send-email/
# https://medium.com/mlearning-ai/use-python-to-send-outlook-emails-d673ce9e33e4
import smtplib
import base64

filename = "/tmp/test.txt"

# Read a file and encode it into base64 format
fo = open(filename, "rb")
filecontent = fo.read()
encodedcontent = base64.b64encode(filecontent)  # base64

sender = 'mcp@buschegroup.com'
reciever = 'bgroves@buschegroup.com'

marker = "AUNIQUEMARKER"

body ="""
This is a test email to send an attachement.
"""
# Define the main headers.
part1 = """From: Mobex Computing Platform <mcp@buschegroup.com>
To: Brent Groves <bgroves@buschegroup.com>
Subject: Sending Attachement
MIME-Version: 1.0
Content-Type: multipart/mixed; boundary=%s
--%s
""" % (marker, marker)

# Define the message action
part2 = """Content-Type: text/plain
Content-Transfer-Encoding:8bit

%s
--%s
""" % (body,marker)

# Define the attachment section
part3 = """Content-Type: multipart/mixed; name=\"%s\"
Content-Transfer-Encoding:base64
Content-Disposition: attachment; filename=%s

%s
--%s--
""" %(filename, filename, encodedcontent, marker)
message = part1 + part2 + part3

try:
   smtpObj = smtplib.SMTP('mobexglobal-com.mail.protection.outlook.com')
   smtpObj.sendmail(sender, reciever, message)
   print("Successfully sent email")
except Exception:
   print("Error: unable to send email")


#!/miniconda/bin/python
#!/usr/bin/python
# https://www.tutorialspoint.com/python/python_sending_email.htm
# https://www.tutorialspoint.com/python/python_sending_email.htm
# https://www.ionos.com/digitalguide/e-mail/technical-matters/smtp/
import smtplib

sender = 'mcp@mobexglobal.com'
receivers = ['bgroves@buschegroup.com']

message = """From: Mobex Computing Platform <mcp@mobexglobal.com>
To: Brent Groves <bgroves@buschegroup.com>
Subject: SMTP e-mail test

This is a test e-mail message.
"""

try:
   smtpObj = smtplib.SMTP('mobexglobal-com.mail.protection.outlook.com')
   smtpObj.sendmail(sender, receivers, message)         
   print("Successfully sent email")
except Exception:
   print("Error: unable to send email")