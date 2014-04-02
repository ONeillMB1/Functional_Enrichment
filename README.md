Functional_Enrichment
=====================

Scripts for functional enrichment analysis

###funcEnr_makeFiles.py

This script takes a file with various statistics for genes and outputs the
required files for the functional enrichment test for the statistic in the
column provided by the user. Input file should have a header. Column indexing
begins at 0. Gene names should be in first column.

Requirements: NumPy
Current Versions: Python 2.7.3, NumPy 1.6.1

Usage: funcEnr_makeFiles.py -i [input file name] -c [column number of statistic to be analyzed]
