#!/usr/bin/python3
import sys
import subprocess
import ast

p1 = subprocess.Popen('./getGeneFasta.py genes2BeProcessed0', shell=True)	
p2 = subprocess.Popen('./getGeneFasta.py genes2BeProcessed1', shell=True)	
p3 = subprocess.Popen('./getGeneFasta.py genes2BeProcessed2', shell=True)	
p4 = subprocess.Popen('./getGeneFasta.py genes2BeProcessed3', shell=True)	
p5 = subprocess.Popen('./getGeneFasta.py genes2BeProcessed4', shell=True)	
p6 = subprocess.Popen('./getGeneFasta.py genes2BeProcessed5', shell=True)	
p7 = subprocess.Popen('./getGeneFasta.py genes2BeProcessed6', shell=True)	
p8 = subprocess.Popen('./getGeneFasta.py genes2BeProcessed7', shell=True)	
p9 = subprocess.Popen('./getGeneFasta.py genes2BeProcessed8', shell=True)	
p10 = subprocess.Popen('./getGeneFasta.py genes2BeProcessed9', shell=True)
exit_codes = [p.wait() for p in [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10]]
fileToWrite = open('processedGenes', 'a+')
fileToWrite.seek(0)
count = fileToWrite.read().count('\n')
geneDictFile = open('geneDict.txt', 'r+')
geneDict = ast.literal_eval(geneDictFile.read())
for x in range(0, 10):
	geneList = open('genes2BeProcessed' + str(x) + '_P', 'r').read().split('}\n')
	for y in geneList:
		y = y.replace('\n', '^')
		if y != '':
			geneDict[int(y.split(':')[0].strip('{'))].append(count)
			fileToWrite.write(y + '}\n')
			count += 1
geneDictFile = open('geneDict.txt','w+')
geneDictFile.write(str(geneDict))
subprocess.call('rm genes2BeProcessed*_P', shell=True)
