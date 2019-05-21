#!/usr/bin/python3
import sys
import subprocess as sp
import time
import threading
import os

# fileName = sys.argv[1]
# fileOpen = open(fileName, 'r')
# fileToWrite = open(fileName + '_P', 'w+')
# lastProcFile = open(fileName + '_LP', 'a+')
# lastProcFile.seek(0)
# lastProc = lastProcFile.read().strip()
# loc = 0
# count = 0
# geneList = fileOpen.read().strip().rstrip('\n').split('\n')
PATH_TO_FASTA = os.path.expanduser("~/Research/Data/FASTA/")

class GeneFASTACaller:
	def __init__(self, geneList, p = 0):
		self.tempName =".geneFASTACaller_" + str(p)
		self.geneList = geneList
		
	def getEachFASTA(self):
		count = 0	
		for x in self.geneList:
			p = sp.run("~/edirect/efetch -db nuccore -id %s -seq_start %s -seq_stop %s -format fasta" % (x.getAcc(), x.getStart(), x.getEnd()), shell=True, stdout=sp.PIPE)
			f = open('%s' % (PATH_TO_FASTA + x.getName() + '.fasta'), 'w+')
			f.write(p.stdout.decode('utf-8'))
			f.close()
			time.sleep(1.0)
			

			x.setGeneData(FASTA=('%s'%(PATH_TO_FASTA + x.getName() + '.fasta')))
			print('Done & printed to file: %s' % (PATH_TO_FASTA + x.getName() + '.fasta'))			
		

		# if lastProc != '':
			# for x in geneList:
				# y = x.split()
				# loc += 1
				# if 	y[0] == lastProc:
					# lastProc = loc + 1 
					# break
				
	

			

