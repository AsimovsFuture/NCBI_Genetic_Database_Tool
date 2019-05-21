# This script will get the Gene Locations for the DB

import sys
import subprocess as sp

class GeneCaller:
	def __init__(self, gList, p = 0):
		self.gList = gList
		self.callerID = p
		self.gListInfo = None
	
	def getEachGeneInfo(self):
		print("GeneCaller #%d is called" % self.callerID)
		lC = -1
		try: 
		    t = open('/tmp/.geneCaller_%d_LP' % self.callerID, 'r') 
		except FileNotFoundError: 
			lC = 0
		f = open('/tmp/.geneCaller_%d' % self.callerID, 'a+')
		count = 0
		for x in self.gList[lC:]:
			count += 1
			t = open('/tmp/.geneCaller_%d_LP' % self.callerID, 'w+')
			p = sp.run("./callScript.sh %d" % int(x.getID()), shell=True, stdout=sp.PIPE)
			info = p.stdout.decode("utf-8").strip().split()
			#print(p.stderror)
			try:
				x.setGeneData(Acc=info[0], Start=info[1], End=info[2])
				f.write(repr(x) + '\n')
			except IndexError:
				m = open('missing_gene_locations', 'a+')
				m.write(str(x.getID()) + "\n")
				
			
			t.write(str(x.getID())) 
		sp.run("rm /tmp/.geneCaller_%d_LP" % self.callerID, shell=True)
		sp.run("mv /tmp/.geneCaller_%d ./" % self.callerID, shell=True)

	def removeTempFile(self):
		sp.run("rm ./.geneCaller_%d" % self.callerID, shell=True)
