Functional_Enrichment
=====================

Scripts for functional enrichment analysis

###funcEnr_makeFiles.py

This script takes a file with various statistics for genes and outputs the
required files for the functional enrichment test for the statistic in the
column provided by the user. Input file should have a header. Column indexing
begins at 0. Gene names should be in first column. Script outputs members of 
the top & bottom 1%, 5%, and 10% of the distribution of the statistic.

Requirements: NumPy

Current Versions: Python 2.7.3, NumPy 1.6.1

Usage: funcEnr_makeFiles.py -i [input file name] -c [column number of statistic to be analyzed]

###FuncEnr_GenerateCounts.py

This script generates counts for a Fisher's Exact Test of functional enrichment. 
It looks for files in the format output by funcEnr_makeFiles.py. Inputs to the 
script are a file describing the genes in each category and the prefix of the
files output by funcEnr_makeFiles.py. The gene set file can be in one of two 
formats (the first is the default):
>gene1  category

>gene2  category

or

>category1  description gene1 gene2 gene3

>category2  description gene4 gene5

Current Versions: Python 2.7.3

Usage: FuncEnr_GenerateCounts.py [gene set file] [prefix]

###funcEnr_generateCountsOneList.py

This script generates counts for a Fisher's Exact Test of functional enrichment. 
It is designed to work on one list of genes at a time as opposed to FuncEnr_GenerateCounts.py,
which looks for genes in the top 1,5,& 10% of a distribution as output by funcEnr_makeFiles.py.
Inputs to the script are a file describing the genes in each category and a file with a list of
the genes of interest. 

Current Versions: Python 2.7.3

Usage: funcEnr_generateCountsOneList.py [gene set file] [genes of interest file]


###FuncEnr_FindSig.R

This script performs a Fisher's Exact Test on count files produced by FuncEnr_GenerateCounts.py.
It will attempt to perform the test on each file in the current directory, so directory should
only contain counts files. It also performs a multiple test correction. 
Two files are output for each counts file. One describing significance for every category, and
one that describes only those with significance < .05 after correction.

Current Versions: R 3.1.0

Usage: FuncEnr_FindSig.R 

###funcEnr_readKEGGOrthology.py

This script read a file output by KAAS with KEGG Orthology (KO) assignments
for each gene in the analysis and produces a file for futher analysis of  
functional enrichment.

Current Versions: Python 2.7.3

Usage: funcEnr_readKEGGOrthology.py [input file]
