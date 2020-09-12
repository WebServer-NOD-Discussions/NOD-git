#!/usr/bin/python3.6
#       @uthor: TjrNarwani on Fri 31/08/2020

#       USAGE:  python preSumbitCheck.py <mode><InFile.fasta><directory for results>"
import os
import sys
import time as t
import random as rand
import re

#Input variable decralation:
mode=sys.argv[1]
qFile=sys.argv[2]
resDir=sys.argv[3]

"""
def fastaSeqValidate(seq):
    chars = set("ACDEFGHIKLMNPQRSTUVWYX")
    if any((c in chars) for c in seq):
        print(seq)
        return('True')
    else:
        print(seq)
        return('False')
def formatValidate(fType):
 

def modeSanity(mode,inFile):
"""

def main():
#Workflow and calls to the different methods defined in the program.
#Checking the input query_file.
        inFile=open(qFile)
        for lines in inFile.readlines():
            #print(lines)
            if lines.startswith(">"):
                newFasta.write(lines[0:19])
                newFasta.write("\n")
            elif re.match(r'^\s*$', lines):
                pass
            else:
                #newline=lines.replace("\n","")
                newFasta.write(lines)
"""        
        inputSeqNo= len([1 for line in open(sys.argv[2]) if line.startswith(">")])
        if (inputSeqNo > 1) and ("2" in qFile):
            preCheckErr.write("\tERROR:\t %s sequences given in %s:\t 1 expected.\n" %(inputSeqNo,sys.argv[1]))
            exit(0)
        else:
            preCheckErr.write("\tERROR: The file entered in the server is empty or does not compile with Fasta format. Please check your input file again.\nIncase, you are sure that the input file is correct, please use teh contact form to write to us.\n")
            exit(0)

"""
os.system('mkdir -p %s' %resDir)
newFasta=open("%s/query.fasta" %resDir, 'w')
main()
newFasta.close()
