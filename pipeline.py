#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python wrapper for the creation of GIGA subgraphs
Created on Mon May 29 20:12:57 2017

@author: Robin Shaw
"""

import subprocess
import gigaConvert
import json_create
import key
import htmlgraphs
import argparse

#   main function which takes an parsed argument parser object
def main(args):

    # This does NOT work needs to be fixed.
    # If default called use the yeast files
    if args.default:
        dataAddress = "--IDelRisi_expr.txt"
        networkAddress = "-NYeastNetwork.txt"
        namesAddress = "-GYeastGeneAnnot.txt"
        outName = "-OoutTxt.txt"
    else:
        #   Load arguments into variables
        dataAddress = "-I" + args.data
        networkAddress = "-N" + args.network
        namesAddress = "-G" + args.names
        outName = "-O" + args.out

    # Check
    print (dataAddress, networkAddress, namesAddress, outName)

    #   Check to see if the files exist or not


    # # Run perl GIGA program to get gdl file
    # giga = ['perl','giga.pl','-IDelRisi_expr.txt','-NYeastNetwork.txt','-GYeastGeneAnnot.txt','-Ftxt','-OoutTxt.txt']
    # subprocess.call(giga)
    # # Run perl GIGA program again to get the default text file
    # gigaTxt = ['perl','giga.pl','-IDelRisi_expr.txt','-NYeastNetwork.txt','-GYeastGeneAnnot.txt','-Fgdl','-Oout.gdl']
    # subprocess.call(gigaTxt)


    # defaulttext = subprocess.run(giga, stdout=subprocess.PIPE).stdout.decode('utf-8')
    # this extracts the standard output of the program run. However as it is not the default text it is of limited use.


    # # extract giga.pl information into dictionaries
    # gigaConvert.mainGiga()
    # funClasses = gigaConvert.retFC()
    # geneDiction = gigaConvert.retGD()
    #
    # # Build the key file in text
    # key.buildTxt(funClasses, geneDiction)
    #
    # htmlgraphs.main(funClasses, geneDiction)
    #
    #
    # # Create the JSON file
    # json_create.main(funClasses, geneDiction)

    # Convert output to gml
    # subprocess.call(['/Library/Frameworks/Python.framework/Versions/3.6/bin/python3', 'gigaConvert.py'])

    # # Open cytoscope with file
    # # java -Xmx512M -jar cytoscape.jar [OPTIONS]
    # # -N,--network <file>     Load a network file (any format)
    # cyto = ['/Applications/Cytoscape_v3.5.1/cytoscape.sh', '-N', 'cyto_01.gml']
    # subprocess.call(cyto)


#   Get arguments from the command line or run with defaults
parser = argparse.ArgumentParser()

#   File system address of the arguments
parser.add_argument("data",  help="Experimental data")
parser.add_argument("network",  help="Evidence Network")
parser.add_argument("names",  help="Names of omics")

parser.add_argument("out", help="Name of output (no extension required")

#   Optional arguments for sparce networks, not html page, and gml rather than json
parser.add_argument("-s", "--sparce",  action="store_true", help="Use a sparce network")
parser.add_argument("-nh", "--nohtml",  action="store_true", help="Do not make the html")
parser.add_argument("-gml",  action="store_true", help="Make a gml rather than cytoscape JSON")

#   Default to load the yeast data
parser.add_argument("-d", "--default", action="store_true", help="Load default data")

#   parse the command line
args = parser.parse_args()

#   Run the main function and pass args
main(args)