#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Python wrapper for the creation of GIGA subgraphs.
Can create .gml and .cyjs files for visualisation Software.
Also can make a summary html file
Created on Mon May 29 20:12:57 2017

@author: Robin Shaw

Args:
    Positional arguments:
    data - File path for experimental data.
    network - File path for biological network.
    names - File path for omicon annotation file.
    out - Prefix for the visualisation files to be created.

    Optional arguments:
    -s, --sparce    - Use a sparce network.
    -nh, --nohtml   - Do not make the html summary file.
    -gml            - Make a gml rather than cytoscape JSON file.
    --html          - Only make the html summary file.
    -d, --default   - Use the default Yeast data-set.

"""
"""Standard modules used; subprocess, argparse, and os."""
import subprocess
import argparse
import os.path
""" Non-standard modules used; gigaConvert, json_create, key, htmlgraphs, gml_create.
    See modules doctype for functionality."""
import gigaConvert
import json_create
import key
import htmlgraphs
import gml_create

def checkFileExist(args):
    """ Check if all necessary files exist.

        Args:
            Parsed 'argparse' argument parser object."""

    #   Variable to hold if found all files
    found = [True, True, True]

    #   Check for each parameter if the file exists
    if not args.default:
        if not os.path.isfile(args.data):
            found[0] = False
        if not os.path.isfile(args.network):
            found[1] = False
        if not os.path.isfile(args.names):
            found[2] = False

    #   If file not found state which one is absent and close program
    if False in found:
        print("Program exited.")
        if found[0] is False:
            print("Can't find evidence file.")
        if found[1] is False:
            print("Can't find network file.")
        if found[2] is False:
            print("Can't find annotation file.")
        exit()

def is_int(mStr):
    """ Confirm if a string can be converted into a integer.

        Return:
            True if string can be converted.
            False if it cannot be converted.
        Raises:
            Try/except block will catch a ValueError if string cannot be converted into a integer.
        """
    try:
        int(mStr)
        return True
    except ValueError:
        return False

def main(args):
    """Main function takes arguments and calls modules to create
    required visualisation file.

        Args:
            Takes an parsed argparse parser object."""

    # Name to be used for all future files
    fileName = args.out

    # If default called use the yeast files instead
    if args.default:
        dataAddress = "-IDelRisi_expr.txt"
        networkAddress = "-NYeastNetwork.txt"
        namesAddress = "-GYeastGeneAnnot.txt"
        outTxt = "-OoutTxt.txt"
        outGDL = "-OoutGDL.gdl"
        fileName = "DelRisi"
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

    #   Check to see if the files exist or not
    checkFileExist(args)

    # Create basic arguments for the Perl GiGA call
    giga = ['perl', 'giga.pl', dataAddress, networkAddress, namesAddress, '-Ftxt', outTxt]
    gigaTxt = ['perl', 'giga.pl', dataAddress, networkAddress, namesAddress, '-Fgdl', outGDL]

    #   Append call to Perl GiGA depending on arguments
    if args.m is not None and is_int(args.m):
        giga.append("-M " + args.m)

    if args.r:
        giga.append("-R")

    # Run perl GIGA program to get gdl file
    subprocess.call(giga)
    # Run perl GIGA program again to get the default text file
    subprocess.call(gigaTxt)

    # Make filenames to pass to dictionary by stripping Perl GiGA flags from variable.
    outTxt = outTxt[2:]
    outGDL = outGDL[2:]

    # extract giga.pl information into dictionaries
    gigaConvert.mainGiga(outTxt, outGDL)
    funClasses = gigaConvert.retFC()
    omiDiction = gigaConvert.retGD()

    #   Unless flagged make html summary page
    if not args.nohtml:
        htmlgraphs.main(funClasses, omiDiction, fileName)
        # Open the html in a browser
        # use the webbrowser module

    # If only making the html file skip making the graph files
    if not args.html:
        # Create the JSON file and open cytoscape unless flagged not to
        if not args.gml:
            # Need to use argument name for filename
            outJson = fileName + ".cyjs"
            json_create.main(funClasses, omiDiction, outJson)
            # Build the key file in text
            key.buildTxt(funClasses, omiDiction)
        else:
            # Convert output to gml - need to fix this
            gml_create()

""" Use argparse to extract the arguments from the command line."""
#   Get arguments from the command line or run with defaults
parser = argparse.ArgumentParser()

#   File system address of the arguments
parser.add_argument("data",  help="Experimental data")
parser.add_argument("network",  help="Evidence Network")
parser.add_argument("names",  help="Names of omics")

parser.add_argument("out", help="Name of output (no extension required")

#   Optional arguments for sparce networks, not html page, and gml rather than json
parser.add_argument("-s", "--sparce",  action="store_true", help="Use a sparce network.")
parser.add_argument("-nh", "--nohtml",  action="store_true", help="Do not make the html summary file.")
parser.add_argument("-gml",  action="store_true", help="Make a gml rather than cytoscape JSON file.")
parser.add_argument("--html",  action="store_true", help="Only make the html")
parser.add_argument("-m", action="store", help="Set the maximum size of the sub-graphs. Default is 20 omicrons.")
parser.add_argument("-r", action="store_true", help="See the results of a random permutation of the data.")
parser.add_argument("-j", action="store_true", help="Output sub-graphs as plain JSON files.")

#   Default to load the yeast data
parser.add_argument("-d", "--default", action="store_true", help="Load default data")

#   parse the command line
args = parser.parse_args()

#   Run the main function and pass args object
main(args)
