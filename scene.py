import pygame
from player import Player

WIDTH = 1000
HEIGHT = 400

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.clock = pygame.time.Clock()
        self.player = Player(WIDTH/2, HEIGHT/2)
        self.voids = [
            pygame.Rect(0, HEIGHT, WIDTH, 1),
            pygame.Rect(0, 0, -1, HEIGHT),
            pygame.Rect(WIDTH, 0, 1, HEIGHT),
            pygame.Rect(0, 0, WIDTH, -1),
        ]
        self.area_color= "green"

    def handling_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player.velocity[0] = -1
        elif keys[pygame.K_RIGHT]:
            self.player.velocity[0] = 1
        else:
            self.player.velocity[0] = 0
        if keys[pygame.K_UP]:
            self.player.velocity[1] = -1
        elif keys[pygame.K_DOWN]:
            self.player.velocity[1] = 1
        else:
            self.player.velocity[1] = 0
        
            

    def update(self):
        self.player.move()



    def display(self):
        self.screen.fill((0, 153, 153))
        for i in range(len(self.voids)):
            pygame.draw.rect(self.screen, self.area_color, self.voids[i])
        self.player.draw(self.screen)
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handling_events()
            self.update()
            self.display()
            self.clock.tick(60)


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

game = Game(screen)

game.run()

pygame.quit()