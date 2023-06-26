import pygame
import os
from pickle import *


WIDTH_screen = 605
HEIGHT_screen = 1000

WIDTH = 500
HEIGHT = HEIGHT_screen

pygame.init()

screen = pygame.display.set_mode((WIDTH_screen , HEIGHT_screen))

leaderboard = {}

for i in range(10):
    with open("setting.txt","r") as paper:
        setting = paper.readline(-1)

def write(size,text,x ,y ,color=(255, 255, 255), bgcolor=(0, 0, 0, 128)):
    font = pygame.font.Font('freesansbold.ttf', size)
    content = font.render(text, True, color, bgcolor)
    screen.blit(content, (x, y))

f = open ("player.txt","rb")

leaderboard = load(f)

f.close()

while True:
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
    screen.fill((0,0,0))
    pressed = pygame.key.get_pressed()

    with open("test.txt","r") as paper:
        test = paper.read()
        if test == "":
            test = 0
        else:
            test = int(test)

    write(45, "Leaderboard", 163, test)

    i = 0
    for joueur, score in leaderboard.items():

        

        write(32, joueur, 100, 200 + (i*36))
        write(32, str(score), 496 - (len(str(score)) * 17 ), 200 + (i*36))
        i += 1


    pygame.display.flip()

pygame.quit()