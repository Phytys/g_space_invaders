import random
import math
import pygame
from pygame import mixer

### Thanks to Free Code Camp for great tutorials ###

# Initialize pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

# Adding background image
background = pygame.image.load("space_background.png")

# Background sound
mixer.music.load("Reggae-instrumental-music-85-bpm.mp3")
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Glenns Space Invaders")
icon = pygame.image.load("spaceship_2.png")
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load("spaceship_3.png").convert_alpha()
playerX = 370
playerY = 480
playerX_change = 0

# EnemyBoss
enemyBossImg = pygame.image.load("enemy_boss.png").convert_alpha()
enemyBossX   = 0
enemyBossY   = 50
enemyBossX_change = 5
enemyBossY_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 8

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("enemy.png").convert_alpha())
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(2)
    enemyY_change.append(40)
  
# Bullet
# State "ready" means cant see it (fire means it moving)
bulletImg = pygame.image.load("bullet.png").convert_alpha()
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 12
bullet_state = "ready" 

# Score
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)
textX = 10
textY = 10

# Help Functions

def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255,255,255))
    screen.blit(score, (x, y))

def player(x,y):
    screen.blit(playerImg, (x, y))

def enemyBoss(x,y):
    screen.blit(enemyBossImg, (x, y))

def enemy(x,y,i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg,(x + 16, y + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX-bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if distance < 27:
        return True
    else:
        return False


### Game Loop ###

running = True
while running:

    screen.fill((0,10,25))
    # Background image
    screen.blit(background, (0,0))

    for event in pygame.event.get():
        if event.type  ==  pygame.QUIT:
            running = False

        # If keystroke is pressed, check if its left or right
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -4
            if event.key == pygame.K_RIGHT:
                playerX_change = 4
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_Sound = mixer.Sound("laser.wav")
                    bullet_Sound.play()
                    # Get current x coordinates of spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Checking for screen boundaries of spaceships (so it dosnt move outside window)
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy Boss movement
    enemyBossX += enemyBossX_change

    if enemyBossX <= 0:
        enemyBossX_change = 5
    elif enemyBossX >= 736:
        enemyBossX_change = -5

    # Collision EnemyBoss (shooting down enemy boss and get big score)
    collisionEnemyBoss = isCollision(enemyBossX, enemyBossY, bulletX, bulletY)
    if collisionEnemyBoss:
        explosion_Sound = mixer.Sound("explosion.wav")
        explosion_Sound.play()
        bulletY  = 480
        bullet_state = "ready"
        score_value += 100
        enemyBossX = 0

    enemyBoss(enemyBossX, enemyBossY)

    # Enemy movement (many enemies)
    for i in range(num_of_enemies):
        enemyX[i] += enemyX_change[i]

        # Game Over
        if enemyY[i] >= 440:
            game_over = font.render("GAME OVER", True, (255,255,255))
            screen.blit(game_over, (300, 400))
            # Removing enemys from screen after game over
            enemyBossY = 2000
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            break

        if enemyX[i] <= 0:
            enemyX_change[i] = 3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -3
            enemyY[i] += enemyY_change[i]

        # Collision Enemy (shooting down enemies and get scores)
        collisionEnemy = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collisionEnemy:
            explosion_Sound = mixer.Sound("explosion.wav")
            explosion_Sound.play()
            bulletY  = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0,735)
            enemyY[i] = random.randint(50,150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet movement
    if bulletY <=0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change


    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()

