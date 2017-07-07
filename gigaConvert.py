#!/usr/bin/env python3

"""
gigaConvert takes data from the GIGA.pl Pearl program and puts it in data frames that can be used to make
graph files that can be used by network visualisation software.
Robin Shaw
June 2017
"""
# Packages
import re


# Functions
''' 
    Load text GIGA output into an file object
    Input - none
    Output - file object
'''
def openTxt(outTxt):
    try:
        txtFile = open(outTxt, "r")
        return txtFile
    except:
        print ("Sorry, default file not found.")
        exit()

''' 
    Load gdl GIGA output into an file object
    Input - none
    Output - file object
'''
def openGDL(outGDL):
    try:
        gdlFile = open(outGDL, "r")
        return gdlFile
    except:
        print("Sorry, file not found.")
        exit()


''' 
Main code block to fill dictionaries
'''
def mainGiga(outTxt, outGDL):
    # Main code block

    # Variables
    ''' omiDiction is a dictionary that contains information on all the genes
        omiDiction[gene title]:[id, gene ontology information, overall rank of the gene]
    '''
    global omiDiction
    omiDiction = {}
    omiID = 0
    ''' funClasses is a dictionary that contains information on each of the functional classes
        funClasses[functional class/subgraph name]:[[meta],[fcList],[omicronList]]
        meta is a list of other metadata 
        fcList is a list of edges [source id, target id, evidence, edge id]
        omicronList is the list of genes in the functional class [title, rank in functional class]
    '''
    global funClasses
    funClasses = {}
    # meta = [title, p, maxR, numOf]
    meta = []
    # fcList is a list of edges [source id, target id, evidence, edge id]
    fcList = []
    # omicronList is the list of genes in the functional class [title, rank in functional class]
    omicronList = []
    subgraph = None
    fcName = None
    numOf = 0
    rFC = 1


    # Open the Default text output
    txtOut = openTxt(outTxt)

    # omiDiction[gene title]:[id, description of omicron, overall rank of the gene]
    # Work through txtOut and get information on the genes and what genes are in which functional classes
    for line in txtOut:
        line = line.rstrip()
        if (line.startswith('total')):
            # end of information load last functional class into funClasses
            funClasses[fcName] = [meta, omicronList]
            break
        elif re.match('[A-Za-z0-9\s]*\s.*', line) is not None:
            # functional class/subgraph information
            # If not the first functional class complete the last functional class entry
            if fcName is not None:
                # construct the entry for the funClasses dictionary
                # print(meta, fcList, omicronList)
                meta.append(numOf)
                funClasses[fcName] = [meta, omicronList]
                # print(fcName, "-", p, "-", rFC, "-", title, "-", numOf)
                meta = []
                omicronList = []
                numOf = 0
                rFC += 1
            # get functional class name and  p value, number of genes
            #fcName = re.findall('^([A-Za-z0-9]*)\s.*', line)[0]
            p = re.findall('.*\s([0-9e.-]+)\s[0-9]+', line)[0]
            #title = re.findall('^[A-Za-z0-9]*\s([\s\S]*)\s[0-9.e-]+\s.*', line)[0]
            # Fix a quirk in the default text that some times splits the title into two
            # if '\t' in title:
            #     title = re.findall('([A-Za-z0-9\s\S]*)\t.*', title)[0]
            maxR = re.findall('.*\s([0-9]*)', line)[0]

            # create meta list
            #meta = [title, p, rFC, maxR]
        elif (line.startswith('-')):
            if (line.startswith('-1-')):
                fcName = re.findall('[-][0-9]+[-]\s([A-Z0-9]*)\s.*', line)[0]
                title = fcName
                r = re.findall('[-]([0-9]+)[-]\s.*', line)[0]
                r = int(r)
                if r > numOf:
                    numOf = r

                # add gene to omiDiction
                if (title not in omiDiction):
                    description = re.findall('[-][0-9]+[-]\s[A-Z0-9]*\s(.*)\s[0-9]*\s[0-9]*', line)[0]
                    rankAll = re.findall('[-][0-9]+[-]\s[A-Z0-9]*\s.*\s[0-9]*\s([0-9]*)', line)[0]
                    omiDiction[title] = [omiID, description, rankAll]
                    omiID += 1
                # add gene to omicronList
                rankFC = re.findall('[-][0-9]+[-]\s[A-Z0-9]*\s.*\s([0-9]*)\s[0-9]*', line)[0]
                omicronList.append([title, rankFC, r])
                meta = [fcName, p, rFC, maxR]
            # omiDiction and omicronList information
            elif (line.startswith('-')):
                title = re.findall('[-][0-9]+[-]\s([A-Z0-9]*)\s.*', line)[0]
                r = re.findall('[-]([0-9]+)[-]\s.*', line)[0]
                r = int(r)
                if r > numOf:
                    numOf = r

                # add gene to omiDiction
                if (title not in omiDiction):
                    description = re.findall('[-][0-9]+[-]\s[A-Z0-9]*\s(.*)\s[0-9]*\s[0-9]*', line)[0]
                    rankAll = re.findall('[-][0-9]+[-]\s[A-Z0-9]*\s.*\s[0-9]*\s([0-9]*)', line)[0]
                    omiDiction[title] = [omiID, description, rankAll]
                    omiID += 1
                # add gene to omicronList
                rankFC = re.findall('[-][0-9]+[-]\s[A-Z0-9]*\s.*\s([0-9]*)\s[0-9]*', line)[0]
                omicronList.append([title, rankFC, r])

    # close the text file
    txtOut.close()

    # Open gdl file and build network between genes(nodes) in functional classes
    gdlOut = openGDL(outGDL)

    # id for the edges
    edgeID = omiID + 1

    anchors = ([anchor for anchor in funClasses])
    fcNum = 0

    # work through gdlOut to get edges for each functional class
    # Information to make up the edges
    # Build up the functional class dictionary
    # funClasses[functional class/subgraph name]:[[meta],[fcList],[omicronList]]
    for line in gdlOut:
        # Get a new Functional Class/subgraph
        if re.match(r'graph:.*"SUBGRAPH ', line) is not None:
            ''' if not the first functional class then load edge info
            into funClasses and then clear variables '''
            if subgraph is not None:
                # add a id to each edge
                for k in range(0, len(fcList), 1):
                    fcList[k].append(omiID)
                    omiID += 1
                # print(subgraph)
                # print(funClasses[subgraph])
                funClasses[subgraph].insert(1, fcList)
                fcList = []
            # Get title and metadata about the subgraph
            subgraph = anchors[fcNum]
            fcNum += 1
        # Get name of source gene
        elif re.match(r'node:.*title: "[^VIRTUAL].*label', line) is not None:
            omiTitle = re.findall(r'title: "([^"]*)"', line)[0]
        # For each gene in Functional Class get id of source and target gene and use this to build edges
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

    # Add last FC to dictionary
    # add a id to each edge
    for k in range(0, len(fcList), 1):
        fcList[k].append(omiID)
        omiID += 1
    funClasses[subgraph].insert(1, fcList)
    fcList = []

    # close file
    gdlOut.close()

    fcs = 0

    # Calculate weight of omicron
    # Ammend omiDiction with the weight of each node
    for omicron in omiDiction:
        weight = 0
        id = omiDiction[omicron][0]
        for subgraph in funClasses:
            for edge in funClasses[subgraph][1]:
                if id in edge:
                    weight += 1
        # add weight to omiDiction
        omiDiction[omicron].append(weight)

    # Print the funClasses
    # for gene in funClasses:
    #     print(gene)
    #     for ls in funClasses[gene]:
    #         print(ls)

def retFC():
    return funClasses

def retGD():
    return omiDiction




