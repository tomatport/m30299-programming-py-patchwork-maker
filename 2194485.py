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
#####################

# PLAIN PATCH
# To draw a plain coloured patch, we just draw a square :)
def drawPatchPlain(win, tlX, tlY, colour):
	square = Rectangle(Point(tlX, tlY), Point(tlX + patchSize, tlY + patchSize))
	square.setFill(colour)
	square.draw(win)

# PENULTIMATE DIGIT PATCH
# This is the patch that is the word "HI" tiled (#8)
def drawPatchP(win, tlX, tlY, colour):	
	tlX, tlY = int(tlX), int(tlY) # convert to ints to avoid float errors
	colI, rowI = 0, 0 # keep track of which row and column we're on, for the colours

	for y in range(tlY, tlY + 100, 25):
		for x in range(tlX, tlX + 100, 50):
			
			if (colI + rowI) % 2 == 0: # both should be even or odd
				colours = [colour, "white"] # colour background, white foreground
			else:
				colours = ["white", colour] # white background, colour foreground

			# background of the H
			# TODO: is there anything one can do to remove all of these manual offsets?
			bgH = Rectangle(Point(x, y), Point(x + 25, y + 25))
			bgH.setFill(colours[0])
			bgH.draw(win)

			# hide middle top and middle bottom of the bg to make the H
			fgHTop = Rectangle(Point(x + 5, y), Point(x + 20, y + 10))
			fgHTop.setFill(colours[1])
			fgHTop.draw(win)

			fgHBottom = Rectangle(Point(x + 5, y + 15), Point(x + 20, y + 25))
			fgHBottom.setFill(colours[1])
			fgHBottom.draw(win)

			# background of the I
			bgI = Rectangle(Point(x + 25, y), Point(x + 50, y + 25))
			bgI.setFill(colours[0])
			bgI.draw(win)

			# hide middle left and middle right of the bg to make the I
			fgILeft = Rectangle(Point(x + 25, y + 5), Point(x + 35, y + 20))
			fgILeft.setFill(colours[1])
			fgILeft.draw(win)

			fgIRight = Rectangle(Point(x + 40, y + 5), Point(x + 50, y + 20))
			fgIRight.setFill(colours[1])
			fgIRight.draw(win)

			colI += 1 # increment column counter
		rowI += 1 # increment row counter

# FINAL DIGIT PATCH
# This is the patch that has grid lines surrounding a slanted eye shape (#5)
# Code copied verbatim from the programming worksheet
def drawPatchF(win, tlX, tlY, colour):
	# Top Half
	for i in range(0, 110, 10):
		line = Line(Point(i+tlX, tlY), Point(100+tlX, i+tlY))
		line.setOutline(colour)
		line.draw(win)

	# Bottom Half
	for i in range(0, 110, 10):
		line = Line(Point(tlX, i+tlY), Point(i+tlX, 100+tlY))
		line.setOutline(colour)
		line.draw(win)


#####################
# PATCH LAYOUT
# Compute the layout of the patches, using the provided images
#####################
def computePatchLayout(gridSize, colours):
	# init patchwork array of all empty patches
	patchwork = []
	
	for row in range(0, gridSize):
		patchwork.append([]) # each row is an array of patches
		for _ in range(0, gridSize): # for each patch in the row
			patchwork[row].append({
				"type": None,
				"colour": None
			})
	# we now have an array of empty patches, corresponding to the grid size

	# TODO: implement patch layout algorithms
	# first, set patch types
	# then, set correct colours
	
	# in the meantime, randomly assign patch types and colours
	for row in patchwork:
		for patch in row:
			patch["type"] = ["F", "P", "N"][randint(0, 2)]
			patch["colour"] = colours[randint(0, len(colours) - 1)]

	# display the patchwork array, for testing
	for row in patchwork:
		print(row)

	return patchwork

#####################
# RENDER
# render() creates the window and draws the patches on it,
# according to the patchwork array and the given size
# patchwork - array of patches to be drawn
# gridSize - the grid size of the patchwork (eg, 7 will draw 7x7)
#####################
def render(patchwork, gridSize):
	winSize = patchSize * gridSize
	win = GraphWin("Patchwork", winSize, winSize)

	# for testing to see the boundaries of the drawing area
	win.setBackground("grey")

	colI, rowI = 0, 0 # keep track of which row and column we're on, to get patch from patchwork

	# x and y here are the actual coords of the patch, not the array indices
	for y in range(0, winSize, patchSize): 
		for x in range(0, winSize, patchSize):
			patch = patchwork[colI][rowI]

			if patch["type"] == "N":
				drawPatchPlain(win, x, y, patch["colour"])
			elif patch["type"] == "P":
				drawPatchP(win, x, y, patch["colour"])
			elif patch["type"] == "F":
				drawPatchF(win, x, y, patch["colour"])
			else:
				print("Invalid patch type specified!")

			if colI == gridSize - 1:
				colI = 0
			else:
				colI += 1

		rowI += 1

	win.getMouse()

#####################
# Main, program entry
#####################
def main():
	gridSize, colours = getUserInput()

	patchwork = computePatchLayout(gridSize, colours)
	render(patchwork, gridSize)

main()