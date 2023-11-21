# University of Portsmouth
# M30299 Programming, Assessment Item 3
# Python Coursework: A Patchwork Maker

# Thomas Robinson, up2194485
# November/December 2023

# Repo: https://github.com/tomatport/m30299-programming-py-patchwork-maker

from graphics import *

# configurable variables
patchSize = 100

def main():
	patchwork = [
		{"type": 1, "colour": "red"},
		{"type": 1, "colour": "green"},
		{"type": 1, "colour": "blue"},
		{"type": 2, "colour": "red"},
		{"type": 2, "colour": "green"},
		{"type": 2, "colour": "blue"},
		{"type": 3, "colour": "red"},
		{"type": 3, "colour": "green"},
		{"type": 3, "colour": "blue"}
	]
	
	render(patchwork, 3)


# render() creates the window and draws the patches on it,
# according to the patchwork array and the given size
# patchwork - array of patches to be drawn
# size - the grid size of the patchwork (eg, 7 will draw 7x7)
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


# x and y are top left coords of the patch
def drawPatch1(win, x, y, colour):
	square = Rectangle(Point(x, y), Point(x + patchSize, y + patchSize))
	square.setFill(colour)
	square.draw(win)


def drawPatch2(win, x, y, colour):
	circle = Circle(Point(x + patchSize/2, y + patchSize/2), patchSize/2)
	circle.setFill(colour)
	circle.draw(win)


def drawPatch3(win, x, y, colour):
	triangle = Polygon(Point(x, y), Point(x + patchSize, y), Point(x + patchSize/2, y + patchSize))
	triangle.setFill(colour)
	triangle.draw(win)


main()