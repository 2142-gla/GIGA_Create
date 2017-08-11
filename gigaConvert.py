#!/usr/bin/env python3
""" Takes data from the GIGA.pl Perl program and puts it in data frames that can be used to make graph files
    that can be used by network visualisation software.

    Robin Shaw
    June 2017

    Args:
        Filename of Perl GiGA.pl text data file
        Filename of Perl GiGA.pl gdl data file
"""

""" Import regular expressions re module"""
import re


# Functions
def openTxt(outTxt):
    """Load GiGA.pl text data file into an file object.

        Args:
            Filename of text data file.

        Returns:
            File object of text data file.
    """
    try:
        txtFile = open(outTxt, "r")
        return txtFile
    except:
        print ("Sorry, Giga out text file not found.")
        exit()

def openGDL(outGDL):
    """ Load GiGA.pl gdl data file into an file object

        Args:
            gdl filename.

        Returns:
            File object of gdl data file.
    """
    try:
        gdlFile = open(outGDL, "r")
        return gdlFile
    except:
        print("Sorry, file not found.")
        exit()

def checkAnchor(fcName):
    """ Check if there the anchor omicon is already used by
    another subgraph. If so add '-' to end of name.

        Args:
            Omicon name as string variable.

        Returns:
            Omicon name as string variable. Either changed or not
    """
    if fcName in funClasses:
        fcName = fcName + '-'
        checkAnchor(fcName)

    return fcName


def mainGiga(outTxt, outGDL):
    """Main function to control the flow of the program.

    Args:
        String variable of the Filename of the text data file.
        String variable of the Filename of the gdl data file."""

    # Variables
    """ omiDiction is a dictionary that contains information on all the omicons
        omiDiction[omicon title]:[id, omicon ontology information, overall rank of the omicon]
    """
    global omiDiction
    omiDiction = {}
    omiID = 0
    """ funClasses is a dictionary that contains information on each of the functional classes
        funClasses[functional class/subgraph name]:[[meta],[fcList],[omiconList]]
        meta is a list of other metadata 
        fcList is a list of edges [source id, target id, evidence, edge id]
        omiconList is the list of omicons in the functional class [title, rank in functional class]
    """
    global funClasses
    funClasses = {}
    # meta = [title, p, maxR, numOf]
    meta = []
    # fcList is a list of edges [source id, target id, evidence, edge id]
    fcList = []
    # omiconList is the list of omicons in the functional class [title, rank in functional class]
    omiconList = []
    subgraph = None
    fcName = None
    numOf = 0
    rFC = 1

    # Open the Default text output
    txtOut = openTxt(outTxt)

    # omiDiction[omicon title]:[id, description of omicon, overall rank of the omicon]
    # Work through txtOut and get information on the omicons 
    # and what omicons are in which functional classes.
    for line in txtOut:
        line = line.rstrip()

        if (line.startswith('total')):
            # end of information load last functional class into funClasses

            #   If the anchor omicon is already read used add '-' extension
            fcName = checkAnchor(fcName)

            funClasses[fcName] = [meta, omiconList]
            break
        elif re.match('[A-Za-z0-9\s]*\s.*', line) is not None:
            # functional class/subgraph information
            # If not the first functional class complete the last functional class entry
            if fcName is not None:
                # construct the entry for the funClasses dictionary

                #   If the anchor omicon is already used call 
                # checkAnchor() to add '-' extension to name.
                fcName = checkAnchor(fcName)

                meta.append(numOf)
                funClasses[fcName] = [meta, omiconList]
                meta = []
                omiconList = []
                numOf = 0
                rFC += 1
            # Get functional class name, p value, 
            # and number of omicons in subgraph.
            p = re.findall('.*\s([0-9e.-]+)\s[0-9]+', line)[0]
            maxR = re.findall('.*\s([0-9]*)', line)[0]

            # create meta list
            # meta = [title, p, rFC, maxR]
        elif (line.startswith('-')):
            if (line.startswith('-1-')):
                fcName = re.findall('[-][0-9]+[-]\s([A-Za-z0-9]*)\s.*', line)[0]
                title = fcName
                r = re.findall('[-]([0-9]+)[-]\s.*', line)[0]
                r = int(r)
                if r > numOf:
                    numOf = r

                # add omicon to omiDiction
                if (title not in omiDiction):
                    description = re.findall('[-][0-9]+[-]\s[A-Za-z0-9]*\s(.*)\s[0-9]*\s[0-9]*', line)[0]
                    rankAll = re.findall('[-][0-9]+[-]\s[A-Za-z0-9]*\s.*\s[0-9]*\s([0-9]*)', line)[0]
                    omiDiction[title] = [omiID, description, rankAll]
                    omiID += 1

                # add omicson to omiconList
                rankFC = re.findall('[-][0-9]+[-]\s[A-Za-z0-9]*\s.*\s([0-9]*)\s[0-9]*', line)[0]
                omiconList.append([title, rankFC, r])
                meta = [fcName, p, rFC, maxR]
            # omiDiction and omiconList information
            elif (line.startswith('-')):
                title = re.findall('[-][0-9]+[-]\s([A-Za-z0-9]*)\s.*', line)[0]
                r = re.findall('[-]([0-9]+)[-]\s.*', line)[0]
                r = int(r)
                if r > numOf:
                    numOf = r

                # add omicon to omiDiction
                if (title not in omiDiction):
                    description = re.findall('[-][0-9]+[-]\s[A-Za-z0-9]*\s(.*)\s[0-9]*\s[0-9]*', line)[0]
                    rankAll = re.findall('[-][0-9]+[-]\s[A-Za-z0-9]*\s.*\s[0-9]*\s([0-9]*)', line)[0]
                    omiDiction[title] = [omiID, description, rankAll]
                    omiID += 1
                # add omicon to omiconList
                rankFC = re.findall('[-][0-9]+[-]\s[A-Za-z0-9]*\s.*\s([0-9]*)\s[0-9]*', line)[0]
                omiconList.append([title, rankFC, r])

    # close the text file
    txtOut.close()

    # Open gdl data file and build network between omicons(nodes) in functional classes.
    gdlOut = openGDL(outGDL)

    # id for the edges
    edgeID = omiID + 1

    anchors = ([anchor for anchor in funClasses])
    fcNum = 0

    # Work through gdlOut to get edges for each functional class,
    # information to make up the edges, and
    # build up the functional class dictionary.
    # funClasses[anchor/subgraph name]:[[meta],[fcList],[omiconList]]
    for line in gdlOut:
        # Get a new Functional Class/subgraph
        if re.match(r'graph:.*"SUBGRAPH ', line) is not None:
            ''' if not the first functional class then load edge info
            into funClasses and then clear variables '''
            if subgraph is not None:
                # add a id to each edge
                for k in range(0, len(fcList), 1):
                    fcList[k].append(omiID)
                funClasses[subgraph].insert(1, fcList)
                fcList = []
            # Get title and metadata about the subgraph
            subgraph = anchors[fcNum]
            fcNum += 1
        # Get name of source omicon
        elif re.match(r'node:.*title: "[^VIRTUAL].*label', line) is not None:
            omiTitle = re.findall(r'title: "([^"]*)"', line)[0]
        # For each omicon in Functional Class get id of source and target omicon and use this to build edges
        elif re.match(r'edge:.*', line) is not None:
            if re.match(r'edge:.*source:"[^VIRTUAL]', line):
                id1 = omiDiction[omiTitle][0]
                id2 = omiDiction[re.findall(r'.*source:"(\S*)"', line)[0]][0]
                # Sort id's by size
                if id1 > id2:
                    n = id1
                    id1 = id2
                    id2 = n
                evidence = re.findall(r'.*target: "(.*)"', line)[0]
                edge = [id1, id2, evidence]

                # Check if edge is already in list
                if edge not in fcList:
                    fcList.append(edge)

    # Add the last Functional Class to the dictionary and
    # add a id to each edge.
    for k in range(0, len(fcList), 1):
        fcList[k].append(omiID)
        omiID += 1
    funClasses[subgraph].insert(1, fcList)
    fcList = []

    # close file
    gdlOut.close()

    # Calculate degree for each omicon in each subgraph
    for omicon in omiDiction:
        degree = 0
        id = omiDiction[omicon][0]
        for subgraph in funClasses:
            for edge in funClasses[subgraph][1]:
                if id == edge[0] or id == edge[1]:
                    degree += 1
        # add weight to omiDiction
        omiDiction[omicon].append(degree)


def retFC():
    """ Returns the funClasses dictionary data structure. This contains
    information on all the sub-graphs/functional classes.

    Returns:
        funClasses data structure"""
    return funClasses

def retGD():
    """Returns the omiDiction data structure. This contains information on
    all the omicons.

    Returns:
        omiDiction"""
    return omiDiction




