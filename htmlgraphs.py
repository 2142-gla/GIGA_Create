#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Create an html description of the subgraphs
'''
#
import networkx as nx
import matplotlib.pyplot as plt
import os

# Get a omicon name from an id
def getName(id, omiDiction):
    for title in omiDiction:
        if id == omiDiction[title][0]:
            return title
    return '-1'

# Create a html file and directories using the out filename. Returns the file object
def createFile(filename):

    currentDr = os.getcwd() + '/'
    wrDir = currentDr + filename

    os.makedirs(currentDr + filename, exist_ok=True)
    os.chdir(wrDir)
    os.makedirs('images', exist_ok=True)
    os.makedirs('css', exist_ok=True)

    try:
        filename = filename + ".html"
        htmlFile = open(filename, 'w')
        return htmlFile
    except:
        print ("Can't create file!")
        exit()

# Make the graph
def makeGraph(index, anchor, funClasses, omiDiction):
    # Make a graph object from the data dictionaries
    graph = nx.MultiGraph()
    # Clear the graph
    graph.clear()

    edgeNum = 0
    nodeNum = 0
    #print(anchor + " at makeGraph")

    # Get the list of omicons for the subgraph
    omiconList = funClasses[anchor][2]
    #print(len(omiconList))
    num = 0

    # Create nodes and use titles rather than id
    for omiconDetails in omiconList:
        nodeomicon = omiconDetails[0]
        #print(nodeomicon)
        graph.add_node(nodeomicon)
        # add labels to nodes
        graph.node[nodeomicon]['label'] = omiconDetails[0]
        graph.nodes(data=True)
        num += 1

    #print ("Nodes", num)
    # print("---")
    # print(graph.nodes())
    # Create edges
    edgesList = funClasses[anchor][1]

    for edge in edgesList:
        # get the name of each omicon in the list
        n1 = getName(edge[0], omiDiction)
        n2 = getName(edge[1], omiDiction)
        graph.add_edge(n1, n2)
        edgeNum += 1

    #print("Edges", edgeNum)

    nx.draw(graph, with_labels=True, node_size=2000, node_shape='o')


    # Create a graph with evidence as nodes
    #   Create a file from the graph
    indName = '{:03}'.format(index+1)
    graphName = "graph" + indName + ".png"

    plt.savefig('images/'+graphName)
    # Clear the matplotlib.pyplot
    plt.gcf().clear()

    # HTML for graph
    graphHTML = """
        <div align="center">
            <br/>
            <h2>Subgraph {}</h2>
            <br/>
            <img src="{}" width="75%" border="1px"/>
            <p>omicon Network anchored on omicon {}</p>
        </div>""".format(indName, ('images/'+graphName), anchor)
    #print(graphHTML)

    #   Pass the graph to make the nodes table - need this for the weight information.
    # Make the node table text
    nodehtml = nodeTable(anchor, funClasses, omiDiction, graph)

    # Make the edge table text

    # Clear the graph
    graph.clear()

    #print ("Nodes in graph: ", graph.nodes())


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
    			<td>Description of omicon</td>
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

# Make the edge table
def edgeTable (anchor, omiDiction, funClasses):
    print("edges!")
    edgehead = """<div>
        	<!-- Table of information about each edge -->
        	<br />
        	<h2>Edges between each omicon</h2>
        	<table border="2">
        	    <tr>
        	        <td colspan="3" align="center"></td>
        	    </tr>
        		<tr>
        		    <td>Index</td>
        			<td>Scource</td>
        			<td>Target</td>
        			<td>Evidence</td>
        		</tr>
        		"""

    edgehtml = edgehead
    # Add information for each row
    index = 1
    for edge in funClasses[anchor][1]:

        source = getName(edge[0], omiDiction)
        target = getName(edge[1], omiDiction)
        evidence = edge[2]

        edgeRow = """
            		<tr>
    			<td>{:03}</td>
    			<td align="center">{}</td>
    			<td align="center">{}</td>
    			<td>{}</td>
    		</tr>""".format(index, source, target, evidence)
        edgehtml = edgehtml + edgeRow
        index +=1

    # close of node table div
    edgehtml = edgehtml + """
    	</table>
    	<br />
    	<hr width="75%">
    	<br />
    </div>"""

    # print (nodehtml)

    return edgehtml

# Main function receives the two data dictionaries
def main (funClasses, omiDiction, filename):

    # Create the html file
    htmlFile = createFile(filename)

    # Write head to file
    head = """
    <!DOCTYPE html>
    <html>
        <head>
            <title>GIGA omicon Networks</title>
        
        </head>
        <body>
            <h1 align="center">GIGA omicon Networks</h1>
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
        print (i, key)
        #   Make graph and add to html
        #print ("graph:", i)
        node = makeGraph(i, key, funClasses, omiDiction)
        htmlFile.write(node[0])
        htmlFile.write(node[1])
        # Edge Table
        htmlFile.write(edgeTable(key, omiDiction, funClasses))


    # Write tail to file
    tail = """
        </body>
    </html>
    """
    htmlFile.write(tail)

    htmlFile.close()

    #