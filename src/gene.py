#!/usr/bin/python3
import sys
import ast

class Gene:
	
	##
	# args = options //Not Implemented
	# kwargs:
	# 	id   = The database ID of the gene
	# 	name =
	#
	def __init__(self, gene = None, **kwargs):
		# print("*args:\n\t" + str(args))
		# print("**kwargs:\n\t" + str(kwargs))
		# print("\trepr  = " + repr(kwargs))
		# print("\tstr   = " + str(kwargs))
		# print("\tprint = ", end="")
		# print(kwargs)
		if isinstance(gene, Gene):
			kwargs = ast.literal_eval(repr(gene).split(' ', 1)[1])
		if isinstance(gene, str):
			kwargs = ast.literal_eval(gene.split(' ', 1)[1])
		self.geneID = kwargs.get('ID')
		self.geneName = kwargs.get('Name')
		self.geneAcc = kwargs.get('Acc')
		self.geneLocStart = kwargs.get('Start')
		self.geneLocEnd = kwargs.get('End')
		self.geneFASTA = kwargs.get('FASTA')
		self.geneLen = kwargs.get('Len')
		if self.geneLen == None and self.geneLocStart != None and self.geneLocEnd != None:
			self.geneLen = abs(int(self.geneLocStart) - int(self.geneLocEnd)) + 1   
			
	@classmethod
	def fromGene(cls, rep):
		gene = ast.literal_eval(rep.split(' ', 1)[1])
		return cls(**gene)
		
	def getFASTA_File(self):
		return self.geneFASTA
	
	def getFASTA_Seq(self):
		with open(self.geneFASTA, 'r+') as f:
			seqString = ''
			for x in f:
				if not x.startswith('>'):
					seqString += x
			
			return seqString
			
	def getLen(self):
		return self.geneLen
			
	def getID(self):
		return self.geneID
	
	def getAcc(self):
		return self.geneAcc
	
	def getStart(self):
		return self.geneLocStart
		
	def getEnd(self):
		return self.geneLocEnd
	
	def getName(self):
		return self.geneName

	def setGeneData(self, **kwargs):
		self.geneID = kwargs.get('ID', self.geneID)
		self.geneName = kwargs.get('Name', self.geneName)
		self.geneAcc = kwargs.get('Acc', self.geneAcc)
		self.geneLocStart = kwargs.get('Start', self.geneLocStart)
		self.geneLocEnd = kwargs.get('End', self.geneLocEnd)
		self.geneFASTA = kwargs.get('FASTA', self.geneFASTA)
		if self.geneFASTA != None:			
			with open(self.geneFASTA, 'r+') as f:
				t = 0
				for x in f:
					if not x.startswith('>'):
						t += len(x.strip())
				self.geneLen = t
	
	def isReverse(self):
		return self.geneLocStart > self.geneLocEnd	

	def __repr__(self):
		reprRet = 'Gene {'
		reprRet += '\'ID\': '    + repr(self.geneID)       + ', '
		reprRet += '\'Name\': '  + repr(self.geneName)     + ', '
		reprRet += '\'Acc\': '   + repr(self.geneAcc)      + ', '
		reprRet += '\'Start\': ' + repr(self.geneLocStart) + ', '
		reprRet += '\'End\': '   + repr(self.geneLocEnd)   + ', '
		reprRet += '\'Len\': '   + repr(self.geneLen)      + ', '
		reprRet += '\'FASTA\': ' + repr(self.geneFASTA)    + '}'
		return reprRet
	
	def __str__(self):
		strRet  = 'Gene'
		strRet += '\tID   : ' + repr(self.geneID)       + '\n'
		strRet += '\tName : ' + repr(self.geneName)     + '\n'
		strRet += '\tAcc  : ' + repr(self.geneAcc)      + '\n'
		strRet += '\tStart: ' + repr(self.geneLocStart) + '\n'
		strRet += '\tEnd  : ' + repr(self.geneLocEnd)   + '\n'
		strRet += '\tLen  : ' + repr(self.geneLen)      + '\n'
		strRet += '\tFASTA: ' + repr(self.geneFASTA)    + '\n'
		return strRet
