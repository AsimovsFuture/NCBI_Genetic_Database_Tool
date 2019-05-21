# NCBI_Genetic_Database_Tool
Project for getting,handling, and saving genomic data from the public NCBI database.

Currently little to absolutely no comments on each script, when I start creating the first prototype of the actual system it will have comments and should be usable on most linux systems with no editing of code or python idle interactions

Right now it isn't really implemente, but if you want to try to use it you can. It can work if you adjust the data to work with your linux based system with python 3.x

Will require idle or a new script written to run the geneDB.py script correctly.

Will also require you to download eutils from NCBI for the terminal instructions found at https://www.ncbi.nlm.nih.gov/books/NBK179288/

Gene.tsv is great for test usage.

    - cd to src folder 
	- run python idle by typing 'python3' or 'python' depending on whether python3 is your standard install or not
		from geneDB import GeneDB
		testDB = GeneDB(tsv='Gene.tsv')
		testDB.populateInfoFromNCBI()
		##press ctrl-c after a few moments
		##the gene objects should still have the info that was updated
		testDB.makeFASTA(id=1)
		testDB.saveDB('TestDB.db')
		exit()
	- start idle again
		from geneDB import GeneDB
		## This should recreate the database from the first idle session
		testDB = GeneDB.fromDB('TestDB.db')
		## This should display gene 1 with all info filled
		## Open the fasta file in the location given by the gene to see the fasta seq of that gene
		testDB.get(id=1)
		
		
	
		
