import random

piece_score={'K':0,
             'Q':9,
             'R':5,
             'N':3,
             'B':3,
             'p':1}
knight_score=[[1,1,1,1,1,1,1,1],
              [1,2,2,2,2,2,2,1],
              [1,2,4,3,3,4,2,1],
              [1,3,3,4,4,3,3,1],
              [1,3,3,4,4,3,3,1],
              [1,2,4,3,3,4,2,1],
              [1,2,2,2,2,2,2,1],
              [1,1,1,1,1,1,1,1]]

bishop_score=[[2,1.5,1,0.5,0.5,1,1.5,2],
              [3,4,3,2,2,3,4,3],
              [2,3,4,3,3,4,3,2],
              [1,2,3,3.9,3.9,3,2,1],
              [1,2,3,3.9,3.9,3,2,1],
              [2,3,4,3,3,4,3,2],
              [3,4,3,2,2,3,4,3],
              [2,1.5,1,0.5,0.5,1,1.5,2]]

queen_score=[[1,1,1,3,1,1,1,1],
             [1,2,3,3,3,1,1,1],
             [1,4,3,3,3,4,2,1],
             [1,2,3,3,3,2,2,1],
             [1,2,3,3,3,2,2,1],
             [1,4,3,3,3,4,2,1],
             [1,2,3,3,3,1,1,1],
             [1,1,1,3,1,1,1,1]]



rook_score=[[4,3,4,4,4,4,3,4],
            [4,4,4,4,4,4,4,4],
            [1,1,2,3,3,2,1,1],
            [1,2,3,4,4,3,2,1],
            [1,2,3,4,4,3,2,1],
            [1,1,2,3,3,2,1,1],
            [4,4,4,4,4,4,4,4],
            [4,3,4,4,4,4,3,4]]

white_pawn_score=[[9,9,9,9,9,9,9,9],
                  [8,8,8,8,8,8,8,8],
                  [5,6,6,7,7,6,6,5],
                  [2,3,3,5,5,3,3,2],
                  [1,2,3,4,4,3,2,1],
                  [1,1,2,3,3,2,1,1],
                  [1,1,1,0,0,1,1,1],
                  [0,0,0,0,0,0,0,0]]

black_pawn_score=[[0,0,0,0,0,0,0,0],
                  [1,1,1,0,0,1,1,1],
                  [1,1,2,3,3,2,1,1],
                  [1,2,3,4,4,3,2,1],
                  [2,3,3,5,5,3,3,2],
                  [5,6,6,7,7,6,6,5],
                  [8,8,8,8,8,8,8,8],
                  [9,9,9,9,9,9,9,9]]


piece_pos_scores={"N":knight_score,
                  "Q":queen_score,
                  "B":bishop_score,
                  "R":rook_score,
                  "wp":white_pawn_score,
                  "bp":black_pawn_score}
check_mate=1000
stale_mate=0
DEPTH=4
def find_random_move(valid_moves):

    return(valid_moves[random.randint(0,len(valid_moves)-1)])


'''Helper method to make first call'''
def find_best_move_min_max(gs,valid_moves,):
    global next_move
    next_move = None
    random.shuffle(valid_moves)
    #find_move_min_max(gs,valid_moves,DEPTH,gs.whiteToMove)
    find_move_nega_max_alpha_beta(gs,valid_moves,DEPTH,-check_mate,check_mate, 1 if gs.whiteToMove else -1)
    return next_move


def find_move_nega_max_alpha_beta(gs,valid_moves,depth,alpha,beta,turn_multiplier):
    global next_move
    if depth==0:
        return turn_multiplier*score_board(gs,next_move)
    #move ordering - will implement latter maybe
    max_score= -check_mate
    for move in valid_moves:
        gs.make_move(move)
        next_moves=gs.get_valid_moves()
        score = -find_move_nega_max_alpha_beta(gs,next_moves,depth-1,-beta,-alpha,-turn_multiplier)
        if score>max_score:
            max_score=score
            if depth==DEPTH:
                next_move=move
                #print(move,score)

        gs.undo()
        if max_score>alpha:#This is where pruing happens
            alpha=max_score
        if alpha>=beta:
            break
    return max_score
'''
+ve score is good for white and a neg score is better for black
'''
def score_board(gs,move):
    if(gs.check_mate):
        if(gs.whiteToMove):
            return -check_mate
        else:
            return check_mate
    elif gs.stale_mate:
        return stale_mate

    score = 0
    for row in range(len(gs.board)):
        for col in range(len(gs.board[row])):
            square = gs.board[row][col]
            piece_pos_score = 0
            if (square != '--'):
                if (square[1] != "K"):
                    if (square[1] == "p"):
                        piece_pos_score = piece_pos_scores[square][row][col]
                    else:
                        piece_pos_score = piece_pos_scores[square[1]][row][col]
                try:
                    if move.is_castle_move:
                        piece_pos_score+=0.5
                except:
                    pass
                if (square[0] == 'w'):
                    score += piece_score[square[1]] + piece_pos_score * 0.1
                elif (square[0] == 'b'):
                    score -= piece_score[square[1]] + piece_pos_score * 0.1
    return round(score,3)
