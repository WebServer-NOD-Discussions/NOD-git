#!/usr/bin/python
#	@uthor: TjrNarwani on Fri 13/08/2020

import cgi, cgitb
cgitb.enable()
import os

import random as rand
import subprocess
import time
#Create instance for fieldStorage.
form= cgi.FieldStorage()
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
            <li class="active"><a href="webpages/run.html">Run-Options</a></li>
            <li><a href="webpages/archives.html">Arch-NOD</a></li>
			<li><a href="webpages/faq.html">F.A.Q</a></li>
            <li><a href="webpages/team.html">The Team</a></li>
            <li><a href="webpages/contact.html">Contact</a></li>
  
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
			<h2><i>To submit new queries:</i><a href="webpages/run.html" class="btn-special">START OVER</a></h2>
            <p style="font-size:16px; color: #913A1E"> <br><br><b><u>NOTE:</b></u> <i>The results for your job will be stored on NOD server for <u><b>10 more days</b></u> after you have received the email.
            All result files will be automatically deleted after that. We recommend users to download and store the result files in their local system as soon as the email is received.</>
        </div>
        </div>
        
		<div class="grid-child" class="img-fluid animated">
		<img src="img/NOD_img2.png" class="logo" alt="waiting for image to load..." height="500" width="500">
        </div>
</section>	<!-- End welcome Section -->
""" %(head1,head2)
	return(string)
		#Obtaining values from input form.
jobTitle= form.getvalue('title')
email= form.getvalue('toaddr')
sequence= form.getvalue('sequence')
infile= form['uploadBtn']	#Get data from the upload file option.
checked= form.getvalue('declare')
qCov= form.getvalue('sliderVal') # Extracting the raw slider value.
#qCov=sliderValue[1] #Since Mode-1 has range 40 to 100, a list is passed instead of single integer.

jobId=jobTitle.replace(" ","") # to remove all spaces from user input JobId. Comment this if form validation for no space and underscore are in place.
jobTitle=jobId
upld_path="/prod/www/nslab/NOD/"
resDir= "Results/" + ("%s_results_%s" %(jobId,round(rand.random(),3)))
upld_dir= upld_path + resDir
os.system('mkdir -p %s' %(upld_dir)) #Making directory with userspecific JobId+RandomNumber.
#Reading the input file and storing it in user directory.    
fn = os.path.basename(infile.filename) # strip leading path from file name
#Reading contents of fasta file and validating that a single sequence is passed to the server.
open(upld_dir+"/qFile.fasta", 'wb').write(infile.file.read()) #reading and writing the contents of input file in qFile.fasta
inputSeqNo= len([1 for line in open("%s/qFile.fasta" %upld_dir) if line.startswith(">")])

if inputSeqNo > 5000:
    msg1="<b>WARNING</b>: <i>The uploaded file contains more than 5000 sequences.</i>"
    msg2="""
    Mode-1 is computationally demanding as it treats each uploaded protein sequence individually, therefore it may take 36 - 48 hours to compile your results. <br>
    If you wish to generate faster results, we recommend that you split the large number of sequences into smaller parts and try again.<br>
    An email containing <i><u>\"%s\"</i></u> in the subject<br>will be sent to <i><u>%s</u></i>.<br><br>
    """ %(jobId,email)
    html_pg= html_pg+heroSec(msg1,msg2)
    #Setup Conda local environment for using rdkit and JackHmmer. Calling main python script from bash wrapper.
    #print('%s/bin/envSetup.sh mode1 %s/qFile.fasta %s/ %s %s %s %s &> %s/shOut.log &' %(upld_path,upld_dir,upld_dir,jobId,jobTitle,email,resDir,upld_dir))
    os.system('%s/bin/envSetup.sh mode1 %s/qFile.fasta %s/ %s \"%s\" %s %s %s &> %s/shOut.log &' %(upld_path,upld_dir,upld_dir,jobId,jobTitle,email,resDir,qCov,upld_dir))
else:
    msg1="<i>Your Results are being compiled...</i>"
#   msg2="It may take some time to find the approved drugs against your protein sequence.<br><br> An email containing <i><u>\"%s\"</i></u> in the subject<br>will be sent to <i><u>%s</u></i>.<br><br>Start Over to submit new queries." %(jobId,email)
    msg2="""It may take some time to run your submitted job.<br><br>
    An e-mail with the given job title: <b><u>%s</u></b> in the subject will be sent to: <b><u>%s</u></b> <br>
    from: <b><u>nod.server.pushemail@gmail.com</u></b>.<br><br>
    """%(jobTitle,email)
    html_pg= html_pg+heroSec(msg1,msg2)
#Setup Conda local environment for using rdkit and JackHmmer. Calling main python script from bash wrapper.
    #print('%s/bin/envSetup.sh mode1 %s/qFile.fasta %s/ %s %s %s %s &> %s/shOut.log &' %(upld_path,upld_dir,upld_dir,jobId,jobTitle,email,resDir,upld_dir))
    os.system('%s/bin/envSetup.sh mode1 %s/qFile.fasta %s/ %s \"%s\" %s %s %s &> %s/shOut.log &' %(upld_path,upld_dir,upld_dir,jobId,jobTitle,email,resDir,qCov,upld_dir))

"""        else:
        msg1="MANDATORY: A valid email address"
        msg2= "Sorry! I could not find a valid email address?<br><br><i>I do have your results, but now I don't know where to send them.</i>"
        html_pg= html_pg+heroSec(msg1,msg2)
else:
	msg1="MANDATORY ENTRY MISSING: Job Title."
	msg2="Sorry! you have not entered a valid Job Title. Please respect the rules mentioned in the help."
	html_pg= html_pg+heroSec(msg1,msg2)
"""            

html_pg=html_pg+ """
  <!-- ======= Footer ======= -->
  <footer id="footer">
    <div class="container footer-bottom clearfix">
		<div class="copyright">
      <p>If you find NOD useful for your work:<br> Please cite:
(Manuscript under preparation...)</p>
		</div>
      <div class="credits">
      <p>Designed by <a href="https://www.linkedin.com/in/tarun-jairaj-narwani-92447928/"><strong>Tarun Jairaj Narwani</strong></a><br>
	  &copy; Copyright <a href="http://pauling.mbu.iisc.ac.in/"><strong><span>NSlab-MBU</span></strong></a>. All Rights Reserved</p>
      </div>
    </div>
  </footer><!-- End Footer -->
<!--  Main JS File --
		<script src="assets/js/main.js"></script>
		</body>
	</html>
"""
print (html_pg)
