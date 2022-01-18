import pygame
import random
import math
from pygame import mixer


# initialize
pygame.init()

# create screen display
screen = pygame.display.set_mode((800, 600))

# title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

# background image
background = pygame.image.load('background.jpg')
# background sound
mixer.music.load('background.wav')
mixer.music.play(-1) # adding -1 will loop in the game
# score
score = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10
# gameover font
over_font = pygame.font.Font('freesansbold.ttf', 64)

# player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0
playerX_speed = 0.4

#enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png')) 
    enemyX.append(random.randint(64, 736))
    enemyY.append(random.randint(30, 50))
    enemyX_change.append(0.3)
    enemyY_change.append(40) 

#bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 5
bullet_state = "ready"


# move player
def player(x ,y):
    screen.blit(playerImg, (x, y))

def enemy(x ,y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y):  
    global bullet_state
    
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY,2)))
    if distance < 27:
        return True
    else:
        return False

def show_score(x, y):
    score_font = font.render("Score : " + str(score), True, (255, 255, 255))
    screen.blit(score_font, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER",True, (255, 255, 255))
    screen.blit(over_text, (200, 250))
# game loop
is_running = True
while is_running:
    # rgb for background
    screen.fill((192, 192, 192))
    # bg image
    screen.blit(background, (0, 0))
    #playerX += .1
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # game will run until you hit 'x' in the game window
            is_running = False

        #keystroke
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                playerX_change = - playerX_speed
            if event.key == pygame.K_d:
                playerX_change = playerX_speed
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                playerX_change = 0
            if event.key == pygame.K_d:
                playerX_change = 0 
    
    playerX += playerX_change 
    #boundaries
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    # bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= 3.5 # bullet speed
    # enemy movement
    for i in range(num_of_enemies):
        # game over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        
        # moving all enemies
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.5
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.5
            enemyY[i] += enemyY_change[i]

        # collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score += 1
            
            enemyX[i] = random.randint(64, 736)
            enemyY[i] = random.randint(30, 50)
    
        enemy(enemyX[i], enemyY[i], i)
    
    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
