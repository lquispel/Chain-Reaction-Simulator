import pygame
import sys
from math import *
from atomic_node import Atomic_Node
from board import Board
from pgameplayer.minimax_tree import *

# constants
AI_PLAYER= 1
# grid settings
width = 420
height = 420
grid_blocks = 70
d = grid_blocks / 2 - 2
cols = 6 # int(width / grid_blocks)
rows = 6 # int(height / grid_blocks)
# Color Schema
border = Board.BORDER
background = (21, 67, 96)
red = (231, 76, 60)
green = (88, 214, 141)
white = (244, 246, 247)
violet = (136, 78, 160)
yellow = (244, 208, 63)
playerColor = [red, green, violet, yellow]
# Initialize
pygame.init()
display = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Times New Roman", 30)
sys.setrecursionlimit(7000)
if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")
# globals
the_grid = []
player_count = 2
players = []
turns = 0
ai_search_depth = 1
lost_count = []

# subclass of Board with added draw functionality
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
        not_won_yet = self._blow_up(cell, color, i, j)
        self._show_explosion(i,j)
        if not_won_yet:
            for (i, j) in cell.neighbors:
                if self._board[i][j].nr_atoms >= self._board[i][j].nr_neighbours:
                    self._explode(self._board[i][j], color, i, j)

# display the current board/grid
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
            if the_grid.get_cell_occupation(i,j) == 1:
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
            elif the_grid.get_cell_occupation(i, j) == 4:
                pygame.draw.ellipse(display, the_grid.get_cell_color(i, j),
                                    (r + 5, c + grid_blocks / 2 - d / 2 - vibrate, d, d))
                pygame.draw.ellipse(display, the_grid.get_cell_color(i, j),
                                    (r + d / 2 + grid_blocks / 2 - d / 2 + vibrate, c + grid_blocks / 2 - d / 2, d, d))
                pygame.draw.ellipse(display, the_grid.get_cell_color(i, j),
                                    (r + 5, c + grid_blocks / 2 - vibrate, d, d))
                pygame.draw.ellipse(display, the_grid.get_cell_color(i, j),
                                    (r + d / 2 + grid_blocks / 2 - d / 2 + vibrate, c + grid_blocks / 2 - vibrate, d, d))

    pygame.display.update()

# game over, show winning player
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

# welcome players and select mode
def welcome_players():
    global player_count
    pygame.display.set_caption("Chain Reaction" )
    print("\n\n\t\tWELCOME TO CHAIN REACTION")
    player_count = int(input("\nEnter number of players (1-4). Enter 1 to play against AI:\t"))
    if player_count == 1:
        difficulty = setup_ai()
    return player_count

# get ai difficulty level from player
def setup_ai():
    global ai_search_depth
    print("\n\n\t\tWELCOME AGAIN, THIS IS ATOMIC INTELLIGENCE")
    print("Recursion limit: " + str(sys.getrecursionlimit()) + ", set lower if you experience stack overflows.")
    print("Difficulty levels:")
    print(" 1) Cylon (easy) ")
    print(" 2) Kitt (normal) ")
    print(" 3) Baltar (hard) ")
    print(" 4) HAL (N.B.: turns take very long) ")
    ai_search_depth = int(input("\nEnter difficulty level (1-4):\t"))
    if ai_search_depth < 1 or ai_search_depth > 4:
        ai_search_depth = 2
        print(" !!! Invalid difficulty, using 2 instead.")
    return ai_search_depth

# let the ai do its thing
def ai_move():
    if turns > 0:
        node = Atomic_Node(the_grid, playerColor)
        move, eval = depth_limited_minimax(node, ai_search_depth, True)
        i = move._moves[0][0]
        j = move._moves[0][1]
        the_grid.move(i, j, playerColor[AI_PLAYER])
    else:
        # start at a corner
        if not the_grid.move(0, 0, playerColor[AI_PLAYER]):
            the_grid.move(cols - 1, rows - 1, playerColor[AI_PLAYER])

# Main Loop
def re_game():
    global the_grid, players, player_count, turns, lost_count
    if player_count == 1:
        # need to give the ai a player slot
        the_grid = Drawing_Board(cols, rows, playerColor, 2)
        for i in range(2):
            players.append(playerColor[i])
            lost_count.append(0)
    else:
        the_grid = Drawing_Board(cols, rows, playerColor, player_count)
        for i in range(player_count):
            players.append(playerColor[i])
            lost_count.append(0)
    turns = 0
    # start loop
    loop = True
    currentPlayer = 0
    vibrate = .5
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
                    display_current_grid()
                    currentPlayer += 1
                    pygame.time.wait(2000)
                    if player_count == 1:
                        if currentPlayer == AI_PLAYER:
                            ai_move()
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
            scores = the_grid.get_score_list()
            loosers = 0
            for i in range(player_count):
                if scores[i] == 0:
                    lost_count[i] == 1
                    loosers += 1
            if player_count == 1:
                if lost_count[0] == 1:
                    gameOver(1)
                if lost_count[1] == 1:
                    gameOver(0)
            else:
                if loosers == player_count-1:
                    for i in range(player_count):
                        if lost_count[i] != 1:
                            gameOver(i)
        clock.tick(20)

def main():
    welcome_players()
    re_game()

if __name__ == "__main__":
    main()