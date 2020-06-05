import pygame
import sys
from math import *

# Initializing the Game grid
pygame.init()
if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")

width = 400
height = 400
display = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# Color Schema
border = (208, 211, 212)
background = (21, 67, 96)

red = (231, 76, 60)
green = (88, 214, 141)
white = (244, 246, 247)
violet = (136, 78, 160)
yellow = (244, 208, 63)


playerColor = [red, green, violet, yellow]

font = pygame.font.SysFont("Times New Roman", 30)

grid_blocks = 40

# print("\n\n\t\tWELCOME TO CHAIN REACTION")
# player_count = int(input("\n\nEnter number of players between 2 to 4:\t"))

pygame.display.set_caption("Chain Reaction AI" )

score_count = []
for i in range(player_count):
    score_count.append(0)

players = []
for i in range(player_count):
    players.append(playerColor[i])

d = grid_blocks / 2 - 2

cols = int(width / grid_blocks)
rows = int(height / grid_blocks)

the_grid = []

# Initializing the_grid with null player account
def initialize_the_grid():
    global the_grid, score_count, players
    score_count = []
    for i in range(player_count
):
        score_count.append(0)

    players = []
    for i in range(player_count
):
        players.append(playerColor[i])

    the_grid = [[] for _ in range(cols)]
    for i in range(cols):
        for j in range(rows):
            newObj = my_spot()
            the_grid[i].append(newObj)
    for i in range(cols):
        for j in range(rows):
            the_grid[i][j].neighbour_append(i, j)


# for Each position in Grid
class my_spot():
    def __init__(self):
        self.color = border
        self.neighbors = []
        self.noAtoms = 0

    def neighbour_append(self, i, j):
        if i > 0:
            self.neighbors.append(the_grid[i - 1][j])
        if i < rows - 1:
            self.neighbors.append(the_grid[i + 1][j])
        if j < cols - 1:
            self.neighbors.append(the_grid[i][j + 1])
        if j > 0:
            self.neighbors.append(the_grid[i][j - 1])



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
            if the_grid[i][j].noAtoms == 0:
                the_grid[i][j].color = border
            elif the_grid[i][j].noAtoms == 1:
                pygame.draw.ellipse(display, the_grid[i][j].color,
                                    (r + grid_blocks / 2 - d / 2 + vibrate, c + grid_blocks / 2 - d / 2, d, d))
            elif the_grid[i][j].noAtoms == 2:
                pygame.draw.ellipse(display, the_grid[i][j].color, (r + 5, c + grid_blocks / 2 - d / 2 - vibrate, d, d))
                pygame.draw.ellipse(display, the_grid[i][j].color,
                                    (r + d / 2 + grid_blocks / 2 - d / 2 + vibrate, c + grid_blocks / 2 - d / 2, d, d))
            elif the_grid[i][j].noAtoms == 3:
                angle = 90
                x = r + (d / 2) * cos(radians(angle)) + grid_blocks / 2 - d / 2
                y = c + (d / 2) * sin(radians(angle)) + grid_blocks / 2 - d / 2
                pygame.draw.ellipse(display, the_grid[i][j].color, (x - vibrate, y, d, d))
                x = r + (d / 2) * cos(radians(angle + 90)) + grid_blocks / 2 - d / 2
                y = c + (d / 2) * sin(radians(angle + 90)) + 5
                pygame.draw.ellipse(display, the_grid[i][j].color, (x + vibrate, y, d, d))
                x = r + (d / 2) * cos(radians(angle - 90)) + grid_blocks / 2 - d / 2
                y = c + (d / 2) * sin(radians(angle - 90)) + 5
                pygame.draw.ellipse(display, the_grid[i][j].color, (x - vibrate, y, d, d))

    pygame.display.update()


# Increment the orb when clicked 
def add_Orb(i, j, color):
    the_grid[i][j].noAtoms += 1
    the_grid[i][j].color = color
    if the_grid[i][j].noAtoms >= len(the_grid[i][j].neighbors):
        split_boom(the_grid[i][j], color)


# Split the orb when it Increases the valency
def split_boom(cell, color):
    display_current_grid()
    cell.noAtoms = 0
    for m in range(len(cell.neighbors)):
        cell.neighbors[m].noAtoms += 1
        cell.neighbors[m].color = color
        if cell.neighbors[m].noAtoms >= len(cell.neighbors[m].neighbors):
            split_boom(cell.neighbors[m], color)


# Winning condition check
def check_player_game():
    global score_count
    playerScore = []
    for i in range(player_count
):
        playerScore.append(0)
    for i in range(cols):
        for j in range(rows):
            for k in range(player_count
        ):
                if the_grid[i][j].color == players[k]:
                    playerScore[k] += the_grid[i][j].noAtoms
    score_count = playerScore[:]


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


def did_win():
    num = 0
    for i in range(player_count):

        if score_count[i] == 0:
            num += 1
    if num==player_count- 1:
        for i in range(player_count):
                        if score_count[i]:
                            return i

    return 9999


# After Game over terminate the Game Window
def close():
    pygame.quit()
    sys.exit()

    
# Main Loop
def re_game():
    initialize_the_grid()
    loop = True

    turns = 0

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
                if the_grid[i][j].color == players[currentPlayer] or the_grid[i][j].color == border:
                    turns += 1
                    add_Orb(i, j, players[currentPlayer])
                    currentPlayer += 1
                    if currentPlayer >= player_count:
                        currentPlayer = 0
                if turns >= player_count:
                    check_player_game()
                # let the AI do its thing

        display.fill(background)
        # Vibrate the Atoms in their Cells
        vibrate *= -1

        create_grid(currentPlayer)
        display_current_grid(vibrate)

        pygame.display.update()

        res = did_win()
        if res < 9999:
            gameOver(res)

        clock.tick(20)


re_game()
