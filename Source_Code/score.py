



def get_scores(board,player_count,player_color):
    player_score = []
    for i in range(player_count):
        player_score.append(0)
    for i in range(len(board)):
        for j in range(len(board[i])):
            for k in range(player_count):
                if board[i][j].color == player_color[k]:
                    player_score[k] += board[i][j].noAtoms
    return player_score