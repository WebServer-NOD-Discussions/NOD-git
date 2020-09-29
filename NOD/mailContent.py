#!/usr/bin/python
#	@uthor: TjrNarwani on Fri 15/08/2020

import cgi, cgitb
cgitb.enable()
import os
import pandas

import smtplib
import sys

# <!--Email Content Definition Section-->
mode=sys.argv[1]
resDir=sys.argv[2]
tblDir=sys.argv[3]
jobId= sys.argv[4]
print("Arguments Enterd:\nmode:%s,\nresDir:%s,\ntblDir:%s,\njobId:%s\n" %(mode,resDir,tblDir,jobId))
print("Content-type:text/html\r\n\r\n")
html_pg="""
<!DOCTYPE html>
	<html lang="en">
		<head>
	<meta charset="utf-8">
	<meta content="width=device-width, initial-scale=1.0" name="viewport">
<!--TABLE STYLING-->
<style>
table {
  border-spacing:5px;
  width: 100%;
  padding: 5px;
  border-collapse: collapse;
}

th, td {
  padding: 10px;
  text-align:center;
  border-bottom: 1px solid #ddd;
  border-collapse: collapse;
}

tr:hover {background-color:#f5f5f5;}
</style>

	<title>NOD-New use of Old Drugs</title>
	<meta content="" name="description">
	<meta content="" name="keywords">

  <!-- Favicons -->
  <link href="../../NOD/img/NOD_img2.png" rel="icon">


  <!-- Google Fonts -->
  <!--  Main CSS File -->
  <link href="../../NOD/css/style.css" rel="stylesheet">

  <!-- =======================================================
  *Name: WS-NOD - v 1.2.0
  *Author: Tarun Jairaj Narwani
  *License: Creative Commons
  ======================================================== -->
</head>

<body>
<!-- ======= Header ======= -->
<header>
    <div id="header" class="container">
        <div>
        <h1 class="logo"><a href="../../NOD/index.html"><img src="../../NOD/img/icons/NOD_logo.png" height="60px" width="180px"></a></h1>
        </div>
        <div>
        <nav>
          <ul>
            <li><a href="../../NOD/index.html">Home</a></li>
            <li><a href="../../NOD/webpages/about.html">About-NOD</a></li>
            <li><a href="../../NOD/webpages/instructions.html">Instructions</a></li>
            <li class="active"><a href="../../NOD/webpages/run.html">Run-Options</a></li>
            <!--<li><a href="../../NOD/webpages/organisms.html">Model Organisms</a></li>-->
			<li><a href="../../NOD/webpages/faq.html">F.A.Q</a></li>
            <li><a href="../../NOD/webpages/team.html">The Team</a></li>
            <li><a href="../../NOD/webpages/contact.html">Contact</a></li>
  
          </ul>
        </nav><!-- .nav-menu -->
        </div>
      </div>
</header>"""
html_pg=html_pg+"""
<!-- ======= Tables Section ======= -->
	<div id="noheader" class="noheader section-bg">
        <div id="results" class="section-title">
        <h2> Results for the Job Title: %s </h2>
        <div style="text-align: center"><p>The following table consists of potent drug candidates against your query proteins.<br><br><i>Any valid drug candidate that has been approved at least once during its lifetime is included.<br>You can find the essential information in the table to make a decision.</i><br></p></div>
		<h5> Instructions to understand the result table organization.</h5>
        </div>
""" %jobId

if '1' in mode:
# Open table output from master_handler script and print each row.
    tbl=pandas.read_csv("%s/%s_matches.tbl" %(tblDir,mode), sep="\t", engine="python")
    tbl.rename(columns={"Unnamed: 0":"No.s"}, inplace=True)

    html_pg= html_pg+ """
    <div class="container">
        <table id="resDisplay" style="border: 1px solid black">
			<thead>
			<tr>
			<th>Number</th>
			<th>Query</th>
            <th>Target homolog</th>
            <th>DrugBank ID</th>
			<th>Molecule Name</th>
			<th>Regulatory Status</th>
			<th>SMILES</tr>
            </tr>
			</thead>
			<tr>
			<td><i> No. of approved drugs hit against the query protein(s)</td></i>
			<td><i> Input query name based on which hits are retreived.</td></i>
            <td><i> The UNIPROT id for target protein sequence that is homologous to the query protein is reported</td></i>
            <td><i> The DrugBank id of the molecule targetting homolog protein sequence. A single protein can be a target of multiple compounds.</td></i>
            <td><i> Name of the molecule as defined in DrugBank.</td></i>
			<td><i> Regulatory status and category of the chemical compound. Drugs that passed the trials and got the approval but had to be discontinued later are also listed.</td></i>
            <td><i> 2-D coordinates for generating the drug molecule. If unavailable, a Nan value is printed. These coordinates can be directly used in standard drug chemistry softwares.</td></i>
			</tr>
		</table>	
	</div>
    <div style="text-align: center"><p><b>NOTE:</b> <i>NOD users are encouraged to use the <a href="#">clickable links</a> provided in the table to access further details about the compound or the protein.</i></b></p></div>
    <div class="container section-fg">
		<a href="%s_matches.tbl" class="btn-special">Download Table</a></tfoot></div>
			<table id="resDisplay">
                <thead>
                <tr>
                    <th>#</th>
                    <th>Query</th>
                    <th>Target Homolog</th>
		<th>Query Coverage</th>
		<th>Alignment From</th>
		<th>Alignment Until</th>
                    <th>DrugBank ID</th>
                    <th>Molecule Name</th>
                    <th>Regulatory Status</th>
                    <th>SMILES</th>
                </thead>
                </tr>
"""

    for row in tbl.index:
        html_pg= html_pg+'<tr>'
        html_pg= html_pg+'<td> %s </td>' %(tbl["No.s"][row]+1)
        html_pg= html_pg+'<td> %s </td>' %tbl["Query"][row]
        html_pg= html_pg+'<td><a href="https://www.uniprot.org/uniprot/%s"> %s </a></td>' %(tbl["Target"][row],tbl["Target"][row])
        html_pg= html_pg+'<td> %s </td>' %tbl["Query-Cov"][row]
        html_pg= html_pg+'<td> %s </td>' %tbl["Align-From"][row]
        html_pg= html_pg+'<td> %s </td>' %tbl["Align-To"][row]
        html_pg= html_pg+'<td><a href="https://www.drugbank.ca/drugs/%s"> %s </a></td>' %(tbl["DrugBank ID"][row],tbl["DrugBank ID"][row])
        html_pg= html_pg+'<td> %s </td>' %tbl["Mol.Name"][row]
        html_pg= html_pg+'<td> %s </td>' %tbl["Reg.Status"][row]
        html_pg= html_pg+'<td style="word-wrap:break-word;"> %s </td>' %tbl["SMILES"][row]
        html_pg= html_pg+'</tr>'
    html_pg= html_pg+'</table>'
    html_pg= html_pg+'<tfoot style="align: right"><a href="%s_matches.tbl" class="btn-special">Download Table</a></tfoot></div>' %(mode)

if '2' in mode:
# Open table output from master_handler script and print each row.
    tbl=pandas.read_csv("%s/%s_matches.tbl" %(tblDir,mode), sep="\t", engine="python")
    tbl.rename(columns={"Unnamed: 0":"No.s"}, inplace=True)
    html_pg= html_pg+ """
		<div class="container">
        <table id="resDisplay" style="border: 1px solid black">
			<thead>
            <tr><i>Results for Query protein entered</i></tr>
            <tr>
            <th>Target homolog</th>
            <th>1&deg;Candidate</th>
			<th>Molecule Name</th>
			<th>Regulatory Status</th>
            <th>2&deg;Candidate</th>
			<th>Molecule Name</th>
			<th>Regulatory Status</th>
            <th>Similarity (T<sub>C</sub>)</th>
			</tr>
			</thead>
            <tr>
            <td><i> The UNIPROT id for the target protein sequence that is homologous to the query protein.</td></i>
            <td><i> The DrugBank id for the target homolog protein sequence. The query protein can be a target of multiple drugs in DrugBank.</td></i>
            <td><i> Name of the 1&deg;Candidate (Molecues found while searching in the complete dataset).</td></i>
			<td><i> Regulatory status and category of the 1&deg; Candidate.</td></i>
            <td><i> The DrugBank id for the 2&deg; Candidate that is similar in structure to the 1&deg;Candidate.</td></i>
            <td><i> Name of the 2&deg;Candidate.</td></i>
			<td><i> Regulatory status and category of the 2&deg;Candidate.</td></i>
            <td><i> 2D chemical similarity index, Tanimoto Co-efficient*(T<sub>C</sub>), obtained by comparing 1&deg;Candidate and 2&deg;Candidate is reported.</td></i>
			</tr>
		</table>
            <tfoot><p style="text-align: right">*T<sub>C</sub> ranges from 0 to 1. Values > 0.7 are selected to ensure that highly similar 2&deg;Candidates are reported.<br></tfoot>
	</div>
        <div style="text-align: center"><p><i>NOTE: NOD Users are encouraged to use the <a href="#">clickable links</a> provided in the table to access further details about the compound or the protein.</i></b></p></div>
    <div class="container section-fg">
			<table id="resDisplay">
                <thead>
                <tr><strong>Query protein: %s</strong><br></tr>
                <tr></tr><tr>
                    <th>S.No</th>
                    <th>Target homolog</th>
		<th>Query Coverage</th>
                <th>Alignment From</th>
                <th>Alignment Until</th>
                    <th>1&deg;Candidate</th>
                    <th>Molecule Name (1&deg;)</th>
                    <th>Regulatory Status (1&deg;)</th>
                    <th>2&deg;Candidate</th>
                    <th>Molecule Name (2&deg;)</th>
                    <th>Regulatory Status (2&deg;)</th>
                    <th>Similarity (T<sub>C</sub>)</th>
                </thead>
                </tr>
"""%tbl["Query"][1]

    for row in tbl.index:
        html_pg= html_pg+'<tr>'
        html_pg= html_pg+'<td> %s </td>' %(tbl["No.s"][row]+1)
        #html_pg= html_pg+'<td> %s </td>' %tbl["Query"][row]
        html_pg= html_pg+'<td><a href="https://www.uniprot.org/uniprot/%s"> %s </a></td>' %(tbl["Target"][row],tbl["Target"][row])
        html_pg= html_pg+'<td> %s </td>' %tbl["Query-Cov"][row]
        html_pg= html_pg+'<td> %s </td>' %tbl["Align-From"][row]
        html_pg= html_pg+'<td> %s </td>' %tbl["Align-To"][row]
        html_pg= html_pg+'<td><a href="https://www.drugbank.ca/drugs/%s"> %s </a></td>' %(tbl["1-Candidate"][row],tbl["1-Candidate"][row])
        html_pg= html_pg+'<td> %s </td>' %tbl["1-Mol.Name"][row]
        html_pg= html_pg+'<td> %s </td>' %tbl["1-Reg.Status"][row]
        html_pg= html_pg+'<td> <a href="https://www.drugbank.ca/drugs/%s"> %s </a></td>' %(tbl["2-Candidate"][row],tbl["2-Candidate"][row])
        html_pg= html_pg+'<td> %s </td>' %tbl["2-Mol.Name"][row]
        html_pg= html_pg+'<td> %s </td>' %tbl["2-Reg.Status"][row]
        html_pg= html_pg+'<td> %s </td>' %tbl["Similarity by Tcoff"][row]
        #html_pg= html_pg+'<td> %s </td>' %tbl["SMILES"][row]
        html_pg= html_pg+'</tr>'
        html_pg= html_pg+'</tr>'
    html_pg= html_pg+'</table>'
    html_pg= html_pg+'<tfoot style="text-align: right"><a href="%s_matches.tbl" class="btn-special">Download Table</a></tfoot></div>' %(mode)
    
html_pg= html_pg+"""
<div style="text-align:left; padding:10px; color:#913A1E;"><p><b><u>DISCLAIMER</u></b>: The drugs displayed in this table are derived from homology based similarity searches against the DrugBank database.<br>
These are predictive results and are meant to help experts in the field of drug repurposing.<br>
Therefore, Team NOD advices its users to <b>NOT</b> consume any drug without proper consulation with their general practitioner.</i></b></p></div>			
            <!-- Table Section ENDED -->
	</div>
</div>
			<!--  Main JS File --
			<script src="webpages/assets/js/main.js"></script>
	</body>
</html>
"""
print(html_pg)
html_file= open("%s/%s.html" %(resDir,jobId), 'w')
html_file.write(html_pg)
