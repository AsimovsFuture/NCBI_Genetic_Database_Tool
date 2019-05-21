# This script takes a tsv list of genes and start populating gene info
#
# If the script is called with no options then it will assume the tsv 
# 	list syntax will be
#		'[x]\t[NCBI_Gene_ID]\t[NCBI_GENE_Name]
# If the user wants to specify a different format they will need to call
# 	the script with parameters: 
#		"'ID' = [expected ID index]"
#		"'Name' = [expected Name index]"
# 
import sys 
from gene import Gene
from geneCaller import GeneCaller
from getGeneFasta import GeneFASTACaller as GFC
import multiprocessing as mp

class GeneDB:
	def __init__(self, **kwargs):
		self.geneFile   = kwargs.get('tsv')
		self.geneDBname = kwargs.get('db', 'geneDB.db')
		self.geneList   = kwargs.get('genes', [])
		if self.geneFile != None:
			with open(self.geneFile, 'r+') as f:
				for x in f:
					y = x.strip().split('\t')
					self.geneList.append(Gene(ID = y[kwargs.get('ID', 1)], Name = y[kwargs.get('Name', 2)]))
	
	@classmethod
	def fromDB(cls, fileName = 'geneDB.db'):
		with open(fileName, 'r+') as f:
			geneList = []
			for x in f:
				geneList.append(Gene(x))
			return cls(genes = geneList, db=fileName)
			
	def popFromDB(self, fileName = ''):
		if fileName == '':
			fileName = self.geneDBname
			
		with open(fileName, 'r+') as f:
			self.geneList = []
			for x in f:
				self.geneList.append(Gene(x))


	def saveDB(self, fileName = ''):
		if fileName == '':
			fileName = self.geneDBname
			
		with open(fileName, 'w+') as f:
			for x in self.geneList:
				if isinstance(x, Gene):
					f.write(repr(x) + '\n')
					
					
		
	def populateInfoFromNCBI(self, limit = 5):
		geneList       = []
		geneCallerList = []
		p              = []
		lLen           = 0
		
		for x in self.geneList:
			if x.getAcc() == None:
				geneList.append(x)
				
		lLen = int(len(geneList) / limit)

		for x in range(0, limit - 1):
			geneCallerList.append(GeneCaller(geneList[(x * lLen): ((x + 1) * lLen)], x))
			
		geneCallerList.append(GeneCaller(geneList[((limit - 1) * lLen):], limit - 1))
				
		## Need to change this so that it runs it in parallel 
		## Use threading 
		for x in geneCallerList:
			p.append(mp.Process(target=x.getEachGeneInfo()))
		
		for x in p:
			x.start()
		
		for x in geneCallerList:
			x.removeTempFile()

	def makeFASTA(self, limit = 10, **kwargs):
		p = []
		
		if kwargs.get('id') != None:\
			gFCProcessors = [GFC([ self.get( id= kwargs.get('id') ) ])]
			
		else:
			lLen = int(len(self.geneList) / limit)
			gFCProcessors = []
			
			for x in range(0, limit -1):
				 gFCProcessors.append(GFC(self.geneList[(x * lLen): ((x + 1) * lLen)], x))
				 
			gFCProcessors.append(GFC(self.geneList[((limit - 1) * lLen):], limit - 1))
						
		## Need to change this so that it runs it in parallel 
		## Use threading 
		for x in gFCProcessors:
			p.append(mp.Process(target=x.getEachFASTA()))
				
		for x in p:
			x.start()
		

	def getGeneIDs(self):
		retList = []
		for x in self.geneList:
			retList.append(x.getID)
		return retList
		
	def get(self,**kwargs):
		t = kwargs.get('type', 'gene')
		id = kwargs.get('id', 0)
		ret = None
		for x in self.geneList:

			if x.getID() == str(id):
				return x
		return ret
	 
			
	def __repr__(self):
		stringRep = ''
		for x in self.geneList:
			stringRep += repr(x) + '\n'
		return stringRep
