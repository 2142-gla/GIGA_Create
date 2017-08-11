#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Make gml files for the sub-graphs.

"""
import networkx as nx
import os
import json
from networkx.readwrite import json_graph

def getName(id, omiDiction):
    """ Get a omicon name from an id

    :param id: Integer of the id of the omicon.
    :param omiDiction: Dictionary data structure of information about the omicons.
    :return: String name of the omicon or -1 if not found.
    """
    for title in omiDiction:
        if id == omiDiction[title][0]:
            return title
    return '-1'

def makeGraph(index, anchor, funClasses, omiDiction):
    """ Make the gml sub-graph.

    :param index: Integer of the index of the sub-graph.
    :param anchor: String name of the anchor omicon for the sub-graph.
    :param funClasses: Dictionary data structure containing information about the omicons.
    :param omiDiction: Dictionary data structure of information about the omicons.
    :return:
    """
    # Make a graph object from the data dictionaries
    graph = nx.MultiGraph()

    edgeNum = 0
    nodeNum = 0

    # Get the list of omicons for the subgraph
    omiconList = funClasses[anchor][2]
    # print(len(omiconList))
    num = 0

    # Create nodes and use titles rather than id
    for omiconDetails in omiconList:
        nodeomicon = omiconDetails[0]
        # print(nodeomicon)
        graph.add_node(nodeomicon)
        # add labels to nodes
        graph.node[nodeomicon]['label'] = omiconDetails[0]
        graph.nodes(data=True)
        num += 1

    edgesList = funClasses[anchor][1]

    #   Create the edges
    for edge in edgesList:
        # get the name of each omicon in the list
        n1 = getName(edge[0], omiDiction)
        n2 = getName(edge[1], omiDiction)
        graph.add_edge(n1, n2, evidence=edge[2])
        edgeNum += 1

    #   Create a file from the graph
    indName = '{:03}'.format(index + 1)
    graphName = "graph" + indName + ".png"

    #   Create gml file for each sub-graph
    nx.write_gml(graph, 'gml/' + 'graph' + indName + '.gml')

def main(funClasses, omiDiction, filename):
    """ Main function to make directory for gml files and call makeGraph.

    :param funClasses: Dictionary data structure containing information about the omicons.
    :param omiDiction: Dictionary data structure of information about the omicons.
    :param filename: String name to be used as part of the filename.
    :return:
    """

    # Make folder
    currentDr = os.getcwd() + '/'
    wrDir = currentDr + filename
    os.makedirs(currentDr + filename, exist_ok=True)
    os.chdir(wrDir)
    os.makedirs('gml', exist_ok=True)

    # Create graph, and tables for each subgraph
    for i, key in enumerate(funClasses):
        makeGraph(i, key, funClasses, omiDiction)




