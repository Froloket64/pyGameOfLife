## Imports
from os import system
from time import sleep
import pygame as pg
import sys

pg.init()
clock = pg.time.Clock()


## Color Constants
BLACK = (0 , 0 , 0)
GREY = (46, 46, 46)
WHITE = (255 , 255 , 255)


## A window instance
windowSize = 600
window = pg.display.set_mode((windowSize, windowSize))  ## Setting the window's size
window.fill(GREY)  ## Setting the window's color


## Drawing the board (cells)
size = 20
l = windowSize / size

for vert in range(size + 1):  ## VERTical lines
    pg.draw.line(window, BLACK, (vert * l, 0), (vert * l, size * l))
for horiz in range(size + 1):  ## HORIZontal lines
    pg.draw.line(window, BLACK, (0, horiz * l), (size * l, horiz * l))


## Showing the board on the screen
pg.display.update()


## The real (backend) board
board = [[f'O:{h}:{v}' for v in range(size)] for h in range(size)]


## Base configuration (1st generation)
board[1][4] = board[1][4].replace('O', 'X')
board[2][4] = board[2][4].replace('O', 'X')
board[3][4] = board[3][4].replace('O', 'X')
board[5][4] = board[5][4].replace('O', 'X')
board[0][size - 1] = board[0][size - 1].replace('O','X')



## The real stuff begins
interval = 0.5  ## Interval between updates
while True:  ## == "on each update (with -inteval-)"
    for event in pg.event.get():  ## Check what's happening
        if event.type == pg.QUIT:  ## If a cross (exit) button was pressed,
            pg.quit()              ## close the program
            sys.exit()             ## (properly ;) )

        if event.type == pg.KEYDOWN:  ## - Key Bindings -
            if event.key == pg.MOUSEBUTTONDOWN:  ## - Mouse Bindings -
                if (event.button == 4) and (interval - 1 != 0):  ## If a scroll up was performed (and interval don't go into 0),
                    interval -= .1  ## Increase the speed
                elif event.button == 5:  ## If a scroll down was performed,
                    interval += .1  ## Decrease the speed

    system('clear')


    ## Just another way of viewing the current config.
    ## Useful for debug, that's all.
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


    ## The LOGIC!
    ##  Plan:
    ## 1. [ ] Get a list of all neighbors   !!!?
    ## 2. [-] Check amount of alive ones
    ## 3. [-] Change the cell's state
    for row in board:
        for cell in row:
            isAlive = cell.split(':')[0]
            column = int( cell.split(':')[1] )
            line = int( cell.split(':')[2] )

            isUpperAlive = board[line - 1][column][0] == 'X' if line - 1 >= 0 else False  ## Check the upper one
            isLowerAlive = board[line - 1][column][0] == 'X' if (line + 1) & size else False  ## Check the lower one
            isLeftAlive = board[line - 1][column][0] == 'X' if column - 1 >= 0 else False  ## Check the left one
            isRightAlive = board[line - 1][column][0] == 'X' if (column + 1) % size else False  ## Check the right one

            neighbors = 0


            ## Increasing the neighbor counter (when needed)
            if isUpperAlive:
                neighbors += 1
            if isLowerAlive:
                neighbors += 1
            if isLeftAlive:
                neighbors += 1
            if isRightAlive:
                neighbors += 1

            ## Modifying the cell's state, based
            ## on the amount of neighbors
            if isAlive == 'X':
                if neighbors <= 1:
                    board[line][column] = 'O' + cell[1:]
                elif neighbors == 2 or neighbors == 3:
                    continue
                elif neighbors > 3:
                    board[line][column] = 'O' + cell[1:]
            elif isAlive == 'O':
                if neighbors == 3:
                    board[line][column] = 'X' + cell[1:]


    pg.display.update()  ## Updating the screen ;)

    sleep(1)  ## Waiting... (speed of the game)
    # clock.tick(60)
