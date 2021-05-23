## Imports
from os import system
from time import sleep
import pygame as pg
import sys

pg.init()


## Color Constants
BLACK = (0 , 0 , 0)
GREY = (46, 46, 46)
WHITE = (255 , 255 , 255)


## A window instance
window = pg.display.set_mode((700, 500))  ## Setting the window's size
window.fill(GREY)  ## Setting the window's color


## Drawing the board (cells)
size = 10

for vert in range(size + 1):  ## VERTical lines
    pg.draw.line(window, BLACK, (vert * 20, 0), (vert * 20, window.get_height()))
for horiz in range(size + 1):  ## HORIZontal lines
    pg.draw.line(window, BLACK, (0, horiz * 20), (window.get_width(), horiz * 20))


## Showing the board on the screen
pg.display.update()


## The real (backend) board
board = [[f'O:{h}:{v}' for v in range(size)] for h in range(size)] # [[0 for i in range(size)] for ii in range(size)]
## Hint: ^^^ for such stuff: 0 0 1 1 0
##                                 ^ -- index? --> 2 (NOT GOOD)


## Base configuration (1st )
board[1][4] = board[1][4].replace('O', 'X')
board[2][4] = board[2][4].replace('O', 'X')
board[3][4] = board[3][4].replace('O', 'X')
board[5][4] = board[5][4].replace('O', 'X')



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


    ## The cell display
    for row in board:
        for cell in row:
            if cell[0] == 'X':
                left = int( cell.split(':')[1] )
                top = int( cell.split(':')[2] )
                pg.draw.rect( window, WHITE, pg.Rect(top*20, left*20, 20, 20) )


    ## The LOGIC!
    ## it's kinda empty...


    ## Just another way of viewing the current config.
    ## Useful for debug, that's all.
    dboard = ''
    for row in board:
        for each in row:
            if each[0] == 'O':
                dboard += '- '
            elif each[0] == 'X':
                dboard += 'X '
        dboard += '\n'

    print(dboard)
    # print(board)


    sleep(interval)

    pg.display.update()
