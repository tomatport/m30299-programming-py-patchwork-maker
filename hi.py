from graphics import *

def makePatchP(tlX, tlY, colour):
	patchElements = []

	tlX, tlY = int(tlX), int(tlY)  # convert to ints to avoid float errors
	colI, rowI = 0, 0  # keep track of which row and column we're on, for the colours

	for y in range(tlY, tlY + 100, 25):
		for x in range(tlX, tlX + 100, 50):

			if (colI + rowI) % 2 == 0:  # both should be even or odd
				colours = [colour, "white"]  # colour background, white foreground
			else:
				colours = ["white", colour]  # white background, colour foreground

			# background of the H
			bgH = Rectangle(Point(x, y), Point(x + 25, y + 25))
			bgH.setFill(colours[0])
			patchElements.append(bgH)

			# hide middle top and middle bottom of the bg to make the H
			fgHTop = Rectangle(Point(x + 5, y), Point(x + 20, y + 10))
			fgHTop.setFill(colours[1])
			patchElements.append(fgHTop)

			fgHBottom = Rectangle(Point(x + 5, y + 15), Point(x + 20, y + 25))
			fgHBottom.setFill(colours[1])
			patchElements.append(fgHBottom)

			# background of the I
			bgI = Rectangle(Point(x + 25, y), Point(x + 50, y + 25))
			bgI.setFill(colours[0])
			patchElements.append(bgI)

			# hide middle left and middle right of the bg to make the I
			fgILeft = Rectangle(Point(x + 25, y + 5), Point(x + 35, y + 20))
			fgILeft.setFill(colours[1])
			patchElements.append(fgILeft)

			fgIRight = Rectangle(Point(x + 40, y + 5), Point(x + 50, y + 20))
			fgIRight.setFill(colours[1])
			patchElements.append(fgIRight)

			colI += 1  # increment column counter
		rowI += 1  # increment row counter

	return patchElements


def makePatchPNew(tlX, tlY, colour):
	patchElements = []

	tlX, tlY = int(tlX), int(tlY)  # convert to ints to avoid float errors

	return patchElements
	

def main():
	win = GraphWin("Patch", 500, 500)
	
	colour = "red"

	while True:
		click = win.getMouse()
		tlX, tlY = click.getX(), click.getY()
		patch = makePatchPNew(tlX, tlY, colour)

		for element in patch:
			element.draw(win)

main()