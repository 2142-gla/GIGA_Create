#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Take GIGA information and create a JSON file suitable for Cytoscape 

"""

# Make a json file
def nodeJSON(node, omicron):
    # Make nodes
    # if omicron is a key in funClasses then it is a an anchor omicron\
    idnum = omiDiction[omicron][0]
    name = omicron
    description = omiDiction[omicron][1]
    shape = shapeNode(omicron)
    colour = colorNode(omicron)

    omicronDetails = [gd for gd in funClasses[getFC(omicron)[0]][2] if omicron in gd][0]
    print (omicronDetails)
    rankAll = omiDiction[omicron][2]
    rankFC = omicronDetails[1]

    meta = str(omicronDetails[2]) + ": "+ omiDiction[omicron][1]

    # node: id, name, description, shape, background colour, transparency, meta information
    #print ((node) % (idnum, name, description, shape, colour[0], colour[1], meta))
    return ((node) % (idnum, name, description, rankAll, rankFC, shape, colour[0], colour[1], meta))

#   Check of the omicron is a anchor omicron
#   Input: name of the omicron
#   Output: Shape of the node
def shapeNode(omicron):
    anchors = [anchor for anchor in funClasses]
    if omicron in anchors:
        return "Rounded Rectangle"
    else:
        return "Ellipse"

#   From a omicron title get the functional classes it belongs to. The functional class are sorted by smallest p
#   Input: omicron title
#   Output: list of names of functional classes
def getFC(omicron):
    fcGroup = []
    # Check if omicron is in the omicronList of each Functional Class
    for key in funClasses:
        # If omicron found in omicron list add the name of the functional class to the fcGroup
        if any(omicron in omicronlist for omicronlist in funClasses[key][2]):
            fcGroup.append(key)
        #     print(omicron, "found")
        # else:
        #     print (omicron,"not found")
    #print ("getFC", fcGroup)
    return fcGroup

# #   Create the metadata for the tooltip. This will depend on wither the omicron is a anchor or normal omicron
# #   Input: omicron and shape
# #   Output: string format for meta data
# def metaNode(omicron, shape):
#     #print ('metaNode calls getFC')
#     fcGroup = getFC(omicron)
#
#     # Need to calculate rank in fc
#     omicronls = funClasses[fcGroup[0]][2]
#     # Get the rank in functional class for the omicron in the main functional class int(funClasses[fcomicron][2])
#     rank = int([i[1] for i in omicronls if i[0] == omicron][0])
#     m = 0
#
#     if shape == "Ellipse" and len(fcGroup) > 1:
#         metaFor = ("%s Rank of omicron Overall: %s ") % (omicron, omiDiction[omicron][2])
#         for fc in fcGroup:
#             omicronls = funClasses[fcGroup[m]][2]
#             # Get the rank in functional class for the omicron in the main functional class int(funClasses[fcomicron][2])
#             rank = int([i[1] for i in omicronls if i[0] == omicron][0])
#             addMeta = " Rank in Functional Class %s: %s. " % (fc, funClasses[fc][2][1])
#             metaFor = metaFor + addMeta
#             m += 1
#     elif shape == "Ellipse":
#         metaFor = "%s Rank of omicron Overall: %s. Rank in Functional Class %s: %s"
#         metaFor = metaFor % (omiDiction[omicron][1], omiDiction[omicron][2], fcGroup[0], rank)
#     else:
#         metaFor = "Subgraph Description: %s. P value: %s. Number of omicrons in Class: %s. "
#         metaFor = metaFor % (funClasses[fcGroup[0]][0][0], funClasses[fcGroup[0]][0][1], rank)
#         anchor = "Anchor omicron description %s Rank of omicron Overall: %s. Rank in Functional Class %s: %s."
#         anchor = anchor % (omiDiction[omicron][1], omiDiction[omicron][2], fcGroup[0], rank)
#         metaFor = metaFor + anchor
#
#     return metaFor

#   Creates the colour of the node based on the PC value of the Functional Class and rank in the class
#   Input: name of the omicron
#   Output: a list containing rgb of list of the colour and value of the transparency.
def colorNode(omicron):
    # dictionary of colour blind safe colours
    colors = {"Vermillion": [213, 94, 0], "Orange": [230, 159, 0], "Yellow": [240, 228, 66],
              "Bluish Green": [0, 158, 115], "Blue": [0, 114, 178], "Sky Blue": [86, 189, 233],
              "Reddish purple": [204, 121, 167]}
    colList = ["Vermillion", "Orange", "Yellow", "Bluish Green", "Sky Blue", "Blue", "Reddish purple"]
    transpLst = [255, 200, 175, 150, 125, 100, 75, 50, 25]

    # Get the main functional class a omicron belongs to
    fcomicron = getFC(omicron)[0]
    # rank of function class in evidence network (based on PC value)
    posFC = 1
    for anchor in funClasses:
        if fcomicron == anchor:
            break
        else:
            posFC += 1
    # Variables
    transp = 255
    rgb = []
    omicronls = funClasses[fcomicron][2]
    # Get the rank in functional class for the omicron in the main functional class int(funClasses[fcomicron][2])
    rank = int([i[1] for i in omicronls if i[0] == omicron][0])
    totalNumomicron = funClasses[fcomicron][0][3]
    numOfFc = len(funClasses)
    color = ""
    # position of omicron in subgraph/functional class
    omicronPos = [m[2] for m in funClasses[fcomicron][2] if omicron == m[0]][0]

    # Color of the Functional Class
    if posFC <= 7:
        rgb = colors[(colList[posFC - 1])]
        if (omicronPos-1) < 9:
            transp = transpLst[omicronPos - 1]
        else:
            transp = 25
    elif posFC >= 8:
        t = posFC // 7
        if t > 6:
            transp = 25
        else:
            if (omicronPos + t - 1) < 9:
                transp = transpLst[(omicronPos + t - 1)]
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

def main(fcDiction, omDiction, filename):
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
    global omiDiction
    funClasses = fcDiction
    omiDiction = omDiction

    # Create the JSON file
    jsFile = createJS(filename)

    # print out and create json file
    print(top, end='')
    jsFile.write(top)

    # print node section
    print(nodetop, end='')
    jsFile.write(nodetop)

    # print the nodes
    for n, omicron in enumerate(omiDiction):
        print (n, omicron)
        if n == len(omiDiction) - 1:
            # last element®
            nodeTxt = nodeJSON(node, omicron)
            nodeTxt = nodeTxt + " " + comma + " " + sel

            jsFile.write(nodeTxt)
        else:
            nodeTxt = nodeJSON(node, omicron)
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

