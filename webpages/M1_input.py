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
# <!-- ======= Hero Section ======= -->
print('<section id="hero" class="d-flex align-items-center">')
#in_title=form['textinput'] #Use this id for results directory.
in_item= form["uploadBtn"]	#Get data from text input- Mode-1
print (form.getvalue('textinput'),form.getvalue('sequence'))
print (in_item)
os.system("python3 ../WS-NOD_vm/bin/master_handler.py mode1 %s"%in_item)
print('</section>')
#<!-- End Hero -->
