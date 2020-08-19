#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 15:38:31 2020

@author: sohini
"""

from __future__ import print_function
from rdkit import Chem
from rdkit import DataStructs
from rdkit.Chem.Fingerprints import FingerprintMols
#from rdkit.Chem import AllChem
import pandas as pd
#f1 = open('/home/sohini/WORK/work/Project_data_materials/corona_virus/review_comments/Query_compound.csv', 'r')
f1 = open(sys.argv[1], 'r')
TC_megalist = []
for x in f1:
    a = x.split(',')[0] #SMILE
    b = x.split(',')[1] #Compd. ID
    m = Chem.MolFromSmiles(a)
    fps1 = FingerprintMols.FingerprintMol(m)
    #print(m)
    #print(AllChem.Compute2DCoords(m)) #2D structure display
    #f2 = open('/home/sohini/WORK/work/Project_data_materials/corona_virus/review_comments/Target_compound.csv', 'r')
    f2 = open(sys.argv[2], 'r')
    TC_array = [b]
    for y in f2:
        c = y.split(',')[0] #SMILE; for DrugBank file [6]
        d = y.split(',')[1] #Compd. ID; ; for DrugBank file [0]
        n = Chem.MolFromSmiles(c)
        fps2 = FingerprintMols.FingerprintMol(n)
        TC= DataStructs.FingerprintSimilarity(fps1, fps2)
        if TC >= 0.7 :
            print(b, d, TC)
            #print(AllChem.Compute2DCoords(n)) #2D structure display
            TC_array.append(TC)
    f2.close()
    #print(TC_array[0])
    #print(TC_array)
    TC_megalist.append(TC_array)
print(TC_megalist)
df = pd.DataFrame(TC_megalist)
#df.to_csv('TC_cal.csv', index=False, header=False)
#print(df)
