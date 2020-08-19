#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 24 18:15:26 2019

@author: sohini
"""
path="/home/sohini/WORK/work/Project_data_materials/Cancer_drug_repurposing/Aurora_Kinase_A/ROCS/filtered_approved_db_hits/rpt_files_Aurora-A_all_ligs_screened_against_approved_db/hits_ATP_site_ligs_rpt_files/"

file1="inhibitor_wise_hit_analysis/83H_ATP_site_single_digit_nM_inhibitor_query_reliable_hits.csv"
file2="inhibitor_wise_hit_analysis/83H_hits_smiles"

f1 = open("path"/file1, 'r')
f3 = open("path"/file2, 'a')

'''
for x in f1:
    a = x.split('\t')[1]
    #print(a)
    f2 = open(path/"ATP_site_all_reliable_hits_DB-id_smiles", 'r')
    for y in f2:
        b = y.split('\t')[0]
        c = y.split('\t')[1].strip()
        #print(c)
        #print(b)
        if a == c:
            f3.write(y)
            break
    f2.close()
f1.close()
f3.close()
'''
f1.close()
f2.close()

