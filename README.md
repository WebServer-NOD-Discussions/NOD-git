# WS-NOD_vm
 New use of Old Drugs


-Contents:
1. bin- Contains all the binary files and the main python executable (master_handler.py)
2. source- Contains the downloaded databases and tables.
3. test- Contains input sequence files for testing.

-Dependencies:
1. python3.6 or above.
2. specific python packages: pandas, numpy, and rdkit.
3. Anaconda package manager for python-rdkit library.

-To Run:
1. Set the working directory as the WS-NOD_vm directory, i.e the parent directory of bin/ source/ and test/
2. Execute the python file: bin/master_handler.py. 
	The script takes two arguments:\
	A) Mention the mode you want to enter. The mode names can vary but it should contain "1" or "2".
		For eg: Mode1, Mod1, Mo1, Md1, Md2, Mod2, Mode2 are all legal entries.\
	B) The input sequence file in fasta format.
		For Mode1: User is allowed to enter multiple sequences in fasta format.
		For Mode2: User is restricted to enter only a singel sequence in fasta format.

3. From the work directory WS-NOD_vm.\
Execute-\
prompt> python3 bin/master_handler.py <MODE CHOICE> <Input Fasta Sequence>\
Example case-\
prompt> python3 bin/master_handler.py mod2 test/Query_mod2.fasta

-Definitions for mode of operations:
--Mode1- When the user is interested to find potential drugs against a set of target sequences or all sequences of a model organism (providing its taxonomy id)
--Mode2- When the user has already attained a specific target protein, eg. Sars-Cov2 Mprotease, and want to identify all potential approved drugs against it.

-Output Results:
All output files, error and check logs would be in a directory called: Results_<a random number>/
