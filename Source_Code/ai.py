from pgameplayer import minimax_tree
from board import Board
import copy

class Atomic_Node(minimax_tree.Node):

    def __init__(self,board,colors,difficulty=0):
        self.state = Board(board._cols,board._rows,colors)
        for i in range(board._cols):
            for j in range(board._rows):
                self.state.set_cell_occupation(i,j,board.get_cell_occupation(i,j))
                self.state.set_cell_color(i,j,board.get_cell_color(i,j))
        self.player = True
        self.value = None
        self.best_move = None
        self.player_colors = colors
        self.difficulty = difficulty

    def set_difficulty(self,difficulty):
        self.difficulty = difficulty

    def print_board(self):
        self.state.print_board()

    def copy_board(self,oboard):
        tboard = Board(self.state._cols,self.state._rows,self.player_colors)
        for i in range(self.state._cols):
            for j in range(self.state._rows):
                tboard.set_cell_occupation(i,j,oboard.get_cell_occupation(i,j))
                tboard.set_cell_color(i,j,oboard.get_cell_color(i,j))
        return tboard

    def get_player_color(self,player):
        if player:
            return self.player_colors[1]
        else:
            return self.player_colors[0]

    def if_leaf(self):
        player_scores = self.state.get_scores()
        for score in player_scores:
            if score == 0:
                return True
        return False

    def generate_moves(self,player):
        next_state = []
        for i in range (self.state._cols):
            for j in range(self.state._rows):
                new_board = self.copy_board(self.state)
                if new_board.move(i,j,self.get_player_color(player)):
                    next_state.append(Atomic_Node(new_board,self.player_colors))
        return next_state

    def evaluate(self):
        player_scores = self.state.get_scores()
        if player_scores[1] == 0:
            self.value = minimax_tree.NINF
        elif player_scores[0] == 0:
            self.value = minimax_tree.PINF
        else:
            if not self.difficulty:
                # just count the atoms.
                self.value = player_scores[1]
        return self.value
