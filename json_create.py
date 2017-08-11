#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Take GiGA information and create a JSON cyjs file suitable for Cytoscape.

"""


def nodeJSON(node, omicon):
    """ Make nodes for the JSON file
     If omicon is a key in funClasses then it is an anchor omicon

    Args:
        node - a string containing JSON text for nodes with string format markers
        omicon - the title of the omicon in string format

    Returns:
        node - a string of the node JSON text for the omicon.
     """
    idnum = omiDiction[omicon][0]
    name = omicon
    description = omiDiction[omicon][1]
    shape = shapeNode(omicon)
    colour = colorNode(omicon)

    omiconDetails = [gd for gd in funClasses[getFC(omicon)[0]][2] if omicon in gd][0]
    rankAll = omiDiction[omicon][2]
    rankFC = omiconDetails[1]
    meta = str(omiconDetails[2]) + ": "+ omiDiction[omicon][1]

    return ((node) % (idnum, name, description, rankAll, rankFC, shape, colour[0], colour[1], meta))

def shapeNode(omicon):
    """ Check if the omicon is an acnhor omicon

    :param omicon: string name of the omicon
    :return: String name of the shape the node should take.
    """
    anchors = [anchor for anchor in funClasses]
    if omicon in anchors:
        return "Rounded Rectangle"
    else:
        return "Ellipse"

def getFC(omicon):
    """ From a omicon title get the functional classes it belongs to. The functional class are sorted by smallest p

    :param omicon: string name of the omicon
    :return: list of omicon names in functional class/sub-graph
    """
    fcGroup = []
    # Check if omicon is in the omiconList of each Functional Class
    for key in funClasses:
        # If omicon found in omicon list add the name of the functional class to the fcGroup
        if any(omicon in omiconlist for omiconlist in funClasses[key][2]):
            fcGroup.append(key)

    return fcGroup

def colorNode(omicon):
    """ Creates the colour of the node based on the p-value value of the Functional Class and rank in the class

    :param omicon: string name of the omicon
    :return: a list containing rgb of list of the colour and value of the transparency.
    """
    # dictionary of colour blind safe colours
    colors = {"Vermillion": [213, 94, 0], "Orange": [230, 159, 0], "Yellow": [240, 228, 66],
              "Bluish Green": [0, 158, 115], "Blue": [0, 114, 178], "Sky Blue": [86, 189, 233],
              "Reddish purple": [204, 121, 167]}
    colList = ["Vermillion", "Orange", "Yellow", "Bluish Green", "Sky Blue", "Blue", "Reddish purple"]
    transpLst = [255, 200, 175, 150, 125, 100, 75, 50, 25]

    # Get the main functional class the omicon belongs to
    fcomicon = getFC(omicon)[0]
    # rank of function class in evidence network (based on p-value value)
    posFC = 1
    for anchor in funClasses:
        if fcomicon == anchor:
            break
        else:
            posFC += 1
    # Variables
    transp = 255
    rgb = []
    omiconls = funClasses[fcomicon][2]
    # Get the rank in functional class for the omicon in the main functional class int(funClasses[fcomicon][2])
    rank = int([i[1] for i in omiconls if i[0] == omicon][0])
    totalNumomicon = funClasses[fcomicon][0][3]
    numOfFc = len(funClasses)
    color = ""
    # position of omicon in subgraph/functional class
    omiconPos = [m[2] for m in funClasses[fcomicon][2] if omicon == m[0]][0]

    # Color of the Functional Class
    if posFC <= 7:
        rgb = colors[(colList[posFC - 1])]
        if (omiconPos-1) < 9:
            transp = transpLst[omiconPos - 1]
        else:
            transp = 25
    elif posFC >= 8:
        t = posFC // 7
        if t > 6:
            transp = 25
        else:
            if (omiconPos + t - 1) < 9:
                transp = transpLst[(omiconPos + t - 1)]
            else:
                transp = 25
        posFC = posFC % 7
        rgb = colors[(colList[posFC - 1])]

    color = ("rgb(%s, %s, %s)") % (rgb[0], rgb[1], rgb[2])

    return [color, transp]

def getTitle(idOmi):
    """ Get the name of the omicon from its id.

    :param idOmi: integer id of the omicon
    :return: String of the name of the omicon or -1 if not found.
    """
    for title in omiDiction:
        if omiDiction[title][0] == idOmi:
            return title
    else:
        return "-1"

def edgeJSON(text, link):
    """ Make the text for an edge in JSON format.

    :param text: String containing JSON text for edges and markers for string format.
    :param link: List containing edge information.
    :return: edgeFor: String containing formated JSON text for edge.
    """
    # make edge
    edgeID = link[3]
    source = link[0]
    target = link[1]
    interaction = link[2]
    sourceName = getTitle(source)
    targetName = getTitle(target)
    name = '%s %s %s' % (sourceName, interaction, targetName)
    edgeFor = text % (edgeID, name, source, target, interaction)
    return edgeFor

def createJS(filename):
    """ Creates the file object for the cyjs file.

    :raise File exception if you can't find the file and closes the program.
    :param filename: String name of the file.
    :return: File object
    """
    try:
        jsFile = open(filename, 'w')
        return jsFile
    except:
        print ("Can't create file!")
        exit()

def main(fcDiction, omDiction, filename):
    """ Main function for the program.  Creates the JSON cyjs file and calls helper methods.

    :param fcDiction: Dictionary data structure containing information about the sub-graphs/functional classes.
    :param omDiction: Dictionary data structure containing information about each node.
    :param filename: String to be used as name of JSON cyjs file.
    """
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

    global funClasses
    global omiDiction
    funClasses = fcDiction
    omiDiction = omDiction

    # Create the JSON file
    jsFile = createJS(filename)

    # Write top text for JSON file
    jsFile.write(top)

    # Write top of node section text for JSON file
    jsFile.write(nodetop)

    # Write the nodes
    for n, omicon in enumerate(omiDiction):
        if n == len(omiDiction) - 1:
            # last element
            nodeTxt = nodeJSON(node, omicon)
            nodeTxt = nodeTxt + " " + comma + " " + sel

            jsFile.write(nodeTxt)
        else:
            nodeTxt = nodeJSON(node, omicon)
            nodeTxt = nodeTxt + " " + comma + " " + sel
            jsFile.write(nodeTxt)
            jsFile.write(comma)

    # close the nodes
    jsFile.write(close + comma)

    # Start the edges
    jsFile.write(edgetop)

    # Write edge section
    for o, item in enumerate(funClasses):
        fcList = funClasses[item][1]
        for m, link in enumerate(fcList):
            if o == (len(funClasses) - 1) and m == (len(fcList) -1):
                # Last edge
                edgeTxt = edgeJSON(edge, link) + " " + comma + " " + sel
                jsFile.write(edgeTxt)
            else:
                edgeTxt = edgeJSON(edge, link) + " " + comma + " " + sel
                jsFile.write(edgeTxt)
                jsFile.write(comma)


    # Write end of edges
    jsFile.write(close)
    # Write footer
    jsFile.write(end)

    # close the json file
    jsFile.close()