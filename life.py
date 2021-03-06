## TODO:
## 1. Make a better neighborShow implementation
## ? 2. Rewrite the whole damn thing to be more functional programming-like

## Imports
from os import system
from math import ceil
import pygame as pg
import sys

pg.init()
clock = pg.time.Clock()

print('''
"""
Key Bindings:

esc - Exit
space - Pause
r - Clear
"""''')  ## Yeah, that's just a hint for keybinds

debug = 0  ## The level of debug info:
## 0: No output
## 1: Terminal board
## 2: ^^^ and detailed cell info

assert debug in (0, 1, 2), "`debug` should equal 0, 1 or 2"


## Colors
BLACK = (0 , 0 , 0)
GREY = (46, 46, 46)
WHITE = (255 , 255 , 255)


## The real (backend) board
size = 20

board = [[f'O:{h}:{v}:O' for v in range(size)] for h in range(size)]


## Creating a window instance
windowSize = (720, 720)  ## A hint: you can add some width on [0] if you would like to make a tools section on the right, it'll not break anything
window = pg.display.set_mode(windowSize)  ## Setting the window's size
window.fill(GREY)  ## Setting the window's color


## Drawing the board (cells)
l = windowSize[1] / size  ## Why "l"? ... God knows

for vert in range(size + 1):  ## VERTical lines
	pg.draw.line(window, BLACK, (vert * l, 0), (vert * l, size * l))
for horiz in range(size + 1):  ## HORIZontal lines
	pg.draw.line(window, BLACK, (0, horiz * l), (size * l, horiz * l))


## Showing the board on the screen
pg.display.update()


## Clearing the board
def clear(board):
	for row in board:
		for cell in row:
			line = int( cell.split(':')[1] )
			column = int( cell.split(':')[2] )

			board[line][column] = cell.replace('X', 'O')


fps = 10  ## Well, FPS
timeScale = 1  ## 1 == Time going (is that the word?); 0 == Time stopped (oh yeah)
while True:  ## == "on each frame"
	assert timeScale in (0, 1), "Wow, a strange thing mystifying: timeScale not 0 nor 1"
	###  ! Events tracking  ###
	for event in pg.event.get():  ## For each event happened,
		if event.type == pg.QUIT:  ## If a cross (exit) button was pressed,
			pg.quit()              ## close the program
			sys.exit()             ## (properly)

		if event.type == pg.KEYDOWN:  ## - Key Bindings -
			if event.key == pg.K_ESCAPE:  ## esc
				pg.quit()  ##  |-- Exit
				sys.exit()  ## |
			
			if event.key == pg.K_SPACE:  ## space
				timeScale = (timeScale + 1) % 2  ## Well, if not going in detail, stop/resume time on space press
			
			if event.key == pg.K_r:  ## r
				clear(board)  ## "Clearing the board"

		if event.type == pg.MOUSEBUTTONDOWN:  ## - Mouse Bindings -
			if event.button == 1:  ## If LMB is pressed
				if event.pos[0] <= windowSize[1] and event.pos[1] <= windowSize[1]:  ## and the click is in board zone (just in case you'd want to add some non-board space)
					x = event.pos[0]
					y = event.pos[1]

					board[ceil(y // l)][ ceil(x // l) ] = board[ceil(y // l)][ ceil(x // l) ].replace('O', 'X')  ## Make the cell under cursor alive

			if event.button == 3:  ## If RMB is pressed
				if event.pos[0] <= windowSize[1] and event.pos[1] <= windowSize[1]:  ## and the click is in board zone (just in case you'd want to add some non-board space)
					x = event.pos[0]
					y = event.pos[1]

					board[ceil(y // l)][ ceil(x // l) ] = board[ceil(y // l)][ ceil(x // l) ].replace('X', 'O')  ## Make the cell under cursor dead

			elif (event.button == 4) and (fps + 1 != 10):  ## On scroll up
				fps += 1  ## Increase the speed (to the max of 15FPS)
			if (event.button == 5) and (fps - 1 != 0):  ## On scroll down
				fps -= 1  ## Decrease the speed (if only fps don't turn 0)


	## Redrawing the grey squares,
	## because otherwise the white ones
	## will not disappear
	for row in board:
		for cell in row:
			left = int( cell.split(':')[1] )
			top = int( cell.split(':')[2] )
			pg.draw.rect( window, GREY, pg.Rect(top * l, left * l, l, l) )

	for vert in range(size + 1):  ## VERTical lines
		pg.draw.line(window, BLACK, (vert * l, 0), (vert * l, size * l))
	for horiz in range(size + 1):  ## HORIZontal lines
		pg.draw.line(window, BLACK, (0, horiz * l), (size * l, horiz * l))


	neighborShow = {}

	## Cleaning all previous terminal
	## debug output
	if debug != 0:
		system('clear')


	## Just another way of viewing the current config.
	## Useful for debug, that's all.
	if debug >= 1:
		dboard = ''
		for row in board:
			for cell in row:
				if cell[0] == 'O':
					dboard += '- '
				elif cell[0] == 'X':
					dboard += 'X '
			dboard += '\n'

		print(dboard)
		# print(board)


	## The cell display
	for row in board:
		for cell in row:
			if cell[0] == 'X':
				left = int( cell.split(':')[1] )
				top = int( cell.split(':')[2] )
				pg.draw.rect( window, WHITE, pg.Rect(top * l, left * l, l, l) )


	###  ! The LOGIC  ###
	if timeScale == 1:
		for row in board:
			for cell in row:
				isAlive = cell.split(':')[0]
				line = int( cell.split(':')[1] )
				column = int( cell.split(':')[2] )

				neighbors = -1 if isAlive == 'X' else 0 
				## Because it will count itself later on (if it is
				## alive), we need to negate that by subtracting
				## it from the counter


				## Increasing the neighbor counter (if they are alive)
				for hi in range(-1, 2):  # in (-1, 0, 1):
					if line + hi in range(0, size):
						for vi in range(-1, 2):
							if column + vi in range(0, size):
								if board[line + hi][column + vi][0] == 'X':
									neighbors += 1


				## Changing the cell's state based
				## on the amount of neighbors alive
				if isAlive == 'X':
					if neighbors <= 1:
						board[line][column] = cell[:-1] + 'O'
					elif neighbors in (2, 3):
						continue
					elif neighbors > 3:
						board[line][column] = cell[:-1] + 'O'
				else:
					if neighbors == 3:
						board[line][column] = cell[:-1] + 'X'

				if debug == 2:
					neighborShow.update({cell: neighbors})

	if debug == 2:
		print(neighborShow)
	
	if timeScale == 1:
		for row in board:
			for cell in row:
				line = int( cell.split(':')[1] )
				column = int( cell.split(':')[2] )

				board[line][column] = cell.replace(cell[0], cell[-1])

	pg.display.update()  ## Updating the screen

	clock.tick(fps)  ## Setting the FPS (and speed of the game)