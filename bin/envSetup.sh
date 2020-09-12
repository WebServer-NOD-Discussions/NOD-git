cd /prod/www/nslab/nod_de
#cd /prod/www/nslab/NOD
#Variables_in_order:
#$1= mode,  $2= QueryFile, $3=complete Result_Dir, $4= JobId, $5=Job Title(original), $6= email ID, $7= actual resDir
source dependencies/conda_rc
conda activate
conda activate rdkit-env

echo $1,$2,$3, $4, $5
python bin/preSubmitCheck.py $1 $2 $3 &> $3/preSubmit.log
echo -e "python bin/preSubmitCheck.py $1 $2 $3 &> preSubmit.log\n\n"
python bin/master_handler_v2.py $1 $3/query.fasta $3 &> $3/handler.log
echo -e "python bin/master_handler_v2.py $1 $3/query.fasta $3 &> $3/handler.log\n\n"
python NOD/mailContent.py $1 $3 $7 $4 &> $3/mailContent.log
echo -e "python NOD/mailContent.py $1 $3 $7 $4 &> $3/mailContent.log\n\n"
#len(open("testErrorCases/ResDir_Scov/mode2_matches.tbl").readlines(  ))
#wc -l
python bin/postEmail.py $1 $7 $4 $5 $6 &> $3/pushMail.log
echo -e "python bin/postEmail.py $1 $7 $4 $5 $6 &> $3/pushMail.log\n\n"

conda deactivate
conda deactivate

