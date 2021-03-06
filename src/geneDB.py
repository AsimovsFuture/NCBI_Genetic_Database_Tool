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
import subprocess as sp
import math
import os # will be used for creating directories

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
		self.raisedError = kwargs.get('errors',[])
	
	@classmethod
	def fromDB(cls, fileName = 'geneDB.db'):
		with open(fileName, 'r+') as f:
			geneList = []
			for x in f:
				geneList.append(Gene(x))
			return cls(genes = geneList, db=fileName)
			
	def openDB(self, fileName = ''):
		if fileName == '':
			fileName = self.geneDBname
			
		with open(fileName, 'r+') as f:
			self.geneList = []
			for x in f:
				
				#self.geneList.append(Gene(x))

				##Start of testing###########################
				if x.startswith("Gene"):          ##Testing##
					self.geneList.append(Gene(x)) ##Testing##
				else: 					          ##Testing##
					self.raisedError.append(x)    ##Testing##
				##End of testing#############################

	def saveDB(self, fileName = ''):
		if fileName == '':
			fileName = self.geneDBname
			
		with open(fileName, 'w+') as f:
			for x in self.geneList:
				if isinstance(x, Gene):
					f.write(repr(x) + '\n')
		
			##Start of testing#####################
			for x in self.raisedError: ##Testing##
				f.write(x)              ##Testing##
			##End of testing#######################
			
	def parallelCallScriptFix(self, geneToCall):				
		p = sp.run("./callScriptFix.sh %d" % int(geneToCall.getID()), shell=True, stdout=sp.PIPE)
		info = p.stdout.decode("utf-8").strip().split()
		missing = []
		try:
			if int(info[0]) != 0:
				print("gene %s has status %s" % (geneToCall.getID(), info[0]))
				missing = [info[0],geneToCall.getID()]
		except IndexError:
			print('Error getting info for gene id %d' % int(geneToCall.getID()))
		return missing

	def parallelCallScript(self, geneToCall):				
		p = sp.run("./callScript.sh %d" % int(geneToCall.getID()), shell=True, stdout=sp.PIPE)
		info = p.stdout.decode("utf-8").strip().split()
		try:
			geneToCall.setGeneData(Acc=info[0], Start=info[1], End=info[2])
		except IndexError:
			print('Error getting info for gene id %d' % int(geneToCall.getID()))
		return geneToCall
	
	def testParallelCallScript(self, geneToCall):				
		p = sp.run("./testCallScript.sh %d" % int(geneToCall.getID()), shell=True, stdout=sp.PIPE)
		info = p.stdout.decode("utf-8").strip().split()
		try:
			geneToCall.setGeneData(Status=info[0], Acc=info[1], Start=info[2], End=info[3])
		except IndexError:
			try:
				self.raisedError.append(geneToCall.getID())
				geneToCall.setGeneData(Status=info[0])
			except IndexError:
				print('Error getting info for gene id %d' % int(geneToCall.getID()))
		return geneToCall
		
	def testPopulateInfoFromNCBI(self, limit = 5):
		geneList       = []
		geneIndex      = []
		geneCallerList = []
		p              = []
		lLen           = 0
		
		pool = mp.Pool(processes=limit)
		
		count = 0
		for x in self.geneList:
			if x.getAcc() == None:
				geneIndex.append(count)
				geneList.append(x)
			count += 1
			
		lLen = int(math.ceil(len(geneList) / limit))

		#Start progress bar
		progString = ('%d out of %d [%%%.2f]' % (0, len(geneList),round(0.00, 2)))
		width = len(progString) #For backspacing
		sys.stdout.write(progString)
		sys.stdout.flush()
		sys.stdout.write("\b" * (width)) #Backspace to beginning of bar	

		for x in range(0,lLen - 1):
			results = pool.map(self.testParallelCallScript, geneList[x*limit:((x+1)*limit)])
						
			for y in range(len(results)):
				self.geneList[geneIndex[(x*limit)+y]].setGeneData(gene=results[y])

			#Keep updating progress bar
			progString = ("%d out of %d [%%%.2f]" % (((x+1)*limit), len(geneList),round(((float((x+1)*limit)/len(geneList))*100.0), 2)))
			width = len(progString) 
			sys.stdout.write(progString)
			sys.stdout.flush()
			sys.stdout.write("\b" * (width)) 
			
		results = pool.map(self.testParallelCallScript, geneList[(lLen - 1)*limit:])
		
		#Print final progress report
		progString = ("%d out of %d [%%100.00]\n" % (len(geneList), len(geneList)))
		sys.stdout.write(progString)
		sys.stdout.flush()

		for y in range(len(results)):
			self.geneList[geneIndex[((lLen - 1)*limit)+y]].setGeneData(gene=results[y])
		pool.close()
		pool.join()
		
	def populateInfoFromNCBI(self, limit = 5):
		geneList       = []
		geneIndex      = []
		geneCallerList = []
		p              = []
		lLen           = 0
		
		pool = mp.Pool(processes=limit)
		
		count = 0
		for x in self.geneList:
			if x.getAcc() == None:
				geneIndex.append(count)
				geneList.append(x)
			count += 1
			
		lLen = int(math.ceil(len(geneList) / limit))

		#Start progress bar
		progString = ('%d out of %d [%%%.2f]' % (0, len(geneList),round(0.00, 2)))
		width = len(progString) #For backspacing
		sys.stdout.write(progString)
		sys.stdout.flush()
		sys.stdout.write("\b" * (width)) #Backspace to beginning of bar	
		
		for x in range(0,lLen - 1):
			results = pool.map(self.parallelCallScript, geneList[x*limit:((x+1)*limit)])

			for y in range(len(results)):
				self.geneList[geneIndex[(x*limit)+y]].setGeneData(gene=results[y])
			
			#Keep updating progress bar
			progString = ("%d out of %d [%%%.2f]" % (((x+1)*limit), len(geneList),round(((float((x+1)*limit)/len(geneList))*100.0), 2)))
			width = len(progString) 
			sys.stdout.write(progString)
			sys.stdout.flush()
			sys.stdout.write("\b" * (width)) 	

		results = pool.map(self.parallelCallScript, geneList[(lLen - 1)*limit:])
		
		#Print final progress report
		progString = ("%d out of %d [%%100.00]\n" % (len(geneList), len(geneList)))
		sys.stdout.write(progString)
		sys.stdout.flush()
		
		for y in range(len(results)):
			self.geneList[geneIndex[((lLen - 1)*limit)+y]].setGeneData(gene=results[y])
		pool.close()
		pool.join()

			
	def populateInfoFromNCBIFix(self, limit = 5):
		geneList       = []
		geneIndex      = []
		geneCallerList = []
		p              = []
		lLen           = 0
		
		pool = mp.Pool(processes=limit)
		
		count = 0
		for x in self.geneList:
			if x.getAcc() == None:
				geneIndex.append(count)
				geneList.append(x)
			count += 1
			
		lLen = int(math.ceil(len(geneList) / limit))
		results = {'1':[],'2':[]}
		for x in range(0,lLen - 1):
			result = pool.map(self.parallelCallScriptFix, geneList[x*limit:((x+1)*limit)])
			for y in result:
				if len(y) > 0:
					results[y[0]].append(y[1])
			#if len(result) > 0:
				#print(result)
				#results.update(result)	
		result = pool.map(self.parallelCallScriptFix, geneList[(lLen - 1)*limit:])
		for y in result:
			if len(y) > 0:
				results[y[0]].append(y[1])
		#if len(result) > 0:
		#	print(result)
			#results.update(result)

		self.geneErrorDict = results
			
		pool.close()
		pool.join()

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
			retList.append(x.getID())
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
