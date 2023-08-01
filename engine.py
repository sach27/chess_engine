import chessmain as chessmain
import pygame as py 
width=height=512
dim=8
sq_size=width//dim
max_fps=15 #For animations will use later
images={}
'''
Intialize a global dict of image
'''
def load_images():
    pieces=['wp','wR','wN','wB','wK','wQ','bp','bR','bN','bB','bK','bQ']
    for piec in pieces:
        images[piec]=py.transform.scale(py.image.load(r'C:/Users/SACH/OneDrive/Desktop/Projects/chess_engine/images/'+piec+'.png'),(sq_size,sq_size))

'''
Main diver of code, this handles user input and updating graphics
'''
def main():
    py.init()
    screen=py.display.set_mode((width,height))
    clock=py.time.Clock()
    screen.fill(py.Color("Grey"))
    gs=chessmain.GameState()
    valid_moves=gs.get_valid_moves()
    move_made=False 
    load_images()
    running=True
    sq_selected=()#keep track of last click of user
    player_click=[]#keep track of player cliks
    while running:
        for e in py.event.get():
            if e.type== py.QUIT:
                running=False
            elif e.type==py.MOUSEBUTTONDOWN:
                location=py.mouse.get_pos()
                col=location[0]//sq_size
                row=location[1]//sq_size
                if sq_selected==(row,col):#the user clicked the same square twice
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
                    move=chessmain.Move(player_click[0],player_click[1],gs.board)
                    for i in range(len(valid_moves)):
                        if(move ==valid_moves[i]):
                            gs.make_move(valid_moves[i])
                            move_made=True
                            sq_selected=()#Since move has been made we can empty the tuple and list nowe
                            player_click=[]
                    if(not(move_made)):
                        player_click=[sq_selected]
            elif(e.type==py.KEYDOWN):
                if(e.key==py.K_TAB):
                    gs.undo()
                    valid_moves=gs.get_valid_moves()
                    move_made=True
        if(move_made):
            valid_moves=gs.get_valid_moves()
            move_made=False
        draw_game_state(screen,gs)
        clock.tick(max_fps)
        py.display.flip()
    draw_game_state(screen,gs)

def draw_game_state(screen ,gs):
    draw_board(screen)#Draw squares
    draw_pieces(screen,gs.board)

def draw_board(screen):
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

def draw_pieces(screen,board):
    for r in range(dim):
        for c in range(dim):
            piece=board[r][c]
            if(piece!="--"):
                screen.blit(images[piece],py.Rect(c*sq_size, r*sq_size ,sq_size , sq_size))
main()
