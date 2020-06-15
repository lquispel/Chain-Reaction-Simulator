from pgameplayer import minimax_tree
from board import Board

class Atomic_Node(minimax_tree.Node):

    def __init__(self,board,colors,difficulty=0):
        self.state = Board(board._cols,board._rows,colors)
        self.state._moves = board._moves
        for i in range(board._cols):
            for j in range(board._rows):
                self.state._board[i][j].nr_atoms = board._board[i][j].nr_atoms
                self.state._board[i][j].color = board._board[i][j].color
        self.player = True
        self.value = None
        self.best_move = None
        self.player_colors = colors

    def _copy_board(self,oboard):
        tboard = Board(self.state._cols,self.state._rows,self.player_colors)
        for i in range(self.state._cols):
            for j in range(self.state._rows):
                tboard._board[i][j].nr_atoms = oboard._board[i][j].nr_atoms
                tboard._board[i][j].color = oboard._board[i][j].color
        return tboard

################################################################
#
#   Methods called by perfect game player
#
###############################################################

    def if_leaf(self):
        player_scores = self.state.get_score_list()
        for score in player_scores:
            if score == 0:
                return True
        return False

    def generate_moves(self,player):
        next_state = []
        for i in range (self.state._cols):
            for j in range(self.state._rows):
                new_board = self._copy_board(self.state)
                if new_board.move(i,j,self.player_colors[player]):
                    next_state.append(Atomic_Node(new_board,self.player_colors))
        return next_state

    def evaluate(self):
        player_scores = self.state.get_score_list()
        if player_scores[1] == 0:
            self.value = minimax_tree.NINF
        elif player_scores[0] == 0:
            self.value = minimax_tree.PINF
        else:
            self.value = player_scores[1]
        return self.value
