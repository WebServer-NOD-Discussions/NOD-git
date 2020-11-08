#!/usr/bin/python
import cgi, cgitb
cgitb.enable()

import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# Create instance of FieldStorage 
logger=open("contactMailer.log",'w')
form= cgi.FieldStorage()
#Writing HTML File
print("Content-type:text/html\r\n\r\n")
html_pg= """
<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="utf-8">
  <meta content="width=device-width, initial-scale=1.0" name="viewport">

  <title>NOD-New use of Old Drugs</title>
  <meta content="" name="description">
  <meta content="" name="keywords">

  <!-- Favicons -->
  <link href="img/NOD_img2.png" rel="icon">


  <!-- Google Fonts -->
  <!--  Main CSS File -->
  <link href="css/style.css" rel="stylesheet">

  <!-- =======================================================
  *Name: WS-NOD - v 1.2.0
  *Author: Tarun Jairaj Narwani
  *License: Creative Commons
  ======================================================== -->
</head>

<body>
<header>
    <div id="header" class="container">
        <div>
        <h1 class="logo"><a href="index.html"><img src="img/icons/NOD_logo.png" height="60px" width="180px"></a></h1>
        </div>
        <div>
        <nav>
          <ul>
            <li><a href="index.html">Home</a></li>
            <li><a href="webpages/about.html">About-NOD</a></li>
            <li><a href="webpages/instructions.html">Instructions</a></li>
            <li><a href="webpages/run.html">Run-Options</a></li>
            <li><a href="archives.html">Arch-NOD</a></li>
            <li><a href="webpages/faq.html">F.A.Q</a></li>
            <li><a href="webpages/team.html">The Team</a></li>
            <li class="active"><a href="webpages/contact.html">Contact</a></li>
  
          </ul>
</nav><!-- .nav-menu -->
        </div>
      </div>
</header>
"""
def heroSec(head1,head2):
# <!-- ======= Hero Section ======= -->
        string="""
        <div id="noheader" class="noheader section-bg">
    <section id="about" class="grid-2">
                <div class="grid-child" data-aos="fade-up">
                        <h2>%s</h2>
                <div class="container"> 
            <p style="font-size:20px; color:#283A5A"><b>%s</b></p>
            <p style="font-size:16px; color: #913A1E"> <br><br><b><u>DISCLAIMER:</b></u> <i>TEAM NOD strongly discourages the practice of self-medication. Therefore, any concern relating to usage or dosage of drugs found in NOD results, will not be entertained.
        </div>
        </div>
        
                <div class="grid-child" class="img-fluid animated">
                <img src="img/NOD_img2.png" class="logo" alt="waiting for image to load..." height="500" width="500">
        </div>
</section>      <!-- End welcome Section -->
""" %(head1,head2)
	return(string)
# Reading elements from contact form and compiling it for email.
userName= form.getvalue('userName')
email= form.getvalue('toaddr')
sendEml= 'tjrnarwani@gmail.com'
sbjct= form.getvalue('subject')
msg= form.getvalue('message')

logger.write("Arguments entered:\nUser Name:%s,\nThe email:%s,\nSubject:%s,\n Feedback Message:%s\n" %(userName,email,sbjct,msg))

# COMPOSE EMAIL TO USER using MIME setup.
mail_content="----FWD  content----\n\tHey NOD admin,\n\tA user named: %s\n\tusing an email id: %s\n\thas raised a concern.\n\tThe subject is: \"%s\" and the concern reads as follows:\n\t|--\"%s\"\n" %(userName,email,sbjct,msg)
#TODO: Put an email body footer with DISCLAIMER.
msg=MIMEMultipart()
msg['Subject']=("fwd: NOD-contact: %s" %(sbjct))
msg['From']='nod.server.pushemail@gmail.com'
msg['To']='tjrnarwani@gmail.com'
msg.attach(MIMEText(mail_content,'plain'))

# SEND THE EMAIL.
session= smtplib.SMTP('smtp.gmail.com',587)
# "server started with enabled security TLS"
session.starttls()
#Login to server
session.login('nod.server.pushemail@gmail.com','N0D_S3rv3R')
#"Writing message"
text=msg.as_string()
session.sendmail('nod.server.pushemail@gmail.com',sendEml,text)
#"sent mail"
session.quit()
msg1="Thank you %s..!!" %userName
msg2="<i>Your concern/feedback is welcomed at NOD.<br> A NOD admin will get back to you at <u>%s</u> within 24 hours.</i>\n" %email
html_pg=html_pg+heroSec(msg1,msg2)
print(html_pg)
logger.write("Sent an Email")
