#!/usr/bin/env python

import sys
import os
import getopt

# This script read a file output by KAAS with KEGG Orthology (KO) assignments
# for each gene in the analysis and produces a file for futher analysis of  
# functional enrichment.

def usage():
    print "funcEnr_readKEGGOrthology.py <input file>"

if len(sys.argv) != 2:
    usage()
    sys.exit()

inFile = open(sys.argv[1], 'r')
outFile = open(os.path.splitext(sys.argv[1])[0] + '_KOcategories.txt', 'w')

category = ""
for line in inFile:
    line = line.strip()
    if line[0] == 'C':
        category = line.split()[1]
    if line[0] == 'D':
        outFile.write(line.split()[1][:-1] + '\t' + category + '\n')

inFile.close()
outFile.close()

