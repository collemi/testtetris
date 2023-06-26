import pygame
from tetrominos import *
from random import randrange
import os
import time
import linecache
from pickle import *

WIDTH_screen = 705
HEIGHT_screen = 1000

WIDTH = 500
HEIGHT = HEIGHT_screen

pygame.init()

screen = pygame.display.set_mode((WIDTH_screen , HEIGHT_screen))

running = True

taille_image = 50
decalage = 105

x = 5*50
y = 0

tabpieces = [
    Jtrominos,
    Ltrominos,
    Ztrominos,
    Strominos,
    Ttrominos,
    Itrominos,
    Otrominos
]
strpiece = [
    'Jtrominos',
    'Ltrominos',
    'Ztrominos',
    'Strominos',
    'Ttrominos',
    'Itrominos',
    'Otrominos'
]

tableau = [
    
]

for i in range(20):
    tableau.append([])
    for j in range(12):
        tableau[i].append(int(0))

def affichertableau(tab):
    taby = 0
    tabx = 0
    for ligne in tab:
        for case in ligne:

            image = pygame.image.load('./imgtrominos/0.png').convert()

            for i in range(11):
                if case == i + 1:
                    image = pygame.image.load(f'./imgtrominos/{i + 1}.png').convert()
                
            screen.blit(image, ((tabx*taille_image), (taby*taille_image)))

            tabx += 1
        taby += 1
        tabx = 0

def afficherpiece(strpiece, tabpiece, x, y):
    ind = tetromindex[f'{strpiece}']
    image = pygame.image.load(f'./imgtrominos/{ind}.png').convert()
    for i in range(len(tabpiece[pos])):
        for j in range(len(tabpiece[pos][i])):
            if tabpiece[pos][i][j] != 0:
                screen.blit(image, (x + j*taille_image, y + i*taille_image))

def spiece(strpiece, tabpiece):
    image = pygame.image.load(f'./imgtrominos/0.png').convert()
    for i in range(len(tabpiece[1])):
        for j in range(len(tabpiece[1][i])):
            screen.blit(image, (WIDTH + decalage + 20 + (j*10), 15 + i*10))

    ind = tetromindex[f'{strpiece}']
    image = pygame.image.load(f'./imgtrominos/{ind}.png').convert()
    image_small = pygame.transform.scale(image, (10, 10))
    for i in range(len(tabpiece[1])):
        for j in range(len(tabpiece[1][i])):
            if tabpiece[1][i][j] != 0:
                screen.blit(image_small, (WIDTH + decalage + 35 + j*10, 30 + i*10))

def hpiece(hold, strpiece, tabpiece):
    if hold != -1:
        image = pygame.image.load(f'./imgtrominos/0.png').convert()
        for i in range(len(tabpiece[1])):
            for j in range(len(tabpiece[1][i])):
                screen.blit(image, (-10 + 20 + (j*10), 15 + i*10))

        ind = tetromindex[f'{strpiece}']
        image = pygame.image.load(f'./imgtrominos/{ind}.png').convert()
        image_small = pygame.transform.scale(image, (10, 10))
        for i in range(len(tabpiece[1])):
            for j in range(len(tabpiece[1][i])):
                if tabpiece[1][i][j] != 0:
                    screen.blit(image_small, (-10 + 35 + j*10, 30 + i*10))

def breakanimation(tableau, nbrpiece, holdpiece, x, y):
    nbrligne = 0
    for frame in range(4):
        for j in range(len(tableau)):
            if tableau[j].count(0) == 2:
                for k in range(len(tableau[j]) - 2):
                    tableau[j][k + 2] = 8 + frame
                nbrligne += 1
        if nbrligne >= 1:
            affichertableau(tableau)
            afficherpiece(strpiece[nbrpiece], tabpieces[nbrpiece], x, y)
            hpiece(holdpiece, strpiece[holdpiece], tabpieces[holdpiece])
            pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(- 10, 100, 105, 5))
            pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(decalage - 10, 0, 5, HEIGHT_screen))
            pygame.display.flip()
            time.sleep(0.1)

        

def write(size,text,x ,y ,color=(255, 255, 255), bgcolor=(0, 0, 0, 128)):
    font = pygame.font.Font('freesansbold.ttf', size)
    content = font.render(text, True, color, bgcolor)
    screen.blit(content, (x, y))
                
def verifcanmovedown(tabpiece, tableau, pos, x, y):
    try:
        for i in range(len(tabpiece[pos])):
            for j in range(len(tabpiece[pos][i])):
                # tabpiece[pos][i][j] case de la piece dans la piece
                if tabpiece[pos][i][j] != 0:
                    if tableau[(int(y / 50) + i)+1][int(x / (WIDTH/10))+j] != 0:
                        return True
        return False
    except IndexError:
        return True

def verifcanmoveright(tabpiece, tableau, pos, x, y):
    try:
        for i in range(len(tabpiece[pos])):
            for j in range(len(tabpiece[pos][i])):
                # tabpiece[pos][i][j] case de la piece dans la piece
                if tabpiece[pos][i][j] != 0:
                    if tableau[(int(y / 50) + i)][(int(x / (WIDTH/10))+j) + 1] != 0:
                        return True
        return False
    except IndexError:
        return True

def verifcanmoveleft(tabpiece, tableau, pos, x, y):
    
    for i in range(len(tabpiece[pos])):
        for j in range(len(tabpiece[pos][i])):
            if tabpiece[pos][i][j] != 0:
                if ((int(x / (WIDTH/10))+j)) <= 0:
                    return True
            # tabpiece[pos][i][j] case de la piece dans la piece
                if tableau[(int(y / 50) + i)][(int(x / (WIDTH/10))+j) - 1] != 0:
                    return True
    for i in range(len(tabpiece[pos])):
        for j in range(len(tabpiece[pos][i])):
            if tabpiece[pos][i][j] != 0:
                if (int(x / (WIDTH/10))+j) - 1 == 1:
                    return True
    return False

def verifrightrotation(tabpiece, tableau, pos, x, y):
    if pos == 3:
        tpos = 0
    else:
        tpos = pos + 1
    try:
        for i in range(len(tabpiece[tpos])):
            for j in range(len(tabpiece[tpos][i])):
                if tabpiece[tpos][i][j] != 0:
                    if ((int(x / (WIDTH/10))+j)) <= 1:
                        return True
                    if tableau[(int(y / 50) + i)][(int(x / (WIDTH/10))+j)] > 0:
                        return True          
        
        return False
    except IndexError:
        return True

def verifleftrotation(tabpiece, tableau, pos, x, y):
    if pos == 0:
        tpos = 3
    else:
        tpos = pos - 1
    try:
        for i in range(len(tabpiece[tpos])):
            for j in range(len(tabpiece[tpos][i])):
                if tabpiece[tpos][i][j] != 0:
                    if ((int(x / (WIDTH/10))+j)) <= 1:
                        return True
                    if tableau[(int(y / 50) + i)][(int(x / (WIDTH/10))+j)] > 0:
                        return True

        return False
    except IndexError:
        return True

def fixeThePiece(tabpiece, tableau, pos, x, y):
    for i in range(len(tabpiece[pos])):
        for j in range(len(tabpiece[pos][i])):
            if tabpiece[pos][i][j] != 0:
                tableau[(int(y / 50) + i)][(int(x / (WIDTH/10))+j)] = tabpiece[pos][i][j]
    return tableau

def clearLine(tableau, score):
    nbrline = 0
    for i in range(len(tableau)):
        if tableau[i].count(0) == 2:
            del(tableau[i])
            nbrline += 1
            tableau.insert(0, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    
    if nbrline == 4:
        score += 500
    else:
        score += 100*nbrline

    return tableau, score
def gameOver(tabpiece, tableau, pos, x, y):
    for i in range(len(tabpiece[pos])):
        for j in range(len(tabpiece[pos][i])):
            # tabpiece[pos][i][j] case de la piece dans la piece
            if tabpiece[pos][i][j] != 0:
                if tableau[(int(y / 50) + i)][int(x / (WIDTH/10))+j] != 0:
                    return True
    return False


tps = 0
appuyer = False
fixe = False
pos = 0
nbrpiece = randrange(0,7)
second_piece = randrange(0,7)
holdpiece = -1
clock = pygame.time.Clock()
score = 9600
level = (45 - (( score // 250) + 1))
isholdpressed = True
isholded = False

pygame.mixer.music.load('tetrissound.mp3')
pygame.mixer.music.play(-1)

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    pressed = pygame.key.get_pressed()
    if(pressed[pygame.K_LSHIFT] and not isholdpressed and not isholded):
        isholdpressed = True
        if holdpiece == -1:
            holdpiece = nbrpiece
            nbrpiece = second_piece
            second_piece = randrange(0,7)
            isholded = True
        else:
            holdpiece, nbrpiece = nbrpiece, holdpiece
            isholded = True
        x = 5*50
        y = 0
        
        

    if(not pressed[pygame.K_LSHIFT] and isholdpressed):
        isholdpressed = False

    if (pressed[pygame.K_q] 
        and not appuyermove 
        and not verifcanmoveleft(tabpieces[nbrpiece], tableau, pos, x, y)):

        x -= (WIDTH/10)
        appuyermove = True

    if (pressed[pygame.K_d] 
        and not appuyermove
        and not verifcanmoveright(tabpieces[nbrpiece], tableau, pos, x, y)):

        x += (WIDTH/10)
        appuyermove = True

    if (pressed[pygame.K_LEFT] 
        and not appuyerrot 
        and not verifleftrotation(tabpieces[nbrpiece], tableau, pos, x, y)):

        pos -= 1
        appuyerrot = True
    if (pressed[pygame.K_RIGHT] 
        and not appuyerrot 
        and not verifrightrotation(tabpieces[nbrpiece], tableau, pos, x, y)):
        
        pos += 1
        appuyerrot = True

    if pos > 3:
        pos = 0
    if pos < 0:
        pos = 3

    if not pressed[pygame.K_RIGHT] and not pressed[pygame.K_LEFT]:
        appuyerrot = False
    if not pressed[pygame.K_q] and not pressed[pygame.K_d]:
        appuyermove = False

    affichertableau(tableau)

    if level > 5:
        level = (45 - (( score // 250) + 1))
    else:
        level = 5

    if tps >= level:
        fixe = verifcanmovedown(tabpieces[nbrpiece], tableau, pos, x, y)
        if fixe == False:
            y += 50
        tps = 0

    if fixe == True:
        tableau = fixeThePiece(tabpieces[nbrpiece], tableau, pos, x, y)
        isholded = False
        nbrpiece = second_piece
        second_piece = randrange(0,7)
        x = 5*50
        y = 0
        fixe = False



    afficherpiece(strpiece[nbrpiece], tabpieces[nbrpiece], x, y)

    spiece(strpiece[second_piece], tabpieces[second_piece])

    hpiece(holdpiece, strpiece[holdpiece], tabpieces[holdpiece])

    breakanimation(tableau, nbrpiece, holdpiece, x, y)
    
    tableau, score = clearLine(tableau, score)

    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(WIDTH + decalage - 5, 0, 5, HEIGHT_screen))
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(WIDTH + decalage, 100, 105, 5))
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(- 10, 100, 105, 5))
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(decalage - 10, 0, 5, HEIGHT_screen))
    write(20,"score :",(WIDTH + 25) + decalage ,125)
    write(20,str(score),(WIDTH + 25) + decalage, 150)
    # pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(WIDTH + 20, 15, 5, 5))

    pygame.display.flip()

    if pressed[pygame.K_DOWN]:
        tps += level//3
    else:
        tps += 1
    
    if gameOver(tabpieces[nbrpiece], tableau, pos, x, y):
        running = False

    # rien ici sinon jte ban
    clock.tick(60)



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    screen.fill((0, 0, 0))
    write(70,"GAME OVER",((WIDTH)/5)-10,HEIGHT/3)

    write(30,"press c to close",((WIDTH)/3) + 30,(HEIGHT/3) + 85)
    write(30,"press space to play again",((WIDTH)/4) - 5,(HEIGHT/3) + 120)

    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_SPACE]:
        with open("setting.txt","w") as setting:
            setting.write("replay")
        break
    if pressed[pygame.K_c]:
        with open("setting.txt","w") as setting:
            setting.write("quit")
        break

    pygame.display.flip()

f = open ("player.txt","rb")

leaderboard = load(f)

f.close()

f = open("player.txt","wb")
lb = []
while True:
    pseudo = input("Enter votre pseudo : ")
    if len(pseudo) <= 10:
        break
    elif len(pseudo) == 0:
        print("Vous devez avoir un nom !")
    else:
        print("Vous ne pouvez pas dépasser 10 charactère !")

lb.append([pseudo,score])
for joueur, score in leaderboard.items():
    lb.append([joueur,score])

lbtrier = sorted(lb, key=lambda x: x[1], reverse=True)

leaderboard = {}

if len(lbtrier) >= 10:
    for i in range(10):
        key = lbtrier[i][0]
        value = lbtrier[i][1]
        leaderboard[key] = value

else:
    for joueur, score in lbtrier:
        leaderboard[joueur] = score

dump(leaderboard, f)

f.close()

for joueur, score in leaderboard.items():
    print(f"{joueur} => {score}")

pygame.quit()

# écriture dynamique
#
# with open("test.txt","r") as paper:
#     test = paper.read()
#     if test == "":
#         test = 0
#     else:
#         test = int(test)
