#!/usr/bin/python

import cgi, cgitb
cgitb.enable()
import os

#Create instance for fieldStorage.
form= cgi.FieldStorage()
html=[]

print ("Content-type:text/html\r\n\r\n")
print('<!DOCTYPE html>')
print('<html lang="en">')
print('<head>')
print('<meta charset="utf-8">')
print('<meta content="width=device-width, initial-scale=1.0" name="viewport">')
print('<title>NOD-New use of Old Drugs</title>')
print('<meta content="" name="description">')
print('<meta content="" name="keywords">')
#	<!-- Favicons -->
print('<link href="assets/img/DrugRepurp.png" rel="icon">')
print('<link href="assets/img/DrugRepurp.png" rel="DrugRepurp.png">')
#	<!-- Google Fonts -->
print('<link href="https://fonts.googleapis.com/css?family=Open+Sans:300,300i,400,400i,600,600i,700,700i|Jost:300,300i,400,400i,500,500i,600,600i,700,700i|Poppins:300,300i,400,400i,500,500i,600,600i,700,700i" rel="stylesheet">')

#	<!-- Vendor CSS Files -->
print('<link href="assets/vendor/bootstrap/css/bootstrap.min.css" rel="stylesheet">')
print('<link href="assets/vendor/icofont/icofont.min.css" rel="stylesheet">')
print('<link href="assets/vendor/boxicons/css/boxicons.min.css" rel="stylesheet">')
print('<link href="assets/vendor/remixicon/remixicon.css" rel="stylesheet">')
print('<link href="assets/vendor/venobox/venobox.css" rel="stylesheet">')
print('<link href="assets/vendor/owl.carousel/assets/owl.carousel.min.css" rel="stylesheet">')
print('<link href="assets/vendor/aos/aos.css" rel="stylesheet">')

#	<!--  Main CSS File -->
print('<link href="assets/css/style.css" rel="stylesheet">')
print('</head>')

print('<body>')
# <!-- ======= Header ======= -->
print('<header id="header" class="fixed-top ">')
print('<div class="container d-flex align-items-center">')
print('<h1 class="logo mr-auto"><a href="index.html">WS-NOD</a></h1>')
print('<nav class="nav-menu d-none d-lg-block">')
print('<ul>')
print('<li class="active"><a href="index.html">Home</a></li>')
print('<li><a href="index.html#about">About-NOD</a></li>')
print('<li><a href="index.html#instructions">Instructions</a></li>')
print('<li class="drop-down"><a href="index.html#runOps">Run-Options</a>')
print('<ul>')
print('<li class="drop-down"><a href="index.html#mode-1">MODE-1</a>')
print('<ul>')
print('<li><a href="index.html#mode-1">Custom Dataset</a></li>')
print('<li><a href="index.html#modelOrg">Model Organisms</a></li>')
print('<ul>')
print('<li>')
print('<li><a href="index.html#mode-2">MODE-2</a></li>')
print('<li><a href="index.html#mode-2">Play Around</a></li>')
print('<ul>')
print('<li>')
print('<li><a href="index.html#modelOrg">Model Organisms</a></li>')
print('<li><a href="index.html#team">The Team</a></li>')
print('<li><a href="index.html#contact">Contact</a></li>')
print('</ul>')
print('</nav>')
print('<a href="index.html" class="get-started-btn scrollto">Start Over</a>')
print('</div>')
print('</header>')
# <-- End Header -->
print('<section id="hero" class="d-flex align-items-center">')
#in_title=form['textinput'] #Use this id for results directory.
#print (form.getvalue('textinput'),form.getvalue('sequence'))
jobId= form.getvalue('title')
sequence= form.getvalue('sequence')
checked= form.getvalue('declare')


if jobId:
	print('<div class="d-flex">')
	print('<textarea class="form-control" id="sequence" name="sequence" rows="6" value="file">%s</textarea></div>' %sequence)
else:
	print ('<div class="container=-fluid" value="error">Job Title is mandatory. It will be the identity of your job in our servers/n</div>')

if checked:
	print (jobId)
	sequence.split(">")
#	print("os.system\"echo -e %s >> %s.FASTA\" (sequence,jobId))")
#	os.system("python /prod/www/NOD_v1_2/bin/master_handler.py mode1 %s"%in_file)

infile= form['uploadBtn']	#Get data from the upload file option.

if infile.file:
	lc=0
	while True:
		line= infile.file.readline()
		if not line: break
		lc= lc+1

		msg= "The file"+ lc +"was uploaded successfully"
else:
	msg= "\nNo file was uploaded\n"

print('<div class="col-md-4">')
print('<textarea class="form-control" id="sequence" name="sequence" rows="6" value="file">%s</textarea></div>' %msg)

print('</section>'
#<!-- End Hero -->
