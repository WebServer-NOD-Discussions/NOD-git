#!/usr/bin/python3.6
#	@uthor: TjrNarwani on Fri 31/07/2020

#print "\n\n\tUSAGE:\tpython master_handler.py <Mode> <QuerySeq>\n\n"
import os
import sys
import pandas as pd
import time as t
import random as rand

from rdkit import Chem as chem
from rdkit import DataStructs as d_str
from rdkit.Chem.Fingerprints import FingerprintMols as fngrPrnt
from rdkit.Chem import AllChem
#import re
#import collections

def Sanitizer (fileIn,fileOut):
#	Following command is standardized for JackHmmer parsing. Took multiple tries to optimize.
#target name(1-23), accession(24-33), tlen(35-40), query(41-62), accession(64-73), qlen(75-79), E-value(81-89), score(91-96), bias(98-102),   No.ofDom(104-107),  TtlDom(108-111),  c-eval(112-121),  i-eval(122-130), domScore(132-137), domBias(139-143), hmm-from(145-149), hmm-to(151-155), align-from(157-161), align-to(163-167), envlp-from(169-173), envlp-to(175-179), accur.(181-184), Desc.(186-)
	os.system("grep -v \"#\" %s | cut -c \"1-23,24-33,35-40,41-62,64-73,75-79,81-89,91-97,98-103,157-161,163-167,186-\" --output-delimiter=\"!\" | sed -e \"s/!/\\t/g\" > %s" %(fileIn,fileOut))
	return(print("\n\tFORMATTED: Homology Search output into Tables\n"))

def searchInFile(file, keyword):
	results = []
	with open(file, 'r') as fhandle:
		for line in fhandle:
			if keyword in line:
				results.append((line.rstrip()))
	return results

def searchInTbl(file, keyword):
	db_tbl= pd.read_csv(file, sep=",", engine="python")
	for row in db_tbl.index:
		if keyword in db_tbl["DrugBank ID"][row]:
			match= (db_tbl["DrugBank ID"][row],db_tbl["Drug Groups"][row],db_tbl["Name"][row],db_tbl["SMILES"][row])
	return(match)
    
def HomologySearch(alignFile,tblName,inQformat,DBformat,eVal,InQry,DBname):
#TODO later:
#import subprocess
#process = subprocess.run(['echo', 'Even more output'], stdout=subprocess.PIPE, universal_newlines=True)
#return process()

	print("\tINITIATIED Homology Search") #with\t"+alignFile+"\t"+tblName+"\t"+inQformat+"\t"+eVal+"\t"+DBformat+"\t"+InQry+"\t"+DBname+"\n")
	os.system("jackhmmer -A %s --domtblout %s -N 3 --noali --incE %d --qformat %s --tformat %s %s %s > /dev/null 2>&1" %(alignFile,tblName,int(eVal),inQformat,DBformat,InQry,DBname))
	#Format assertion : Query- qformat <fasta>, Target:	tformat <fasta>

	return(print("\tCOMPLETED Homology Search"))

def filterTbl(in_tbl,out_tbl):
#To open the tsv file, check if it is not empty. Filter based on e-value. Calculate qCov as ('coord from'-'ali from')/qlen and filter the dataset.
#Compile into a single output file.
#	print (in_tbl)
	print("\n\tHomology table is being FILTERED based on e-value and query coverage\n")
	if	os.stat(in_tbl).st_size ==0: #to check if the file is not empty.
		print("EMPTY TABLE FOUND"); exit(0)
	else:
		colms=("Tname","Tacc","Tlen","Qname","Qacc","Qlen","e-val","score","bias","aliStart","aliEnd","Description")
		df= pd.read_csv(in_tbl, sep='\t', names=colms,  engine="python")
		df["qCov"]=((df["aliEnd"]-df["aliStart"])/df["Qlen"])*100
		Filter_df= df.loc[df["qCov"] > 70]
		Filter_df.to_csv(out_tbl, sep="\t")

#Call the DBmap function to map the DBids onto csv in either Mode1 or Mode2.
#	DBmap(sys.argv[1],Filter_df,DB_all, DB_approved)
	return(print("\n\tRETEIVED: Relevant hits from homology table\n"))
	
def DBmap(mode,table,target):
	print("\n\tMAPPING the ids onto DrugBank database to find potent compunds\n")
#	outFile=open("Dgbk_FetchedRecords",'w')	
	F_tbl= pd.read_csv(table, sep="\t", engine="python")
	db_tbl=pd.read_csv(target,sep=",", engine="python")
	mtchdLine=[]
	for row in F_tbl.index:
		#print (row)
		comment=((F_tbl["Description"][row]).split("(")[1].strip(")"))
		print("\n\tExtracted DBids from jackHmmer:\t",comment)
		for DBids in comment.split(";"):
#			db_tbl[db_tbl["SMILES"].str.match(DBids.strip(" "))]
			mtchdLine.append(searchInTbl(target, DBids.strip(" ")))
	outDB=pd.DataFrame(mtchdLine, columns=["DrugBank ID","Category","Common Name","SMILES"])
	print("\n\tFETCHED: Potent Drugbank compounds details\n")
	return(outDB)

#TODO
'''
def genFngrPrnts(inDB):
	fps=[]
	for row in (inDB[inDB["SMILES"].notnull()]).index:
		print (inDB["SMILES"][row])
		fps.append(fngrPrnt.FingerprintMol(chem.MolFromSmiles(inDB["SMILES"][row])))
	
	return(fps)
'''

def TCmxGen(qryDB,TrgtDB):
	sbjDB=pd.read_csv(TrgtDB,sep=",", engine="python")
	chk=open(resDir+"/chkLog.txt",'w')
	errSmiles=open(resDir+"/ErrorSmiles.txt",'w')
	mtchdLine=[]
	qry=qryDB.fillna("NIL");	sbj=sbjDB.fillna("NIL")
	for idx1 in qry.index:
		try:
			qFps= fngrPrnt.FingerprintMol(chem.MolFromSmiles(qry["SMILES"][idx1]))
		except:
			print("\t\tYour SMILE is corrupted\n")
			errSmiles.write("%s\t%s\n" %(qry["DrugBank ID"][idx1], qry["SMILES"][idx1]))
		print(qFps)
		for idx2 in sbj.index:
			if (sbj["SMILES"][idx2] is not "NIL" and qry["SMILES"][idx1] is not "NIL"):
				try:
					sbjFps= fngrPrnt.FingerprintMol(chem.MolFromSmiles(sbj["SMILES"][idx2]))
				except:
					print("\t\tYour SMILE is corrupted ;)\n")
					errSmiles.write("%s\t%s\n" %(sbj["DrugBank ID"][idx2], sbj["SMILES"][idx2]))
				
			Tcoff= d_str.FingerprintSimilarity(qFps, sbjFps)
			if (Tcoff > 0.7):
				print(Tcoff)
				x=(sbj["DrugBank ID"][idx2],sbj["Drug Groups"][idx2],sbj["Name"][idx2],sbj["SMILES"][idx2])
				mtchdLine.append(x)
				chk.write(("%s\t%s\n%s\n%s\n%f\n")%(idx1,idx2,qry["SMILES"][idx1],sbj["SMILES"][idx2],Tcoff))
	tblOut=pd.DataFrame(mtchdLine, columns=["DrugBank ID","Category","Common Name","SMILES"])
	return (tblOut)

'''	qryDB["qFps"]=genFngrPrnts(qryDB)
	sbjDB["sFps"]=genFngrPrnts(sbjDB)
	print(qryDB)
	print(sbjDB)
'''
def main():
#Workflow and calls to the different methods defined in the program.
#TODO: Making each method as a seperate class.

#Checking if the input query_file is not EMPTY.
	inputSeqNo= len([1 for line in open(sys.argv[2]) if line.startswith(">")])
	if inputSeqNo !=0:
		print("\tNumber of sequences input by user are:",inputSeqNo)
	else:
		print("\tEMPTY FILE ENTERED\n")
		exit(0)
#Check for the input file to be in FASTA format.
	if ">" not in open(sys.argv[2]): #TODO: Check if the input sequence is protein.
		print("\nIncorrect Format\n")
		
#Running JackHmmer to search for homologs of the input protein sequences with e-val threshold as 1e-05.
	HomologySearch (resDir+"/pyRunHmmer.align",resDir+"/pyRunHmmer.tsv","fasta","fasta","05",sys.argv[2],Hmlgy_DB)
#Sanitizing the output table from JackHmmer into a usable tab seperated format.
	Sanitizer(resDir+"/pyRunHmmer.tsv",resDir+"/formattedTsv.hmmer")
#Filtering the tsv table into relevant hits based on Query Coverage.
	filterTbl(resDir+"/formattedTsv.hmmer", resDir+"/FilteredTbl.hmmer")
#Reading the input mode by the user and defining workflow accordingly.
	if "1" in sys.argv[1]:
		print("\tEntered in MODE-1\n")
#MODE-1 with multifasta file or all proteins of an organism. Mapping the relevant homology hits onto approved drugs database.
		outDB=DBmap(sys.argv[1],resDir+"/FilteredTbl.hmmer",DB_all)
		outDB.to_csv(resDir+"/Mode1_Matches.tbl",sep="\t")

	elif "2" in sys.argv[1]:
		print("\tEntered in MODE-2\n")
#MODE-2 with single fasta file of a target protein. Mapping the relevant jackhmmer homologs onto a comprehensive drug DB. 
		outDB=DBmap(sys.argv[1],resDir+"/FilteredTbl.hmmer",DB_approved)
#Extracting uniq homologs and comparing their structure with all available structures in approved DB.
		tbl_mod2=TCmxGen(outDB,DB_all)
		tbl_mod2.to_csv(resDir+"/Mode2_Matches.tbl",sep="\t")
	else:
		print("\tPlease enter a mode of operation from \'1\' or \'2\'\n\tEntered Mode is INCORRECT\n")

####################################################################################
################## Calling MAIN method to initiate the program. ####################
####################################################################################

#Source path of hardcoded files required by the program, like the Databases and Resulting Directories.
DB_approved="source/2-DgB_approved_details.csv"
DB_all="source/3-DgB_all_details.csv"
Hmlgy_DB="source/1-DgB_TargetProteins.fasta"
#Calling a random number to generate a new directory for results.
resDir=("Results_%s"%rand.random())
os.system("mkdir %s"%resDir)
#Time method used on main() to calculate exact run-time for the script.
t1=t.time()
#Check if the input command has correct number of arguments and start Main.
if (len(sys.argv) == 3):
	main()
	t2=t.time()
	print("\nRun Time:\t",t2-t1,"\n")
else:
	print("INCORRECT arguments given in the run command.\n\tPlease check the list of arguments.")
