# University of Portsmouth
# M30299 Programming, Assessment Item 3
# Python Coursework: A Patchwork Maker

# Thomas Robinson, up2194485
# November/December 2023

# Repo: https://github.com/tomatport/m30299-programming-py-patchwork-maker

from graphics import *

#####################
# CONSTANTS
#####################
patchSize = 100 # size of each patch, in pixels
validColours = ["red", "green", "blue", "magenta", "orange", "yellow", "cyan"]
validGrid = [5, 7, 9]

#####################
# SHAPES
# Wrappers for graphics.py's shapes, they return the shape object with the given parameters
#####################
def makeRectangle(tlX, tlY, brX, brY, colour):
	rect = Rectangle(Point(tlX, tlY), Point(brX, brY))
	rect.setFill(colour)
	return rect

def makeLine(tlX, tlY, brX, brY, colour):
	line = Line(Point(tlX, tlY), Point(brX, brY))
	line.setFill(colour)
	return line


#####################
# PATCH DRAWING
# tlX and tlY are top left coords of the patch
# colour is the colour of the patch (or the elements within it)
# they return a list of the elements drawn, so they can be draw/modified later
#####################

###############
### Plain Patch
# To draw a plain coloured patch, we just draw a square :)
def makePatchPlain(tlX, tlY, colour):
	square = makeRectangle(tlX, tlY, tlX + patchSize, tlY + patchSize, colour)
	return [square] # only one element in this patch


###########################
### Penultimate Digit Patch
# This is the patch that is the word "HI" tiled (#8)
# HIColour makes the "HI" with the foreground as the colour, bg unfilled
# HIInvert makes the "HI" with the leters unfilled, bg as the colour
# makePatchPenultimate uses these two functions to create the patch
def makeHIForeground(tlX, tlY, colour):
	patchElements = []
	tlX, tlY = int(tlX), int(tlY)

	# H, not inverted
	# left vertical
	hLeft = makeRectangle(tlX, tlY, tlX + 5, tlY + 25, colour)
	patchElements.append(hLeft)
	# right vertical
	hRight = makeRectangle(tlX + 20, tlY, tlX + 25, tlY + 25, colour)
	patchElements.append(hRight)
	# horizontal
	hHoriz = makeRectangle(tlX + 5, tlY + 10, tlX + 20, tlY + 15, colour)
	patchElements.append(hHoriz)

	# I, not inverted
	# top horizontal
	iTop = makeRectangle(tlX + 25, tlY, tlX + 50, tlY + 5, colour)
	patchElements.append(iTop)
	# bottom horizontal
	iBottom = makeRectangle(tlX + 25, tlY + 20, tlX + 50, tlY + 25, colour)
	patchElements.append(iBottom)
	# vertical
	iVert = makeRectangle(tlX + 35, tlY + 5, tlX + 40, tlY + 20, colour)
	patchElements.append(iVert)

	return patchElements

def makeHIBackground(tlX, tlY, colour):
	patchElements = []
	tlX, tlY = int(tlX), int(tlY)

	# hide middle top and middle bottom of the bg to make the H
	hTop = makeRectangle(tlX + 5, tlY, tlX + 20, tlY + 10, colour)
	patchElements.append(hTop)

	hBottom = makeRectangle(tlX + 5, tlY + 15, tlX + 20, tlY + 25, colour)
	patchElements.append(hBottom)

	# hide middle left and middle right of the bg to make the I
	iLeft = makeRectangle(tlX + 25, tlY + 5, tlX + 35, tlY + 20, colour)
	patchElements.append(iLeft)

	iRight = makeRectangle(tlX + 40, tlY + 5, tlX + 50, tlY + 20, colour)
	patchElements.append(iRight)

	return patchElements

def makePatchPenultimate(tlX, tlY, colour):
	patchElements = []

	tlX, tlY = int(tlX), int(tlY) # convert to ints to avoid float errors
	colI, rowI = 0, 0 # keep track of which row and column we're on, for the colours

	for y in range(tlY, tlY + 100, 25):
		for x in range(tlX, tlX + 100, 50):
			if (colI + rowI) % 2 == 0:
				patchElements.extend(makeHIForeground(x, y, colour))
			else:
				patchElements.extend(makeHIBackground(x, y, colour))

			colI += 1

		rowI += 1
	return patchElements

#####################
### Final Digit Patch
# This is the patch that has grid lines surrounding a slanted eye shape (#5)
# Code copied verbatim from the programming worksheet
def makePatchFinal(tlX, tlY, colour):
	patchElements = []

	# Top Half
	for i in range(0, patchSize+10, 10):
		line = makeLine(i+tlX, tlY, patchSize+tlX, i+tlY, colour)
		patchElements.append(line)

	# Bottom Half
	for i in range(0, patchSize+10, 10):
		line = makeLine(tlX, i+tlY, i+tlX, patchSize+tlY, colour)
		patchElements.append(line)

	return patchElements


#####################
# PATCH COLOURS
# Compute the colour that each patch needs to be
# Based on where it is in the grid
#####################
def computePatchColour(row, col, gridSize, colours):
	gridMid = gridSize // 2  # middle of the grid

	# TOP LEFT CORNER (blue in example)
	if row < gridMid and col < gridMid:
		return colours[0]

	# TOP RIGHT CORNER (red)
	if row < gridMid and col > gridMid:
		return colours[2]

	# BOTTOM LEFT CORNER (red)
	if row > gridMid and col < gridMid:
		return colours[2]

	# BOTTOM RIGHT CORNER (blue)
	if row > gridMid and col > gridMid:
		return colours[0]

	# CROSS (orange)
	if row == gridMid or col == gridMid:
		return colours[1]

	# if we're here, we missed something
	return "black"


#####################
# PATCH LAYOUT
# computePatchLayout() figures out the layout of the patches, using the functions below
# makeEmptyPatchwork() makes an empty array of patches
# fillXPatches() adds elements to the patches, according to where each design should be positioned
#####################
def computePatchLayout(gridSize, colours):
	# make an array of empty patches
	patchwork = makeEmptyPatchwork(gridSize)

	# fill the patches with the correct elements
	patchwork = fillFinalPatches(patchwork, gridSize, colours)
	patchwork = fillPenultimatePatches(patchwork, gridSize, colours)
	patchwork = fillPlainPatches(patchwork, gridSize, colours)

	return patchwork

def makeEmptyPatchwork(gridSize):
	patchwork = []
	
	for row in range(0, gridSize):
		patchwork.append([])
		for _ in range(0, gridSize): # for each patch in the row
			patchwork[row].append({
				"elements": [], # the elements that make up the patch, so we can modify them later
			})

	return patchwork

#################
### PATCH FILLING
# "Fill" the spots where the respective patches should be

def fillFinalPatches(patchwork, gridSize, colours):
	for rowI in range(0, gridSize):  # every row
		for colI in range(0, gridSize, 2):  # every other column
			x, y = colI * patchSize, rowI * patchSize
			patchwork[rowI][colI]["elements"] = makePatchFinal(
				x, y, computePatchColour(rowI, colI, gridSize, colours))
			
	return patchwork

def fillPenultimatePatches(patchwork, gridSize, colours):
	for rowI in range(0, gridSize): # every row
		for colI in range(1, gridSize, 2): # every other column, but offset by 1
			x, y = colI * patchSize, rowI * patchSize
			patchwork[rowI][colI]["elements"] = makePatchPenultimate(x, y, computePatchColour(rowI, colI, gridSize, colours))

	return patchwork

def fillPlainPatches(patchwork, gridSize, colours):
	# the top and bottom of the columns of P patches are plain
	for colI in range(1, gridSize, 2): # every other column, offset by 1
		# top
		x, y = colI * patchSize, 0
		patchwork[0][colI]["elements"] = makePatchPlain(
			x, y, computePatchColour(0, colI, gridSize, colours))

		# bottom
		x, y = colI * patchSize, (gridSize - 1) * patchSize
		patchwork[gridSize - 1][colI]["elements"] = makePatchPlain(
			x, y, computePatchColour((gridSize-1), colI, gridSize, colours))


#####################
# DRAW PATCHES
# Draw the elements of each patch to a window
#####################
def drawPatches(win, patchwork):
	for row in patchwork:
		for patch in row:
			for element in patch["elements"]:
				element.setWidth(0) # remove outlines (there is no "none" option, only 0 width)
				element.draw(win)


#####################
# USER INPUT
# getUserInput() requests the grid size and colours from the user,
# then returns these values as a tuple
#####################
def getUserInput():
	return 9, ["blue", "orange", "red"]  # for testing

	global validColours, validGrid

	gridSize = None
	colours = []

	print(f"= GRID SIZE =\nChoose one from {validGrid}")
	while True:  # keep asking until valid
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
			print(f"😔 Your grid size must be one of {validGrid}\n")

	print(f"\n= COLOURS =\nChoose 3 from {validColours}")
	while len(colours) < 3:  # keep going until we have three colours
		while True:
			givenColCount = len(colours) + 1
			colour = input(f"🎨 Enter colour {givenColCount}/3: ")

			colour = colour.lower()  # convert input to lowercase for comparison

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
# MAIN
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