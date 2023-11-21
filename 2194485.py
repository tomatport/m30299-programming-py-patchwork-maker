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
	gridSize = None
	validGrid = [3, 7, 9]

	colours = []
	validColours = ["red", "green", "blue", "magenta", "orange", "yellow", "cyan"]

	while True:
		givenSize = input("Enter the grid size: ")
		
		if not givenSize.isdigit():  # check if input is a number
			print("Invalid grid size entered!\nMust be a number.")
			continue

		# if it is a number, check if it's a valid grid size
		if int(givenSize) in validGrid:
			gridSize = int(givenSize)  # update global grid variable to input
			break
		else:
			print(f"Invalid grid size entered!\nMust be one of {validGrid}")


	while len(colours) < 3: # request 3 colours
		while True:
			colour = input("Enter a colour: ")

			if colour in colours:
				print("Colour already entered!")
				continue

			if colour in validColours:
				colours.append(colour)
				break
			else:
				print(f"Invalid colour entered!\nMust be one of {validColours}")

	return gridSize, colours


#####################
# RENDER
# render() creates the window and draws the patches on it,
# according to the patchwork array and the given size
# patchwork - array of patches to be drawn
# size - the grid size of the patchwork (eg, 7 will draw 7x7)
#####################
def render(patchwork, size):
	win = GraphWin("Patchwork", patchSize * size, patchSize * size)
	
	# top left coords of the patch
	x = 0
	y = 0

	for patch in patchwork:
		print(patch, x, y)
		
		if patch["type"] == 1:
			drawPatch1(win, x, y, patch["colour"])
		elif patch["type"] == 2:
			drawPatch2(win, x, y, patch["colour"])
		elif patch["type"] == 3:
			drawPatch3(win, x, y, patch["colour"])
		else:
			print("Invalid patch type specified!")
			

		# move onto next column
		x += patchSize

		# move onto the next row if we've reached the end of the row
		if (x % size == 0) and (x != 0):
			x = 0
			y += patchSize
	
	win.getMouse()


#####################
# PATCH DRAWING
# x and y are top left coords of the patch
# For testing, these are a simple square, circle and triangle
#####################

def drawPatch1(win, x, y, colour):
	square = Rectangle(Point(x, y), Point(x + patchSize, y + patchSize))
	square.setFill(colour)
	square.draw(win)
	return square

def drawPatch2(win, x, y, colour):
	circle = Circle(Point(x + patchSize/2, y + patchSize/2), patchSize/2)
	circle.setFill(colour)
	circle.draw(win)
	return circle

def drawPatch3(win, x, y, colour):
	triangle = Polygon(Point(x, y), Point(x + patchSize, y), Point(x + patchSize/2, y + patchSize))
	triangle.setFill(colour)
	triangle.draw(win)
	return triangle

#####################
# Main, program entry
#####################
def main():
	patchwork = []

	gridSize, colours = getUserInput()

	# generate random patchwork, for testing
	for _ in range(0, gridSize*gridSize):
		patchwork.append({
			"type": randint(1, 3),
			"colour": colours[randint(0, len(colours) - 1)]
		})
	
	render(patchwork, 3)

main()