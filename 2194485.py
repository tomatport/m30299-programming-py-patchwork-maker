# University of Portsmouth
# M30299 Programming, Assessment Item 3
# Python Coursework: A Patchwork Maker

# Thomas Robinson, up2194485
# November/December 2023

# Repo: https://github.com/tomatport/m30299-programming-py-patchwork-maker

from graphics import *

# CONSTANTS
PATCHSIZE = 100
BORDERWIDTH = PATCHSIZE // 25 # 4 if PATCHSIZE is 100
VALIDCOLOURS = ["red", "green", "blue", "magenta", "orange", "yellow", "cyan"]
VALIDGRID = [5, 7, 9]

# SHAPES
def makeRectangle(tlX, tlY, brX, brY, colour):
	"""
	Creates a rectangle with the given parameters

	Parameters:
		- tlX, tlY (int): Top left X and Y cords
		- brX, brX (int): Bottom right X and Y cords
		- colour (string): Colour of the rectangle
	
	Returns:
		- Rectangle object
	"""
	rect = Rectangle(Point(tlX, tlY), Point(brX, brY))
	rect.setFill(colour)
	return rect


def makeLine(tlX, tlY, brX, brY, colour):
	"""
	Creates a line with the given parameters

	Parameters:
		- tlX, tlY (int): Top left X and Y cords
		- brX, brX (int): Bottom right X and Y cords
		- colour (string): Colour of the line

	Returns:
		- Line object
	"""

	line = Line(Point(tlX, tlY), Point(brX, brY))
	line.setFill(colour)
	return line


# PATCH DRAWING

# Plain Patch
def makePatchPlain(tlX, tlY, colour):
	"""
		Creates a plain patch (a solid square) with the given parameters

		Parameters:
			- tlX, tlY (int): Top left X and Y cords
			- colour (string): Colour of the patch
		
		Returns:
			- List of elements that make up the patch
	"""

	square = makeRectangle(tlX, tlY, tlX + PATCHSIZE, tlY + PATCHSIZE, colour)
	return [square] # only one element in this patch


# Penultimate Digit Patch
def makeHIForeground(tlX, tlY, colour):
	"""
		Creates the "HI" text with the given colour as the foreground, on a white background

		Parameters:
			- tlX, tlY (int): Top left X and Y cords
			- colour (string): Colour of the foreground
		
		Returns:
			- List of elements that make up the "HI" text
	"""

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
	"""
		Creates the "HI" text with the given colour as the background, on a white foreground

		Parameters:
			- tlX, tlY (int): Top left X and Y cords
			- colour (string): Colour of the background
		
		Returns:
			- List of elements that make up the "HI" text
	"""

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
	"""
		Creates the penultimate patch (the "HI" text) with the given parameters,
		using makeHIForeground() and makeHIBackground()

		Parameters:
			- tlX, tlY (int): Top left X and Y cords
			- colour (string): Colour of the patch

		Returns:
			- List of elements that make up the patch
	"""

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

# Final Digit Patch
def makePatchFinal(tlX, tlY, colour):
	"""
		Creates the final digit patch (eye shape surrounding by gridlines)

		Parameters:
			- tlX, tlY (int): Top left X and Y cords
			- colour (string): Colour of the patch

		Returns:
			- List of elements that make up the patch
	"""

	patchElements = []

	for i in range(0, PATCHSIZE+10, 10):  # Top Half
		line = makeLine(i+tlX, tlY, PATCHSIZE+tlX, i+tlY, colour)
		patchElements.append(line)

	for i in range(0, PATCHSIZE+10, 10):  # Bottom Half
		line = makeLine(tlX, i+tlY, i+tlX, PATCHSIZE+tlY, colour)
		patchElements.append(line)

	return patchElements


# PATCH COLOURING
def computePatchColour(row, col, gridSize, colours):
	"""
		Given the position of a patch, figure out what colour it should be

		Parameters:
			- row, col (int): Row and column of the patch
			- gridSize (int): Size of the grid
			- colours (list): List of colours to choose from

		Returns:
			- String of the colour to use
	"""

	gridMid = gridSize // 2  # middle of the grid

	if row < gridMid and col < gridMid:  # TOP LEFT CORNER (blue in example)
		return colours[0]

	if row < gridMid and col > gridMid:  # TOP RIGHT CORNER (red)
		return colours[2]

	if row > gridMid and col < gridMid:  # BOTTOM LEFT CORNER (red)
		return colours[2]

	if row > gridMid and col > gridMid:  # BOTTOM RIGHT CORNER (blue)
		return colours[0]

	if row == gridMid or col == gridMid:  # CROSS (orange)
		return colours[1]

	return "black"  # if we're here, we missed something


# PATCH LAYOUT
def computePatchLayout(gridSize, colours):
	"""
		Computes the layout of the patches

		Parameters:
			- gridSize (int): Size of the grid
			- colours (list): List of colours to choose from

		Returns:
			- 2D array containing the patches with their correct elements
			  (patchwork[row][col] = patch dict)
	"""

	# make an array of empty patches
	patchwork = makeEmptyPatchwork(gridSize)

	# fill the patches with the correct elements
	patchwork = fillFinalPatches(patchwork, gridSize, colours)
	patchwork = fillPenultimatePatches(patchwork, gridSize, colours)
	patchwork = fillPlainPatches(patchwork, gridSize, colours)

	return patchwork


def makeEmptyPatchwork(gridSize):
	"""
		Makes an empty patchwork array

		Parameters:
			- gridSize (int): Size of the grid (eg, 5 for 5x5)

		Returns:
			- 2D array containing empty patches (patchwork[row][col] = patch dict)
	"""

	patchwork = []

	for row in range(0, gridSize):
		patchwork.append([])
		for _ in range(0, gridSize): # for each patch in the row
			patchwork[row].append({
				"elements": [], # the elements that make up the patch, so we can modify them later
				"selected": False, # whether the patch is selected or not (for the challenge)
				"border": [] # the border around the patch (for the challenge)
			})

	return patchwork


# PATCH FILLING
def fillFinalPatches(patchwork, gridSize, colours):
	"""
		Fills in a given patchwork array with the final digit patch design

		Parameters:
			- patchwork (2D array): Patchwork array to add the final digit patches to
			- gridSize (int): Size of the grid
			- colours (list): List of colours to choose from

		Returns:
			- 2D array with the final digit patches added in the correct places
	"""

	filledPatchwork = patchwork

	for rowI in range(0, gridSize):  # every row
		for colI in range(0, gridSize, 2):  # every other column
			x, y = colI * PATCHSIZE, rowI * PATCHSIZE
			patchwork[rowI][colI]["elements"] = makePatchFinal(
				x, y, computePatchColour(rowI, colI, gridSize, colours))

	return filledPatchwork


def fillPenultimatePatches(patchwork, gridSize, colours):
	"""
		Fills in a given patchwork array with the penultimate digit patch design

		Parameters:
			- patchwork (2D array): Patchwork array to add the penultimate digit patches to
			- gridSize (int): Size of the grid
			- colours (list): List of colours to choose from

		Returns:
			- 2D array with the penultimate digit patches added in the correct places
	"""

	filledPatchwork = patchwork

	for rowI in range(0, gridSize): # every row
		for colI in range(1, gridSize, 2): # every other column, but offset by 1
			x, y = colI * PATCHSIZE, rowI * PATCHSIZE
			filledPatchwork[rowI][colI]["elements"] = makePatchPenultimate(x, y, computePatchColour(rowI, colI, gridSize, colours))

	return filledPatchwork


def fillPlainPatches(patchwork, gridSize, colours):
	"""
		Fills in a given patchwork array with the plain patch design

		Parameters:
			- patchwork (2D array): Patchwork array to add the plain patches to
			- gridSize (int): Size of the grid
			- colours (list): List of colours to choose from

		Returns:
			- 2D array with the plain patches added in the correct places
	"""

	filledPatchwork = patchwork

	# the top and bottom of the columns of P patches are plain
	for colI in range(1, gridSize, 2): # every other column, offset by 1
		# top
		x, y = colI * PATCHSIZE, 0
		filledPatchwork[0][colI]["elements"] = makePatchPlain(
			x, y, computePatchColour(0, colI, gridSize, colours))

		# bottom
		x, y = colI * PATCHSIZE, (gridSize - 1) * PATCHSIZE
		filledPatchwork[gridSize - 1][colI]["elements"] = makePatchPlain(
			x, y, computePatchColour((gridSize-1), colI, gridSize, colours))
	
	return filledPatchwork


# DRAW PATCHES
def drawPatchElements(win, patchwork):
	"""
		Draws the elements of the patches in the given patchwork array to a window

		Parameters:
			- win (GraphWin): Window to draw the patches to
			- patchwork (2D array): Patchwork array to draw the patches from

		Returns:
			- None
	"""
	
	for row in patchwork:
		for patch in row:
			for element in patch["elements"]:
				element.setWidth(0) # remove outlines (there is no "none" option, only 0 width)
				element.draw(win)


# USER INPUT
def getUserInput():
	"""
		Asks the user for (and validates) the grid size and colours to use

		Parameters:
			- None

		Returns:
			A tuple containing:
			- gridSize (int): Size of the grid
			- colours (list): List of colours to use
	"""

	return 9, ["blue", "orange", "red"]  # for testing

	global VALIDCOLOURS, VALIDGRID

	gridSize = None
	colours = []

	print(f"= GRID SIZE =\nChoose one from {VALIDGRID}")
	while True:  # keep asking until valid
		givenSize = input("🧱 Enter the grid size: ")

		if not givenSize.isdigit():  # check if input is a number
			print("😔 That doesn't look like a number...\n")
			continue

		# if it is a number, check if it's a valid grid size
		givenSize = int(givenSize)
		if givenSize in VALIDGRID:
			gridSize = givenSize
			break
		else:
			print(f"😔 Your grid size must be one of {VALIDGRID}\n")

	print(f"\n= COLOURS =\nChoose 3 from {VALIDCOLOURS}")
	while len(colours) < 3:  # keep going until we have three colours
		while True:
			givenColCount = len(colours) + 1
			colour = input(f"🎨 Enter colour {givenColCount}/3: ")

			colour = colour.lower()  # convert input to lowercase for comparison

			if colour in colours:
				print(f"👀 You have already entered {colour}!\n")
				continue

			if colour in VALIDCOLOURS:
				colours.append(colour)
				break

			else:
				print(f"😔 That's a funny looking colour! Must be one of {VALIDCOLOURS}\n")

	return gridSize, colours

# SELECTION MODE (challenge feature)
def selectionMode(win, patchwork, gridSize):
	"""
		Handles the selection mode for the challenge feature

		Parameters:
			- win (GraphWin): Window to draw the patches to
			- patchwork (2D array): Patchwork array to draw the patches from
			- gridSize (int): Size of the grid (for the close button)

		Returns:
			- mode (string): The mode to enter next (edit or selection)
	"""

	clicked = win.getMouse()

	# if we clicked the ok button, enter edit mode
	if clicked.getX() < 30 and clicked.getY() < 30:
		return "edit"
	


	# which patch did we click on?
	rowI = int(clicked.getY() // PATCHSIZE)
	colI = int(clicked.getX() // PATCHSIZE)
	patch = patchwork[rowI][colI]

	# figure out our top left X and Y cords
	patchX = colI * PATCHSIZE
	patchY = rowI * PATCHSIZE

	patch["selected"] = not patch["selected"] # toggle selected state

	# draw border around patch
	if patch["selected"]:		
		# inset border (by BORDERWIDTH)		
		border = Rectangle(
				Point(patchX + BORDERWIDTH, patchY + BORDERWIDTH),
				Point(patchX + PATCHSIZE - BORDERWIDTH, patchY + PATCHSIZE - BORDERWIDTH)
			)
		border.setFill("")
		border.setWidth(BORDERWIDTH*2)
		border.setOutline("black")
		
		patch["border"] = border
		patch["border"].draw(win)
	else:
		patch["border"].undraw()

# EDIT MODE (challenge feature)
def editMode(win, patchwork, mode):
	"""
		Handles the edit mode for the challenge feature

		Parameters:
			- win (GraphWin): Window to draw the patches to
			- patchwork (2D array): Patchwork array to draw the patches from
			- mode (string): Current mode (selection or edit)

		Returns:
			- mode (string): If user pressed "s", returns "selection" to switch to selection mode
	"""

	selectedPatches = getSelectedPatches(patchwork)
	key = win.getKey()

	match key:
		case "s": # enter selection mode
			return "selection"
		
		case "d": # deselect all selected patches
			deselectAllPatches(patchwork)

		# colours
		case "r":
			updatePatchColour(selectedPatches, "red")
		case "g":
			updatePatchColour(selectedPatches, "green")
		case "b":
			updatePatchColour(selectedPatches, "blue")
		case "m":
			updatePatchColour(selectedPatches, "magenta")
		case "o":
			updatePatchColour(selectedPatches, "orange")
		case "y":
			updatePatchColour(selectedPatches, "yellow")
		case "c":
			updatePatchColour(selectedPatches, "cyan")
		
	return "edit" # stay in edit mode

		
def updatePatchColour(patches, colour):
	"""
		Given a list of patches, set their new fill colour

		Parameters:
			- patches (list): List of patches to update
			- colour (string): Colour to set the elements to
		
		Returns:
			- None
	"""
	
	for patch in patches:
		for element in patch["elements"]:
			element.setFill(colour)

def getSelectedPatches(patchwork):
	"""
		Gets a list of all the selected patches in the given patchwork array

		Parameters:
			- patchwork (2D array): Patchwork array to get the selected patches from

		Returns:
			- List of selected patches
	"""

	selectedPatches = []

	for row in patchwork:
		for patch in row:
			if patch["selected"]:
				selectedPatches.append(patch)

	return selectedPatches

def deselectAllPatches(patchwork):
	"""
		Deselect (and undraw the border of) all patches in the given patchwork array
		
		Parameters:
			- patchwork (2D array): Patchwork array to deselect the patches in

		Returns:
			- None
	"""

	for row in patchwork:
		for patch in row:
			patch["selected"] == False
			if patch["border"]: patch["border"].undraw()

def makeOkButton():
	"""
		Creates an OK button in the top left corner of the window
		
		Parameters:
			- None

		Returns:
			- okButton (list): List of elements that make up the button
	"""

	buttonElements = []

	buttonBG = Rectangle(Point(0, 0), Point(30, 30))
	buttonBG.setFill("black")
	buttonElements.append(buttonBG)

	buttonText = Text(Point(15, 15), "OK")
	buttonText.setTextColor("white")
	buttonElements.append(buttonText)

	return buttonElements

# MAIN
def main():
	"""
		Program entry point, joins all the other functions together
	"""

	gridSize, colours = getUserInput()

	winSize = PATCHSIZE * gridSize
	win = GraphWin("Patchwork", winSize, winSize)
	win.setBackground("white")

	patchwork = computePatchLayout(gridSize, colours)

	drawPatchElements(win, patchwork)

	# Challenge Feature: Selecting and Modifying Patches
	mode = "selection"

	# text displaying the current mode
	modeText = Text(Point(winSize//2, 10),  mode)
	modeText.setTextColor("black")
	modeText.draw(win)
		
	okButton = makeOkButton()

	while True:
		modeText.setText(mode)

		if mode == "selection":
			# in selection mode, we want the ok button
			for element in okButton:
				# draw if not already drawn
				if element not in win.items: element.draw(win)

			newMode = selectionMode(win, patchwork, gridSize)

			if newMode: mode = newMode

		elif mode == "edit":
			# in edit mode, we don't want the ok button
			for element in okButton: element.undraw()

			newMode = editMode(win, patchwork, mode)

			if newMode: mode = newMode


			

main()