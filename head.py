import pygame
import os
import random
import time


pygame.init()

t = 0
score = 0
width = 600
height = 600
screen = pygame.display.set_mode((width, height))


def text(words, size):
    cz = pygame.font.SysFont("Arial", size)
    rend = cz.render(words, 1, (132, 0, 255))
    x = (width - rend.get_rect().width) / 2
    y = (height - rend.get_rect().height) / 2
    screen.blit(rend, (x, y))


def textx(words, size, y):
    cz = pygame.font.SysFont("Arial", size)
    rend = cz.render(words, 1, (132, 0, 255))
    x = (width - rend.get_rect().width) / 2
    screen.blit(rend, (x, y))


def texts(words, size, x, y):
    cz = pygame.font.SysFont("Arial", size)
    rend = cz.render(words, 1, (132, 0, 255))
    screen.blit(rend, (x, y))


show = "menu"


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.h = 40
        self.w = 40
        self.look = pygame.Rect(self.x, self.y, self.h, self.w)
        self.img = pygame.image.load(os.path.join('player.png'))

    def draw(self):
        screen.blit(self.img, (self.x, self.y))

    def move(self, v):
        self.y = self.y + v
        self.look = pygame.Rect(self.x, self.y, self.h, self.w)


player = Player(280, 280)

dy = 1.5


class Cliff:
    def __init__(self, x, length):
        self.x = x
        self.lenght = length
        self.y_top = -1000
        self.f_top = random.randint(180, 290)+1000
        self.space = 100
        self.y_bot = self.f_top + self.space - 1000
        self.f_bot = 1000
        self.color = (149, 6, 6)
        self.look_top = pygame.Rect(self.x, self.y_top, self.lenght, self.f_top)
        self.look_bot = pygame.Rect(self.x, self.y_bot, self.lenght, self.f_bot)

    def draw(self):
        pygame.draw.rect(screen, self.color, self.look_top, 0)
        pygame.draw.rect(screen, self.color, self.look_bot, 0)

    def move(self, v):
        self.x = self.x - v
        self.look_top = pygame.Rect(self.x, self.y_top, self.lenght, self.f_top)
        self.look_bot = pygame.Rect(self.x, self.y_bot, self.lenght, self.f_bot)

    def collision(self, player):
        if self.look_top.colliderect(player) or self.look_bot.colliderect(player):
            return True
        else:
            return False


cliff = []
for i in range(3):
    cliff.append(Cliff(i*width/3+700, width/20))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if show == "menu":
                    show = "game"
                    player = Player(280, 280)
                if show == "game":
                    dy = -1.1
                    t = 0
            if event.key == pygame.K_w:
                if show == "finish":
                    show = "game"
                    player = Player(280, 280)
                    for c in cliff:
                        cliff.remove(c)
                    cliff.append((Cliff(width+100, width / 20)))
                    cliff.append((Cliff(width+300, width / 20)))
                    cliff.append((Cliff(width+500, width / 20)))
                    player = Player(280, 280)
                    score = 0

    screen.fill((0, 0, 0))

    if show == "menu":
        text("Click space", 40)
        img = pygame.image.load(os.path.join('start.png'))
        screen.blit(img, (236, 100))

    elif show == "game":
        for c in cliff:
            c.move(1)
            c.draw()

            if c.collision(player.look):
                show = "finish"
                for c in cliff:
                    cliff.remove(c)

        for c in cliff:
            if c.x <= -c.lenght:
                cliff.remove(c)
                cliff.append((Cliff(width, width/20)))
            if c.x == width/2:
                score += 1
        player.draw()
        player.move(dy)
        texts(str(score), 20, 50, 50)

    if show == "finish":
        text('Your score: ' + str(score), 30,)
        textx('Click "w"', 30, 330)

    pygame.display.update()
    time.sleep(0.005)
    t += 1
    if t == 30:
        dy = 1.1
