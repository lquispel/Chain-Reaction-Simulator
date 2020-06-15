class Cell():

    def __init__(self,border_color):
        self.color = border_color
        self.neighbors = []
        self.nr_atoms = 0
        self.nr_neighbours = 0

    def set_neighbours(self,board,i,j,cols,rows):
        if i > 0:
            self.neighbors.append((i-1,j))
            self.nr_neighbours += 1
        if i < rows -1:
            self.neighbors.append((i+1,j))
            self.nr_neighbours += 1
        if j > 0:
            self.neighbors.append((i,j-1))
            self.nr_neighbours += 1
        if j < cols - 1:
            self.neighbors.append((i,j+1))
            self.nr_neighbours += 1

class Board():

    BORDER = (208, 211, 212)

    def __init__(self,cols,rows,colors,player_count=2):
        self._cols = cols
        self._rows = rows
        self._player_colors = colors
        self._nr_players = player_count
        self._board = [[] for _ in range(cols)]
        self._moves = []
        self._scores = dict()
        for colour in self._player_colors:
            self._scores[colour] = 0
        for i in range(self._cols):
            for j in range(self._rows):
                self._board[i].append(Cell(Board.BORDER))
        for i in range(self._cols):
            for j in range(self._rows):
                self._board[i][j].set_neighbours(self._board,i,j,self._cols,self._rows)

    def move(self,i,j,color):
        if i < 0 or j < 0 or i >= self._cols or j >= self._rows:
            return False
        occ = self._board[i][j].nr_atoms
        if occ != 0:
            if self._board[i][j].color != color:
                return False
        occ += 1
        self._board[i][j].nr_atoms += 1
        self._board[i][j].color = color
        self._scores[color] += 1
        m = [i,j]
        self._moves.append(m)
        if occ >= self._board[i][j].nr_neighbours:
             self._explode(self._board[i][j], color,i,j)
        return True

    def _explode(self,cell,color,i,j):
        if self._blow_up(cell,color,i,j):
            for (i, j) in cell.neighbors:
                if self._board[i][j].nr_atoms >= self._board[i][j].nr_neighbours:
                    self._explode(self._board[i][j], color,i,j)

    def _blow_up(self, cell, color, i, j):
        self._board[i][j].nr_atoms -= self._board[i][j].nr_neighbours
        if self._board[i][j].nr_atoms < 1:
            self._board[i][j].color = Board.BORDER
        for (n, m) in cell.neighbors:
            n_color = self._board[n][m].color
            if n_color == color:
                self._scores[color] += self._board[n][m].nr_atoms
            else:
                self._board[n][m].color = color
                if n_color != Board.BORDER:
                    self._scores[n_color] -= self._board[n][m].nr_atoms
            self._board[n][m].nr_atoms += 1
        # we want to stop recursion when we have a winner
        not_won_yet = True
        for player in range(self._nr_players):
            if self._scores[self._player_colors[player]] == 0:
                not_won_yet = False
        return not_won_yet

    def get_score_list(self):
        scores = []
        for i in range(self._nr_players):
            scores.append(0)
        for i in range(self._cols):
            for j in range(self._rows):
                if self._board[i][j].nr_atoms > 0:
                    for n in range(self._nr_players):
                        if self._board[i][j].color == self._player_colors[n]:
                            scores[n] += 1
        return scores

    def get_cell_color(self, x_pos, y_pos):
        return self._board[x_pos][y_pos].color

    def get_cell_occupation(self, x_pos, y_pos):
        return self._board[x_pos][y_pos].nr_atoms

    def print_board(self):
        ret = ""
        for j in range(self._rows):
            ret += "|| "
            for i in range(self._cols):
                occ = 0
                for n in range(len(self._player_colors)):
                    if self._board[i][j].color == self._player_colors[n]:
                        occ = 1
                        ret += "p" + str(n) + ":" + str(self._board[i][j].nr_atoms)
                        break
                if occ == 0:
                    ret += "    "
                ret += "|"
            ret += "|\n"
        print(ret)






