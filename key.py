#!/usr/bin/env python3
""" Build a png image file as a key for the cytoscape graph.
    Take the dictionaries to build the file based on a table of the sub-graph's anchor omicon and p-value.
    One function buildTxt that takes dictionaries containing information about omicons and sub-graphs.
"""

# Modules
import PIL
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

def buildTxt(funClasses, omiDiction):
    """ Build a text key of the index and turn this into an image.

    :param funClasses: Dictionary data structure containing information
    :param omiDiction: Dictionary data structure containing information
    """

    # Variables
    # Hold the y position of the pen
    posy = 0

    # Set the font to Verdana
    font = ImageFont.truetype("~/Verdana.ttf",18)

    # Make the shape of the image
    img = Image.new("RGBA", (350, 250), (255, 255, 255))
    # Make a image object
    draw = ImageDraw.Draw(img)

    lineFormat = "%2s   %s  %.4g"
    ancFormat = "%10s"
    pFormat = "%10.4g"
    posFormat = "%2s"

    # Header for the file
    print ("Evidence Network Key")
    draw.text((0, 0), "Evidence Network Key", (0, 0, 0), font = font)
    headerSz = draw.textsize("Evidence Network Key")
    posy += 25

    line1 = ""

   #"Subgraph Rank    Anchor omicron         p-value Value")
    for anchor in funClasses:
        position = funClasses[anchor][0][2]
        pc = funClasses[anchor][0][1]
        pc = float(pc)

        # Get size of anchor text
        ancSz = draw.textsize(anchor)

        # Create a line with the information for the subgraph
        col1 = posFormat % (position)
        col2 = ancFormat % (anchor)
        col3 = pFormat % (pc)

        # Draw the text onto the image
        draw.text((0, posy), col1, (0, 0, 0), font = font)
        draw.text((30, posy), col2, (0, 0, 0), font=font)
        draw.text((200, posy), col3, (255,0,0), font = font)

        # Advance the y position of the pen
        posy += 20

    # Save the image.
    img.save("key.png")
