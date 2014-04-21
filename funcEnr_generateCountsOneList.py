#!/usr/bin/env python

import sys
import os

# This script produces a counts file for the Fisher's Exact test of the
# functional enrichment analysis. It needs a list of genes and their
# categories and a list of genes of interest.

def usage():
    print "FuncEnr_counts.py <Gene Categories File> <Genes of Interest File>"

def get_categories(geneSetFile):
    """ Makes a dictionary of categories and their corresponding genes for files
    that a formatted as a list of genes with their categories"""
    catDict = {}
    allList = []
    catFile = open(geneSetFile, 'r')
    for line in catFile:
        line = line.strip()
        line = line.split('\t')
        if len(line) == 1:
            cat = "undefined"
        else:
            cat = line[1]
        gene = line[0].split()[0]
        allList.append(gene)
        if cat in catDict:
            catDict[cat].append(gene)
        else:
            catDict[cat] = [gene]
    return (catDict, allList)

def get_genes(genesListFile):
    """ Gets a list of genes from file containing genes of interest. """
    geneList = []
    geneFile = open(genesListFile, 'r')
    for line in geneFile:
        line = line.strip()
        geneList.append(line)
    geneFile.close()
    return geneList

def get_counts(catDict, allList, geneList):
    countsDict = {}
    for key in catDict:
        countsDict[key] = {}
        countsDict[key]['totalGenes'] = len(catDict[key])
        catSet = set(catDict[key])
        allSet = set(allList)
        geneSet = set(geneList)
        allinCat = allSet.intersection(catSet)
        geneinCat = geneSet.intersection(catSet)
        alldiffCat = allSet.difference(catSet)
        genediffCat = geneSet.difference(catSet)
        countsDict[key]['totalGenesInSample'] = len(allinCat)
        countsDict[key]['sampleGenesNotCat'] = len(alldiffCat)
        countsDict[key]['genesInSample'] = len(geneinCat)
        countsDict[key]['genesNotCat'] = len(genediffCat)
    return countsDict

def write_files(genesListFile, countsDict):
    prefix = os.path.splitext(genesListFile)[0]
    countFile = open(prefix + '_counts.txt', 'w')
    for key in countsDict:
        countFile.write("%s\t%i\t%i\t%i\t%i\t%i\n" %
        (key, countsDict[key]['genesInSample'],
        countsDict[key]['totalGenesInSample'],
        countsDict[key]['genesNotCat'],
        countsDict[key]['sampleGenesNotCat'], countsDict[key]['totalGenes']))
    countFile.close()

if len(sys.argv) != 3:
    usage()
    sys.exit(0)
geneSetFile, genesListFile = sys.argv[1:]
catDict, allList = get_categories(geneSetFile)
geneList = get_genes(genesListFile)
countsDict = get_counts(catDict, allList, geneList)
write_files(genesListFile, countsDict)
