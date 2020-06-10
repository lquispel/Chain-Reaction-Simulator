import pygame
import sys
from math import *
from ai import Atomic_Node
from board import Board
from pgameplayer.minimax_tree import *

# Initializing the Game grid
pygame.init()
sys.setrecursionlimit(7000)
if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")

width = 420
height = 420
grid_blocks = 70
d = grid_blocks / 2 - 2
cols = 6 # int(width / grid_blocks)
rows = 6 # int(height / grid_blocks)

display = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# Color Schema
border = Board.BORDER
background = (21, 67, 96)

red = (231, 76, 60)
green = (88, 214, 141)
white = (244, 246, 247)
violet = (136, 78, 160)
yellow = (244, 208, 63)
playerColor = [red, green, violet, yellow]
turns = 0
font = pygame.font.SysFont("Times New Roman", 30)


print("\n\n\t\tWELCOME TO CHAIN REACTION")
print("Recursion limit: " + str(sys.getrecursionlimit()))
print("Set recursion limit lower if you experience stack overflows.")
# player_count = int(input("\n\nEnter number of players between 2 to 4:\t"))

pygame.display.set_caption("Chain Reaction AI - Atomic Intelligence ! " )
player_count = 2

the_grid = []

# Initializing the_grid with null player account
def initialize_the_grid():
    global the_grid, players
    players = []
    for i in range(player_count):
        players.append(playerColor[i])
    the_grid = Board(cols,rows,playerColor,player_count)

#plotting the grid in pygame plot
def create_grid(currentIndex):
    r = 0
    c = 0
    for i in range(int(width / grid_blocks)):
        r += grid_blocks
        c += grid_blocks
        pygame.draw.line(display, players[currentIndex], (c, 0), (c, height))
        pygame.draw.line(display, players[currentIndex], (0, r), (width, r))

# display the current Situation of the_grid
def display_current_grid(vibrate=1):
    r = -grid_blocks
    c = -grid_blocks
    for i in range(cols):
        r += grid_blocks
        c = -grid_blocks
        for j in range(rows):
            c += grid_blocks
            if the_grid.get_cell_occupation(i,j) == 0:
                the_grid.set_cell_color(i,j,border)
            elif the_grid.get_cell_occupation(i,j) == 1:
                pygame.draw.ellipse(display, the_grid.get_cell_color(i,j),
                                    (r + grid_blocks / 2 - d / 2 + vibrate, c + grid_blocks / 2 - d / 2, d, d))
            elif the_grid.get_cell_occupation(i,j) == 2:
                pygame.draw.ellipse(display, the_grid.get_cell_color(i,j), (r + 5, c + grid_blocks / 2 - d / 2 - vibrate, d, d))
                pygame.draw.ellipse(display, the_grid.get_cell_color(i,j),
                                    (r + d / 2 + grid_blocks / 2 - d / 2 + vibrate, c + grid_blocks / 2 - d / 2, d, d))
            elif the_grid.get_cell_occupation(i,j) == 3:
                angle = 90
                x = r + (d / 2) * cos(radians(angle)) + grid_blocks / 2 - d / 2
                y = c + (d / 2) * sin(radians(angle)) + grid_blocks / 2 - d / 2
                pygame.draw.ellipse(display, the_grid.get_cell_color(i,j), (x - vibrate, y, d, d))
                x = r + (d / 2) * cos(radians(angle + 90)) + grid_blocks / 2 - d / 2
                y = c + (d / 2) * sin(radians(angle + 90)) + 5
                pygame.draw.ellipse(display, the_grid.get_cell_color(i,j), (x + vibrate, y, d, d))
                x = r + (d / 2) * cos(radians(angle - 90)) + grid_blocks / 2 - d / 2
                y = c + (d / 2) * sin(radians(angle - 90)) + 5
                pygame.draw.ellipse(display, the_grid.get_cell_color(i,j), (x - vibrate, y, d, d))
    pygame.display.update()

# GAME OVER
def gameOver(playerIndex):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    close()
                if event.key == pygame.K_r:
                    re_game()
        text = font.render("Player %d Won!" % (playerIndex + 1), True, white)
        text2 = font.render("Press \'r\' to Reset!", True, white)
        display.blit(text, (width / 3, height / 3))
        display.blit(text2, (width / 3, height / 2))
        pygame.display.update()
        clock.tick(60)

# After Game over terminate the Game Window
def close():
    pygame.quit()
    sys.exit()

# Main Loop
def re_game():
    global the_grid, players
    players = []
    for i in range(player_count):
        players.append(playerColor[i])
    the_grid = Board(cols,rows,playerColor,player_count)
    loop = True
    currentPlayer = 0
    vibrate = .5
    turns = 0
    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    close()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                i = int(x / grid_blocks)
                j = int(y / grid_blocks)
                if the_grid.move(i,j,playerColor[currentPlayer]):
                    print("Player Move: " + str(i) + "," + str(j))
                    display_current_grid()
                    currentPlayer += 1
                    if currentPlayer == 1:
                        if turns > 0:
                            node = Atomic_Node(the_grid, playerColor)
                            move, eval = depth_limited_minimax(node, 1, True)
                            for i in range(cols-1):
                                for j in range(rows-1):
                                    if the_grid.get_cell_occupation(i,j) != move.get_cell_occupation(i,j):
                                        break
                            the_grid.move(i,j,playerColor[currentPlayer])
                            currentPlayer += 1
                            print("AI Move: " + str(i) + "," + str(j) + "  value:" + str(eval))
                        else:
                            if not the_grid.move(0,0,playerColor[currentPlayer]):
                                the_grid.move(cols-1,rows-1,playerColor[currentPlayer])
                                print("AI Move: " + str(cols-1) + "," + str(rows-1))
                            else:
                                print("AI Move: 0,0")
                            currentPlayer += 1
                        if currentPlayer >= player_count:
                            currentPlayer = 0
                            turns += 1
                else:
                    print("No valid move !!! ")
        display.fill(background)
        # Vibrate the Atoms in their Cells
        vibrate *= -1
        create_grid(currentPlayer)
        display_current_grid(vibrate)
        pygame.display.update()
        if turns > 1:
            scores = the_grid.get_scores()
            lost_count = 0
            for i in range(len(scores)):
                if scores[i] == 0:
                    lost_count += 1
                    print("Player " + str(i) + " lost !!!")
            if lost_count == player_count-1:
                gameOver(i)
        clock.tick(20)
re_game()
