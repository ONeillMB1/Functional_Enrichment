#!/usr/bin/env python

import sys

# This script produces a counts file for the Fisher's Exact test of the
# functional enrichment analysis.

def usage():
    print "FuncEnr_counts.py <Gene Set File> <Sample Prefix>"

def get_categories(geneSetFile):
    """ Makes a dictionary of categories and their corresponding genes for files
    that a formatted as a list of genes with their categories"""
    catDict = {}
    catFile = open(geneSetFile, 'r')
    for line in catFile:
        line = line.strip()
        line = line.split('\t')
        cat = line[1]
        gene = line[0].split()[0]
        if cat in catDict:
            catDict[cat].append(gene)
        else:
            catDict[cat] = [gene]
    return catDict

def get_categories2(geneSetFile):
    """ Makes a dictionary of categories and their corresponding genes for
    files that are formatted as a list of cateogories with their genes"""
    catDict = {}
    catFile = open(geneSetFile, 'r')
    for line in catFile:
        line = line.strip()
        line = line.split('\t')
        cat = line[0]
        catDict[cat] = line[2].split()
    return catDict

def get_genes(prefix, percentile):
    """ Gets a list of genes from three files. One representing all genes in a
    sample, one representing the upper tail of a distribution of those genes,
    and one representing the lower tail of a distribution of those genes. """
    allList = []
    botList = []
    topList = []
    allFile = open(prefix + '_all.txt', 'r')
    botFile = open(prefix + '_bot' + percentile + '.txt', 'r')
    topFile = open(prefix + '_top' + percentile + '.txt', 'r')
    for line in allFile:
        line = line.strip()
        allList.append(line)
    for line in botFile:
        line = line.strip()
        botList.append(line)
    for line in topFile:
        line = line.strip()
        topList.append(line)
    allFile.close()
    botFile.close()
    topFile.close()
    return (allList, botList, topList)

def get_counts(catDict, allList, botList, topList):
    countsDict = {}
    for key in catDict:
        countsDict[key] = {}
        countsDict[key]['totalGenes'] = len(catDict[key])
        catSet = set(catDict[key])
        allSet = set(allList)
        botSet = set(botList)
        topSet = set(topList)
        allinCat = allSet.intersection(catSet)
        topinCat = topSet.intersection(catSet)
        botinCat = botSet.intersection(catSet)
        alldiffCat = allSet.difference(catSet)
        topdiffCat = topSet.difference(catSet)
        botdiffCat = botSet.difference(catSet)
        countsDict[key]['totalGenesInSample'] = len(allinCat)
        countsDict[key]['sampleGenesNotCat'] = len(alldiffCat)
        countsDict[key]['topGenesInSample'] = len(topinCat)
        countsDict[key]['topGenesNotCat'] = len(topdiffCat)
        countsDict[key]['botGenesInSample'] = len(botinCat)
        countsDict[key]['botGenesNotCat'] = len(botdiffCat)   
    return countsDict

def write_files(prefix, percentile, countsDict):
    botCountFile = open(prefix + '_bot' + percentile + '_counts.txt', 'w')
    topCountFile = open(prefix + '_top' + percentile + '_counts.txt', 'w')
    for key in countsDict:
        botCountFile.write("%s\t%i\t%i\t%i\t%i\t%i\n" %
        (key, countsDict[key]['botGenesInSample'],
        countsDict[key]['totalGenesInSample'],
        countsDict[key]['botGenesNotCat'],
        countsDict[key]['sampleGenesNotCat'], countsDict[key]['totalGenes']))
        topCountFile.write("%s\t%i\t%i\t%i\t%i\t%i\n" %
        (key, countsDict[key]['topGenesInSample'],
        countsDict[key]['totalGenesInSample'],
        countsDict[key]['topGenesNotCat'],
        countsDict[key]['sampleGenesNotCat'], countsDict[key]['totalGenes']))
    botCountFile.close()
    topCountFile.close()

if len(sys.argv) != 3:
    usage()
    sys.exit(0)
geneSetFile, prefix = sys.argv[1:]
catDict = get_categories(geneSetFile)
for percentile in ['1', '5', '10']:
    allList, botList, topList = get_genes(prefix, percentile)
    countsDict = get_counts(catDict, allList, botList, topList)
    write_files(prefix, percentile, countsDict)
