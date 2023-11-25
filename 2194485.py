# University of Portsmouth
# M30299 Programming, Assessment Item 3
# Python Coursework: A Patchwork Maker

# Thomas Robinson, up2194485
# November/December 2023

# Repo: https://github.com/tomatport/m30299-programming-py-patchwork-maker

from graphics import *
from random import randint # for testing

#####################
# CONSTANTS
#####################
patchSize = 100 # size of each patch, in pixels


#####################
# USER INPUT
# getUserInput() requests the grid size and colours from the user,
# then returns these values as a tuple
#####################
def getUserInput():
	return 9, ["blue", "orange", "red"] # for testing

	gridSize = None
	validGrid = [5, 7, 9]

	colours = []
	validColours = ["red", "green", "blue", "magenta", "orange", "yellow", "cyan"]

	print(f"= GRID SIZE =\nChoose one from {validGrid}")
	while True: # keep asking until valid
		givenSize = input("🧱 Enter the grid size: ")

		if not givenSize.isdigit():  # check if input is a number
			print("😔 That doesn't look like a number...\n")
			continue

		# if it is a number, check if it's a valid grid size
		givenSize = int(givenSize)
		if givenSize in validGrid:
			gridSize = givenSize
			break
		else:
			print(f"😔 Your grid size must be one of {validGrid}\n" )
			# can't use .join() to make this look nicer :(

	
	print(f"\n= COLOURS =\nChoose 3 from {validColours}")
	while len(colours) < 3: # keep going until we have three colours
		while True:
			givenColCount = len(colours) + 1	
			colour = input(f"🎨 Enter colour {givenColCount}/3: ")

			colour = colour.lower() # convert input to lowercase for comparison

			if colour in colours:
				print(f"👀 You have already entered {colour}!\n")
				continue

			if colour in validColours:
				colours.append(colour)
				break
			else:
				print(f"😔 That's a funny looking colour! Must be one of {validColours}\n")

	return gridSize, colours


#####################
# PATCH DRAWING
# tlX and tlY are top left coords of the patch
# colour is the colour of the patch (or the elements within it)
# they return a list of the elements drawn, so they can be modified later
#####################

### PLAIN PATCH
# To draw a plain coloured patch, we just draw a square :)
def makePatchPlain(tlX, tlY, colour):
	square = Rectangle(Point(tlX, tlY), Point(tlX + patchSize, tlY + patchSize))
	square.setFill(colour)

	return [square] # only one element in this patch

### PENULTIMATE DIGIT PATCH
# This is the patch that is the word "HI" tiled (#8)

# HIColour makes the "HI" with the foreground as the colour, bg unfilled
def makeHIColour(tlX, tlY, colour):
	patchElements = []
	tlX, tlY = int(tlX), int(tlY)

	# H, not inverted
	# left vertical
	hLeft = Rectangle(Point(tlX, tlY), Point(tlX + 5, tlY + 25))
	hLeft.setFill(colour)
	patchElements.append(hLeft)
	# right vertical
	hRight = Rectangle(Point(tlX + 20, tlY), Point(tlX + 25, tlY + 25))
	hRight.setFill(colour)
	patchElements.append(hRight)
	# horizontal
	hHoriz = Rectangle(Point(tlX + 5, tlY + 10), Point(tlX + 20, tlY + 15))
	hHoriz.setFill(colour)
	patchElements.append(hHoriz)

	# I, not inverted
	# top horizontal
	iTop = Rectangle(Point(tlX + 25, tlY), Point(tlX + 50, tlY + 5))
	iTop.setFill(colour)
	patchElements.append(iTop)
	# bottom horizontal
	iBottom = Rectangle(Point(tlX + 25, tlY + 20), Point(tlX + 50, tlY + 25))
	iBottom.setFill(colour)
	patchElements.append(iBottom)
	# vertical
	iVert = Rectangle(Point(tlX + 35, tlY + 5), Point(tlX + 40, tlY + 20))
	iVert.setFill(colour)
	patchElements.append(iVert)

	return patchElements

# HIInvert makes the "HI" with the leters unfilled, bg as the colour
def makeHIInvert(tlX, tlY, colour):
	patchElements = []
	tlX, tlY = int(tlX), int(tlY)

	# hide middle top and middle bottom of the bg to make the H
	hTop = Rectangle(Point(tlX + 5, tlY), Point(tlX + 20, tlY + 10))
	hTop.setFill(colour)
	patchElements.append(hTop)

	hBottom = Rectangle(Point(tlX + 5, tlY + 15), Point(tlX + 20, tlY + 25))
	hBottom.setFill(colour)
	patchElements.append(hBottom)

	# hide middle left and middle right of the bg to make the I
	iLeft = Rectangle(Point(tlX + 25, tlY + 5), Point(tlX + 35, tlY + 20))
	iLeft.setFill(colour)
	patchElements.append(iLeft)

	iRight = Rectangle(Point(tlX + 40, tlY + 5), Point(tlX + 50, tlY + 20))
	iRight.setFill(colour)
	patchElements.append(iRight)

	return patchElements

# This actually draws the patch, using HIInvert and HIColour
def makePatchP(tlX, tlY, colour):
	patchElements = []

	tlX, tlY = int(tlX), int(tlY) # convert to ints to avoid float errors
	colI, rowI = 0, 0 # keep track of which row and column we're on, for the colours

	for y in range(tlY, tlY + 100, 25):
		for x in range(tlX, tlX + 100, 50):
			if (colI + rowI) % 2 == 0:
				patchElements.extend(makeHIColour(x, y, colour))
			else:
				patchElements.extend(makeHIInvert(x, y, colour))

			colI += 1

		rowI += 1
	return patchElements

### FINAL DIGIT PATCH
# This is the patch that has grid lines surrounding a slanted eye shape (#5)
# Code copied verbatim from the programming worksheet
def makePatchF(tlX, tlY, colour):
	patchElements = []

	# Top Half
	for i in range(0, patchSize+10, 10):
		line = Line(Point(i+tlX, tlY), Point(patchSize+tlX, i+tlY))
		line.setOutline(colour)
		patchElements.append(line)

	# Bottom Half
	for i in range(0, patchSize+10, 10):
		line = Line(Point(tlX, i+tlY), Point(i+tlX, patchSize+tlY))
		line.setOutline(colour)
		patchElements.append(line)

	return patchElements


#####################
# PATCH LAYOUT
# Compute the layout of the patches, using the provided images
#####################
def computePatchLayout(gridSize, colours):
	# init patchwork array of all empty patches
	# the patchwork is an array of rows, each row is an array of patches
	# patchwork[row][patch] = patch dict
	patchwork = []
	
	for row in range(0, gridSize):
		patchwork.append([])
		for _ in range(0, gridSize): # for each patch in the row
			patchwork[row].append({
				"elements": [], # the elements that make up the patch, so we can modify them later
				"selected": False, # whether the patch is selected (for challenge)
				"border": None # used to store the border around the patch so it can be removed later
			})
	# we now have an array of empty patches, corresponding to the grid size

	# F PATCH COLUMNS
	for rowI in range(0, gridSize): # every row
		for colI in range(0, gridSize, 2): # every other column
			x, y = colI * patchSize, rowI * patchSize
			patchwork[rowI][colI]["elements"] = makePatchF(x, y, computePatchColour(rowI, colI, gridSize, colours))

	# P PATCHES
	for rowI in range(0, gridSize): # every row
		for colI in range(1, gridSize, 2): # every other column, but offset by 1
			x, y = colI * patchSize, rowI * patchSize
			patchwork[rowI][colI]["elements"] = makePatchP(x, y, computePatchColour(rowI, colI, gridSize, colours))
			

	# the top and bottom of these columns are plain
	# again, every other column, offset by 1
	for colI in range(1, gridSize, 2): # every other column
		# top
		x, y = colI * patchSize, 0
		patchwork[0][colI]["elements"] = makePatchPlain(
			x, y, computePatchColour(0, colI, gridSize, colours))
		
		#bottom
		x, y = colI * patchSize, (gridSize - 1) * patchSize
		patchwork[gridSize - 1][colI]["elements"] = makePatchPlain(
			x, y, computePatchColour((gridSize-1), colI, gridSize, colours))

	return patchwork


#####################
# COLOUR COMPUTER
# Compute the colour that each patch needs to be
# Based on where it is in the grid
#####################
def computePatchColour(row, col, gridSize, colours):
	gridMid = gridSize // 2 # middle of the grid

	# TOP LEFT CORNER (blue in example)
	if row < gridMid and col < gridMid: return colours[0]
	
	# TOP RIGHT CORNER (red)
	if row < gridMid and col > gridMid: return colours[2]

	# BOTTOM LEFT CORNER (red)
	if row > gridMid and col < gridMid: return colours[2]
	
	# BOTTOM RIGHT CORNER (blue)
	if row > gridMid and col > gridMid: return colours[0]

	# CROSS (orange)
	if row == gridMid or col == gridMid: return colours[1]
	
	# if we're here, we missed something
	return "black"


#####################
# DRAW PATCHES
# Draw the elements of each patch to the window
#####################
def drawPatches(win, patchwork):
	for row in patchwork:
		for patch in row:
			for element in patch["elements"]:
				element.setWidth(0) # remove outlines (there is no "none" option, only 0 width)
				element.draw(win)


#####################
# MAIN
# Program entry point
#####################
def main():
	gridSize, colours = getUserInput()

	winSize = patchSize * gridSize
	win = GraphWin("Patchwork", winSize, winSize)
	win.setBackground("white")	

	patchwork = computePatchLayout(gridSize, colours)

	drawPatches(win, patchwork)

	win.getMouse()


main()