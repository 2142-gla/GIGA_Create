#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Create an HTML summary file description of the subgraphs from the GiGA.

"""

""" Modules used:
    networkx: create and analysis networks.
    matplotlib.puplot: create images
    os: file structure functions
    json: convert information to json
"""
import networkx as nx
import matplotlib.pyplot as plt
import os
import json
from networkx.readwrite import json_graph

def getName(id, omiDiction):
    """ Get a omicon name from an id and return string of name.

    :param id: Integer id of omicon
    :param omiDiction: Dictionary data structure contiain information on omicons.
    :return: String containg omicon name or -1 if not found.
    """
    for title in omiDiction:
        if id == omiDiction[title][0]:
            return title
    return '-1'

def createFile(filename):
    """  Create a HTML file and directories using the out filename. Returns the file object

    :param filename: String name of the file
    :return: File object.
    """

    currentDr = os.getcwd() + '/'
    wrDir = currentDr + filename

    os.makedirs(currentDr + filename, exist_ok=True)
    os.chdir(wrDir)
    os.makedirs('images', exist_ok=True)
    os.makedirs('css', exist_ok=True)

    try:
        filename = filename + ".html"
        htmlFile = open(filename, 'w')
        cssFile = open('css/giga.css', 'w')
        cssFile.write(createCSS())
        cssFile.close()
        return htmlFile
    except:
        print ("Can't create file!")
        exit()

def makeGraph(index, anchor, funClasses, omiDiction):
    """ Make the image of the graph and HTML string for the image and node table.

    :param index: Integer of the sub-graph.
    :param anchor: String of the anchor omicon for the sub-graph.
    :param funClasses: Dictionary data structure contiain information on the sub-graphs.
    :param omiDiction: Dictionary data structure contiain information on omicons.
    :return:
    """
    #   Check if it is a second graph
    if anchor.endswith('-'):
        anch = anchor[:-1]
    else:
        anch = anchor

    # Make a graph object from the data dictionaries
    graph = nx.MultiGraph()
    # Clear the graph
    graph.clear()

    edgeNum = 0
    nodeNum = 0
    node_sizes = []

    # Get the list of omicons for the subgraph
    omiconList = funClasses[anchor][2]
    #print(len(omiconList))
    num = 0

    # Create nodes and use titles rather than id
    for omiconDetails in omiconList:
        nodeomicon = omiconDetails[0]
        #print(nodeomicon)
        graph.add_node(nodeomicon)
        #   Add node to node_list. If anchor = 2000 otherwise 0.
        if nodeomicon == anch:
            node_sizes.append(2000)
        else:
            node_sizes.append(0)
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

    #   Draw the graph
    nx.draw_shell(graph, with_labels=True, node_size=node_sizes, node_shape='o', node_color="#db4e51", edge_color="#558dd6")

    #   Create a file from the graph
    indName = '{:03}'.format(index+1)
    graphName = "graph" + indName + ".png"

    #   Save the image file to directory
    plt.savefig('images/'+graphName)
    # Clear the matplotlib.pyplot
    plt.gcf().clear()

    # HTML for graph
    graphHTML = """
        <div class="image">
            <br/>
            <h2>Subgraph {}</h2>
            <br/>
            <img src="{}" width="75%" border="1px"/>
            <p class="graphTitle">Network anchored on omicon {}</p>
        </div>
        
        """.format(indName, ('images/'+graphName), anchor)

    # Add infromation about the graph
    deg_max = 0
    deg_lst = []

    for n in graph.nodes():
        if len(graph.neighbors(n)) > deg_max:
            deg_max = len(graph.neighbors(n))

    for o in graph.nodes():
        if len(graph.neighbors(o)) == deg_max:
            deg_lst.append(o)

    deg_omicons = ", ".join(deg_lst)

    deg_cent = nx.degree_centrality(graph)
    high_deg = 0
    h_deg_lst =[]
    for i in deg_cent:
        if deg_cent[i] > high_deg:
            high_deg = deg_cent[i]

    for j in deg_cent:
        if deg_cent[j] == high_deg:
            h_deg_lst.append(i)

    highest = ', '.join(h_deg_lst)

    p_value = funClasses[anchor][0][1]

    graph_table ="""
           <div>
        <br/>
            <h2>Sub-graph Description</h2>
            <table>
                <tr>
                    <td>Anchor Omicon</td>
                    <td>{}</td>
                </tr>
                <tr>
                    <td>Highest number of neighbours</td>
                    <td>{}</td>
                </tr>
                <tr>
                    <td>Omicon(s) with most neigbours</td>
                    <td>{}</td>
                </tr>
                <tr>
                    <td>Highest degree centrality</td>
                    <td>{}</td>
                </tr>
                <tr>
                    <td>Omicon(s) with highest degree centrality</td>
                    <td>{}</td>
                </tr>
                <tr>
                    <td>p-value for sub-graph</td>
                    <td>{}</td>
                </tr>
            </table>
        </div>
    """.format(anchor,deg_max, deg_omicons, high_deg, highest, p_value)

    #   Append graph_table to graphHTML
    graphHTML += graph_table

    #   Pass the graph to make the nodes table - need this for the weight information.
    # Make the node table text
    nodehtml = nodeTable(anchor, funClasses, omiDiction, graph)

    # Clear the graph
    graph.clear()

    # return the html to main
    return [graphHTML, nodehtml]

def nodeTable(key, funClasses, omiDiction, graph):
    """ Make the node table HTML.

    :param key: String of the anchor omicon.
    :param funClasses: Dictionary data structure contiain information on the sub-graphs.
    :param omiDiction: Dictionary data structure contiain information on the omicons
    :param graph: Integer index of sub-graph.
    :return: String HTML text for node table.
    """

    nodehead = """<div>
    	<!-- Table of information about each node -->
    	<h2>Omicon Description</h2>
    	<table border="2">
    		<tr class="header">
    			<th colspan="4">Information on each omicon in network</th>
    			<th colspan="2" align="center">Rank</th>
    		</tr>
    		<tr class="header">
    			<th>Index</th>
    			<th>Label</th>
    			<th>Description of omicon</th>
    			<th>Edges</th>
    			<th>Overall</th>
    			<th>Network</th>
    		</tr>
    		"""

    nodehtml = nodehead
    # Add information for each row
    for omi in funClasses[key][2]:
        index = omi[2]
        label = omi[0]
        description = omiDiction[label][1]
        degree = omiDiction[label][3]
        ovRank = omiDiction[label][2]
        onRank = omi[1]
        nodeRow = """
        		<tr>
			<td>{:03}</td>
			<td><a href="http://www.ensembl.org/Multi/Search/Results?q={};site=ensembl_all">{}</a></td>
			<td>{}</td>
			<td align="left">{}</td>
			<td align="center">{}</td>
			<td align="center">{}</td>
		</tr>""".format(index, label, label, description, degree, ovRank, onRank)
        nodehtml = nodehtml + nodeRow

    # close of node table div
    nodehtml = nodehtml + """
	</table>
	<br />
</div>"""

    return nodehtml

def edgeTable (anchor, omiDiction, funClasses):
    """ Make the edge table HTML.

    :param anchor: String of the name of the anchor omicon
    :param funClasses: Dictionary data structure contiain information on the sub-graphs.
    :param omiDiction: Dictionary data structure contiain information on the omicons
    :return: String containing HTML for the edge table.
    """
    edgehead = """<div>
        	<!-- Table of information about each edge -->
        	<br />
        	<h2>Edges between each omicon</h2>
        	<table border="2">
        		<tr class="header">
        		    <th>Index</th>
        			<th>Scource</th>
        			<th>Target</th>
        			<th>Evidence</th>
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
    			<td>{}</td>
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

    return edgehtml

def createCSS():
    """ Create the CSS text for the summary file

    :return: String containing CSS text.
    """
    css = """
        body{
        background-color: #F3F3F3;
    }

    title {
        font-family: Helvetica, Arial, sans-serif;
        text-align: center;
    }

    h1	{
        color: #333; 
        font-family: Helvetica, Arial, sans-serif;
        text-align: center;
    }

    h2 {
        font-family: Helvetica, Arial, sans-serif;
        text-align: center;
    }

    .graphTitle {
        font-family: Helvetica, Arial, sans-serif;
        font-style: italic;
    }

    table {
        margin-left:auto;
        margin-right: auto;
        color: #333; 
        font-family: Helvetica, Arial, sans-serif;
        width: 90%; 
        border-collapse: 
        collapse; border-spacing: 0; 
        background: #F3F3F3;
    }
    
    td, th { border: 1px solid #CCC; height: 30px; } 
    
    th {   
        font-weight: bold; 
    }

    td {  
        background: #FAFAFA; 
        text-align: center; 
    }

    .header{
        background: #E4F0F5;
    }
    
    .image{
    text-align: center; 
    }
    """
    return css

def main (funClasses, omiDiction, filename):
    """ Main function to create the HTML and CSS files.

    :param funClasses: Dictionary data structure contiain information on the sub-graphs.
    :param omiDiction: Dictionary data structure contiain information on the omicons
    :param filename: String name of the filename to be used.
    """

    # Create the html file
    htmlFile = createFile(filename)

    # Write head to file
    head = """
    <!DOCTYPE html>
    <html>
        <head>
            <title>GIGA omicon Networks</title>
            <link rel="stylesheet" type="text/css" href="css/giga.css">
        </head>
        <title>GiGA study of {}</title>
        <body>
            <div class="banner">
                <h1>GiGA study of {}</h1>
                <hr width="75%">
                <br/>
            </div>
    """.format(filename, filename)
    htmlFile.write(head)

    # Add head information to the html file
    # How many subgraphs?
    subs = len(funClasses)

    # Create graph, and tables for each subgraph
    for i, key in enumerate(funClasses):
        #   Make graph and add to html
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
