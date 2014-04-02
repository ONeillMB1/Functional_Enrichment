#!/usr/bin/env python

import sys
import os
import getopt
import numpy as np

# This script takes a file with various statistics for genes and outputs the
# required files for the functional enrichment test for the statistic in the
# column provided by the user. Input file should have a header. Column indexing
# begins at 0. Gene names should be in first column.

def get_arguments(argv):
    if len(argv) == 0:
        usage()
        sys.exit()
    inputFile = None
    statColumn = None
    try:
        opts, args = getopt.getopt(argv, "i:c:")
    except getopt.GetoptError:
        usage()
        sys.exit()
    for opt, arg in opts:
        if opt == '-i':
            inputFile = arg
        elif opt == '-c':
            statColumn = int(arg)
    return(inputFile, statColumn)

def usage():
    print "funcEnr_makeFiles.py\n \
        -i <input file>\n \
        -c <column number of statistic>"

def get_data(inputFile, statColumn):
    nameDict = {}
    statList = []
    infile = open(inputFile, 'r')
    for i, line in enumerate(infile):
        if i > 0:
            line = line.strip()
            data = line.split('\t')
            name = data[0]
            try:
                stat = float(data[statColumn])
            except ValueError, e:
                print '%s does not have value for this statistic' % name
            nameDict[name] = stat
            statList.append(stat)
    infile.close()
    return (nameDict, statList)

def calculate_cutoff(statList):
    a = np.array(statList)
    print 'Minimum: %s, Maximum: %s' % (a.min(), a.max())
    print 'Median: %s, Mean: %s' % (np.median(a), np.mean(a))
    bottomCutoff = np.percentile(a, 5)
    topCutoff = np.percentile(a, 95)
    print '5th percentile: %s, 95th percentile: %s' % (bottomCutoff, topCutoff)
    return (bottomCutoff, topCutoff)

def write_files(inputFile, nameDict, bottomCutoff, topCutoff):
    prefix = os.path.splitext(inputFile)[0]
    allFile = open(prefix + '_all.txt', 'w')
    botFile = open(prefix + '_bot.txt', 'w')
    topFile = open(prefix + '_top.txt', 'w')
    for name in nameDict:
        allFile.write(name + '\n')
        if nameDict[name] < bottomCutoff:
            botFile.write(name + '\n')
        elif nameDict[name] > topCutoff:
            topFile.write(name + '\n')
    allFile.close()
    botFile.close()
    topFile.close()

inputFile, statColumn = get_arguments(sys.argv[1:])

if inputFile is None or statColumn is None:
    usage()
    sys.exit()

nameDict, statList = get_data(inputFile, statColumn)
bottomCutoff, topCutoff = calculate_cutoff(statList)
write_files(inputFile, nameDict, bottomCutoff, topCutoff) 
