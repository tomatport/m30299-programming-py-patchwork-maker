from graphics import *

def hiPatchTest():
	win = GraphWin("Patch", 100, 100)
	win.setBackground("grey")


	# background of the H
	backgroundH = Rectangle(Point(0, 0), Point(25, 25))
	backgroundH.setFill("red")
	backgroundH.draw(win)

	# foreground rectangles to make the H
	foregroundH1 = Rectangle(Point(5, 0), Point(20, 10))
	foregroundH1.setFill("white")
	foregroundH1.draw(win)

	foregroundH2 = Rectangle(Point(5, 15), Point(20, 25))
	foregroundH2.setFill("white")
	foregroundH2.draw(win)


	# background of the I
	backgroundI = Rectangle(Point(25, 0), Point(50, 25))
	backgroundI.setFill("red")
	backgroundI.draw(win)

	# foreground rectangles to make the I
	foregroundI1 = Rectangle(Point(25, 5), Point(35, 20))
	foregroundI1.setFill("white")
	foregroundI1.draw(win)

	foregroundI2 = Rectangle(Point(40, 5), Point(50, 20))
	foregroundI2.setFill("white")
	foregroundI2.draw(win)

	win.getMouse()


def drawHiPatch(win, tlX, tlY):
	letterWidth = 50
	letterHeight = 25
	
	tlX, tlY = int(tlX), int(tlY) # convert to ints to avoid float errors
	xI, yI = 0, 0 # keep track of which row and column we're on, for the colours

	for y in range(tlY, tlY + 100, 25):
		for x in range(tlX, tlX + 100, 50):
			
			if (xI + yI) % 2 == 0: # both should be even or odd
				colours = ["red", "white"] # red background, white foreground
			else:
				colours = ["white", "red"] # white background, red foreground

			# background of the H
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

			yI += 1 # increment column counter
		xI += 1 # increment row counter

def main():
	win = GraphWin("Patch", 1000, 1000)
	win.setBackground("grey")

	while True:
		click = win.getMouse()
		drawHiPatch(win, click.getX(), click.getY())

	win.getMouse()

main()