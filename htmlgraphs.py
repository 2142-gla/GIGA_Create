#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Create an html description of the subgraphs
'''
#
import networkx as nx
import matplotlib.pyplot as plt

# Get a gene name from an id
def getName(id, omiDiction):
    for key in omiDiction:
        if id in omiDiction[key]:
            return key
    return '-1'

# Create a html file using the out filename. Returns the file object
def createFile(filename):
    try:
        filename = filename + ".html"
        htmlFile = open(filename, 'w')
        return htmlFile
    except:
        print ("Can't create file!")
        exit()

# Make the graph
def makeGraph(index, key, funClasses, omiDiction):
    # Make a graph object from the data dictionaries
    graph = nx.MultiGraph()

    # Use for the first functional class for this one
    geneList = funClasses[key][2]

    # Create nodes and use titles rather than id
    for geneDetails in geneList:
        nodeGene = geneDetails[0]
        #print(nodeGene)
        graph.add_node(nodeGene)
        # add labels to nodes
        graph.node[nodeGene]['label'] = geneDetails[0]

        graph.nodes(data=True)

    #print(graph.nodes())
    # Create edges
    edgesList = funClasses[key][1]

    for edge in edgesList:
        n1 = getName(edge[0], omiDiction)
        n2 = getName(edge[1], omiDiction)
        graph.add_edge(n1, n2)

    #print(graph.edges())

    nx.draw(graph, with_labels=True, node_size=2000, node_shape='o')

    # http://networkx.readthedocs.io/en/networkx-1.11/reference/generated/networkx.drawing.nx_pylab.draw_networkx_labels.html#networkx.drawing.nx_pylab.draw_networkx_labels
    # G = nx.path_graph(4)
    # pos = nx.spring_layout(G)

    # Create a graph with evidence as nodes
    #plt.show()
    #   Create a file from the graph
    indName = '{:03}'.format(index+1)
    graphName = "graph" + indName + ".png"
    plt.savefig(graphName)

    # HTML for graph
    graphHTML = """
        <div align="center">
            <br/>
            <h2>Subgraph {}</h2>
            <br/>
            <img src="{}" width="75%" border="1px"/>
            <p>Omicron Network anchored on omicron {}</p>
        </div>""".format(indName, graphName, key)
    #print(graphHTML)

    #   Pass the graph to make the nodes table - need this for the weight information.
    # Make the node table text
    nodehtml = nodeTable(key, funClasses, omiDiction, graph)

    # Make the edge table text

    # return the html to main
    return [graphHTML, nodehtml]

# Make the node table
def nodeTable(key, funClasses, omiDiction, graph):
    print("nodes!")
    nodehead = """<div>
    	<!-- Table of information about each node -->
    	<h2>Omicon Description</h2>
    	<table border="2">
    		<tr>
    			<td colspan="4">Information on each omicon in network</td>
    			<td colspan="2" align="center">Rank</td>
    		</tr>
    		<tr>
    			<td>Index</td>
    			<td>Label</td>
    			<td>Description of omicron</td>
    			<td>Weight</td>
    			<td>Overall</td>
    			<td>Network</td>
    		</tr>
    		"""

    nodehtml = nodehead
    # Add information for each row
    for omi in funClasses[key][2]:
        index = omi[2]
        label = omi[0]
        description = omiDiction[label][1]
        weight = omiDiction[label][3]
        ovRank = omiDiction[label][2]
        onRank = omi[1]
        nodeRow = """
        		<tr>
			<td>{:03}</td>
			<td>{}</td>
			<td>{}</td>
			<td align="center">{}</td>
			<td align="center">{}</td>
			<td align="center">{}</td>
		</tr>""".format(index, label, description, weight, ovRank, onRank)
        nodehtml = nodehtml + nodeRow

    # close of node table div
    nodehtml = nodehtml + """
	</table>
	<br />
	<hr width="75%">
	<br />
</div>"""

    #print (nodehtml)

    return nodehtml




# Main function receives the two data dictionaries
def main (funClasses, omiDiction, filename):
    # Start
    print ('Main')

    # Create the html file
    htmlFile = createFile(filename)

    # Write head to file
    head = """
    <!DOCTYPE html>
    <html>
        <head>
            <title>GIGA Omicron Networks</title>
        
        </head>
        <body>
            <h1 align="center">GIGA Omicron Networks</h1>
            <hr width="75%">
            <br/>
    """
    #print(head)
    htmlFile.write(head)

    # Add head information to the html fil

    # How many subgraphs?
    subs = len(funClasses)

    # Create graph, and tables for each subgraph
    for i, key in enumerate(funClasses):
        #   Make graph and add to html
        #print ("graph:", i)
        node = makeGraph(i, key, funClasses, omiDiction)
        htmlFile.write(node[0])
        htmlFile.write(node[1])
        # Pass the key and index plus one
        #   Make node table and add to html
        #print("node table:" , i)
        #   Make edge table and add to html
        #print("edge table:" , i)



    # Write tail to file
    tail = """
        </body>
    </html>
    """
    htmlFile.write(tail)

    htmlFile.close()

    #