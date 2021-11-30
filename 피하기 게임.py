import pygame
from pygame.rect import *
import random

def restart():
    global isGameOver, score
    isGameOver = False
    score = 0
    for i in range(len(bomb)):
        recBomb[i].y = -1

#배경
background=pygame.image.load("C:/Users/user/OneDrive/바탕 화면/bg.png")

def eventProcess():
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()

            if event.key == pygame.K_LEFT:
                move.x = -1
            if event.key == pygame.K_RIGHT:
                move.x = 1
            if event.key == pygame.K_UP:
                move.y = -1
            if event.key == pygame.K_DOWN:
                move.y = 1
            if event.key == pygame.K_r:
                restart()
    SCREEN.fill((0, 0, 255))
    SCREEN.blit(background, (0, 0))
###################################################################
###################################################################
def movePlayer():
    if not isGameOver:
        recPlayer.x += move.x
        recPlayer.y += move.y
    if recPlayer.x < 0:
        recPlayer.x = 0
    if recPlayer.x > SCREEN_WIDTH-recPlayer.width:
        recPlayer.x = SCREEN_WIDTH-recPlayer.width
    if recPlayer.y < 0:
        recPlayer.y = 0
    if recPlayer.y > SCREEN_HEIGHT-recPlayer.height:
        recPlayer.y = SCREEN_HEIGHT-recPlayer.height        
    SCREEN.blit(player, recPlayer)
###################################################################
###################################################################
def timeDelay500ms():
    global time_delay_500ms
    if time_delay_500ms > 5:
        time_delay_500ms = 0
        return True    
    time_delay_500ms += 1
    return False
    
def makeBomb():
    if isGameOver:
        return
    if timeDelay500ms():
        idex = random.randint(0, len(bomb)-1)
        if recBomb[idex].y == -1:
            recBomb[idex].x = random.randint(0, SCREEN_WIDTH)
            recBomb[idex].y = 0

def moveBomb():
    makeBomb()
    for i in range(len(bomb)):
        if recBomb[i].y == -1:
            continue
        if not isGameOver:
            recBomb[i].y += 1
        if recBomb[i].y > SCREEN_HEIGHT:
            recBomb[i].y = 0
        SCREEN.blit(bomb[i], recBomb[i])

def makeLove():
    if isGameOver:
        return
    if timeDelay500ms():
        idex = random.randint(0, len(love)-1)
        if recLove[idex].y == -1:
            recLove[idex].x = random.randint(0, SCREEN_WIDTH)
            recLove[idex].y = 0

def moveLove():
    makeLove()
    for i in range(len(love)):
        if recLove[i].y == -1:
            continue
        if not isGameOver:
            recLove[i].y += 1
        if recLove[i].y > SCREEN_HEIGHT:
            recLove[i].y = 0
        SCREEN.blit(love[i], recLove[i])

###################################################################
###################################################################
def CheckCollision():   
    global score, isGameOver
    if isGameOver:
        return
    for rec in recBomb:
        if rec.y == -1:
            continue
        if rec.top < recPlayer.bottom \
            and recPlayer.top < rec.bottom \
            and rec.left < recPlayer.right \
            and recPlayer.left < rec.right:
            print('충돌')
            isGameOver = True
            break
    score += 1
###################################################################
###################################################################
def blinking():
    global time_dealy_4sec, toggle
    time_dealy_4sec += 1
    if time_dealy_4sec > 40:
        time_dealy_4sec = 0
        toggle = ~toggle    
    return toggle

def setText():
    mFont = pygame.font.SysFont("arial",20, True, False)
    SCREEN.blit(mFont.render(
        f'score : {score}', True, 'green'), (10, 10, 0, 0))

    if isGameOver and blinking():
        SCREEN.blit(mFont.render(
            'Game Over!!', True, 'red'), (80, 60, 0, 0))
        SCREEN.blit(mFont.render(
            'press R - Restart', True, 'red'), (14, 32, 0, 0))
###################################################################
###################################################################
#1.변수초기화
isActive = True
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 350
move = Rect(0,0,0,0)
time_delay_500ms = 0
time_dealy_4sec = 0
toggle = False
score = 0
isGameOver = False

#2.스크린생성
pygame.init()
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('피하기 게임')

#3. player 생성
player = pygame.image.load('person.png')
player = pygame.transform.scale(player,(50,50))
recPlayer = player.get_rect()
recPlayer.centerx = (SCREEN_WIDTH/2)
recPlayer.centery = (SCREEN_HEIGHT/2)
#4. 폭탄 생성
bomb = [pygame.image.load('bomb.png') for i in range(40)]
recBomb = [None for i in range(len(bomb))]
for i in range(len(bomb)):
    bomb[i] = pygame.transform.scale(bomb[i], (22, 22))
    recBomb[i] = bomb[i].get_rect()
    recBomb[i].y = -1

love = [pygame.image.load('love.png') for i in range(40)]
recLove = [None for i in range(len(love))]
for i in range(len(love)):
    love[i] = pygame.transform.scale(love[i], (22, 22))
    recLove[i] = love[i].get_rect()
    recLove[i].y = -1

    
#5. 기타
clock = pygame.time.Clock()

#####반복####
while isActive:
    #1.화면 지움
    SCREEN.fill((0,0,0))
    #2.이벤트처리
    eventProcess()
    #3.플레이어 이동
    movePlayer()
    #4.폭탄 생성 및 이동
    moveBomb()
    moveLove()
    #5.충돌 확인
    CheckCollision()
    #6.text업데이트
    setText()
    #7.화면 갱신
    pygame.display.flip()
    clock.tick(100)
