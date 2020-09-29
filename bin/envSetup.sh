
#cd /prod/www/nslab/NOD
cd /prod/www/nslab/nod_de
#Variables_in_order:
#$1= mode,  $2= QueryFile, $3=complete Result_Dir, $4= Job Title, $5= email ID, $6= actual resDir
source dependencies/conda_rc
conda activate
conda activate my-rdkit-env

#echo $1,$2,$3, $4, $5
python bin/master_handler.py $1 $2 $3 &> $3/handler.log
python webpages/mailContent.py $1 $3 $6 $4 &> $3/mailContent.log

#len(open("testErrorCases/ResDir_Scov/mode2_matches.tbl").readlines(  ))
#wc -l
python bin/postEmail.py $1 $6 $4 $5 > $3/pushMail.log


conda deactivate
conda deactivate

