"""
This is going to store all the info on what is the current state of the game
Second thing it will do is to is to validate moves
Thirdly it will also store the log
"""
import pygame as py

class GameState():
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        # here our board is represented by a 2d array which is 8X8
        # First letter represents color of piece second represents the name of it
        # The "--" represents the empty space, you could for example use 0 here but we are using --
        self.whiteToMove = True
        self.moveLog = []
        # Keeping track of kings location so that when we need to validate it for checks, we know where it is
        self.white_king_location = (7, 4)
        self.black_king_location = (0, 4)
        # to Check on weather it is stale mate or check mate or not
        self.check_mate = False
        self.stale_mate = False
        # here we have a better algo for checking checks will try to implement it
        # If we are able to will remove the previous one completely
        self.in_check = False
        self.enpasent_possible = ()
        self.enpasent_possible_log=[self.enpasent_possible]
        self.pins = []
        self.checks = []
        self.currentCastlingRight = Castle_rights(True,True,True,True)
        self.castleRightsLog = [Castle_rights(self.currentCastlingRight.wks,self.currentCastlingRight.bks,self.currentCastlingRight.wqs,self.currentCastlingRight.bqs)]

    def make_move(self, move):
        '''
        This takes a move and make it.
        This doesn't work with casteling and enpasent
        '''
        # Basically we are assuming every move that comes here is valid one
        # Validation is done before move arrives here and not here
        self.board[move.start_row][move.start_col] = "--"  # Jaha se piece hata vho blank space ho gai
        self.board[move.end_row][move.end_col] = move.piece_moved  # Jaha pe gaya vho jagah pe uss piece ka nam aa gaya
        run = True

        if (move.is_pawn_pro):
            while run:
                for event in py.event.get():
                    if (event.type == py.KEYDOWN):
                        if (event.key == py.K_q):
                            self.board[move.end_row][move.end_col] = move.piece_moved[0] + 'Q'
                            run = False
                        elif (event.key == py.K_r):
                            self.board[move.end_row][move.end_col] = move.piece_moved[0] + 'R'
                            run = False
                        elif (event.key == py.K_b):
                            self.board[move.end_row][move.end_col] = move.piece_moved[0] + 'B'
                            run = False
                        elif (event.key == py.K_k):
                            self.board[move.end_row][move.end_col] = move.piece_moved[0] + 'N'
                            run = False
        if (move.is_enpasant_move==True):
            self.board[move.start_row][move.end_col]='--'
        self.moveLog.append(move)  # Move log mai store karo so that kabhi undo karna ho tho
        self.whiteToMove = not (self.whiteToMove)  # Finally jiss ki bhi move thi aab oposite side ki aaye gi so...
        if (move.piece_moved[1]=='p' and abs(move.start_row-move.end_row)==2):
            self.enpasent_possible=((move.start_row+move.end_row)//2,move.start_col)
        else:
            self.enpasent_possible=()
        #Making a castle move
        if(move.is_castle_move):
            if(move.end_col-move.start_col==2):#That would mean king side castle
                self.board[move.end_row][move.end_col-1]=self.board[move.end_row][move.end_col+1]
                self.board[move.end_row][move.end_col+1]='--'
            else:#It is a queen side castle
                self.board[move.end_row][move.end_col+1]=self.board[move.end_row][move.end_col-2]

                self.board[move.end_row][move.end_col-2]='--'

        if (move.piece_moved == "bK"):

            self.black_king_location = (move.end_row, move.end_col)
        elif (move.piece_moved == "wK"):

            self.white_king_location = (move.end_row, move.end_col)

        #Updating castling rights - we do that when a rook or a king has moved
        self.update_castle_rights(move)
        self.castleRightsLog.append(Castle_rights(self.currentCastlingRight.wks,self.currentCastlingRight.bks,self.currentCastlingRight.wqs,self.currentCastlingRight.bqs))
        self.enpasent_possible_log.append(self.enpasent_possible)
    def undo(self):
        if (len(self.moveLog) > 0):
            self.check_mate=False
            self.stale_mate=False
            move = self.moveLog.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved

            self.board[move.end_row][move.end_col] = move.piece_captured
            self.whiteToMove = not (self.whiteToMove)
            if (move.piece_moved == "bK"):

                self.black_king_location = (move.start_row, move.start_col)
            elif (move.piece_moved == "wK"):

                self.white_king_location = (move.start_row, move.start_col)
            #undoing enpassant move
            if(move.is_enpasant_move):
                self.board[move.end_row][move.end_col]=='--'
                if(move.piece_moved[0]=='b'):
                    self.board[move.end_row-1][move.end_col]= 'wp'
                else:
                    self.board[move.end_row + 1][move.end_col] = 'bp'
            self.enpasent_possible_log.pop()
            self.enpasent_possible=self.enpasent_possible_log[-1]


            #Undo castling rights
            self.castleRightsLog.pop()#remove the previous castle rights
            self.currentCastlingRight=self.castleRightsLog[-1]#get the new ones
            #undoing castle move
            if(move.is_castle_move):
                if(move.end_col-move.start_col==2):
                    self.board[move.end_row][move.end_col+1]=self.board[move.end_row][move.end_col-1]
                    self.board[move.end_row][move.end_col-1]='--'
                else:
                    self.board[move.end_row][move.end_col-2]=self.board[move.end_row][move.end_col+1]
                    self.board[move.end_row][move.end_col+1]='--'

    def update_castle_rights(self,move):

        if(move.piece_moved=='wK'):
            self.currentCastlingRight.wks=False

            self.currentCastlingRight.wqs=False
        elif(move.piece_moved=='bK'):
            self.currentCastlingRight.bks=False
            self.currentCastlingRight.bqs=False
        elif(move.piece_moved=='wR'):
            if(move.start_row==7):
                if(move.start_col==0):#This means it is a queen side rook
                    self.currentCastlingRight.wqs=False
                elif(move.start_col==7): #if it is not a queen side rook and it is a rook then it is king side one
                    self.currentCastlingRight.wks=False

        elif(move.piece_moved=='bR'):
            if (move.start_row == 0):
                if (move.start_col == 0):  # This means it is a queen side rook
                    self.currentCastlingRight.bqs = False
                elif (move.start_col == 7):  # if it is not a queen side rook and it is a rook then it is king side one
                    self.currentCastlingRight.bks = False
        if(move.piece_captured=='wR'):
            if(move.end_row==7):
                if(move.end_col==0):
                    self.currentCastlingRight.wqs=False
                elif(move.end_col==7):
                    self.currentCastlingRight.wks=False
        if(move.piece_captured=='bR'):
            if(move.end_row==0):
                if(move.end_col==0):
                    self.currentCastlingRight.bqs=False
                elif(move.end_col==7):
                    self.currentCastlingRight.bks=False


    def check_for_pins_checks(self):
        pins = []
        checks = []
        in_check = False
        if self.whiteToMove:
            enemy_color = 'b'
            ally_color = 'w'
            start_row = self.white_king_location[0]
            start_col = self.white_king_location[1]
        else:
            enemy_color = 'w'
            ally_color = 'b'
            start_row = self.black_king_location[0]
            start_col = self.black_king_location[1]
        direction = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        # checking in outward directions of king for check and pins
        for j in range(len(direction)):
            d = direction[j]
            possible_pin = ()  # reset possible pins
            for i in range(1, 8):
                end_row = start_row + d[0] * i
                end_col = start_col + d[1] * i
                if (0 <= end_row < 8 and 0 <= end_col < 8):
                    end_piece = self.board[end_row][end_col]

                    if (end_piece[0] == ally_color and end_piece[
                        1] != 'K'):  # PHANTOM KING PROBLEM, I.E WHEN WE ASSUME THAT KING
                        # HAS MOVED TO CHECK IF IT CAN, THEN AT THAT TIME FOR ALGO TWO KINGS EXIST AND HENCE ONE BLOCKS THE OTHER
                        if (possible_pin == ()):
                            possible_pin = (end_row, end_col, d[0], d[1])
                        else:  # if it is the second piece in line then it is not pin so yeh kind of ignore it
                            break
                    elif (end_piece[0] == enemy_color):
                        type = end_piece[1]
                        '''
                        HERE WE HAVE 5 CASES
                        1> WE HAVE A ROOK IN SAME ROW OR COLOUMN
                        2> WE HAVE A BISHOP IN SAME DIAGONAL
                        3> WE HAVE A QUEEN IN SAME DIAGONAL OR IN SAME ROW/COLOUMN
                        4> WE HAVE A PAWN DIAGONALLY ONE SQUARE AWAY FROM IT
                        5> THE NEXT SQUARE IS CONTROLED BY OPPONENT'S KING, WE CAN'T LET KING'S BE NEXT TO EACH OTHER THEREFORE THIS IS IMPORTANT
                        '''
                        # THERE WILL ALSO BE A SIXTH CASE OF KNIGHT BUT WILL HANDLE THAT DIFFERENTLY AS KNIGH CAN JUMP OVER UNLIKE ALL THESE
                        if ((0 <= j <= 3 and type == 'R') or
                                (4 <= j <= 7 and type == 'B') or
                                (i == 1 and type == 'p' and ((enemy_color == 'w' and 6 <= j <= 7) or (
                                        enemy_color == 'b' and 4 <= j <= 5))) or
                                (type == 'Q') or
                                (i == 1 and type == 'K')):
                            if (
                                    possible_pin == ()):  # King is under attack and no piece blocking means it is under check
                                in_check = True
                                checks.append((end_row, end_col, d[0], d[1]))
                                break
                            else:
                                pins.append(possible_pin)
                                break
                        else:  # Enemy piece not giving check
                            break
                else:
                    break
        # NOW WE WILL CHECK FOR KNIGHT MOVES
        knight_moves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for m in knight_moves:
            end_row = start_row + m[0]
            end_col = start_col + m[1]
            if (0 <= end_row < 8 and 0 <= end_col < 8):
                end_piece = self.board[end_row][end_col]
                if (end_piece[0] == enemy_color and end_piece[1] == 'N'):
                    in_check = True
                    checks.append((end_row, end_col, m[0], m[1]))
                    # NOTE THAT SINCE KNIGHT CAN'T BE BLOCKED WE DON'T CHECK FOR PINS OR ANYTHING
                    # IF THERE EXISTS A KNIGH THAT IS ATTACKING KING, THERE ISN'T ANYTHING THAT CAN BE DONE ABOUT IT
                    # EXCPET FOR CAPTURING IT OR MOVING KING AWAY, THEREFORE ONLY VALUE THAT MATTERS IS 'IN_CHECK'
        return (in_check, pins, checks)

    def get_valid_moves(self):
        '''
            See get all possible moves actually gives us the moves we can make with all the pieces
            but here is the deal, some pieces might be pined, or certain king moves might not be possible
            so for all those we have a function called get valid move, it will handle all those stuff
            get all possible moves is just going to tell us where can those pieces move, wether they are valid or not is a differnet thing
            '''
        temp_enpassant_possible=self.enpasent_possible
        '''
        Here I am gonna try to implement a new solution if that works it does otherwise will go back to old one
        '''
        self.in_check, self.pins, self.checks = self.check_for_pins_checks()


        if (self.whiteToMove):
            king_row = self.white_king_location[0]
            king_col = self.white_king_location[1]
        else:
            king_row = self.black_king_location[0]
            king_col = self.black_king_location[1]
        if (self.in_check):
            if (len(self.checks) == 1):  # If there is only one check coming you can block caputre or move, if it is more that one than you have to move
                moves = self.get_all_possible_moves()  # We are getting all the moves that are possible then we will filter out which are legal
                check_row = self.checks[0][0]  # Row of first and the only piece giving the check
                check_col = self.checks[0][1]  # Col of that piece
                ###NOTE CHECKS LIST HAS THAT PIECES ROW AND COLOUMN ALONG WITH THE DIRECTIONS IT CAN MOVE IN FROM THAT PARTICULAR PLACE, THEY ARE STORED AT 2,3 PLACE IN LIST
                piece_checking = self.board[check_row][
                    check_col]  # getting the details of piece that is giving the check
                vaild_squares = []  # list of squares that piece can move to, i.e at which squares can it be blocked before reaching king
                if (piece_checking == 'N'):  # If night is the one giving the check there is no point in thinking it can be blocked
                    # So the only thing that can happent to it is that it can be caputred, so the only location at which your pieces can move to is the location of that knight itsefl
                    vaild_squares = [(check_row, check_col)]
                else:
                    for i in range(1, 8):
                        vaild_square = (
                        king_row + self.checks[0][2] * i, king_col + self.checks[0][3] * i)  # 2,3 are diections
                        # It is basically saying that the point from where the king lies, if there is any square between king and that piece in the direction from where the check is coming
                        # Then it is the potiential square that can be blocked to protect the king
                        vaild_squares.append(vaild_square)  # Therefore we append that one in
                        if (vaild_square[0] == check_row and vaild_square[1] == check_col):
                            break  # Basically you have reached the point from where check was comming so no point going further
                # Now after doing all this we need to remove the moves that are not in the set of moves that either
                # Block the check, capture the piece or move away the king
                for i in range(len(moves) - 1, -1, -1):  # From end till start
                    if (moves[i].piece_moved[1] != 'K'):  # I.E the piece moved is not the king
                        if not (moves[i].end_row, moves[i].end_col) in vaild_squares:
                            moves.remove(moves[i])
            else:
                # here we have a double check so only king can move nothing else is possible
                moves=[]
                self.king_moves(king_row, king_col, moves)
        else:
            moves = self.get_all_possible_moves()  # Since king isn't under check every move is fine
        self.enpasent_possible=temp_enpassant_possible
        if (self.whiteToMove):
            self.get_castle_moves(self.white_king_location[0], self.white_king_location[1], moves, 'w')
        else:
            self.get_castle_moves(self.black_king_location[0],self.black_king_location[1],moves,'b')
        if(len(moves)==0):
            if(self.in_check):
                self.check_mate=True
            else:
                self.stale_mate=True
        return (moves)

    def square_under_attack(self, r, c):
        '''
        It tells if enemy can attack that square
        '''
        self.whiteToMove = not (self.whiteToMove)  # Opponent's pov
        opp_moves = self.get_all_possible_moves()
        self.whiteToMove = not (self.whiteToMove)  # Once we have genrated all the moves we switch back
        for move in opp_moves:
            if (move.end_row == r and move.end_col == c):
                return True
        return False

    def get_all_possible_moves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]  # basically first char of our piece on that square
                if ((turn == 'w' and self.whiteToMove) or (turn == 'b' and not (self.whiteToMove))):
                    '''
                    So if we have a black piece and it is the move of black, then we have to see where that piece can move
                    and vice versa
                    '''
                    pi = self.board[r][c][1]  # This gives us which piece is it
                    if (pi == 'p'):
                        self.pawn_moves(r, c, moves)
                    elif (pi == 'R'):
                        self.rook_moves(r, c, moves)
                    elif (pi == 'B'):
                        self.bishop_moves(r, c, moves)
                    elif (pi == "N"):
                        self.knight_moves(r, c, moves)
                    elif (pi == 'Q'):
                        self.queen_moves(r, c, moves)
                    elif (pi == "K"):
                        self.king_moves(r, c, moves)

        return (moves)

    def pawn_moves(self, r, c, moves):
        '''
        takes the row, coloums and already avialable moves as input
        then adds the moves which this pawn can make to set of all possible moves
        and then returns that updated set of all possible moves
        '''
        '''
        First we check if piece is pined or not too
        '''
        piece_pined = False
        pin_dir = ()
        if(self.whiteToMove):
            enemy_color='b'
            king_row, king_col=self.white_king_location
        else:
            enemy_color='w'
            king_row, king_col=self.black_king_location
        for i in range(len(self.pins) - 1, -1, -1):
            if (self.pins[i][0] == r and self.pins[i][1] == c):
                piece_pined = True
                pin_dir = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        # White pawns starts on 6 and black on 1 in our notation
        if (self.whiteToMove):
            # This is for pushing forward
            if (self.board[r - 1][c] == '--'):  # i.e square in front is empty

                if (not (piece_pined) or pin_dir == (-1, 0)):  # That is that moves are valid only if piece is not pined, or if pin is coming from direction of movement

                    moves.append(Move((r, c), (r - 1, c), self.board))
                    if (r == 6 and self.board[r - 2][c]=='--'):  # For two square move advance
                        moves.append(Move((r, c), (r - 2, c), self.board))
            if (r >= 0):
                if (c >= 1 and c <= 6):
                    if (self.board[r - 1][c - 1][0] == 'b'):
                        if (not (piece_pined) or pin_dir == (-1, -1)):
                            moves.append(Move((r, c), (r - 1, c - 1), self.board))
                    elif ((r - 1, c - 1) == self.enpasent_possible):
                        if (not (piece_pined) or pin_dir == (-1, -1)):
                            attacking_piece=blocking_piece=False
                            if(king_row==r):
                                if(king_col<c):
                                    inside_range=range(king_col+1,c-1)
                                    outside_range=range(c+1,8)
                                else:
                                    inside_range=range(king_col-1,c,-1)
                                    outside_range=range(c-2,-1,-1)
                                for i in inside_range:
                                    if(self.board[r][i]!='--'):
                                        blocking_piece=True
                                for i in outside_range:
                                    square=self.board[r][i]
                                    if(square[0]==enemy_color and (square[1]=='R' or square[1]=='Q')):
                                        attacking_piece=True
                                    elif(square != '--'):
                                        blocking_piece=True
                            if(not attacking_piece or blocking_piece):
                                moves.append(Move((r, c), (r - 1, c - 1), self.board, is_enpasant_move=True))

                    if (self.board[r - 1][c + 1][0] == 'b'):
                        if (not (piece_pined) or pin_dir == (-1, 1)):
                            moves.append(Move((r, c), (r - 1, c + 1), self.board))
                    elif ((r - 1, c + 1) == self.enpasent_possible):
                        if (not (piece_pined) or pin_dir == (-1, 1)):
                            attacking_piece = blocking_piece = False
                            if (king_row == r):
                                if (king_col < c):
                                    inside_range = range(king_col + 1, c)
                                    outside_range = range(c + 2, 8)
                                else:
                                    inside_range = range(king_col - 1, c+1, -1)
                                    outside_range = range(c - 1, -1, -1)
                                for i in inside_range:
                                    if (self.board[r][i] != '--'):
                                        blocking_piece = True
                                for i in outside_range:
                                    square = self.board[r][i]
                                    if (square[0] == enemy_color and (square[1] == 'R' or square[1] == 'Q')):
                                        attacking_piece = True
                                    elif (square != '--'):
                                        blocking_piece = True
                            if (not attacking_piece or blocking_piece):
                                moves.append(Move((r, c), (r - 1, c + 1), self.board, is_enpasant_move=True))
                elif (c == 0):
                    if (self.board[r - 1][c + 1][0] == 'b'):
                        if (not (piece_pined) or pin_dir == (-1, 1)):
                            moves.append(Move((r, c), (r - 1, c + 1), self.board))
                    elif ((r - 1, c + 1) == self.enpasent_possible):
                        if (not (piece_pined) or pin_dir == (-1, 1)):
                            attacking_piece = blocking_piece = False
                            if (king_row == r):
                                if (king_col < c):
                                    inside_range = range(king_col + 1, c)
                                    outside_range = range(c + 2, 8)
                                else:
                                    inside_range = range(king_col - 1, c + 1, -1)
                                    outside_range = range(c - 1, -1, -1)
                                for i in inside_range:
                                    if (self.board[r][i] != '--'):
                                        blocking_piece = True
                                for i in outside_range:
                                    square = self.board[r][i]
                                    if (square[0] == enemy_color and (square[1] == 'R' or square[1] == 'Q')):
                                        attacking_piece = True
                                    elif (square != '--'):
                                        blocking_piece = True
                            if (not attacking_piece or blocking_piece):
                                moves.append(Move((r, c), (r - 1, c + 1), self.board, is_enpasant_move=True))
                elif (c == 7):
                    if (self.board[r - 1][c - 1][0] == 'b'):
                        if (not (piece_pined) or pin_dir == (-1, -1)):
                            moves.append(Move((r, c), (r - 1, c - 1), self.board))
                    elif ((r - 1, c - 1) == self.enpasent_possible):
                        if (not (piece_pined) or pin_dir == (-1, -1)):
                            attacking_piece = blocking_piece = False
                            if (king_row == r):
                                if (king_col < c):
                                    inside_range = range(king_col + 1, c - 1)
                                    outside_range = range(c + 1, 8)
                                else:
                                    inside_range = range(king_col - 1, c, -1)
                                    outside_range = range(c - 2, -1, -1)
                                for i in inside_range:
                                    if (self.board[r][i] != '--'):
                                        blocking_piece = True
                                for i in outside_range:
                                    square = self.board[r][i]
                                    if (square[0] == enemy_color and (square[1] == 'R' or square[1] == 'Q')):
                                        attacking_piece = True
                                    elif (square != '--'):
                                        blocking_piece = True
                            if (not attacking_piece or blocking_piece):
                                moves.append(Move((r, c), (r - 1, c - 1), self.board, is_enpasant_move=True))
        else:  # black move
            if (self.board[r + 1][c] == '--'):  # i.e square in front is empty
                if (not (piece_pined) or pin_dir == (1, 0)):
                    moves.append(Move((r, c), (r + 1, c), self.board))
                    if (r == 1 and self.board[r + 2][c]=='--'):  # For two square move advance
                        moves.append(Move((r, c), (r + 2, c), self.board))
            if (r <= 7):
                if (c >= 1 and c <= 6):
                    if (self.board[r + 1][c - 1][0] == 'w'):
                        if (not (piece_pined) or pin_dir == (1, -1)):
                            moves.append(Move((r, c), (r + 1, c - 1),self.board))
                    elif ((r + 1, c - 1) == self.enpasent_possible):
                        if (not (piece_pined) or pin_dir == (1, -1)):
                            attacking_piece = blocking_piece = False
                            if (king_row == r):
                                if (king_col < c):
                                    inside_range = range(king_col + 1, c - 1)
                                    outside_range = range(c + 1, 8)
                                else:
                                    inside_range = range(king_col - 1, c, -1)
                                    outside_range = range(c - 2, -1, -1)
                                for i in inside_range:
                                    if (self.board[r][i] != '--'):
                                        blocking_piece = True
                                for i in outside_range:
                                    square = self.board[r][i]
                                    if (square[0] == enemy_color and (square[1] == 'R' or square[1] == 'Q')):
                                        attacking_piece = True
                                    elif (square != '--'):
                                        blocking_piece = True
                            if (not attacking_piece or blocking_piece):
                                moves.append(Move((r, c), (r + 1, c - 1), self.board, is_enpasant_move=True))
                    if (self.board[r + 1][c + 1][0] == 'w'):
                        if (not (piece_pined) or pin_dir == (1, 1)):
                            moves.append(Move((r, c), (r + 1, c + 1), self.board))
                    elif ((r + 1, c + 1) == self.enpasent_possible):
                        if (not (piece_pined) or pin_dir == (1, 1)):
                            attacking_piece = blocking_piece = False
                            if (king_row == r):
                                if (king_col < c):
                                    inside_range = range(king_col + 1, c)
                                    outside_range = range(c + 2, 8)
                                else:
                                    inside_range = range(king_col - 1, c + 1, -1)
                                    outside_range = range(c - 1, -1, -1)
                                for i in inside_range:
                                    if (self.board[r][i] != '--'):
                                        blocking_piece = True
                                for i in outside_range:
                                    square = self.board[r][i]
                                    if (square[0] == enemy_color and (square[1] == 'R' or square[1] == 'Q')):
                                        attacking_piece = True
                                    elif (square != '--'):
                                        blocking_piece = True
                            if (not attacking_piece or blocking_piece):
                                moves.append(Move((r, c), (r + 1, c + 1), self.board, is_enpasant_move=True))
                elif (c == 0):
                    if (self.board[r + 1][c + 1][0] == 'w'):
                        if (not (piece_pined) or pin_dir == (1, 1)):
                            moves.append(Move((r, c), (r + 1, c + 1), self.board))
                    elif ((r + 1, c + 1) == self.enpasent_possible):
                        if (not (piece_pined) or pin_dir == (1, 1)):
                            attacking_piece = blocking_piece = False
                            if (king_row == r):
                                if (king_col < c):
                                    inside_range = range(king_col + 1, c)
                                    outside_range = range(c + 2, 8)
                                else:
                                    inside_range = range(king_col - 1, c + 1, -1)
                                    outside_range = range(c - 1, -1, -1)
                                for i in inside_range:
                                    if (self.board[r][i] != '--'):
                                        blocking_piece = True
                                for i in outside_range:
                                    square = self.board[r][i]
                                    if (square[0] == enemy_color and (square[1] == 'R' or square[1] == 'Q')):
                                        attacking_piece = True
                                    elif (square != '--'):
                                        blocking_piece = True
                            if (not attacking_piece or blocking_piece):
                                moves.append(Move((r, c), (r + 1, c + 1), self.board, is_enpasant_move=True))
                elif (c == 7):
                    if (self.board[r + 1][c - 1][0] == 'w'):
                        if (not (piece_pined) or pin_dir == (1, -1)):
                            moves.append(Move((r, c), (r + 1, c - 1), self.board))
                    elif ((r + 1, c + 1) == self.enpasent_possible):
                        if (not (piece_pined) or pin_dir == (1, -1)):
                            attacking_piece = blocking_piece = False
                            if (king_row == r):
                                if (king_col < c):
                                    inside_range = range(king_col + 1, c - 1)
                                    outside_range = range(c + 1, 8)
                                else:
                                    inside_range = range(king_col - 1, c, -1)
                                    outside_range = range(c - 2, -1, -1)
                                for i in inside_range:
                                    if (self.board[r][i] != '--'):
                                        blocking_piece = True
                                for i in outside_range:
                                    square = self.board[r][i]
                                    if (square[0] == enemy_color and (square[1] == 'R' or square[1] == 'Q')):
                                        attacking_piece = True
                                    elif (square != '--'):
                                        blocking_piece = True
                            if (not attacking_piece or blocking_piece):
                                moves.append(Move((r, c), (r + 1, c - 1), self.board, is_enpasant_move=True))

    def rook_moves(self, r, c, moves):
        '''
        takes the row, coloums and already avialable moves as input
        then adds the moves which this rook can make to set of all possible moves
        and then returns that updated set of all possible moves
        '''
        piece_pined = False
        pin_dir = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if (self.pins[i][0] == r and self.pins[i][1] == c):
                piece_pined = True
                pin_dir = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        direction = ((-1, 0), (0, -1), (1, 0), (0, 1))
        if (self.whiteToMove):
            capture_color = 'b'
        else:
            capture_color = 'w'
        for d in direction:
            for i in range(1, 8):
                end_row = r + d[0] * i
                end_col = c + d[1] * i
                if ((end_row >= 0 and end_row <= 7) and (end_col >= 0 and end_col <= 7)):
                    if (not (piece_pined) or pin_dir == d or pin_dir == (-d[0], -d[1])):
                        target_sq = self.board[end_row][end_col]
                        if (target_sq != '--'):
                            if (target_sq[0] == capture_color):
                                moves.append(Move((r, c), (end_row, end_col), self.board))
                                break  # If we find enemy piece all we can do is capture it, but can't go any forward so yeh that is the end
                            else:
                                break  # If we find out piece then obviously there is no way going forward or going to that square
                        else:
                            moves.append(Move((r, c), (end_row, end_col), self.board))
                else:
                    break  # we are simply of the board

    def bishop_moves(self, r, c, moves):
        '''
        takes the row, coloums and already avialable moves as input
        then adds the moves which this bishop can make to set of all possible moves
        and then returns that updated set of all possible moves
        '''
        piece_pined = False
        pin_dir = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if (self.pins[i][0] == r and self.pins[i][1] == c):
                piece_pined = True
                pin_dir = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        direction = ((-1, 1), (1, 1), (1, -1), (-1, -1))
        if (self.whiteToMove):
            capture_color = 'b'
        else:
            capture_color = 'w'
        for d in direction:
            for i in range(1, 8):
                end_row = r + d[0] * i
                end_col = c + d[1] * i
                if ((end_row >= 0 and end_row <= 7) and (end_col >= 0 and end_col <= 7)):
                    if (not (piece_pined) or pin_dir == d or pin_dir == (-d[0], -d[1])):
                        target_sq = self.board[end_row][end_col]
                        if (target_sq == '--'):
                            moves.append(Move((r, c), (end_row, end_col), self.board))
                        else:
                            if (target_sq[0] == capture_color):
                                moves.append(Move((r, c), (end_row, end_col), self.board))
                                break  # If we find enemy piece all we can do is capture it, but can't go any forward so yeh that is the end
                            else:
                                break  # If we find out piece then obviously there is no way going forward or going to that square

                else:
                    break  # we are simply of the board

    def knight_moves(self, r, c, moves):
        '''
        takes the row, coloums and already avialable moves as input
        then adds the moves which this knight can make to set of all possible moves
        and then returns that updated set of all possible moves
        '''
        piece_pined = False
        pin_dir = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if (self.pins[i][0] == r and self.pins[i][1] == c):
                piece_pined = True
                pin_dir = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        direction = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        if (self.whiteToMove):
            capture_color = 'b'
        else:
            capture_color = 'w'
        for i in range(8):
            end_row = r + direction[i][0]
            end_col = c + direction[i][1]
            if ((end_row >= 0 and end_row <= 7) and (end_col >= 0 and end_col <= 7)):
                if (not (piece_pined)):
                    target_sq = self.board[end_row][end_col]
                    if (target_sq == '--' or (target_sq[0] == 'b' and self.whiteToMove) or (
                            target_sq[0] == 'w' and not (self.whiteToMove))):
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                    else:
                        pass

    def queen_moves(self, r, c, moves):
        '''
        takes the row, coloums and already avialable moves as input
        then adds the moves which this queen can make to set of all possible moves
        and then returns that updated set of all possible moves
        remember queen is just the addition of bisop and rook
        i.e queen moves=rook moves+bisop moves
        '''
        piece_pined = False
        pin_dir = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if (self.pins[i][0] == r and self.pins[i][1] == c):
                piece_pined = True
                pin_dir = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        direction = ((-1, 1), (1, -1), (1, 1), (-1, -1), (-1, 0), (0, -1), (1, 0), (0, 1))
        if (self.whiteToMove):
            capture_color = 'b'
        else:
            capture_color = 'w'
        for d in direction:
            for i in range(1, 8):
                end_row = r + d[0] * i
                end_col = c + d[1] * i
                if ((end_row >= 0 and end_row <= 7) and (end_col >= 0 and end_col <= 7)):
                    if (not (piece_pined) or pin_dir == d or pin_dir == (-d[0], -d[1])):
                        target_sq = self.board[end_row][end_col]
                        if (target_sq != '--'):
                            if (target_sq[0] == capture_color):
                                moves.append(Move((r, c), (end_row, end_col), self.board))
                                break  # If we find enemy piece all we can do is capture it, but can't go any forward so yeh that is the end
                            else:
                                break  # If we find out piece then obviously there is no way going forward or going to that square
                        else:
                            moves.append(Move((r, c), (end_row, end_col), self.board))
                else:
                    break  # we are simply of the board

    def king_moves(self, r, c, moves):
        '''
        takes the row, coloums and already avialable moves as input
        then adds the moves which this king can make to set of all possible moves
        and then returns that updated set of all possible moves
        '''
        direction = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        if (self.whiteToMove):
            capture_color = 'b'
        else:
            capture_color = 'w'
        for i in range(8):
            end_row = r + direction[i][0]
            end_col = c + direction[i][1]
            if ((end_row >= 0 and end_row <= 7) and (end_col >= 0 and end_col <= 7)):
                target_sq = self.board[end_row][end_col]
                if (target_sq == '--' or (target_sq[0] == 'b' and self.whiteToMove) or (
                        target_sq[0] == 'w' and not (self.whiteToMove))):
                    ######ASSUMING KING MOVES TO NEXT LOCATON######
                    if (self.whiteToMove):
                        self.white_king_location = (end_row, end_col)
                    else:
                        self.black_king_location = (end_row, end_col)
                    ####CHECKING IF IT LENDS IN CHECK THERE######3
                    in_check, pins, checks = self.check_for_pins_checks()
                    if (not (in_check)):
                        ######IF IT DOESN'T ADD THAT MOVE IN######
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                    #####PLACE KING BACK TO ORIGNAL POSSITON#######
                    if (self.whiteToMove):
                        self.white_king_location = (r, c)
                    else:
                        self.black_king_location = (r, c)
                else:
                    pass

    def get_castle_moves(self,r,c,moves,allycolor):
        if(self.square_under_attack(r,c)):#If you are in check u can't castel
            return
        if((self.whiteToMove and self.currentCastlingRight.wks) or (not self.whiteToMove and self.currentCastlingRight.bks)):
            self.get_king_side_castle_moves(r,c,moves,allycolor)
        if ((self.whiteToMove and self.currentCastlingRight.wqs) or (
                not self.whiteToMove and self.currentCastlingRight.bqs)):
            self.get_queen_side_castle_moves(r, c, moves, allycolor)

    def get_king_side_castle_moves(self,r,c,moves,allycolor):
        if(self.board[r][c+1]=='--' and self.board[r][c+2]=='--'):#If that ain't empty then you can't castel
            if((not self.square_under_attack(r,c+1)) and (not self.square_under_attack(r,c+2))):
                moves.append(Move((r,c),(r,c+2),self.board,is_castle_move=True))
    def get_queen_side_castle_moves(self,r,c,moves,allycolor):
        if (self.board[r][c - 1] == '--' and self.board[r][c - 2] == '--' and self.board[r][c-3]=='--'):  # If that ain't empty then you can't castel
            if ((not self.square_under_attack(r, c - 1)) and (not self.square_under_attack(r, c - 2))):
                moves.append(Move((r, c), (r, c - 2), self.board, is_castle_move=True))

class Castle_rights():
    def __init__(self,wks,bks,wqs,bqs):
        self.wks=wks
        self.bks=bks
        self.wqs=wqs
        self.bqs=bqs
class Move():
    # Here we are gonna convert programing notation to chess notaion
    rank_to_row = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    row_to_rank = {v: k for k, v in rank_to_row.items()}
    files_to_cols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    col_to_files = {v: k for k, v in files_to_cols.items()}

    def __init__(self, start_sq, end_sq, board,is_enpasant_move=False, is_castle_move=False):
        self.start_row = start_sq[0]
        self.start_col = start_sq[1]
        self.end_row = end_sq[0]
        self.end_col = end_sq[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        self.is_pawn_pro = ((self.piece_moved == 'wp' and self.end_row == 0) or (self.piece_moved == 'bp' and self.end_row == 7))

        # For Enpasant
        self.is_enpasant_move = is_enpasant_move
        self.is_capture = self.piece_captured != "--"
        self.is_castle_move=is_castle_move
        self.move_id = 1000 * self.start_row + 100 * self.start_col + 10 * self.end_row + self.end_col
        # Till here we haven't really done anything, we are just storing info on what goes from where to where
        # Now the location of starting squares tells us which piece is being moved
        # Location of end square tells us which piece is being captured
        # That is, if a piece is being captured, if not then well it is pretty much it we will ignore it...

    def __eq__(self, other):
        if isinstance(other, Move):
            return (self.move_id == other.move_id)
        return (False)

    def get_chess_notation(self):
        return (self.get_rank_files(self.start_row, self.start_col) + self.get_rank_files(self.end_row, self.end_col))

    def get_rank_files(self, r, c):
        return (self.col_to_files[c] + self.row_to_rank[r])

    #will override string function now
    def __str__(self):
        #Castle looks like 'o-o' or 'o-o-o'
        if(self.is_castle_move):
            return 'o-o' if self.end_col==6 else 'o-o-o'
        end_square=self.get_rank_files(self.end_row,self.end_col)
        #Pawn moves
        if(self.piece_moved[1]=='p'):
            if(self.is_capture):
                return self.col_to_files[self.start_col]+'x'+end_square
            else:
                return end_square
        #picece moves
        move_string=self.piece_moved[1]
        if(self.is_capture):
            move_string+='x'
        return move_string+end_square
