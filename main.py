import pygame
from sys import exit
from random import choice

def pos_to_coords(pos):
    '''pos is a tuple representing desired indices, returns tuple of pixel coordinates for blit centering'''
    x_coord = 60 + 80*pos[0]
    y_coord = 60 + 80*(7-pos[1])
    return (x_coord,y_coord)

class White(pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.image = pygame.image.load('graphics/white.png').convert_alpha()
        self.image = pygame.transform.rotozoom(self.image,0,1/4)
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]
        self.color = 'white'
        self.rect = self.image.get_rect(center=pos_to_coords(pos))

class Black(pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.image = pygame.image.load('graphics/black.png').convert_alpha()
        self.image = pygame.transform.rotozoom(self.image,0,1/4)
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]
        self.color = 'black'
        self.rect = self.image.get_rect(center=pos_to_coords(pos))

class Highlight(pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.image = pygame.image.load('graphics/highlight1.png').convert_alpha()
        self.image = pygame.transform.rotozoom(self.image,0,1/4)
        self.pos = pos
        self.rect = self.image.get_rect(center=pos_to_coords(pos))

def reset_board():
    white.empty()
    black.empty()
    for i in range(1,7):
        white.add(White((i,7)))
        white.add(White((i,0)))
        black.add(Black((7,i)))
        black.add(Black((0,i)))

def valid_move_y(t_piece, t_list, t_len, opp_color, inc):
    '''Helper for get_moves that checks valid moves based on y conditions'''
    add_move = True
    if inc:
        for p in t_list:
            if (t_piece.y + t_len > 7) or (p.color == opp_color and p.y < t_piece.y + t_len) or (p.color != opp_color and p.y == t_piece.y + t_len):
                add_move = False
                break
    else:
        for p in t_list:
            if (t_piece.y - t_len < 0) or (p.color == opp_color and p.y > t_piece.y - t_len) or (p.color != opp_color and p.y == t_piece.y - t_len):
                add_move = False
                break
    return add_move

def valid_move_x(t_piece, t_list, t_len, opp_color, inc):
    '''Helper for get_moves that checks valid moves based on x conditions'''
    add_move = True
    if inc:
        for p in t_list:
            if (t_piece.x + t_len > 7) or (p.color == opp_color and p.x < t_piece.x + t_len) or (p.color != opp_color and p.x == t_piece.x + t_len):
                add_move = False
                break
    else:
        for p in t_list:
            if (t_piece.x - t_len < 0) or (p.color == opp_color and p.x > t_piece.x - t_len) or (p.color != opp_color and p.x == t_piece.x - t_len):
                add_move = False
                break
    return add_move

def get_moves(piece,piece_list):
    # first collect the pieces that are on all lines that the piece is on, regardless of color
    ns_list = [p for p in piece_list if p.x == piece.x]
    we_list = [p for p in piece_list if p.y == piece.y]
    nw_se_list = [p for p in piece_list if p.x - piece.x == piece.y - p.y]
    ne_sw_list = [p for p in piece_list if p.x - piece.x == p.y - piece.y]
    # define opp_color for checking blocks and captures
    if piece.color == 'white': opp_color = 'black'
    else: opp_color = 'white'
    legal = []
    ns = len(ns_list)
    we = len(we_list)
    nw_se = len(nw_se_list)
    ne_sw = len(ne_sw_list)
    if valid_move_y(piece,ns_list,ns,opp_color,inc=True): # n
        legal.append((piece.x,piece.y+ns))
    if valid_move_y(piece,ns_list,ns,opp_color,inc=False): # s
        legal.append((piece.x,piece.y-ns))
    if valid_move_x(piece,we_list,we,opp_color,inc=True): # e
        legal.append((piece.x+we,piece.y))
    if valid_move_x(piece,we_list,we,opp_color,inc=False): # w
        legal.append((piece.x-we,piece.y))
    if valid_move_y(piece,nw_se_list,nw_se,opp_color,inc=True): # nw
        legal.append((piece.x-nw_se,piece.y+nw_se))
    if valid_move_y(piece,nw_se_list,nw_se,opp_color,inc=False): # se
        legal.append((piece.x+nw_se,piece.y-nw_se))
    if valid_move_y(piece,ne_sw_list,ne_sw,opp_color,inc=True): # ne
        legal.append((piece.x+ne_sw,piece.y+ne_sw))
    if valid_move_y(piece,ne_sw_list,ne_sw,opp_color,inc=False): # sw
        legal.append((piece.x-ne_sw,piece.y-ne_sw))
    return legal

def mouse_to_pos():
    mouse_coords = pygame.mouse.get_pos()
    x_pos = (mouse_coords[0]-20)//80
    y_pos = 7-(mouse_coords[1]-20)//80
    return (x_pos,y_pos)

def check_highlight():
    mouse = pygame.mouse.get_pressed()
    mouse_pos = mouse_to_pos()
    # if right clicked on a square, do highlighting
    if mouse[2] and -1 < mouse_pos[0] < 8 and -1 < mouse_pos[1] < 8:
        select = [h for h in highlight if h.pos == mouse_pos]
        if select == []:
            highlight.add(Highlight((mouse_pos)))
        else:
            select[0].kill()
    # elif left click
    elif mouse[0]:
        # check left click inside window
        mouse_coords = pygame.mouse.get_pos()
        if mouse_coords[0] <= 1000 and mouse_coords[1] <= 680:
            hit = False
            for group in white, black, highlight:
                for i in group:
                    if i.pos == mouse_pos:
                        hit = True
            if not hit:
                highlight.empty()

pygame.init()
screen = pygame.display.set_mode((1000,680))
pygame.display.set_caption('Lines of Action')
clock = pygame.time.Clock()

board_surf = pygame.image.load('graphics/board.png').convert()
board_surf = pygame.transform.scale2x(board_surf)

border_surf = pygame.Surface((680,680))
border_surf.fill('#432616')

bg_surf = pygame.Surface((1000,680))
bg_surf.fill('#757C88')

white = pygame.sprite.Group()
black = pygame.sprite.Group()
highlight = pygame.sprite.Group()

player_color = 'white'

reset_board()
white_list = white.sprites()
black_list = black.sprites()
all_list = white_list + black_list

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            check_highlight()

    screen.blit(bg_surf,(0,0))
    screen.blit(border_surf,(0,0))
    screen.blit(board_surf, (20,20))

    white.draw(screen)
    black.draw(screen)

    highlight.draw(screen)
    print(mouse_to_pos())

    pygame.display.update()
    clock.tick(60)
