
class Cell():

    def __init__(self,border_color):
        self.color = border_color
        self.neighbors = []
        self.nr_atoms = 0

    def set_neighbours(self,board,i,j,cols,rows):
        if i > 0:
            self.neighbors.append(board[i-1][j])
        if i < rows -1:
            self.neighbors.append(board[i+1][j])
        if j > 0:
            self.neighbors.append((board[i][j-1]))
        if j < cols - 1:
            self.neighbors.append(board[i][j+1])

class Board():

    BORDER = (208, 211, 212)

    def __init__(self,cols,rows,colors,player_count=2):
        self._cols = cols
        self._rows = rows
        self._player_colors = colors
        self.nr_players = player_count
        self._board = [[] for _ in range(cols)]
        for i in range(self._cols):
            for j in range(self._rows):
                self._board[i].append(Cell(Board.BORDER))
        for i in range(self._cols):
            for j in range(self._rows):
                self._board[i][j].set_neighbours(self._board,i,j,self._cols,self._rows)

    def get_cell_color(self,x_pos,y_pos):
        return self._board[x_pos][y_pos].color

    def set_cell_color(self, x_pos, y_pos,color):
        self._board[x_pos][y_pos].color = color

    def get_cell_occupation(self,x_pos,y_pos):
        return self._board[x_pos][y_pos].nr_atoms

    def move(self,i,j,color):
        if self._board[i][j].nr_atoms != 0:
            if self._board[i][j].color != color:
                return False
        self._board[i][j].nr_atoms += 1
        self._board[i][j].color = color
        if self._board[i][j].nr_atoms >= len(self._board[i][j].neighbors):
            self._explode(self._board[i][j], color)
        return True

    def _explode(self,cell,color):
        cell.nr_atoms = 0
        for i in range(len(cell.neighbors)):
            cell.neighbors[i].nr_atoms += 1
            cell.neighbors[i].color = color
            if cell.neighbors[i].nr_atoms >= len(cell.neighbors[i].neighbors):
                self._explode(cell.neighbors[i], color)

    def get_scores(self):
        scores = []
        for i in range(self.nr_players):
            scores.append(0)
        for i in range(self._cols):
            for j in range(self._rows):
                for k in range(self.nr_players):
                    if self._board[i][j].color == self._player_colors[k]:
                        scores[k] += self._board[i][j].nr_atoms
        return scores[:]
