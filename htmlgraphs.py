#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Create an html description of the subgraphs
'''
#
import networkx as nx
import matplotlib.pyplot as plt

# Get a gene name from an id
def getName(id, geneDiction):
    for key in geneDiction:
        if id in geneDiction[key]:
            return key
    return '-1'


# Main function receives the two data dictionaries
def main (funClasses, geneDiction):
    # Start
    print ('Main')

    # Make a graph object from the data dictionaries
    fc01 = nx.MultiGraph()

    # Use for the first functional class for this one
    key = 'YER065C'
    geneList = funClasses[key][2]


    # Create nodes and use titles rather than id
    for geneDetails in geneList:
        nodeGene = geneDetails[0]
        print (nodeGene)
        fc01.add_node(nodeGene)
        # add labels to nodes
        fc01.node[nodeGene]['label'] = geneDetails[0]

    fc01.nodes(data=True)

    print(fc01.nodes())
    # Create edges
    edgesList = funClasses[key][1]

    for edge in edgesList:
        n1 = getName(edge[0], geneDiction)
        n2 = getName(edge[1], geneDiction)
        fc01.add_edge(n1, n2)

    print (fc01.edges())

    nx.draw(fc01, with_labels = True, node_size = 2000, node_shape = 'o')

    # http://networkx.readthedocs.io/en/networkx-1.11/reference/generated/networkx.drawing.nx_pylab.draw_networkx_labels.html#networkx.drawing.nx_pylab.draw_networkx_labels
    # G = nx.path_graph(4)
    # pos = nx.spring_layout(G)

    # Create a graph with evidence as nodes



    plt.show()


    #