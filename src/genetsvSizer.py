#!/usr/bin/python3
import sys



maxNum = int(sys.argv[1])
f = open("Gene.tsv", "r+")
count = 0
f2w = open("Gene%d.tsv" % maxNum, 'w+')
while count <= maxNum:
	x = f.readline()
	f2w.write(x)
	count += 1
