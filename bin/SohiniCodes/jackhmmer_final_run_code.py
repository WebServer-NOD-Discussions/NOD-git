@sohini
#query_seq (input) 6035_target (subject database)
import commands
fq=open('470_finalquery.fasta', 'r')
count=0
i=1 #for counting seq. no. in the query file
for line in fq:
        if count%2==0:
                temp=open('query_seq.fasta', 'w')
                temp.write(line)
        else:
                temp.write(line)
                temp.close()
                commands.getstatusoutput("/home/software/HMMER3.0/binaries/jackhmmer -E 0.0001 -o /home/sohini/results/final_runs_results/txt_files/output'%s'.txt --tblout /home/sohini/results/final_runs_results/tab_files/tabout'%s'.tab --domtblout /home/sohini/results/final_runs_results/dom_files/domout'%s'.dom -A /home/sohini/results/final_runs_results/align_files/align'%s'.align --cpu 3 query_seq.fasta 6035_finaltarget.fasta" %(i,i,i,i))
                i=i+1
        count=count+1
fq.close()

