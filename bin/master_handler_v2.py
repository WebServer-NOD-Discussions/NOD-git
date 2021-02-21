#!/usr/bin/python3.6
#	@uthor: TjrNarwani on Fri 31/07/2020
#	Updated: Mon 15/02/2021

#chkLog.write "\n\n\tUSAGE:\tpython master_handler.py <Mode> <QuerySeq>\n\n"
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
	"""
#	Following command is standardized for JackHmmer parsing. Took multiple tries to optimize.
#target name(1-23), accession(24-33), tlen(35-40), query(41-62), accession(64-73), qlen(74-79), E-value(81-89), score(91-96), bias(98-102),   No.ofDom(104-107),  TtlDom(108-111),  c-eval(112-121),  i-eval(122-130), domScore(132-137), domBias(139-143), hmm-from(145-149), hmm-to(151-155), align-from(156-161), align-to(163-167), envlp-from(169-173), envlp-to(175-179), accur.(181-184), Desc.(186-)
	os.system("grep -v \"#\" %s | cut -c \"1-23,24-32,34-40,41-63,64-73,74-79,80-89,90-97,98-103,156-161,162-167,183-\" --output-delimiter=\"!\" | sed -e \"s/!/\\t/g\" > %s" %(fileIn,fileOut))
	"""
	os.system('grep -v "^#" %s |sed -E "s/ +/\t/g"|sed -E "s/ +//g" | cut -f "-22" > frmTbl1' %fileIn)
	os.system('grep -v "^#" %s |sed -E "s/ +/\t/g"|sed -E "s/ +//g" | cut -f "23-" | sed -e "s/\t/ /g" > frmTbl2' %fileIn)
	os.system('paste frmTbl1 frmTbl2 > %s' %fileOut)
	os.system('rm -f frmTbl*')
	chkLog.write("\n\tFORMATTED: Homology Search output into Tables\n")

def searchInFile(file, keyword):
	results = []
	with open(file, 'r') as fhandle:
		for line in fhandle:
			if keyword in line:
				chkLog.write("searching {} in {}" .format(keyword,line))
				name=" ".join(line.split("(")[0].split()[1:]) #extracting the protein Name from the matched Header.
	return name

#Reading each DBid and searching it in the target database.
def searchInTbl(qry,tAcc,tName,covrg,aliStrt,aliEnd,file,keyword):
	match=""
	db_tbl= pd.read_csv(file, sep=",", engine="python")
	for row in db_tbl.index:
		if keyword in db_tbl["DrugBank ID"][row]:
			match= (qry,tAcc,tName,covrg,aliStrt,aliEnd,db_tbl["DrugBank ID"][row],db_tbl["Drug Groups"][row],db_tbl["Name"][row],db_tbl["AverageMass"][row],db_tbl["Predicted_logp"][row],db_tbl["SMILES"][row])#,db_tbl["KnownUse"][row]) #Fetching information from Target table and returning the list.
	if match:
		return(match)
	else:
		chkLog.write("\t\tSorry! The DBid(s) {} could not matched in the DrugBank\n\n" .format(keyword))
#		return(qry, trgt, keyword,"Sorry!","This ID", "could","NOT","BE","FOUND")
    
def HomologySearch(smryFile,alignFile,tblName,inQformat,DBformat,eVal,InQry,DBname):
	chkLog.write("\n\tINITIATIED Homology Search with\t\n:"+smryFile+"\t"+alignFile+"\t"+tblName+"\t"+inQformat+"\t"+eVal+"\t"+DBformat+"\t"+InQry+"\t"+DBname+"\n")
	os.system("%s -o %s -A %s --domtblout %s -N 3 --noali --incE %d --qformat %s --tformat %s %s %s > /dev/null 2>&1" %(jackhmmer,smryFile,alignFile,tblName,int(eVal),inQformat,DBformat,InQry,DBname))
	#Format assertion : Query- qformat <fasta>, Target:	tformat <fasta>

	chkLog.write("\tCOMPLETED Homology Search\n")

def filterTbl(in_tbl,out_tbl, Threshold):
#To open the tsv file, check if it is not empty. Filter based on e-value. Calculate qCov as ('coord from'-'ali from')/qlen and filter the dataset.
#Compile into a single output file.
	chkLog.write("\n\tHomology table is being FILTERED based on e-value and query coverage\n")
	if	os.stat(in_tbl).st_size ==0: #to check if the file is not empty.
		htmlErrors.write("EMPTY TABLE FOUND after homology search. No homologs were identified for your query protein(s).\n\n"); exit(0);
	else:
		colms=("tName","tAcc", "tLen", "qName","qAcc", "qLen", "eVal", "score", "bias", "domNo", "totDom", "domCval", "domIval", "domScor", "domBias", "hmmStrt", "hmmEnd", "aliStrt", "aliEnd", "envStrt", "envEnd", "envAccu", "description")
		df= pd.read_csv(in_tbl, sep='\t', names=colms,  engine="python")
		try:
#			chkLog.write("%s,%s,%s\n" %(df["aliEnd"], df["aliStrt"], df["qLen"]))
			df["tCov"]=round((((df["aliEnd"]-df["aliStrt"])/df["qLen"])*100),2)
			df["qCov"]=round((((df["hmmEnd"]-df["hmmStrt"])/df["qLen"])*100),2) #MARKED: Validate if an HMM profile is given as input in future versions.
			df.to_csv(resDir+"/UnFiltered.tbl", sep="\t")
#			Filter_df= df.loc[round(df["qCov"],2) > 70.0]
			print("Threshold:"+Threshold)
			Filter_df= df.loc[round(df["qCov"],2) > int(Threshold)]
			Filter_df.to_csv(out_tbl, sep="\t")
		except:
			chkLog.write("Possible errors in parsing the JackHmmer output tsv\n\n Check enteries in the formatted Table\n\n")
			qCov=[]
			for row in df.index:
				try:
					cov= (((df["hmmEnd"][row] - df["hmmStart"][row])/ df["qLen"][row])*100)
					chkLog.write("cov= %s - %s / %s = %s\n" %(df["hmmEnd"][row],df["hmmStart"][row],df["qLen"][row],cov))
				except:
					cov=0
					chkLog.write("Possible Errors in input file. No Qcov Calculated:\n\n Check entries in formatted table with:\t %s\t%s\t%s\n"  %(df["tName"][row],df["qName"][row],df["qName"][row]))
					htmlErrors.write("Qcoverage for formatted hits could not be calculating. This error could arise for very short input sequences.\n\nTo get full details, use NOD's Contact form citing the job Title to get in touch with NOD admin\n\n"); exit(0);
				if (cov >= Threshold):
#					tblRow= (df["Tname"][row], df["Tacc"][row], df["Tlen"][row], df["Qname"][row], df["Qacc"][row], df["Qlen"][row], df["e-val"][row], df["score"][row], df["bias"][row], df["aliStart"][row], df["aliEnd"][row], df["Description"][row], cov)
					qCov.append(cov)
			df["qCov"]=qCov
#			Filter_df= pd.DataFrame(qCov, columns=colms.append("qCov"))
			Filter_df.to_csv(out_tbl, sep="\t")

#Call the DBmap function to map the DBids onto csv in either Mode1 or Mode2.
	chkLog.write("\n\tRETEIVED: Relevant hits from homology table\n")
	
def DBmap(mode,table,target):
	chkLog.write("\n\tMAPPING the ids onto DrugBank database to find potent compunds\n")
	F_tbl= pd.read_csv(table, sep="\t", engine="python")	#FilteredTable
	db_tbl=pd.read_csv(target,sep=",", engine="python")	#TargetTable-DgBank
	mtchdLine=[]
	for row in F_tbl.index:
		tAcc=F_tbl["tName"][row].split("|")[1]
		tName=searchInFile(Hmlgy_DB,tAcc)
		chkLog.write("\nSelected Target Protein Name is:\t{}\n" .format(tName))
		comment=((F_tbl["description"][row]).split("(")[1].strip(")"))
		chkLog.write("\n\tExtracted DBids from jackHmmer:\t{}\n" .format(comment))
		for DBids in comment.split(";"):
			chkLog.write("Find a match against %s in DgBankDB: target\n" %DBids)
			mtchdLine.append(searchInTbl(F_tbl["qName"][row],tAcc,tName,F_tbl["qCov"][row],F_tbl["aliStrt"][row],F_tbl["aliEnd"][row],target,DBids.strip(" "))) #Input string of the DBid search in Target DB and storing the returned list from the function.
	outDB=pd.DataFrame(mtchdLine, columns=["Query","T_Acc","T_Name","Query-Cov","Align-From","Align-To","DrugBank ID","Reg.Status","Mol.Name","Avg.Mass","LogP (pred)","SMILES"])
	chkLog.write("\n\tFETCHED: Potent Drugbank compounds details\n")
	finDB= outDB.sort_values(by=['Query-Cov'], ascending=False)
	return(finDB.drop_duplicates().dropna().reset_index(drop=True))
#TODO
'''
def genFngrPrnts(inDB):
	fps=[]
	for row in (inDB[inDB["SMILES"].notnull()]).index:
		chkLog.write (inDB["SMILES"][row])
		fps.append(fngrPrnt.FingerchkLog.writeMol(chem.MolFromSmiles(inDB["SMILES"][row])))
	return(fps)
'''
def TCmxGen(qryDB,TrgtDB):
	sbjDB=pd.read_csv(TrgtDB,sep=",", engine="python")
	errSmiles=open(resDir+"/ErrorSmiles.txt",'w')
	mtchdLine=[]
	qry=qryDB.fillna("NIL");	sbj=sbjDB.fillna("NIL") #Fill all empty values with NA to better compute using PANDAS>
	qFps=""; sbjFps=""
	for idx1 in qry.index: #Pick the first potential candidate for repurposing.
		if "Found" in qry["SMILES"][idx1]:
			x=(qry["Query"][idx1],qry["T_Acc"][idx1],qry["T_Name"][idx1],qry["Query-Cov"][idx1],qry["Align-From"][idx1],qry["Align-To"][idx1],qry["DrugBank ID"][idx1],qry["Reg.Status"][idx1],qry["Mol.Name"][idx1],qry["Avg.Mass"][idx1],qry["LogP (pred)"][idx1],qry["SMILES"][idx1])
			mtchdLine.append(x)
		else:
			try:
				qFps= fngrPrnt.FingerprintMol(chem.MolFromSmiles(qry["SMILES"][idx1])) #Converting the candidate into SMILES Fingerprint.
			except:
				#ex = sys.exc_info()[0]
				chkLog.write("\n\t\tYour QUERY SMILE is corrupted at %s:\n%s\n" %(qry["DrugBank ID"][idx1],qry["SMILES"][idx1]))
				errSmiles.write("%s\t%s\n" %(qry["DrugBank ID"][idx1], qry["SMILES"][idx1]))
		for idx2 in sbj.index: #Querying the candidate in the approved drug dataset.
			if (sbj["SMILES"][idx2] is not "NIL" and qry["SMILES"][idx1] is not "NIL"):
				try:
					sbjFps= fngrPrnt.FingerprintMol(chem.MolFromSmiles(sbj["SMILES"][idx2])) #Real-time conversion of appoved drugs SMILES in Fingerprints.
				except:
					#ex = sys.exc_info()[0]
					chkLog.write("\n\t\tYour TARGET SMILE is corrupted at %s:\n%s\n" %(sbj["DrugBank ID"][idx2],sbj["SMILES"][idx2]))
					errSmiles.write("%s\t%s\n" %(sbj["DrugBank ID"][idx2], sbj["SMILES"][idx2]))
				try:
					Tcoff= d_str.FingerprintSimilarity(qFps, sbjFps) #Comparing the two fingerprints if they match more than 70%.
					if (Tcoff > 0.7):# and qry["DrugBank ID"][idx1] != sbj["DrugBank ID"][idx2]):
						chkLog.write("\nTcoff above 0.7\t%s\tbetween %s and %s\n" %(round(Tcoff,2),qry["DrugBank ID"][idx1],sbj["DrugBank ID"][idx2]))
						x=(qry["Query"][idx1],qry["T_Acc"][idx1],qry["T_Name"][idx1],qry["Query-Cov"][idx1],qry["Align-From"][idx1],qry["Align-To"][idx1],qry["DrugBank ID"][idx1],qry["Mol.Name"][idx1],qry["Reg.Status"][idx1],qry["Avg.Mass"][idx1],qry["LogP (pred)"][idx1],sbj["DrugBank ID"][idx2],sbj["Name"][idx2],sbj["Drug Groups"][idx2],sbj["AverageMass"][idx2],sbj["Predicted_logp"][idx2],round(Tcoff,2)) #Defining row of the output table.Rounded off Avg. Mass and predicted LogP from the sbj table (approved dataset) as the raw unfiltered table is accessed fr sbj. That is not the case in qry DB.
						mtchdLine.append(x)
				except:
					chkLog.write("No similar structural fingerPrints found for %s.\n" %qry["DrugBank ID"][idx1])
		if (qry["DrugBank ID"][idx1] not in str(mtchdLine)): #when no approved drug is a significant hit.
			chkLog.write("\nNo Secondary Hits found for\t%s\n%s\n" %(qry["DrugBank ID"][idx1],mtchdLine))
			x=(qry["Query"][idx1],qry["T_Acc"][idx1],qry["T_Name"][idx1],qry["Query-Cov"][idx1],qry["Align-From"][idx1],qry["Align-To"][idx1],qry["DrugBank ID"][idx1],qry["Mol.Name"][idx1],qry["Reg.Status"][idx1],qry["Avg.Mass"][idx1],qry["LogP (pred)"][idx1],"NONE","-","-","-","-","-") #Defining row of the output table.Rounded off Avg. Mass and predicted LogP from the sbj table (approved dataset) as the raw unfiltered table is accessed fr sbj. That is not the case in qry DB.
			mtchdLine.append(x)

	if mtchdLine:
		tblOut=pd.DataFrame(mtchdLine, columns=["Query","T_Acc","T_Name","Query-Cov","Align-From","Align-To","1-Candidate","1-Mol.Name","1-Reg.Status","1-Avg.Mass","1-LogP","2-Candidate","2-Mol.Name","2-Reg.Status","2-Avg.Mass","2-LogP","Similarity by Tcoff"]) #defining headers of the output table.
		outDB=tblOut.sort_values(by=['Query-Cov'], ascending=False)
		return (outDB.drop_duplicates().dropna().reset_index(drop=True))#remove duplicates and NA values.Then reset the index.
		#outDB.loc[~outDB.column.isin(['vitamins','supplements'])] # remove selected sets from resulting table.
	else:
#		mtchdLine.append(["SORRY!!","Your Query","Protein sequence", "has generated", "an EMPTY FILE","while", "searching for","similar drugs.","Check FAQ:section"])
		htmlErrors.write("None of the candidates obtained from target homologs could pass the threshold for the 2D structural comparisons index (Tcoff.). The current Tcoff threshold is 0.7 \n\nHere is a link to the intermediate table with possible candidates from first round without applying the threshold.\n\t http://pauling.mbu.iisc.ac.in/NOD/{}/mode2_interm.tbl" .format(actDir)); exit(0)

	errSmiles.close()

def main():
#Workflow and calls to the different methods defined in the program.
#TODO: Making each method as a seperate class.
#Checking if the input query_file is not EMPTY.
	inputSeqNo= len([1 for line in open(sys.argv[2]) if line.startswith(">")])
	if inputSeqNo !=0:
		chkLog.write("\tNumber of sequences input by user are: %s\n" %inputSeqNo)
		if (inputSeqNo > 1) and ("2" in sys.argv[1]):
			htmlErrors.write("\tERROR:\t %s sequences given in %s:\t 1 expected.\n" %(inputSeqNo,sys.argv[1]))
			exit(0)
	else:
		htmlErrors.write("\tERROR: The file entered in the server is empty. Please check your input file again.\n Incase, you are sure that the input file is correct,.\n\nUse NOD's Contact form citing the job Title to get in touch with NOD admin\n\n"); exit(0);

#Running JackHmmer to search for homologs of the input protein sequences with e-val threshold as 1e-05.
	h1=t.time()
	HomologySearch (resDir+"/pyRunHmmer.smry",resDir+"/pyRunHmmer.align",resDir+"/pyRunHmmer.tsv","FASTA","FASTA","05",sys.argv[2],Hmlgy_DB)
	h2=t.time()
	chkLog.write("\nTIME-Homology-Search:\t%s\n" %(round((h2-h1),2)))
#Sanitizing the output table from JackHmmer into a usable tab seperated format.
	if os.stat(resDir+"/pyRunHmmer.tsv").st_size ==0: #to check if the file is not empty.
		htmlErrors.write("ERROR: An EMPTY TABLE was Found after homology search using 3 iterations of jackhmmer with e-val cutoff @ 1e-5. Either no homologs were identified for your query protein(s) or there could be a problem in your input sequence.\nPlease  inspect the input file here:\n\t http://pauling.mbu.iisc.ac.in/NOD/%s/qFile.fasta\n\n" %actDir); exit(0);n 
#If the above condition is true, the code will terminate here.
	s1=t.time()
	Sanitizer(resDir+"/pyRunHmmer.tsv",resDir+"/formattedTsv.hmmer")
	s2=t.time()
	chkLog.write("\nTIME-Sanitize-hmmer:\t%s\n" %(round((s2-s1),2)))
#Filtering the tsv table into relevant hits based on Query Coverage.
	f1=t.time()
	filterTbl(resDir+"/formattedTsv.hmmer", resDir+"/FilteredTbl.hmmer", qThreshold)
	f2=t.time()
	chkLog.write("\nTIME-Filter-Table:\t%s\n" %(round((f2-f1),2)))
#Reading the input mode by the user and defining workflow accordingly.
	if sum(1 for line in open(resDir+"/FilteredTbl.hmmer")) <= 1 : #to check if any filtered hits were found or an empty table is generated.
		htmlErrors.write("None of the target homologs identified for your query protein(s) could pass the alignment coverage filter. The current coverage threshold is 70 percent.\n\nHere is a link to the unfiltered table before applying the coverage threshold.\n\t http://pauling.mbu.iisc.ac.in/NOD/%s/UnFiltered.tbl" %actDir); exit(0);

	if "1" in sys.argv[1]:
		chkLog.write("\tEntered in MODE-1\n")
#MODE-1 with multifasta file or all proteins of an organism. Mapping the relevant homology hits onto approved drugs database.
		m1_1=t.time()
		outDB=DBmap(sys.argv[1],resDir+"/FilteredTbl.hmmer",DB_all)
		outDB.to_csv(resDir+"/mode1_matches.tbl",sep="\t")
		m1_2=t.time()
		chkLog.write("\nTIME-MODE1-Run:\t%s\n" %(round((m1_2-m1_1),2)))

	elif "2" in sys.argv[1]:
		m2_map1=t.time()
		chkLog.write("\tEntered in MODE-2\n")
#MODE-2 with single fasta file of a target protein. Mapping the relevant jackhmmer homologs onto a comprehensive drug DB. 
		outDB=DBmap(sys.argv[1],resDir+"/FilteredTbl.hmmer",DB_all)
		outDB.to_csv(resDir+"/mode2_interm.tbl",sep="\t")
		m2_map2=t.time()
		chkLog.write("\nTIME-MODE2_DBmap-Run:\t%s\n" %(round((m2_map2-m2_map1),2)))
#Extracting uniq homologs and comparing their structure with all available structures in approved DB.
		m2_tc1=t.time()
		tbl_mod2=TCmxGen(outDB,DB_approved)
		tbl_mod2.to_csv(resDir+"/mode2_matches.tbl",sep="\t")
		m2_tc2=t.time()
		chkLog.write("\nTIME-MODE2_Tc-Run:\t%s\n" %(round((m2_tc2-m2_tc1),2)))
		chkLog.write("\nTIME-MODE2-Complete:\t%s\n" %(round((m2_tc2-m2_map1),2)))

	else:
		chkLog.write("\tPlease enter a mode of operation from \'1\' or \'2\'\n\tEntered Mode is INCORRECT\n"); exit(0)


####################################################################################
################## Calling MAIN method to initiate the program. ####################
####################################################################################

#Source path of hardcoded files required by the program, like the Databases and Resulting Directories.
DB_approved="source/2-DgB_approved_details.csv"
#DB_all="source/DB_updates/3-DgB_all_details_082020.csv"
DB_all="source/3-DgB_all_details.csv"
Hmlgy_DB="source/1-DgB_TargetProteins.fasta"
jackhmmer="/prod/www/nslab/NOD/dependencies/hmmer-3.3.1/bin/jackhmmer"
#Calling a random number to generate a new directory for results.
#resDir=("%s_Results_%s"%sys.argv[3],rand.random())
try:
	resDir=sys.argv[3]
except:
	print("ERROR: System arguments not satisfied")
	exit(0)
os.system("mkdir -p %s"%resDir)
htmlErrors=open(resDir+"/htmlErrors.log",'w')
chkLog=open(resDir+"/check.log",'w')
actDir=resDir.split("/")[-3]+"/"+resDir.split("/")[-2]

qThreshold= sys.argv[4]
print("Threshold for alignment coverage:\t {}" .format(qThreshold))
#Time method used on main() to calculate exact run-time for the script.
t1=t.time()
#Check if the input command has correct number of arguments and start Main.
if (len(sys.argv) == 5):
	main()
	t2=t.time()
	chkLog.write("\nTIME-Complete-Run:\t%s\n" %(round((t2-t1),2)))
else:
	chkLog.write("INCORRECT arguments given in the run command.\n\tPlease check the list of arguments.")
chkLog.close()
htmlErrors.close()
