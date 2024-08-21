import pygame
from sys import exit

class White(pygame.sprite.Sprite):
    def __init__(self):
        super().__init()


pygame.init()
screen = pygame.display.set_mode((1000,680))
pygame.display.set_caption('Lines of Action')
clock = pygame.time.Clock()

board_surf = pygame.image.load('graphics/board.png').convert()
board_surf = pygame.transform.scale2x(board_surf)

bg_surf = pygame.Surface((680,680))
bg_surf.fill('#432616')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit(bg_surf,(0,0))
    screen.blit(board_surf, (20,20))

    pygame.display.update()
    clock.tick(60)
