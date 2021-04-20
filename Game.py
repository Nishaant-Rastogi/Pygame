import math
import sys
import time

import pygame
from pygame.locals import *

def events():
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()


pygame.init()
clk = pygame.time.Clock()
screen = pygame.display.set_mode((800, 550))
FPS = 500

bg = pygame.image.load("Background.png").convert()
pygame.mixer.music.load('forest.wav')
pygame.mixer.music.play(-1)

bgW, bgH = bg.get_rect().size
x = 0

archer = pygame.image.load("archer1.png").convert_alpha()
archer = pygame.transform.smoothscale(archer, (120, 120))
P_x = 120
P_y = 360
P_vx = 0
P_vy = 20
jump = False

heart = pygame.image.load("like.png").convert_alpha()
heart = pygame.transform.smoothscale(heart, (30, 30))

arrow = pygame.image.load("arrow.png").convert_alpha()
arrow = pygame.transform.smoothscale(arrow, (90, 60))
arrow_state = "ready"

Marrow = pygame.image.load("arrow.png").convert_alpha()
Marrow = pygame.transform.smoothscale(Marrow, (90, 60))
Marrow_state = "ready"

dragonImage = []
dragonY = []
dragonX = []
X_change = -13
for i in range(2):
    dragonImage.append(pygame.image.load("jTx6757pc-0.png").convert_alpha())
    dragonY.append(90 + (i * 250))
    dragonX.append(900 + (i * 600))

a_vx = 25
Ma_vx = 25
life = 5
arrow_in_quiver=10
score = 0
font = pygame.font.SysFont("Segoe Bold", 40)


def fireSingle(x, y):
    global arrow_state
    arrow_state = "fire"
    screen.blit(arrow, (x + 29, y + 32))


def fireMultiple(x, y):
    global Marrow_state
    Marrow_state = "fire"
    screen.blit(Marrow, (x + 29, y + 32))

def lives():
    lives = font.render("Life : " + str(life), True, (255, 0, 0))
    Score = font.render("Score : " + str(score), True, (0,100,0))
    Arrows = font.render("Arrows : " + str(arrow_in_quiver), True, (0,0,255))
    screen.blit(lives, (180, 10))
    screen.blit(heart, (280, 10))
    screen.blit(Score, (350, 10))
    screen.blit(Arrows,(500,10))

def Player(x, y):
    screen.blit(archer, (x, y))


def Enemies(x, y):
    for i in range(2):
        screen.blit(dragonImage[i],(x,y))


def collisionP(Px, Py, Bx, By):
    d = math.sqrt(math.pow((Px - Bx), 2) + math.pow((Py - By), 2))
    if d < 90:
        return True
    return False

def collisionA(ax, ay, Bx, By):
    d = math.sqrt(math.pow((ax - Bx), 2) + math.pow((ay - By), 2))
    if d < 80:
        return True
    return False

refill=1
while True:
    events()
    if life>0:
        k = pygame.key.get_pressed()
        if k[K_RIGHT] and P_x < 650:
            P_vx = 5
        elif k[K_LEFT] and P_x > 20:
            P_vx = -8
        else:
            P_vx = 0
        if jump is False and k[K_UP]:
            jump = True
        if jump:
            P_y -= P_vy
            P_vy -= 1
            if P_vy < -20:
                jump = False
                P_vy = 20
        rel_x = x % bgW
        screen.blit(bg, (rel_x - bgW, 0))
        if rel_x < 800:
            screen.blit(bg, (rel_x, 0))
        x -= 7
        P_x += P_vx
        lives()
        Player(P_x, P_y)
        if k[K_x]:
            if arrow_state == "ready":
                arrowSound = pygame.mixer.Sound("Arrow+Swoosh+1.wav")
                arrowSound.play()
                arrow_in_quiver -= 1
                a_x = P_x
                a_y = P_y
                fireSingle(a_x, a_y)
                if arrow_in_quiver<=0 and score<5*refill:
                    font1 = pygame.font.SysFont("Segoe Bold", 100)
                    game = font1.render("NO ARROWS LEFT", True, (23, 0, 99))
                    screen.blit(game, (100, 200))
                    pygame.display.update()
                    over = pygame.mixer.Sound("gameover.wav")
                    over.play()
                    time.sleep(3)
                    break
        if arrow_state == "fire":
            fireSingle(a_x, a_y)
            a_x += a_vx
            if a_x > 800:
                arrow_state = "ready"
        if k[K_z]:
            if Marrow_state == "ready":
                arrowSound = pygame.mixer.Sound("Arrow+Swoosh+1.wav")
                arrowSound.play()
                arrow_in_quiver -= 1
                Ma_x = P_x
                Ma_y = P_y
                fireMultiple(Ma_x, Ma_y)
                if arrow_in_quiver<=0 and score<5*refill:
                    font1 = pygame.font.SysFont("Segoe Bold", 100)
                    game = font1.render("NO ARROWS LEFT", True, (23, 0, 99))
                    screen.blit(game, (100, 200))
                    pygame.display.update()
                    over = pygame.mixer.Sound("gameover.wav")
                    over.play()
                    time.sleep(3)
                    break
        if Marrow_state == "fire":
            fireMultiple(Ma_x, Ma_y)
            Ma_x += Ma_vx
            if Ma_x > 800:
                Marrow_state = "ready"

        for i in range(2):
            Enemies(dragonX[i],dragonY[i])
            dragonX[i]+=X_change
            if dragonX[i]<-200:
                dragonX[i]=900+(i * 600)
            if collisionP(P_x, P_y, dragonX[i],dragonY[i]):
                life -= 1
                lost = pygame.mixer.Sound("life.wav")
                lost.play()
                dragonX[i] = 900 + (i * 600)
                break
            if arrow_state=="fire":
                if collisionA(a_x,a_y,dragonX[i],dragonY[i]):
                    if a_x<800:
                        score+=1
                        dragonX[i]=900+(i*600)
                        a_x = 801
                        arrow_state="ready"
            if Marrow_state=="fire":
                if collisionA(Ma_x,Ma_y,dragonX[i],dragonY[i]):
                    if Ma_x<800:
                        score+=1
                        dragonX[i]=900+(i*600)
                        Ma_x = 801
                        Marrow_state="ready"
            if score == 5 * refill:
                refill += 1
                arrow_in_quiver += 5
    else:
        font1 = pygame.font.SysFont("Segoe Bold", 150)
        game = font1.render("GAME OVER", True, (23, 0, 99))
        screen.blit(game, (100, 200))
        pygame.display.update()
        over = pygame.mixer.Sound("gameover.wav")
        over.play()
        time.sleep(3)
        break
    pygame.display.update()
    pygame.time.delay(30)
    clk.tick(FPS)
