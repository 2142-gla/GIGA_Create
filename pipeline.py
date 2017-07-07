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
import os.path

#   main function which takes an parsed argument parser object
def main(args):

    # Variable to hold if found all files
    found = [True, True, True]

    # Name to be used for all future files
    out = args.out

    # If default called use the yeast files instead
    if args.default:
        dataAddress = "-IDelRisi_expr.txt"
        networkAddress = "-NYeastNetwork.txt"
        namesAddress = "-GYeastGeneAnnot.txt"
        outTxt = "-OoutTxt.txt"
        outGDL = "-OoutGDL.gdl"
        out = "DelRisi"
    else:
        #   Load arguments into variables
        dataAddress = "-I" + args.data
        networkAddress = "-N" + args.network
        namesAddress = "-G" + args.names
        outTxt = "-O" + args.out + ".txt"
        outGDL = "-O" + args.out + ".gdl"


    # Change network address if -s --sparse flag used
    if args.sparce:
        networkAddress = "-X"+ args.network

        # Check
    #print (dataAddress, networkAddress, namesAddress, outTxt, outGDL)

    #   Check to see if the files exist or not
    if not args.default:
        if not os.path.isfile(args.data):
            found[0] = False
        if not os.path.isfile(args.network):
            found[1] = False
        if not os.path.isfile(args.names):
            found[2] = False

        if False in found:
            print ("Program exited.")
            if found[0] == False:
                print ("Can't find evidence file.")
            if found[1] == False:
                print("Can't find network file.")
            if found[2] == False:
                print("Can't find annotation file.")
            exit()


    # # Run perl GIGA program to get gdl file
    # giga = ['perl','giga.pl', dataAddress, networkAddress, namesAddress, '-Ftxt',outTxt]
    # subprocess.call(giga)
    # # Run perl GIGA program again to get the default text file
    # gigaTxt = ['perl','giga.pl', dataAddress, networkAddress, namesAddress, '-Fgdl',outGDL]
    # subprocess.call(gigaTxt)

    # Make filenames to pass to dictionary
    outTxt = outTxt[2:]
    outGDL = outGDL[2:]

    #print (outTxt, outGDL)

    # extract giga.pl information into dictionaries
    gigaConvert.mainGiga(outTxt, outGDL)
    funClasses = gigaConvert.retFC()
    geneDiction = gigaConvert.retGD()

    #   Unless flagged make html summary page
    if not args.nohtml:
        htmlgraphs.main(funClasses, geneDiction, out)
        # Open the html in a browser
    #
    # # If only making the html file skip making the graph files
    # if not args.html:
    #     # Create the JSON file and open cytoscape unless flagged not to
    #     if not args.gml:
    #         # Need to use argument name for filename
    #         outJson = args.out + ".cyjs"
    #         json_create.main(funClasses, geneDiction, outJson)
    #         # Build the key file in text
    #         key.buildTxt(funClasses, geneDiction)
    #         # Open cytoscope with file
    #         # java -Xmx512M -jar cytoscape.jar [OPTIONS]
    #         # -N,--network <file>     Load a network file (any format)
    #         cyto = ['/Applications/Cytoscape_v3.5.1/cytoscape.sh', '-N', ]
    #         subprocess.call(cyto)
    #     else:
    #         print()
    #         # Convert output to gml - need to fix this
    #         # subprocess.call(['/Library/Frameworks/Python.framework/Versions/3.6/bin/python3', 'gigaConvert.py'])

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
parser.add_argument("--html",  action="store_true", help="Only make the html")

#   Default to load the yeast data
parser.add_argument("-d", "--default", action="store_true", help="Load default data")

#   parse the command line
args = parser.parse_args()

#   Run the main function and pass args
main(args)