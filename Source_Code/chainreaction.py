import pygame
import sys
from math import *
from ai import Atomic_Node
from board import Board
from pgameplayer.minimax_tree import *

# Initialize
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
# settings
turns = 0
font = pygame.font.SysFont("Times New Roman", 30)
player_count = 2
the_grid = []

class Drawing_Board(Board):

    def _show_explosion(self,i,j):
        display_current_grid()
        x = i * grid_blocks
        y = j * grid_blocks
        pygame.draw.circle(display, white, (int(x + 0.5 * grid_blocks), int(y + 0.5 * grid_blocks)), 35)
        pygame.draw.circle(display, yellow, (int(x + 0.5 * grid_blocks), int(y + 0.5 * grid_blocks)), 25)
        pygame.draw.circle(display, red, (int(x + 0.5 * grid_blocks), int(y + 0.5 * grid_blocks)), 10)
        pygame.display.update()
        pygame.time.wait(500)

    def _explode(self,cell,color,i,j):
        self._blow_up(cell, color, i, j)
        self._show_explosion(i,j)
        for (i, j) in cell.neighbors:
            if self._board[i][j].nr_atoms >= self._board[i][j].nr_neighbours:
                self._explode(self._board[i][j], color, i, j)

# display the current board
def display_current_grid(vibrate=1):
    display.fill(background)
    r = 0
    c = 0
    for i in range(int(width / grid_blocks)):
        r += grid_blocks
        c += grid_blocks
        pygame.draw.line(display, white, (c, 0), (c, height))
        pygame.draw.line(display, white, (0, r), (width, r))
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

# welcome players
pygame.display.set_caption("Chain Reaction AI - Atomic Intelligence ! " )
print("\n\n\t\tWELCOME TO ATOMIC INTELLIGENCE FOR CHAIN REACTION")
print("Recursion limit: " + str(sys.getrecursionlimit()) + ", set lower if you experience stack overflows.\n")
print("Difficulty levels:")
print(" 1) Cylon (easy) ")
print(" 2) Kitt (normal) ")
print(" 3) Baltar (hard) ")
print(" 4) HAL (N.B.: turns take very long) ")
difficulty = int(input("\nEnter difficulty level (1-4):\t"))
if difficulty < 1 or difficulty > 4:
    difficulty = 2
    print(" !!! Invalid difficulty, using 2 instead.")


# Main Loop
def re_game():
    global the_grid, players
    players = []
    for i in range(player_count):
        players.append(playerColor[i])
    the_grid = Drawing_Board(cols,rows,playerColor,player_count)
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
                    print("\nPlayer Move: " + str(i) + "," + str(j))
                    display_current_grid()
                    pygame.time.wait(1000)
                    currentPlayer += 1
                    if currentPlayer == 1:
                        if turns > 0:
                            node = Atomic_Node(the_grid, playerColor)
                            move, eval = depth_limited_minimax(node, difficulty, True)
                            i = move._moves[0][0]
                            j = move._moves[0][1]
                            the_grid.move(i,j,playerColor[currentPlayer])
                            currentPlayer += 1
                            print("AI Move: " + str(i) + "," + str(j) + "  value:" + str(eval))
                            move.print_board()
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
        # Vibrate the Atoms in their Cells
        vibrate *= -1
        display_current_grid(vibrate)
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
