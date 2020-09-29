#!/usr/bin/python
#	@uthor: TjrNarwani on Fri 31/07/2020

import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
#from email.mime.base import MIMEBase
#from email import encoders

mode= sys.argv[1]
resDir=sys.argv[2]
jobId=sys.argv[3]
jobTitle=sys.argv[4]
email=sys.argv[5]

print("Arguments entered:\nMode:%s,\nresDir:%s,\njobId:%s,\njobTitle:%s,\nemail:%s\n" %(mode,resDir,jobId,jobTitle,email))
# COMPOSE EMAIL TO USER using MIME setup.

#mail_content="Dear User\n\nYour Job Titled: %s has finished on NOD server.\nPlease click the following link to see the response.\n\thttp://pauling.mbu.iisc.ac.in/NOD/%s/%s.html\n\n\n -Thank you for using NOD. Have a good day.\n-Team NOD\n" %(jobId,resDir,jobId)
mail_content="Dear User\n\nYour Job Titled: %s has finished on NOD server.\nPlease click the following link to see the response.\n\thttp://pauling.mbu.iisc.ac.in/nod_de/%s/%s.html\n\n\n -Thank you for using NOD. Have a good day.\n-Team NOD\n" %(jobTitle,resDir,jobId)
#TODO: Put an email body footer with DISCLAIMER.
msg=MIMEMultipart()
msg['Subject']=("Response for your Job Title: %s submitted in %s on NOD webserver" %(jobTitle, mode))
msg['From']='nod.server.pushemail@gmail.com'
msg['To']=email
msg.attach(MIMEText(mail_content,'plain'))

# SEND THE EMAIL.
session= smtplib.SMTP('smtp.gmail.com',587)
# "server started with enabled security TLS"
session.starttls()
#Login to server
session.login('nod.server.pushemail@gmail.com','N0D_S3rv3R')
#"Writing message"
text=msg.as_string()
session.sendmail('nod.server.pushemail@gmail.com',email,text)
#"sent mail"
session.quit()
#print ("Email Sent to: %s with Title: %s in Directory:%s" %(email,jobId,resDir))