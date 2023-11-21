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
	return 5, ["red", "green", "blue"] # for testing

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
# RENDER
# render() creates the window and draws the patches on it,
# according to the patchwork array and the given size
# patchwork - array of patches to be drawn
# size - the grid size of the patchwork (eg, 7 will draw 7x7)
#####################
def render(patchwork, size):
	winSize = patchSize * size
	win = GraphWin("Patchwork", winSize, winSize)

	win.setBackground("grey") # for testing to see the boundaries of the drawing area
	
	x, y = 0, 0 # top left coords of the patch
	i = 0 # to keep track of which patch we're on

	for patch in patchwork:

		if patch["type"] == "N":
			drawPatchN(win, x, y, patch["colour"])
		elif patch["type"] == "P":
			drawPatchP(win, x, y, patch["colour"])
		elif patch["type"] == "F":
			drawPatchF(win, x, y, patch["colour"])
		else:
			print("Invalid patch type specified!")
			
		x += patchSize  # move onto next column
		i += 1 # increment patch counter
		
		# move onto the next row if we've reached the end of the row
		if (i % size == 0) and (i != 0):
			x = 0
			y += patchSize
	
	win.getMouse()


#####################
# PATCH DRAWING
# x and y are top left coords of the patch
# For testing, these are a simple square, circle and triangle
#####################

# To draw a plain coloured patch, just draw a square
# N for "Nothing"
def drawPatchN(win, x, y, colour):
	square = Rectangle(Point(x, y), Point(x + patchSize, y + patchSize))
	square.setFill(colour)
	square.draw(win)
	return square

# This is the patch that is the word "HI" tiled (#8)
# P = Penultimate digit of student number
def drawPatchP(win, x, y, colour):
	# TODO: draw the "HI" patch
	# in the meantime, just draw a circle
	centre = Point(x + patchSize/2, y + patchSize/2)
	circle = Circle(centre, patchSize/2)
	circle.setFill(colour)
	circle.draw(win)
	return circle

# This is the patch that looks like a slanted eye (#5)
# F = Final digit of student number
# Code copied verbatim from the programming worksheet
def drawPatchF(win, x, y, colour):
	# Top Half
	for i in range(0, 110, 10):
		line = Line(Point(i+x, y), Point(100+x, i+y))
		line.setOutline(colour)
		line.draw(win)

	# Bottom Half
	for i in range(0, 110, 10):
		line = Line(Point(x, i+y), Point(i+x, 100+y))
		line.setOutline(colour)
		line.draw(win)

#####################
# Main, program entry
#####################
def main():
	patchwork = []

	gridSize, colours = getUserInput()

	# generate random patchwork, for testing
	for _ in range(0, gridSize*gridSize):
		patchwork.append({
			"type": ["F", "P", "N"][randint(0, 2)],
			"colour": colours[randint(0, len(colours) - 1)]
		})
	
	render(patchwork, gridSize)

main()