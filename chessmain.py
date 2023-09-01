import engine as engine
import MoveFinder
import pygame as py 
width=height=512
move_log_panel_width=250
move_log_panel_height=height
dim=8
sq_size=width//dim
max_fps=30 #For animations will use later
images={}
'''
Intialize a global dict of image
'''
def load_images():
    pieces=['wp','wR','wN','wB','wK','wQ','bp','bR','bN','bB','bK','bQ']
    for piec in pieces:
        images[piec]=py.transform.scale(py.image.load(r'C:/Users/SACH/OneDrive/Desktop/Projects/chess_engine/images/'+piec+'.png'),(sq_size,sq_size))

'''
[<engine.Move object at 0x0000021AB94E3D90>, <engine.Move object at 0x0000021AB9FB0610>, <engine.Move object at 0x0000021AB9FB0640>, <engine.Move object at 0x0000021AB9FB06D0>, <engine.
Main diver of code, this handles user input and updating graphics
'''

def main():
    py.init()
    screen=py.display.set_mode((width+move_log_panel_width,height))
    clock=py.time.Clock()
    screen.fill(py.Color("Grey"))
    gs=engine.GameState()
    valid_moves=gs.get_valid_moves()
    move_made=False 
    load_images()
    move_log_font=py.font.SysFont('Arial',15,False,False)
    running=True
    animate=False#if we want animations
    sq_selected=()#keep track of last click of user
    player_click=[]#keep track of player cliks
    game_over=False
    player_one=True#If the human is playing white the variable is true
    player_two=False#Same but for black
    while running:
        is_human_turn=(gs.whiteToMove and player_one) or (not gs.whiteToMove and player_two)

        for e in py.event.get():
            if e.type== py.QUIT:
                running=False

            elif e.type==py.MOUSEBUTTONDOWN:
                if not game_over and is_human_turn:
                    location=py.mouse.get_pos()
                    col=location[0]//sq_size
                    row=location[1]//sq_size
                    if sq_selected==(row,col) or col>=8:#the user clicked the same square twice or he clicked the move log
                        sq_selected=()
                        player_click=[]
                        #here is the deal, in most popular chess eninges, double click means unselect
                        #SO we are gona stick to that convention, and for us too a double click means unselect
                        #Therefore we make our tuple and list empty
                    else:
                        sq_selected=(row,col)
                        player_click.append(sq_selected)# The variable player_click stores both the clicks of user


                    if(len(player_click)==2):#We are checking if we are getting the second click or not
                        #If we co get a second click we move forward
                        move=engine.Move(player_click[0],player_click[1],gs.board)
                        for i in range(len(valid_moves)):
                            if(move ==valid_moves[i]):
                                gs.make_move(valid_moves[i])
                                move_made=True
                                animate=True
                                sq_selected=()#Since move has been made we can empty the tuple and list nowe
                                player_click=[]
                        if(not(move_made)):
                            player_click=[sq_selected]

            elif(e.type==py.KEYDOWN):
                if(e.key==py.K_TAB):
                    gs.undo()
                    valid_moves=gs.get_valid_moves()
                    move_made=True
                    animate=False
                if(e.key==py.K_RSHIFT):
                    gs=engine.GameState()
                    valid_moves=gs.get_valid_moves()
                    sq_selected=()
                    player_click=[]
                    move_made=False
                    animate=False
        #Here we will have moves of AI
        if(not game_over and not is_human_turn):

            AIMove=MoveFinder.find_best_move_min_max(gs,valid_moves)

            if(AIMove==None):
                AIMove=MoveFinder.find_random_move(valid_moves)

            gs.make_move(AIMove)
            move_made=True
            animate=True

        if(move_made):
            if(animate):
                animate_move(gs.moveLog[-1],screen,gs.board,clock)
            valid_moves=gs.get_valid_moves()
            move_made=False
        draw_game_state(screen,gs,valid_moves,sq_selected,move_log_font)
        if gs.check_mate or gs.stale_mate:
            game_over=True
            if(gs.stale_mate):
                text="It is a stale mate"
            else:
                if(gs.whiteToMove):
                    text="Black wins by check mate"
                else:
                    text="White wins by check mate"
            draw_end_game_text(screen,text,move_log_font)
        clock.tick(max_fps)
        py.display.flip()

    draw_game_state(screen,gs,valid_moves,sq_selected,move_log_font)
'''
THIS WILL HIGHLIGHT SQUARE SELECTED AND WHERE IT CAN MOVE
'''
def highlight_squares(screen,gs,valid_moves,sq_selected):
    if(sq_selected!=()):
        r,c=sq_selected
        if(gs.board[r][c][0]==('w' if gs.whiteToMove else 'b')):#making sure square selected can move
            s=py.Surface((sq_size,sq_size))
            s.set_alpha(100)#This is our transperency value ranges from 0 to 255
            s.fill(py.Color('blue'))
            screen.blit(s, (c*sq_size,r*sq_size))

            #highlight possible moves
            s.fill(py.Color('yellow'))
            for move in valid_moves:
                if(move.start_row==r and move.start_col==c):
                    screen.blit(s,(move.end_col*sq_size,move.end_row*sq_size))



def draw_game_state(screen ,gs,valid_moves,sq_selected,move_log_font):
    draw_board(screen)#Draw squares
    highlight_squares(screen,gs,valid_moves,sq_selected)
    draw_pieces(screen,gs.board)
    draw_move_log(screen,gs,move_log_font)

def draw_board(screen):
    global colors
    colors=[py.Color("White"),py.Color("dark green")]
    for r in range(0,8):
        for c in range(0,8):
            colr=colors[((r+c)%2)]
            py.draw.rect(screen,colr,py.Rect(c*sq_size, r*sq_size ,sq_size , sq_size))
            '''
            here is what you need to understand, all even squares in chess are white
            and all odd squares are black, and at 0rth location we have white color
            and at one we have black
            so wherever we get a remainder we know it is odd therefore we go with black color, else we go with white
            '''
'''
The following function will do animation for us
'''
def animate_move(move,screen,board,clock):
    global colors
    coords=[]#list of rows and cols from which the piece will move through
    dR=move.end_row-move.start_row
    dC=move.end_col-move.start_col
    frames_per_sq=15 # frames per square
    frame_count=(abs(dR)+abs(dC))
    for frame in range(frame_count+1):
        r,c=(move.start_row+dR*frame/frame_count, move.start_col+dC*frame/frame_count)
        draw_board(screen)
        draw_pieces(screen,board)
        #Now we don't want piece moved on ending postion so we remove it from there
        color=colors[(move.end_row+move.end_col)%2]
        end_square=py.Rect(move.end_col*sq_size,move.end_row*sq_size,sq_size,sq_size)
        py.draw.rect(screen,color,end_square)
        #If there was a captured piece was there we need to remove it
        if(move.piece_captured!='--'):
            screen.blit(images[move.piece_captured],end_square)
        #Now we have to draw the moving piece
        screen.blit(images[move.piece_moved],py.Rect(c*sq_size,r*sq_size,sq_size,sq_size))
        py.display.flip()
        clock.tick(60)#This is our fps
def draw_move_log(screen,gs,font):

    move_log_rect=py.Rect(width,0,move_log_panel_width,move_log_panel_height)
    py.draw.rect(screen,py.Color('purple'),move_log_rect)
    move_log = gs.moveLog
    move_texts=[]
    for i in range(0,len(move_log),2):
        move_string = str(i//2 +1) + ". " +str(move_log[i])+" "
        if(i+1<len(move_log)):
            move_string+= str(move_log[i+1])+"  "
        move_texts.append(move_string)
    padding=5
    move_per_row=2
    line_spacing=2
    y_shift=padding
    x_shift=5
    for i in range(0,len(move_texts),move_per_row):
        text = ""
        for j in range(move_per_row):
            if(i+j<len(move_texts)):
                text+=move_texts[i+j]
        text_object = font.render(text, True, py.Color('Black'))
        text_location = move_log_rect.move(padding,y_shift)
        screen.blit(text_object, text_location)
        y_shift += text_object.get_height() + line_spacing



def draw_end_game_text(screen,text,font):
    text_object=font.render(text,0,py.Color('Black'))
    text_location=py.Rect(0,0,width,height).move(width/2 -text_object.get_width()/2,height/2-text_object.get_height()/2)
    screen.blit(text_object,text_location)
    text_object=font.render(text,0,py.Color('Gray'))
    screen.blit(text_object,text_location.move(2,2))

def draw_pieces(screen,board):
    for r in range(dim):
        for c in range(dim):
            piece=board[r][c]
            if(piece!="--"):
                screen.blit(images[piece],py.Rect(c*sq_size, r*sq_size ,sq_size , sq_size))
main()
