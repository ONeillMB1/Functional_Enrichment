#!/usr/bin/env python

import sys
from collections import defaultdict

#if len(sys.argv) != 5 :
#	print("Usage:  counts.py  <GeneSetFile.txt> <totsamplefile.txt> <candidatesample> <OutputFile.txt>")
#	sys.exit(0)

#progname,genesetfilename,totsampfilename,candsampfilename,outfilename = sys.argv

#geneset = raw_input("GeneSetFileName: ")
#sample = raw_input("sample: ")
tail = raw_input("top or bot :")


for i in ["a1", "a2", "a3", "b2", "c1", "c2", "a12", "a23", "a13", "b12", "c12"] :
    sample = i

    catdic = {}
#with open(genesetfilename, 'r') as genesetfile:
    with open("/home/peplab/data/marydata/intrahost/bin/gowinda/genesets/func_cat/corrected/GeneSet.txt", 'r') as genesetfile:
        for line in genesetfile:
            key, des, values = line.strip().split('\t')
            catdic[key] = (values.split(" "))

    totdic = defaultdict(list)
    candic = defaultdict(list)
    totlist = []
    candlist = []

#with open(totsampfilename, 'r') as totfile:
    with open(sample + '_all.txt', 'r') as totfile:
        for line in totfile:
            gene = line.strip()
            totlist.append(gene)

#with open(candsampfilename, 'r') as candfile:
    with open(sample + '_' + tail + '.txt', 'r') as candfile:
        for line in candfile:
            gene = line.strip()
            candlist.append(gene)

    print(len(totlist))
    print(len(candlist))

#with open(totsampfilename, 'r') as totsampfile:
    with open(sample + '_all.txt', 'r') as totsampfile:
        for key in catdic:
            totsampfile.seek(0)
            for line in totsampfile:
                gene = line.strip()
                if gene in catdic[key]:
                    totdic[key].append(gene)
                   
#with open(candsampfilename, 'r') as candsampfile:
    with open(sample + '_' + tail + '.txt', 'r') as candsampfile:
        for key in catdic:
            candsampfile.seek(0)
            for line in candsampfile:
                gene = line.strip()
                if gene in catdic[key]:
                    candic[key].append(gene)

    print(len(totdic))
    print(len(candic))
    print(len(catdic))

    with open(sample + '_' + tail + '_FIN' + '.counts', 'w') as outfile:               
        for key in catdic:
            outfile.write(key + '\t' + str(len(candic[key])) + '\t' + str(len(totdic[key])) + '\t' + str(len(candlist)-len(candic[key])) + '\t' + str(len(totlist)-len(totdic[key])) + '\t' + str(len(catdic[key])) + '\n')
