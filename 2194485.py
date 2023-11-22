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
	while True:
		givenSize = input("🧱 Enter the grid size: ")

		if "!" in givenSize:
			print("🤔 Random grid size, coming right up!")
			gridSize = randint(1, 30) * 2 + 1 # pick any odd number between 1 and 30
			break

		if not givenSize.isdigit():  # check if input is a number
			print("😔 That doesn't look like a number...\n")
			continue

		# if it is a number, check if it's a valid grid size
		if int(givenSize) in validGrid:
			gridSize = int(givenSize)  # update global grid variable to input
			break
		else:
			print(f"😔 Your grid size must be one of {validGrid}\n" )
			# can't use .join() to make this look nicer :(

	
	print(f"\n= COLOURS =\nChoose 3 from {validColours}")
	while len(colours) < 3: # request 3 colours
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
# PATCH DRAWING
# tlX and tlY are top left coords of the patch
# colour is the colour of the patch (or the elements within it)
# they return a list of the elements drawn, so they can be modified later
#####################

# PLAIN PATCH
# To draw a plain coloured patch, we just draw a square :)
def makePatchPlain(tlX, tlY, colour):
	patchElements = []
	
	square = Rectangle(Point(tlX, tlY), Point(tlX + patchSize, tlY + patchSize))
	square.setFill(colour)
	patchElements.append(square)

	return patchElements
	

# PENULTIMATE DIGIT PATCH
# This is the patch that is the word "HI" tiled (#8)
def makePatchP(tlX, tlY, colour):
	patchElements = []

	tlX, tlY = int(tlX), int(tlY) # convert to ints to avoid float errors
	colI, rowI = 0, 0 # keep track of which row and column we're on, for the colours

	for y in range(tlY, tlY + 100, 25):
		for x in range(tlX, tlX + 100, 50):
			
			if (colI + rowI) % 2 == 0: # both should be even or odd
				colours = [colour, "white"] # colour background, white foreground

				# background of the H
				bgH = Rectangle(Point(x, y), Point(x + 25, y + 25))
				bgH.setFill(colours[0])
				patchElements.append(bgH)

				# background of the I
				bgI = Rectangle(Point(x + 25, y), Point(x + 50, y + 25))
				bgI.setFill(colours[0])
				patchElements.append(bgI)
			else:
				colours = ["white", colour] # white background, colour foreground

			# hide middle top and middle bottom of the bg to make the H
			fgHTop = Rectangle(Point(x + 5, y), Point(x + 20, y + 10))
			fgHTop.setFill(colours[1])
			patchElements.append(fgHTop)

			fgHBottom = Rectangle(Point(x + 5, y + 15), Point(x + 20, y + 25))
			fgHBottom.setFill(colours[1])
			patchElements.append(fgHBottom)

			# hide middle left and middle right of the bg to make the I
			fgILeft = Rectangle(Point(x + 25, y + 5), Point(x + 35, y + 20))
			fgILeft.setFill(colours[1])
			patchElements.append(fgILeft)

			fgIRight = Rectangle(Point(x + 40, y + 5), Point(x + 50, y + 20))
			fgIRight.setFill(colours[1])
			patchElements.append(fgIRight)

			colI += 1 # increment column counter
		rowI += 1 # increment row counter

	return patchElements

# FINAL DIGIT PATCH
# This is the patch that has grid lines surrounding a slanted eye shape (#5)
# Code copied verbatim from the programming worksheet
def makePatchF(tlX, tlY, colour):
	patchElements = []

	# Top Half
	for i in range(0, 110, 10):
		line = Line(Point(i+tlX, tlY), Point(100+tlX, i+tlY))
		line.setOutline(colour)
		patchElements.append(line)

	# Bottom Half
	for i in range(0, 110, 10):
		line = Line(Point(tlX, i+tlY), Point(i+tlX, 100+tlY))
		line.setOutline(colour)
		patchElements.append(line)

	return patchElements


#####################
# PATCH LAYOUT
# Compute the layout of the patches, using the provided images
#####################
def computePatchLayout(gridSize, colours):
	# init patchwork array of all plain brown patches
	# the patchwork is an array of rows, each row is an array of patches
	# patchwork[row][patch] = patch dict
	patchwork = []
	
	for row in range(0, gridSize):
		patchwork.append([])
		for _ in range(0, gridSize): # for each patch in the row
			patchwork[row].append({
				"type": None, # only used for debugging
				"elements": [],
				"selected": False,
				"border": None # used to store the border around the patch so it can be removed later
			})
	# we now have an array of empty patches, corresponding to the grid size

	# F PATCH COLUMNS
	for rowI in range(0, gridSize): # every row
		for colI in range(0, gridSize, 2): # every other column
			patchwork[rowI][colI]["type"] = "f"
			x, y = colI * patchSize, rowI * patchSize
			patchwork[rowI][colI]["elements"] = makePatchF(x, y, computePatchColour(rowI, colI, gridSize, colours))

	# P PATCHES
	for rowI in range(0, gridSize): # every row
		for colI in range(1, gridSize, 2): # every other column, but offset by 1
			patchwork[rowI][colI]["type"] = "p"
			x, y = colI * patchSize, rowI * patchSize
			patchwork[rowI][colI]["elements"] = makePatchP(x, y, computePatchColour(rowI, colI, gridSize, colours))
			

	# the top and bottom of these columns are plain
	# again, every other column, offset by 1
	for colI in range(1, gridSize, 2): # every other column
		# top
		patchwork[0][colI]["type"] = "plain"
		x, y = colI * patchSize, 0
		patchwork[0][colI]["elements"] = makePatchPlain(
			x, y, computePatchColour(0, colI, gridSize, colours))
		
		#bottom
		patchwork[gridSize - 1][colI]["type"] = "plain"
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
	gridMid = gridSize // 2 # middle of the grid, since we use it a lot

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
# DRAW PATCHES
# Draw the elements of each patch to the window
#####################
def drawPatches(win, patchwork):
	for row in patchwork:
		for patch in row:
			for element in patch["elements"]:
				element.draw(win)

#####################
# Main, program entry
#####################
def main():
	gridSize, colours = getUserInput()

	# create window
	winSize = patchSize * gridSize
	win = GraphWin("Patchwork", winSize, winSize)
	win.setBackground("white")	

	patchwork = computePatchLayout(gridSize, colours)

	drawPatches(win, patchwork)

	while True:
		challengeCode(win, patchwork, gridSize, colours)


def challengeCode(win, patchwork, gridSize, colours):
	clicked = win.getMouse()

	row, col = clicked.getY() // patchSize, clicked.getX() // patchSize
	row, col = int(row), int(col)
	
	patch = patchwork[row][col]
	patch["selected"] = not patch["selected"]

	print(patch["selected"])

	if patch["selected"]:
		borderSize = patchSize // 20

		# inset the border by borderSize pixels
		borderTopLeft = Point(col * patchSize + borderSize,
								row * patchSize + borderSize)
		borderBottomRight = Point(
			(col + 1) * patchSize - borderSize, (row + 1) * patchSize - borderSize)
		border = Rectangle(borderTopLeft, borderBottomRight)
		
		border.setOutline("black")
		border.setWidth(borderSize*2)
		
		patch["border"] = border
		patch["border"].draw(win)
	else:
		for element in patch["elements"]:
			element.setFill(computePatchColour(row, col, gridSize, colours))
			if patch["border"]:
				patch["border"].undraw()
				patch["border"] = None

main()