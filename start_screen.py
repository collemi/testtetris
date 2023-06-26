import pygame
import platform
import os

WIDTH_screen = 605
HEIGHT_screen = 1000

WIDTH = 500
HEIGHT = HEIGHT_screen

pygame.init()

screen = pygame.display.set_mode((WIDTH_screen , HEIGHT_screen))


def write(size,text,x ,y ,color=(255, 255, 255), bgcolor=(0, 0, 0, 128)):
    font = pygame.font.Font('freesansbold.ttf', size)
    content = font.render(text, True, color, bgcolor)
    screen.blit(content, (x, y))

while True:
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_SPACE]:
        pygame.quit()
        if platform.system() == 'Windows':
            os.system("python ./main.py")
        elif platform.system() == 'Linux':
            os.system("python3 ./main.py")
        with open("setting.txt","r") as paper:
            setting = paper.read()
        if setting == "quit":
            break
        elif setting == "replay":
            pygame.init()
            screen = pygame.display.set_mode((WIDTH_screen , HEIGHT_screen))
    
    if pressed[pygame.K_l]:
        pygame.quit()
        
        os.system("python3 ./leaderboard.py")

        pygame.init()
        screen = pygame.display.set_mode((WIDTH_screen , HEIGHT_screen))
        
    write(75,"TETRIS",WIDTH/3, 275)
    write(20,"press SPACE to play TETRIS", WIDTH/3, 400)
    write(20,"press L to see the leaderboard", WIDTH/3 - 7, 450)
    pygame.display.flip()

pygame.quit()