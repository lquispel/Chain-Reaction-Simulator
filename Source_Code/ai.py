from pgameplayer import minimax_tree
import score

class Atomic_Node(minimax_tree.Node):

    def __init__(self,board,colors,difficulty):
        self.state = board
        self.player = True
        self.value = None
        self.best_move = None
        self.player_colors = colors
        self.difficulty = difficulty

    def set_difficulty(self,difficulty):
        self.difficulty = difficulty

    def is_leaf(self):
        # checks if node is either a win, loss or draw.
        # :return: boolean
        player_scores = score.get_scores(self.state,2,self.player_colors)
        for score in player_scores:
            if score == 0:
                return True
        return False

    def generate_moves(self,player):
        # Generates list of valid possible moves
        # :param player: Boolean. x or o
        # :return: list
        current_board  = copy.copy(self.state)
        next_state = []
        for i in range (len(current_board)):
            for j in range(len(current_board[i])):
                if current_board[i][j].color == chainreaction.playerColor[player] or current_board[i][j].noAtoms == 0:
                    next_state.append(current_board[i][j])
        return next_state

    def evaluate(self):
        player_scores = score.get_scores(self.state,2,self.player_colors)
        # check if someone won self.value = minimax_tree.PINF
        if player_scores[1] == 0:
            self.value = minimax_tree.NINF
        elif player_scores[0] == 0:
            self.value = minimax_tree.PINF
        else:
            if not self.difficulty:
                # just count the atoms.
                self.value = player_scores[1]






