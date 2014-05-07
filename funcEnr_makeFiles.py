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
    noData = [None]
    try:
        opts, args = getopt.getopt(argv, "i:c:n:")
    except getopt.GetoptError:
        usage()
        sys.exit()
    for opt, arg in opts:
        if opt == '-i':
            inputFile = arg
        elif opt == '-c':
            statColumn = int(arg)
        elif opt == '-n':
            noData = arg
    return(inputFile, statColumn, noData)

def usage():
    print "funcEnr_makeFiles.py\n \
        -i <input file>\n \
        -c <column number of statistic>\n \
        -n <'no,data,values' (default is None)>"

def get_data(inputFile, statColumn, noData):
    nameDict = {}
    statList = []
    infile = open(inputFile, 'r')
    for i, line in enumerate(infile):
        if i > 0:
            line = line.strip()
            data = line.split('\t')
            name = data[0]
            if data[statColumn] not in noData:
                stat = float(data[statColumn])
                nameDict[name] = stat
                statList.append(stat)
            else:
                print '%s does not have value for this statistic' % name

    infile.close()
    return (nameDict, statList)

def calculate_cutoff(statList):
    a = np.array(statList)
    print 'Minimum: %s, Maximum: %s' % (a.min(), a.max())
    print 'Median: %s, Mean: %s' % (np.median(a), np.mean(a))
    bottom1Cutoff = np.percentile(a, 1)
    bottom5Cutoff = np.percentile(a, 5)
    top1Cutoff = np.percentile(a, 99)
    top5Cutoff = np.percentile(a, 95)
    bottom10Cutoff = np.percentile(a, 10)
    top10Cutoff = np.percentile(a, 90)
    print '5th: %s, 95th: %s' % (bottom5Cutoff, top5Cutoff)
    return (bottom1Cutoff, top1Cutoff, bottom5Cutoff, top5Cutoff, 
    bottom10Cutoff, top10Cutoff)

def write_files(inputFile, nameDict, bottom1Cutoff, top1Cutoff, 
    bottom5Cutoff, top5Cutoff, bottom10Cutoff, top10Cutoff):
    prefix = os.path.splitext(inputFile)[0]
    allFile = open(prefix + '_all.txt', 'w')
    bot1File = open(prefix + '_bot1.txt', 'w')
    top1File = open(prefix + '_top1.txt', 'w')
    bot5File = open(prefix + '_bot5.txt', 'w')
    top5File = open(prefix + '_top5.txt', 'w')
    bot10File = open(prefix + '_bot10.txt', 'w')
    top10File = open(prefix + '_top10.txt', 'w')
    for name in nameDict:
        allFile.write(name + '\n')
        if nameDict[name] < bottom1Cutoff:
            bot1File.write(name + '\n')
        if nameDict[name] < bottom5Cutoff:
            bot5File.write(name + '\n')
        if nameDict[name] < bottom10Cutoff:
            bot10File.write(name + '\n')
        if nameDict[name] > top10Cutoff:
            top10File.write(name + '\n')
        if nameDict[name] > top5Cutoff:
            top5File.write(name + '\n')
        if nameDict[name] > top1Cutoff:
            top1File.write(name + '\n')
    allFile.close()
    bot1File.close()
    top1File.close()
    bot5File.close()
    top5File.close()
    bot10File.close()
    top10File.close()

inputFile, statColumn, noData = get_arguments(sys.argv[1:])

if inputFile is None or statColumn is None:
    usage()
    sys.exit()

if len(noData) > 1:
    noData = noData.split(',')

nameDict, statList = get_data(inputFile, statColumn, noData)
bot1Cutoff, top1Cutoff, bot5Cutoff, top5Cutoff, bot10Cutoff, top10Cutoff = calculate_cutoff(statList)
write_files(inputFile, nameDict, bot1Cutoff, top1Cutoff, bot5Cutoff, top5Cutoff,
bot10Cutoff, top10Cutoff) 
