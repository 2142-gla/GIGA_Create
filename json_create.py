#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Take GIGA information and create a JSON file suitable for Cytoscape 

"""

# Make a json file
def nodeJSON(node, gene):
    # Make nodes
    # if gene is a key in funClasses then it is a an anchor gene\
    idnum = geneDiction[gene][0]
    name = gene
    description = geneDiction[gene][1]
    shape = shapeNode(gene)
    colour = colorNode(gene)

    geneDetails = [gd for gd in funClasses[getFC(gene)[0]][2] if gene in gd][0]
    print (geneDetails)
    rankAll = geneDiction[gene][2]
    rankFC = geneDetails[1]

    meta = str(geneDetails[2]) + ": "+ geneDiction[gene][1]

    # node: id, name, description, shape, background colour, transparency, meta information
    #print ((node) % (idnum, name, description, shape, colour[0], colour[1], meta))
    return ((node) % (idnum, name, description, rankAll, rankFC, shape, colour[0], colour[1], meta))

#   Check of the gene is a anchor gene
#   Input: name of the gene
#   Output: Shape of the node
def shapeNode(gene):
    anchors = [anchor for anchor in funClasses]
    if gene in anchors:
        return "Rounded Rectangle"
    else:
        return "Ellipse"

#   From a gene title get the functional classes it belongs to. The functional class are sorted by smallest p
#   Input: gene title
#   Output: list of names of functional classes
def getFC(gene):
    fcGroup = []
    # Check if gene is in the geneList of each Functional Class
    for key in funClasses:
        # If gene found in gene list add the name of the functional class to the fcGroup
        if any(gene in genelist for genelist in funClasses[key][2]):
            fcGroup.append(key)
        #     print(gene, "found")
        # else:
        #     print (gene,"not found")
    #print ("getFC", fcGroup)
    return fcGroup

# #   Create the metadata for the tooltip. This will depend on wither the gene is a anchor or normal gene
# #   Input: gene and shape
# #   Output: string format for meta data
# def metaNode(gene, shape):
#     #print ('metaNode calls getFC')
#     fcGroup = getFC(gene)
#
#     # Need to calculate rank in fc
#     genels = funClasses[fcGroup[0]][2]
#     # Get the rank in functional class for the gene in the main functional class int(funClasses[fcGene][2])
#     rank = int([i[1] for i in genels if i[0] == gene][0])
#     m = 0
#
#     if shape == "Ellipse" and len(fcGroup) > 1:
#         metaFor = ("%s Rank of Gene Overall: %s ") % (gene, geneDiction[gene][2])
#         for fc in fcGroup:
#             genels = funClasses[fcGroup[m]][2]
#             # Get the rank in functional class for the gene in the main functional class int(funClasses[fcGene][2])
#             rank = int([i[1] for i in genels if i[0] == gene][0])
#             addMeta = " Rank in Functional Class %s: %s. " % (fc, funClasses[fc][2][1])
#             metaFor = metaFor + addMeta
#             m += 1
#     elif shape == "Ellipse":
#         metaFor = "%s Rank of Gene Overall: %s. Rank in Functional Class %s: %s"
#         metaFor = metaFor % (geneDiction[gene][1], geneDiction[gene][2], fcGroup[0], rank)
#     else:
#         metaFor = "Subgraph Description: %s. P value: %s. Number of Genes in Class: %s. "
#         metaFor = metaFor % (funClasses[fcGroup[0]][0][0], funClasses[fcGroup[0]][0][1], rank)
#         anchor = "Anchor gene description %s Rank of Gene Overall: %s. Rank in Functional Class %s: %s."
#         anchor = anchor % (geneDiction[gene][1], geneDiction[gene][2], fcGroup[0], rank)
#         metaFor = metaFor + anchor
#
#     return metaFor

#   Creates the colour of the node based on the PC value of the Functional Class and rank in the class
#   Input: name of the gene
#   Output: a list containing rgb of list of the colour and value of the transparency.
def colorNode(gene):
    # dictionary of colour blind safe colours
    colors = {"Vermillion": [213, 94, 0], "Orange": [230, 159, 0], "Yellow": [240, 228, 66],
              "Bluish Green": [0, 158, 115], "Blue": [0, 114, 178], "Sky Blue": [86, 189, 233],
              "Reddish purple": [204, 121, 167]}
    colList = ["Vermillion", "Orange", "Yellow", "Bluish Green", "Sky Blue", "Blue", "Reddish purple"]
    transpLst = [255, 200, 175, 150, 125, 100, 75, 50, 25]

    # Get the main functional class a gene belongs to
    fcGene = getFC(gene)[0]
    # rank of function class in evidence network (based on PC value)
    posFC = 1
    for anchor in funClasses:
        if fcGene == anchor:
            break
        else:
            posFC += 1
    # Variables
    transp = 255
    rgb = []
    genels = funClasses[fcGene][2]
    # Get the rank in functional class for the gene in the main functional class int(funClasses[fcGene][2])
    rank = int([i[1] for i in genels if i[0] == gene][0])
    totalNumGene = funClasses[fcGene][0][3]
    numOfFc = len(funClasses)
    color = ""
    # position of gene in subgraph/functional class
    genePos = [m[2] for m in funClasses[fcGene][2] if gene == m[0]][0]

    # Color of the Functional Class
    if posFC <= 7:
        rgb = colors[(colList[posFC - 1])]
        if (genePos-1) < 9:
            transp = transpLst[genePos - 1]
        else:
            transp = 25
    elif posFC >= 8:
        t = posFC // 7
        if t > 6:
            transp = 25
        else:
            if (genePos + t - 1) < 9:
                transp = transpLst[(genePos + t - 1)]
            else:
                transp = 25
        posFC = posFC % 7
        rgb = colors[(colList[posFC - 1])]

    color = ("rgb(%s, %s, %s)") % (rgb[0], rgb[1], rgb[2])

    return [color, transp]

def edgeJSON(text, link):
    # make edge
    edgeID = link[3]
    source = link[0]
    target = link[1]
    interaction = link[2]
    name = '%s %s %s' % (source, interaction, target)
    edgeFor = text % (edgeID, name, source, target, interaction)
    return edgeFor

#   Open a file to make the json file
#   Input: None
#   Output: file object
def createJS(filename):
    try:
        jsFile = open(filename, 'w')
        return jsFile
    except:
        print ("Can't create file!")
        exit()

def main(fcDiction, geDiction, filename):
    # Variables to hold part of the json text
    top = '{\n\t"elements" : {\n'
    nodetop = '\t\t"nodes" : [\n'
    # node: id, name, go, shape, background, meta
    node = '\t\t{\n\t\t"data" : {\n\t\t\t"id" : "%s",\n\t\t\t"name" :"%s",\n\t\t\t"description": "%s",\n\t\t\t"rankAll" :"%s",\n\t\t\t"rankFC" :"%s", \n\t\t\t"shape": "%s", \n\t\t\t"background": "%s",\n\t\t\t"transparency" : "%s",\n\t\t\t"meta": "%s",  \n\t\t\t"selected":false\n\t\t}'
    comma = ',\n'
    close = ']'
    edgetop = '\t\t"edges" : [ '
    # edge: id, name, source, target, interaction
    edge = '\n\t\t{\n\t\t"data" : {\n\t\t\t"id" : "%s",\n\t\t\t"name" : "%s",\n\t\t\t"source" : "%s",\n\t\t\t"target" : "%s",\n\t\t\t"interaction" : "%s",\n\t\t\t"selected" : false\n\t\t}'
    end = '\n\t}\n}'
    sel = '\t\t"selected" : false\n\t\t}'
    # variables to hold information to put in json text
    # idnum = ""
    # name = ""
    # go = ""
    # shape = ""
    # meta = ""
    # source = ""
    # target = ""
    # interaction = ""
    # Dictionaries with all the information in them
    global funClasses
    global geneDiction
    funClasses = fcDiction
    geneDiction = geDiction

    # Create the JSON file
    jsFile = createJS(filename)

    # print out and create json file
    print(top, end='')
    jsFile.write(top)

    # print node section
    print(nodetop, end='')
    jsFile.write(nodetop)

    # print the nodes
    for n, gene in enumerate(geneDiction):
        print (n, gene)
        if n == len(geneDiction) - 1:
            # last element®
            nodeTxt = nodeJSON(node, gene)
            nodeTxt = nodeTxt + " " + comma + " " + sel

            jsFile.write(nodeTxt)
        else:
            nodeTxt = nodeJSON(node, gene)
            nodeTxt = nodeTxt + " " + comma + " " + sel
            jsFile.write(nodeTxt)
            jsFile.write(comma)

    # close the nodes
    #print(close + comma, end='')
    jsFile.write(close + comma)


    # Start the edges
    #print(edgetop, end='')
    jsFile.write(edgetop)

    # print edge section
    for o, item in enumerate(funClasses):
        fcList = funClasses[item][1]
        for m, link in enumerate(fcList):
            if o == (len(funClasses) - 1) and m == (len(fcList) -1):
                # Last edge
                edgeTxt = edgeJSON(edge, link) + " " + comma + " " + sel
                jsFile.write(edgeTxt)
            else:
                #print(edgeJSON(edge, link), comma, sel, end='')
                edgeTxt = edgeJSON(edge, link) + " " + comma + " " + sel
                jsFile.write(edgeTxt)
                #print(comma, end='')
                jsFile.write(comma)


    #print(close, end='')
    jsFile.write(close)
    # footer
    #print(end)
    jsFile.write(end)

    # close the json file
    jsFile.close()

