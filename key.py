#!/usr/bin/env python3
''' Build a text file as a key for the cytoscape graph
    Take the dictionaries to build the file
'''

# Modules
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

#   Creates the colour of the node based on the PC value of the Functional Class and rank in the class
#   Input: name of the omicron
#   Output: a list containing rgb of list of the colour and value of the transparency.
# def colorNode(omicron):
#     # dictionary of colour blind safe colours
#     colors = {"Vermillion": [213, 94, 0], "Orange": [230, 159, 0], "Yellow": [240, 228, 66],
#               "Bluish Green": [0, 158, 115], "Blue": [0, 114, 178], "Sky Blue": [86, 189, 233],
#               "Reddish purple": [204, 121, 167]}
#     colList = ["Vermillion", "Orange", "Yellow", "Bluish Green", "Sky Blue", "Blue", "Reddish purple"]
#     transpLst = [255, 200, 175, 150, 125, 100, 75, 50, 25]
#
#     # Get the main functional class a omicron belongs to
#     fcomicron = getFC(omicron)[0]
#     # rank of function class in evidence network (based on PC value)
#     posFC = 1
#     for anchor in funClasses:
#         if fcomicron == anchor:
#             break
#         else:
#             posFC += 1
#     # Variables
#     transp = 255
#     rgb = []
#     omicronls = funClasses[fcomicron][2]
#     # Get the rank in functional class for the omicron in the main functional class int(funClasses[fcomicron][2])
#     rank = int([i[1] for i in omicronls if i[0] == omicron][0])
#     totalNumomicron = funClasses[fcomicron][0][3]
#     numOfFc = len(funClasses)
#     color = ""
#     # position of omicron in subgraph/functional class
#     omicronPos = [m[2] for m in funClasses[fcomicron][2] if omicron == m[0]][0]
#
#     # Color of the Functional Class
#     if posFC <= 7:
#         rgb = colors[(colList[posFC - 1])]
#         if (omicronPos-1) < 9:
#             transp = transpLst[omicronPos - 1]
#         else:
#             transp = 25
#     elif posFC >= 8:
#         t = posFC // 7
#         if t > 6:
#             transp = 25
#         else:
#             if (omicronPos + t - 1) < 9:
#                 transp = transpLst[(omicronPos + t - 1)]
#             else:
#                 transp = 25
#         posFC = posFC % 7
#         rgb = colors[(colList[posFC - 1])]
#
#     color = ("rgb(%s, %s, %s)") % (rgb[0], rgb[1], rgb[2])
#
#     return [color, transp]

def buildTxt(funClasses, omiDiction):

    # Variables
    # Hold the y position of the pen
    posy = 0

    # Set the font to Verdana
    font = ImageFont.truetype("~/Verdana.ttf",18)

    # Make the shape of the image
    img = Image.new("RGBA", (350, 250), (255, 255, 255))
    # Make a image object
    draw = ImageDraw.Draw(img)

    # # Gap to start of the anchor omicron
    # startArX = draw.textsize("-00-\t")[0]

    #txtFile = open("key.txt", 'w')

    # lineFormat = "%2s\t%s\t%.4g"
    lineFormat = "%2s   %s  %.4g"
    ancFormat = "%10s"
    pFormat = "%10.4g"
    posFormat = "%2s"
    #lineFormat = "-{}-\t{}\t{0:.4g}"

    # Header for the file
    print ("Evidence Network Key")
    draw.text((0, 0), "Evidence Network Key", (0, 0, 0), font = font)
    headerSz = draw.textsize("Evidence Network Key")
    posy += 25

    line1 = ""

   #"Subgraph Rank    Anchor omicron         PC Value")
    for anchor in funClasses:
        position = funClasses[anchor][0][2]
        #postion = posFormat % (position)
        pc = funClasses[anchor][0][1]
        pc = float(pc)
        #pc = infoFormat % (pc)
        #info = anchor + pc

        # Get size of anchor text
        ancSz = draw.textsize(anchor)

        # # Use size of anchor text to draw a text box
        # draw.rectangle([(startArX, posy), (ancSz[0] + startArX, ancSz[1] + posy)], outline=(0, 0, 0), fill=(230, 180, 55))

        # Create a line with the information for the subgraph
        # line = lineFormat % (position, anchor, pc)
        # line1 = posFormat % (position)
        # line2 = infoFormat % (anchor, pc)
        col1 = posFormat % (position)
        col2 = ancFormat % (anchor)
        col3 = pFormat % (pc)


        # Draw the text onto the image
        draw.text((0, posy), col1, (0, 0, 0), font = font)
        draw.text((30, posy), col2, (0, 0, 0), font=font)
        draw.text((200, posy), col3, (255,0,0), font = font)

        # Advance the y position of the pen
        posy += 20

        #line = lineFormat.format(position, anchor, pc)
        #line1 = line1 + line + '\n'
        #print (line)

    #img.show()
    img.save("key.png")
    #print (line1)
