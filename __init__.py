# https://vignette.wikia.nocookie.net/metalgear/images/6/64/Wakh.jpg/revision/latest?cb=20150924235431
# Commander in tutorial, Modified using photoshop

# https://d2v9y0dukr6mq2.cloudfront.net/video/thumbnail/0kjHIH6/fireflies-flying-on-a-starry-night-background_s-ydiobue_thumbnail-full01.png
# background of game/tutorial/challenge. dimensions modified using photoshop

# Buttons/texts created using cooltext.com

# Enemy bullet/player bullet, By Master484
# http://m484games.ucoz.com/

# laser attack animation from netcake3, https://opengameart.org/content/laser-effect-sheet
# Enemy ship taken from https://opengameart.org/content/space-ship-construction-kit, by Skorpio
# Explosion effects from player bomb taken from Skorpio's scifi effect set, "explosions".

# Player ship By MillionthVector (http://millionthvector.blogspot.de)
# This work has been released under the Creative Commons BY License: https://creativecommons.org/licenses/by/4.0/
# Modified for ship display while invincible

# Repair powerup taken from https://longfordpc.com/images/wrench-clipart-gear-wrench-6.png,
# Modified into green color using photoshop
# Player bomb icon taken from open2dArt by samoliver

# Sound effect credits:
# Player bullet sound taken from soundbible.com, under License Attribution 3.0
# Enemy explosion sound taken from Michel Baradari,"http://www.cubeengine.com/forum.php4?action=display_thread&thread_id=2164"
# Player bomb sound effect taken from Iwan Gabovitch, https://opengameart.org/content/rumbleexplosion
# Background Music "Dystopic-Mayhem", "Trashy-Aliens", "Automation", "And-the-Machines-Came-at-Midnight" by Eric Matyas from www.soundimage.org

# This file contains the main game function, title screen, and tutorial etc.

import pygame
import os
import sys
import random
import cv2
import time
import numpy as np
import imutils
import copy
from Classes import *
from Levels import levelConstructor,randomEnemy

windowWidth = 600
windowHeight = 800
window = pygame.display.set_mode((windowWidth,windowHeight))
clock = pygame.time.Clock()
gameSpeed = 30

pygame.mixer.init()

pygame.font.init()
hpFont = pygame.font.SysFont('Comic Sans MS', 30)

def spawn(enemyGroup,levels,curLevelProgress,teamEnemyGroup):
    level = curLevelProgress[0]
    curLevel = levels[level-1]
    levelProgress = curLevelProgress[1]
    #Level is the level object, progress is an interger for indexing into list
    
        #Spawn for the last time and return level += 1, set progress to 0
    numSpawn = curLevel.spawnAmount[levelProgress]
    for i in range(numSpawn):

        enemySpec = curLevel.enemyList[levelProgress]
        enemyType = enemySpec[0]
        if enemyType == "Normal":
            curEnemy = Enemy(enemySpec[1],enemySpec[2],enemySpec[3],
                enemySpec[4],enemySpec[5],random.randint(i*windowWidth/numSpawn,
                                                    (i+1)*windowWidth/numSpawn))
            enemyGroup.add(curEnemy)
        elif enemyType == "Moving":
            curEnemy = MoveEnemy(enemySpec[1],enemySpec[2],enemySpec[3],
                enemySpec[4],enemySpec[5],
                random.randint(i*(windowWidth-100)/numSpawn+50,
                                        (i+1)*(windowWidth-100)/numSpawn)-50)
            enemyGroup.add(curEnemy)
        elif enemyType == "MiniBoss":
            curEnemy = MiniBoss1(enemySpec[1],enemySpec[2],
                                    enemySpec[3],enemySpec[4],enemySpec[5])
            enemyGroup.add(curEnemy)
        elif enemyType == "Team":
            curEnemy = TeamEnemy(enemySpec[1])
            teamEnemyGroup.add(curEnemy)
        elif enemyType == "Boss":
            curEnemy = Boss(enemySpec[1])
            enemyGroup.add(curEnemy)
    if levelProgress == len(curLevel.enemyList)-1:
        return (curLevel.spawnWait[levelProgress],(level+1,0))
    else:
        return (curLevel.spawnWait[levelProgress],(level,levelProgress+1))
        
def spawnPowerUp(player,powerUpGroup,enemyPos):
    powerUpType = random.choice(["repair","bomb"])
    if powerUpType == "repair":
        repair = Repair(enemyPos[0],enemyPos[1])
        powerUpGroup.add(repair)
    if powerUpType == "bomb":
        bomb = BombDrop(enemyPos[0],enemyPos[1])
        powerUpGroup.add(bomb)
    
def explode(x,y,scale,explosionGroup):
    curExplosion = Explosion(x,y,scale)
    explosionGroup.add(curExplosion)

###Main game
def titleScreen():
    time.sleep(0.2)
    pygame.mixer.music.load(os.path.join('Assets','Sound','Trashy-Aliens.mp3'))
    pygame.mixer.music.play(-1)
    bgGroup = pygame.sprite.Group()
    bgGroup.add(Background("TitleScreen.png"))
    buttonGroup = pygame.sprite.Group()
    buttonGroup.add(Button(windowWidth//2, windowHeight//2 - 50,
                "StartGame.png","StartGame2.png",CVShooter))
    buttonGroup.add(Button(windowWidth//2,windowHeight//2 + 30 ,
                                    "Tutorial.png","Tutorial2.png",tutorial))
    buttonGroup.add(Button(windowWidth//2,windowHeight//2 + 110,
                                    "Challenge.png","Challenge2.png",challenge))
    buttonGroup.add(Button(windowWidth//2,windowHeight//2 + 190,
                                    "InfiniteMode.png","InfiniteMode2.png",infiniteMode))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        for button in buttonGroup:
            button.update(mouse,click)
        window.fill((0,0,0))
        bgGroup.draw(window)
        buttonGroup.draw(window)
        pygame.display.update()
    return
def winScreen(score):
    bgGroup = pygame.sprite.Group()
    bgGroup.add(Background("WinScreen.png"))
    buttonGroup = pygame.sprite.Group()
    buttonGroup.add(Button(windowWidth//2, windowHeight//2 + 100,
                "Restart.png","Restart2.png",CVShooter))
    buttonGroup.add(Button(windowWidth//2,windowHeight//2 + 200,
                            "ReturnToTitle.png","ReturnToTitle2.png",titleScreen))
    score = hpFont.render("Score: %d" %(score), False, (255,255,255))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        for button in buttonGroup:
            button.update(mouse,click)
        window.fill((0,0,0))
        bgGroup.draw(window)
        window.blit(score,(225,700))
        buttonGroup.draw(window)
        pygame.display.update()
    return
def loseScreen(score):
    score = hpFont.render("Score: %d" %(score), False, (255,255,255))
    bgGroup = pygame.sprite.Group()
    bgGroup.add(Background("LoseScreen.png"))
    buttonGroup = pygame.sprite.Group()
    buttonGroup.add(Button(windowWidth//2, windowHeight//2 + 100,
                "Restart.png","Restart2.png",CVShooter))
    buttonGroup.add(Button(windowWidth//2,windowHeight//2 + 200,
                        "ReturnToTitle.png","ReturnToTitle2.png",titleScreen))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        for button in buttonGroup:
            button.update(mouse,click)
        window.fill((0,0,0))
        bgGroup.draw(window)
        window.blit(score,(225,700))
        buttonGroup.draw(window)
        pygame.display.update()
    return
def endInfinite(score):
    score = hpFont.render("Score: %d" %(score), False, (255,255,255))
    bgGroup = pygame.sprite.Group()
    bgGroup.add(Background("endInfinite.png"))
    buttonGroup = pygame.sprite.Group()
    buttonGroup.add(Button(windowWidth//2, windowHeight//2 + 100,
                "Restart.png","Restart2.png",infiniteMode))
    buttonGroup.add(Button(windowWidth//2,windowHeight//2 + 200,
                        "ReturnToTitle.png","ReturnToTitle2.png",titleScreen))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        for button in buttonGroup:
            button.update(mouse,click)
        window.fill((0,0,0))
        bgGroup.draw(window)
        window.blit(score,(225,700))
        buttonGroup.draw(window)
        pygame.display.update()
    return
def challenge():
    pygame.mixer.music.load(os.path.join('Assets','Sound','And-the-Machines-Came-at-Midnight.mp3'))
    pygame.mixer.music.play(-1)
    video = cv2.VideoCapture(0)
    challenging = True
    playerSpriteGroup = pygame.sprite.Group() 
    player = Player(windowWidth//2,windowHeight - 80)
    playerSpriteGroup.add(player)
    playerBulletGroup = pygame.sprite.Group()
    enemyGroup = pygame.sprite.Group()
    enemyBulletGroup = pygame.sprite.Group()
    explosionGroup = pygame.sprite.Group()
    backgroundGroup = pygame.sprite.Group()
    background = Background("Background.png")
    backgroundGroup.add(background)
    shootInterval = 35
    timeUntilShoot = shootInterval
    challengeBoss = SmartBoss()
    enemyGroup.add(challengeBoss)
    while challenging:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                video.release()
                cv2.destroyAllWindows()
                return
        ##Code adapted from https://docs.opencv.org/3.4/df/d9d/tutorial_py_colorspaces.html
        ##For changing color space and masking
        check, frame = video.read()
        frame = imutils.resize(frame, width=600)
        #Mirrors the frame
        frame = cv2.flip(frame,1)
        blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        lowerRed = np.array([100,150,125])
        higherRed = np.array([120,255,200])
        
        csv = cv2.cvtColor(blurred,cv2.COLOR_RGB2HSV)
        mask = cv2.inRange(csv,lowerRed,higherRed)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        ## Finding contour, code adapted from https://www.pyimagesearch.com/2015/09/14/ball-tracking-with-opencv/
        # find contours in the mask and initialize the current
        # (x, y) center of the ball
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        center = None
    
        # only proceed if at least one contour was found
        if len(cnts) > 0:
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and
            # centroid
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            # only proceed if the radius meets a minimum size
            if radius > 10:
                # draw the circle and centroid on the frame,
                # then update the list of tracked points
                cv2.circle(frame, (int(x), int(y)), int(radius),
                    (0, 255, 255), 2)
                cv2.circle(frame, center, 5, (0, 0, 255), -1)
        
        if center != None:
            if center[0]>=350 and player.rect.right < windowWidth:
                player.rect.centerx += player.velocity
            elif center[0]<=250 and player.rect.left > 0:
                player.rect.centerx -= player.velocity

        cv2.line(frame, (250,0), (250,600), (0,255,0),2)
        cv2.line(frame, (350,0), (350,600), (0,255,0),2)
        cv2.imshow("Webcam",frame)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_t]:
            player.powerLevel = 3
        if keys[pygame.K_d]:
            player.health -= 1
        if keys[pygame.K_RIGHT] and player.rect.right <= windowWidth:
            player.rect.centerx += 5
        if keys[pygame.K_LEFT] and player.rect.left >= 0:
            player.rect.centerx -= 5
        if keys[pygame.K_h]:
            player.health += 1
        if keys[pygame.K_u]:
            for enemy in enemyGroup:
                enemy.tempo -= 1
        if timeUntilShoot <= 0 and challenging:
            player.shoot(playerBulletGroup,"Challenge")
            timeUntilShoot = shootInterval
        else:
            timeUntilShoot -= 1
        player.update(enemyBulletGroup)
        for bullet in playerBulletGroup:
            if isinstance(bullet,SplitBullet):
                bullet.move(enemyBulletGroup)
            bullet.move()
            if bullet.rect.bottom <= 0:
                playerBulletGroup.remove(bullet)
            for enemy in enemyGroup:
                if enemy.rect.colliderect(bullet.rect):
                    enemy.health -= 1
                    print("hit")
                    playerBulletGroup.remove(bullet)
        for enemy in enemyGroup:
            enemy.update(playerBulletGroup,enemyBulletGroup,player)
            enemy.move(player)
            enemy.shoot(player,enemyBulletGroup)
            score = enemy.score
        for bullet in enemyBulletGroup:
            if isinstance(bullet,HomingBullet):
                if bullet.move(player):
                    enemyBulletGroup.remove(bullet)
            elif isinstance(bullet,SplitBullet):
                bullet.move(enemyBulletGroup)
            else:
                bullet.move()
            if bullet.rect.colliderect(player.rect):
                if not player.invincible:
                    player.health -= 1
                    player.invincible = True
                    player.invincibleTimer = 8
                enemyBulletGroup.remove(bullet)
        if player.health <= 0:
            challenging = False
        window.fill((0,0,0))
        
        backgroundGroup.draw(window)
        playerSpriteGroup.draw(window)
        enemyGroup.draw(window)
        enemyBulletGroup.draw(window)
        playerBulletGroup.draw(window)
        playerHP = hpFont.render("Health: "+ str(player.health),False, (255,255,255))
        window.blit(playerHP,(20,windowHeight-50))
        challengeScore = hpFont.render("Score: "+ str(score),False, (255,255,255))
        window.blit(challengeScore,(400,windowHeight-50))
        pygame.display.update()
    video.release()
    cv2.destroyAllWindows()
    pygame.mixer.music.stop()
    challengeEnd(score)
    #Challenge End screen or something
    return
    
def challengeEnd(score):
    bgGroup = pygame.sprite.Group()
    bgGroup.add(Background("ChallengeEnd.png"))
    buttonGroup = pygame.sprite.Group()
    buttonGroup.add(Button(windowWidth//2, windowHeight//2 + 100,
                "Restart.png","Restart2.png",challenge))
    buttonGroup.add(Button(windowWidth//2,windowHeight//2 + 200,
                            "ReturnToTitle.png","ReturnToTitle2.png",titleScreen))
    score = hpFont.render("Score: %d" %(score), False, (255,255,255))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        for button in buttonGroup:
            execute = button.update(mouse,click)
        if execute!=None:
            execute()
        window.fill((0,0,0))
        bgGroup.draw(window)
        window.blit(score,(225,700))
        buttonGroup.draw(window)
        pygame.display.update()
    return

def tutorial():
    pygame.mixer.music.load(os.path.join('Assets','Sound','Dystopic-Mayhem.mp3'))
    pygame.mixer.music.play(-1)
    video = cv2.VideoCapture(0)
    teaching = True
    playerSpriteGroup = pygame.sprite.Group() 
    player = Player(windowWidth//2,windowHeight - 80)
    playerSpriteGroup.add(player)
    backgroundGroup = pygame.sprite.Group()
    background = Background("TutorialBG.png")
    backgroundGroup.add(background)
    while teaching:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                video.release()
                cv2.destroyAllWindows()
                return
        ##Code adapted from https://docs.opencv.org/3.4/df/d9d/tutorial_py_colorspaces.html
        ##For changing color space and masking
        check, frame = video.read()
        frame = imutils.resize(frame, width=600)
        #Mirrors the frame
        frame = cv2.flip(frame,1)
        blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        lowerRed = np.array([100,150,125])
        higherRed = np.array([120,255,200])
    
        
        csv = cv2.cvtColor(blurred,cv2.COLOR_RGB2HSV)
        mask = cv2.inRange(csv,lowerRed,higherRed)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        ## Finding contour, code adapted from https://www.pyimagesearch.com/2015/09/14/ball-tracking-with-opencv/
        # find contours in the mask and initialize the current
        # (x, y) center of the ball
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        center = None
    
        # only proceed if at least one contour was found
        if len(cnts) > 0:
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and
            # centroid
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            # only proceed if the radius meets a minimum size
            if radius > 10:
                # draw the circle and centroid on the frame,
                # then update the list of tracked points
                cv2.circle(frame, (int(x), int(y)), int(radius),
                    (0, 255, 255), 2)
                cv2.circle(frame, center, 5, (0, 0, 255), -1)
        
        if center != None:
            if center[0]>=350 and player.rect.right < windowWidth:
                player.rect.centerx += player.velocity
            elif center[0]<=250 and player.rect.left > 0:
                player.rect.centerx -= player.velocity
            if center[1] >= 250 and player.rect.bottom <= windowHeight:
                player.rect.centery += player.velocity
            elif center[1] <= 175 and player.rect.top >= 0:
                player.rect.centery -= player.velocity
        cv2.line(frame, (250,0), (250,600), (0,255,0),2)
        cv2.line(frame, (350,0), (350,600), (0,255,0),2)
        cv2.line(frame, (0,250), (600,250), (0,255,0),2)
        cv2.line(frame, (0,175), (600,175), (0,255,0),2)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, 'Left', (50,225), font, 1, (0, 255, 0), 1, cv2.LINE_AA)
        cv2.putText(frame, 'Left-Up', (25,100), font, 1, (0, 255, 0), 1, cv2.LINE_AA)
        cv2.putText(frame, 'Right', (500,225), font, 1, (0, 255, 0), 1, cv2.LINE_AA)
        cv2.putText(frame, 'Right-Up', (400,100), font, 1, (0, 255, 0), 1, cv2.LINE_AA)
        cv2.putText(frame, 'Right-Down', (400,350), font, 1, (0, 255, 0), 1, cv2.LINE_AA)
        cv2.putText(frame, 'Left-Up', (25,350), font, 1, (0, 255, 0), 1, cv2.LINE_AA)
        cv2.putText(frame, 'Up', (275,100), font, 1, (0, 255, 0), 1, cv2.LINE_AA)
        cv2.putText(frame, 'Down', (265,400), font, 1, (0, 255, 0), 1, cv2.LINE_AA)
        cv2.imshow("Webcame",frame)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            teaching = False
        if keys[pygame.K_LEFT] and player.rect.left > 0:
            player.rect.centerx -= player.velocity
        if keys[pygame.K_RIGHT] and player.rect.right < windowWidth:
            player.rect.centerx += player.velocity
        if keys[pygame.K_UP] and player.rect.top > 0:
            player.rect.centery -= player.velocity
        if keys[pygame.K_DOWN] and player.rect.bottom < windowHeight:
            player.rect.centery += player.velocity
        window.fill((0,0,0))
        backgroundGroup.draw(window)
        playerSpriteGroup.draw(window)
        pygame.display.update()
    pygame.mixer.music.stop()
    pygame.mixer.music.load(os.path.join('Assets','Sound','Trashy-Aliens.mp3'))
    pygame.mixer.music.play(-1)
    video.release()
    cv2.destroyAllWindows()
    return

def CVShooter():
    gameOver = False
    pygame.mixer.music.load(os.path.join('Assets','Sound','Automation.mp3'))
    pygame.mixer.music.play(-1)
    #Sprite Group for drawing player only
    playerSpriteGroup = pygame.sprite.Group() 
    player = Player(windowWidth//2,windowHeight - 80)
    playerSpriteGroup.add(player)
    bombGroup = pygame.sprite.Group()
    playerBulletGroup = pygame.sprite.Group()
    enemyGroup = pygame.sprite.Group()
    enemyBulletGroup = pygame.sprite.Group()
    preludeGroup = pygame.sprite.Group()
    explosionGroup = pygame.sprite.Group()
    powerUpGroup = pygame.sprite.Group()
    backgroundGroup = pygame.sprite.Group()
    teamEnemyGroup = pygame.sprite.Group()
    teamEnemyModeOfAction = ["Straight","Right","Left"]
    
    background = Background("Background.png")
    backgroundGroup.add(background)
    
    shootInterval = 10
    timeUntilShoot = shootInterval
    ## Wave control
    spawnInterval = 20
    # A list of Level Objects
    levels = levelConstructor()
    #This is a tuple of current level and the progress of the level.
    curLevelProgress = (1,0)
    
    #OpenCV setup
    video = cv2.VideoCapture(0)
    
    endTimer = 50
    levelEnd = False
    winTimer = 50
### Main Game
    while endTimer >= 0:
        background.move()
        spawnInterval -= 1
        
        ##handles spawning here
        if (spawnInterval <= 0) and curLevelProgress[0] <= len(levels) and not levelEnd:
            levelBefore = curLevelProgress[0]
            spawnInterval,curLevelProgress = spawn(enemyGroup,levels,
                                                    curLevelProgress,teamEnemyGroup)
            
            if curLevelProgress[0] > levelBefore:
                levelEnd = True
        elif curLevelProgress[0] > len(levels) and len(enemyGroup) == 0 and len(teamEnemyGroup) == 0:
            winTimer -= 1
            for bullet in enemyBulletGroup:
                if isinstance(bullet,Laser):
                    enemyBulletGroup.remove(bullet)
            if winTimer <= 0:
                print("Currently ended")
                video.release()
                cv2.destroyAllWindows()
                winScreen(player.exp + (player.powerLevel-1)*100)
                return
        if (len(enemyGroup) + len(teamEnemyGroup)) == 0:
            levelEnd = False
        window.fill((0,0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                video.release()
                cv2.destroyAllWindows()
                return
        ##Open CV part Start
        ##Code adapted from https://docs.opencv.org/3.4/df/d9d/tutorial_py_colorspaces.html
        ##For changing color space and masking
        check, frame = video.read()
        frame = imutils.resize(frame, width=600)
        #Mirrors the frame
        frame = cv2.flip(frame,1)
        blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        lowerRed = np.array([100,150,125])
        higherRed = np.array([120,255,200])
    
        csv = cv2.cvtColor(blurred,cv2.COLOR_RGB2HSV)
        mask = cv2.inRange(csv,lowerRed,higherRed)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        ## Finding contour, code adapted from https://www.pyimagesearch.com/2015/09/14/ball-tracking-with-opencv/
        # find contours in the mask and initialize the current
        # (x, y) center of the ball
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        center = None
    
        # only proceed if at least one contour was found
        if len(cnts) > 0:
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and
            # centroid
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            # only proceed if the radius meets a minimum size
            if radius > 10:
                # draw the circle and centroid on the frame,
                # then update the list of tracked points
                cv2.circle(frame, (int(x), int(y)), int(radius),
                    (0, 255, 255), 2)
                cv2.circle(frame, center, 5, (0, 0, 255), -1)
        ##Control player with opencv, original code
        if center != None:
            if center[0]>=350 and player.rect.right < windowWidth:
                player.rect.centerx += player.velocity
            elif center[0]<=250 and player.rect.left > 0:
                player.rect.centerx -= player.velocity
            if center[1] >= 250 and player.rect.bottom <= windowHeight:
                player.rect.centery += player.velocity
            elif center[1] <= 175 and player.rect.top >= 0:
                player.rect.centery -= player.velocity
        cv2.line(frame, (250,0), (250,600), (0,255,0),2)
        cv2.line(frame, (350,0), (350,600), (0,255,0),2)
        cv2.line(frame, (0,250), (600,250), (0,255,0),2)
        cv2.line(frame, (0,175), (600,175), (0,255,0),2)
        cv2.imshow("Webcame",frame)
        
        ##Open CV part end
        
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT] and player.rect.left > 0:
            player.rect.centerx -= player.velocity
        if keys[pygame.K_RIGHT] and player.rect.right < windowWidth:
            player.rect.centerx += player.velocity
        if keys[pygame.K_UP] and player.rect.top > 0:
            player.rect.centery -= player.velocity
        if keys[pygame.K_DOWN] and player.rect.bottom < windowHeight:
            player.rect.centery += player.velocity
        if keys[pygame.K_SPACE] and player.bombs > 0 and player.bombCD <= 0:
            bombGroup.add(Bomb())
            for bullet in enemyBulletGroup:
                enemyBulletGroup.remove(bullet)
            player.bombs -= 1
            player.bombCD = 50
        ### Debug features
        if keys[pygame.K_t]:
            player.exp+=10
            print(player.powerLevel)
        if keys[pygame.K_e]:
            enemyGroup.add(Enemy(3,10,20,"Enemy1.png",5))
        if keys[pygame.K_d]:
            player.health -= 1
        if keys[pygame.K_1]:
            curLevelProgress = (1,0)
            for enemy in enemyGroup:
                enemyGroup.remove(enemy)
            for enemy in teamEnemyGroup:
                teamEnemyGroup.remove(enemy)
        if keys[pygame.K_2]:
            curLevelProgress = (2,0)
            for enemy in enemyGroup:
                enemyGroup.remove(enemy)
            for enemy in teamEnemyGroup:
                teamEnemyGroup.remove(enemy)
        if keys[pygame.K_3]:
            curLevelProgress = (3,0)
            for enemy in enemyGroup:
                enemyGroup.remove(enemy)
            for enemy in teamEnemyGroup:
                teamEnemyGroup.remove(enemy)
        if keys[pygame.K_4]:
            curLevelProgress = (4,0)
            for enemy in enemyGroup:
                enemyGroup.remove(enemy)
            for enemy in teamEnemyGroup:
                teamEnemyGroup.remove(enemy)
        if keys[pygame.K_h]:
            player.health += 1
        if keys[pygame.K_b]:
            player.bombs += 1
        ### Debug feature end
        player.update(enemyBulletGroup)

        shootInterval = 15 - player.powerLevel
        if timeUntilShoot <= 0 and not gameOver:
            player.shoot(playerBulletGroup)
            timeUntilShoot = shootInterval
        else:
            timeUntilShoot -= 1
        ## Looping through items in groups to update game state
        for bullet in playerBulletGroup:
            bullet.move()
            if bullet.rect.bottom <= -10:
                playerBulletGroup.remove(bullet)
        for enemy in enemyGroup:
            enemy.move()
            enemy.update(player.performance)
            if isinstance(enemy,Boss):
                enemy.shoot(enemyBulletGroup,player,preludeGroup)
            else:
                enemy.shoot(enemyBulletGroup,player)
            if enemy.rect.top >= windowHeight + 5:
                enemyGroup.remove(enemy)
            for bullet in playerBulletGroup:
                if enemy.rect.colliderect(bullet.rect):
                    playerBulletGroup.remove(bullet)
                    enemy.health -= bullet.power
                    if enemy.health <= 0:
                        player.exp += enemy.exp
                        if (random.randint(int(player.performance),100) >= 80):
                            spawnPowerUp(player,powerUpGroup,enemy.rect.center)
                        explode(enemy.rect.centerx,enemy.rect.centery,
                                            enemy.rect.size,explosionGroup)
                        enemyGroup.remove(enemy)
            if enemy.rect.colliderect(player.rect):
                if player.invincible == False:
                    player.health-=1
                    player.invincible = True
                    player.invincibleTimer = 40
        for prelude in preludeGroup:
            for enemy in enemyGroup:
                if isinstance(enemy,Boss):
                    xLoc = enemy.rect.centerx
            if prelude.update(xLoc):
                preludeGroup.remove(prelude)
        for bullet in enemyBulletGroup:
            if isinstance(bullet,Laser):
                #do laser updates using the only enemy in enemySpriteGroup, the boss
                for enemy in enemyGroup:
                    if isinstance(enemy,Boss):
                        xLoc = enemy.rect.centerx
                if bullet.rect.colliderect(player.rect):
                    if player.invincible == False:
                        player.health-=1
                        player.invincible = True
                        player.invincibleTimer = 40
                #Equiv to laser.update()
                if bullet.update(xLoc):
                    enemyBulletGroup.remove(bullet)
            else:
                bullet.move()
                if bullet.rect.colliderect(player.rect):
                    if player.invincible == False:
                        player.health-=1
                        player.invincible = True
                        player.invincibleTimer = 50
                    enemyBulletGroup.remove(bullet)
                if bullet.rect.centerx >= windowWidth+10 or bullet.rect.centerx <= -10:
                    enemyBulletGroup.remove(bullet)
                if bullet.rect.centery >= windowHeight+10 or bullet.rect.centery <= -10:
                    enemyBulletGroup.remove(bullet)
        for powerUp in powerUpGroup:
            powerUp.move()
            if powerUp.rect.colliderect(player.rect):
                if isinstance(powerUp,Repair):
                    player.health += int(3 + player.performance//15)
                if isinstance(powerUp,BombDrop):
                    player.bombs += 1
                powerUpGroup.remove(powerUp)
        for bomb in bombGroup:
            if bomb.update():
                bombGroup.remove(bomb)
        teamCounter = 0
        teamEnemyModeOfAction = ["Straight","Right","Left"]
        for teamEnemy in teamEnemyGroup:
            memberLeft = len(teamEnemyGroup)
            if memberLeft <= 2:
                teamEnemy.shootInterval = 10
            teamEnemy.move()
            teamEnemy.shoot(enemyBulletGroup,teamEnemyModeOfAction[teamCounter%3],player)
            teamEnemy.update(player.performance)
            teamCounter += 1
            for bullet in playerBulletGroup:
                if teamEnemy.rect.colliderect(bullet.rect):
                    playerBulletGroup.remove(bullet)
                    teamEnemy.health -= bullet.power
                    if teamEnemy.health <= 0:
                        player.exp += teamEnemy.exp
                        if (random.randint(int(player.performance),100) >= 80):
                            spawnPowerUp(player,powerUpGroup,teamEnemy.rect.center)
                        explode(teamEnemy.rect.centerx,teamEnemy.rect.centery,
                                            teamEnemy.rect.size,explosionGroup)
                        teamEnemyGroup.remove(teamEnemy)
        for explosion in explosionGroup:
            if explosion.update():
                explosionGroup.remove(explosion)
        if player.health <= 0:
            #Explosion effect and gameOver screen
            if not gameOver:
                explode(player.rect.centerx,player.rect.centery,player.rect.size,explosionGroup)
            gameOver = True
            playerSpriteGroup.remove(player)
            endTimer -= 1
        ##Drawing and updating for sprite group
        backgroundGroup.draw(window)
        playerSpriteGroup.draw(window)
        playerBulletGroup.draw(window)
        enemyGroup.draw(window)
        teamEnemyGroup.draw(window)
        bombGroup.draw(window)
        enemyBulletGroup.draw(window)
        powerUpGroup.draw(window)
        preludeGroup.draw(window)
        explosionGroup.draw(window)
        ##Drawing UI, player health etc.
        for i in range(player.bombs):
            icon = pygame.transform.scale(pygame.image.load(os.path.join('Assets',
                        'PowerUps','bomb.png')).convert(),(12,30))
            icon.set_colorkey((255,255,255))
            window.blit(icon,(windowWidth//2 - 10*player.bombs + i*20,windowHeight - 40))
        playerHP = hpFont.render("Health: "+ str(player.health),False, (255,255,255))
        window.blit(playerHP,(20,windowHeight-50))
        if player.powerLevel == 3:
            playerEXP = hpFont.render("Max EXP",False, (255,255,255))
        else:
            playerEXP = hpFont.render("EXP: "+ str(player.exp) + "/100",
                                                    False, (255,255,255))
        window.blit(playerEXP,(420,windowHeight-50))
        pygame.display.update()
        clock.tick(gameSpeed)
    video.release()
    cv2.destroyAllWindows()
    pygame.mixer.music.stop()
    loseScreen(player.exp + (player.powerLevel-1)*100)
    return
def infiniteMode():
    gameOver = False
    pygame.mixer.music.load(os.path.join('Assets','Sound','Automation.mp3'))
    pygame.mixer.music.play(-1)
    #Sprite Group for drawing player only
    playerSpriteGroup = pygame.sprite.Group() 
    player = Player(windowWidth//2,windowHeight - 80)
    playerSpriteGroup.add(player)
    bombGroup = pygame.sprite.Group()
    playerBulletGroup = pygame.sprite.Group()
    enemyGroup = pygame.sprite.Group()
    enemyBulletGroup = pygame.sprite.Group()
    preludeGroup = pygame.sprite.Group()
    explosionGroup = pygame.sprite.Group()
    powerUpGroup = pygame.sprite.Group()
    backgroundGroup = pygame.sprite.Group()
    teamEnemyGroup = pygame.sprite.Group()
    teamEnemyModeOfAction = ["Straight","Right","Left"]
    
    background = Background("Background.png")
    backgroundGroup.add(background)
    
    shootInterval = 10
    timeUntilShoot = shootInterval
    ## Wave control
    spawnInterval = 20
    # A list of Level Objects
    #This is a tuple of current level and the progress of the level.
    
    #OpenCV setup
    video = cv2.VideoCapture(0)
    
    endTimer = 50
    levelEnd = False
    winTimer = 50
### Main Game
    while endTimer >= 0:
        background.move()
        spawnInterval -= 1
        
        ##handles spawning here
        if (spawnInterval <= 0) or len(enemyGroup) == 0:
            enemyToSpawn,spawnInterval = randomEnemy()
            spawnInterval/=(player.powerLevel/2)
            enemyGroup.add(enemyToSpawn)
        window.fill((0,0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                video.release()
                cv2.destroyAllWindows()
                return
        ##Open CV part Start
        ##Code adapted from https://docs.opencv.org/3.4/df/d9d/tutorial_py_colorspaces.html
        ##For changing color space and masking
        check, frame = video.read()
        frame = imutils.resize(frame, width=600)
        #Mirrors the frame
        frame = cv2.flip(frame,1)
        blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        lowerRed = np.array([100,150,125])
        higherRed = np.array([120,255,200])
    
        csv = cv2.cvtColor(blurred,cv2.COLOR_RGB2HSV)
        mask = cv2.inRange(csv,lowerRed,higherRed)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        ## Finding contour, code adapted from https://www.pyimagesearch.com/2015/09/14/ball-tracking-with-opencv/
        # find contours in the mask and initialize the current
        # (x, y) center of the ball
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        center = None
    
        # only proceed if at least one contour was found
        if len(cnts) > 0:
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and
            # centroid
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            # only proceed if the radius meets a minimum size
            if radius > 10:
                # draw the circle and centroid on the frame,
                # then update the list of tracked points
                cv2.circle(frame, (int(x), int(y)), int(radius),
                    (0, 255, 255), 2)
                cv2.circle(frame, center, 5, (0, 0, 255), -1)
        ##Control player with opencv, original code
        if center != None:
            if center[0]>=350 and player.rect.right < windowWidth:
                player.rect.centerx += player.velocity
            elif center[0]<=250 and player.rect.left > 0:
                player.rect.centerx -= player.velocity
            if center[1] >= 250 and player.rect.bottom <= windowHeight:
                player.rect.centery += player.velocity
            elif center[1] <= 175 and player.rect.top >= 0:
                player.rect.centery -= player.velocity
        cv2.line(frame, (250,0), (250,600), (0,255,0),2)
        cv2.line(frame, (350,0), (350,600), (0,255,0),2)
        cv2.line(frame, (0,250), (600,250), (0,255,0),2)
        cv2.line(frame, (0,175), (600,175), (0,255,0),2)
        cv2.imshow("Webcame",frame)
        
        ##Open CV part end
        
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT] and player.rect.left > 0:
            player.rect.centerx -= player.velocity
        if keys[pygame.K_RIGHT] and player.rect.right < windowWidth:
            player.rect.centerx += player.velocity
        if keys[pygame.K_UP] and player.rect.top > 0:
            player.rect.centery -= player.velocity
        if keys[pygame.K_DOWN] and player.rect.bottom < windowHeight:
            player.rect.centery += player.velocity
        if keys[pygame.K_SPACE] and player.bombs > 0 and player.bombCD <= 0:
            bombGroup.add(Bomb())
            for bullet in enemyBulletGroup:
                enemyBulletGroup.remove(bullet)
            player.bombs -= 1
            player.bombCD = 50
        ### Debug features
        if keys[pygame.K_t]:
            player.exp+=10
            print(player.powerLevel)
        if keys[pygame.K_e]:
            enemyGroup.add(Enemy(3,10,20,"Enemy1.png",5))
        if keys[pygame.K_d]:
            player.health -= 1
        if keys[pygame.K_1]:
            curLevelProgress = (1,0)
            for enemy in enemyGroup:
                enemyGroup.remove(enemy)
            for enemy in teamEnemyGroup:
                teamEnemyGroup.remove(enemy)
        if keys[pygame.K_2]:
            curLevelProgress = (2,0)
            for enemy in enemyGroup:
                enemyGroup.remove(enemy)
            for enemy in teamEnemyGroup:
                teamEnemyGroup.remove(enemy)
        if keys[pygame.K_3]:
            curLevelProgress = (3,0)
            for enemy in enemyGroup:
                enemyGroup.remove(enemy)
            for enemy in teamEnemyGroup:
                teamEnemyGroup.remove(enemy)
        if keys[pygame.K_4]:
            curLevelProgress = (4,0)
            for enemy in enemyGroup:
                enemyGroup.remove(enemy)
            for enemy in teamEnemyGroup:
                teamEnemyGroup.remove(enemy)
        if keys[pygame.K_h]:
            player.health += 1
        if keys[pygame.K_b]:
            player.bombs += 1
        ### Debug feature end
        player.update(enemyBulletGroup)

        shootInterval = 15 - player.powerLevel
        if timeUntilShoot <= 0 and not gameOver:
            player.shoot(playerBulletGroup)
            timeUntilShoot = shootInterval
        else:
            timeUntilShoot -= 1
        ## Looping through items in groups to update game state
        for bullet in playerBulletGroup:
            bullet.move()
            if bullet.rect.bottom <= -10:
                playerBulletGroup.remove(bullet)
        for enemy in enemyGroup:
            enemy.move()
            enemy.update(player.performance)
            if isinstance(enemy,Boss):
                enemy.shoot(enemyBulletGroup,player,preludeGroup)
            else:
                enemy.shoot(enemyBulletGroup,player)
            if enemy.rect.top >= windowHeight + 5:
                enemyGroup.remove(enemy)
            for bullet in playerBulletGroup:
                if enemy.rect.colliderect(bullet.rect):
                    playerBulletGroup.remove(bullet)
                    enemy.health -= bullet.power
                    if enemy.health <= 0:
                        player.exp += enemy.exp
                        if (random.randint(int(player.performance),100) >= 80):
                            spawnPowerUp(player,powerUpGroup,enemy.rect.center)
                        explode(enemy.rect.centerx,enemy.rect.centery,
                                            enemy.rect.size,explosionGroup)
                        enemyGroup.remove(enemy)
            if enemy.rect.colliderect(player.rect):
                if player.invincible == False:
                    player.health-=1
                    player.invincible = True
                    player.invincibleTimer = 40
        for prelude in preludeGroup:
            for enemy in enemyGroup:
                if isinstance(enemy,Boss):
                    xLoc = enemy.rect.centerx
            if prelude.update(xLoc):
                preludeGroup.remove(prelude)
        for bullet in enemyBulletGroup:
            if isinstance(bullet,Laser):
                #do laser updates using the only enemy in enemySpriteGroup, the boss
                for enemy in enemyGroup:
                    if isinstance(enemy,Boss):
                        xLoc = enemy.rect.centerx
                if bullet.rect.colliderect(player.rect):
                    if player.invincible == False:
                        player.health-=1
                        player.invincible = True
                        player.invincibleTimer = 40
                #Equiv to laser.update()
                if bullet.update(xLoc):
                    enemyBulletGroup.remove(bullet)
            else:
                bullet.move()
                if bullet.rect.colliderect(player.rect):
                    if player.invincible == False:
                        player.health-=1
                        player.invincible = True
                        player.invincibleTimer = 50
                    enemyBulletGroup.remove(bullet)
                if bullet.rect.centerx >= windowWidth+10 or bullet.rect.centerx <= -10:
                    enemyBulletGroup.remove(bullet)
                if bullet.rect.centery >= windowHeight+10 or bullet.rect.centery <= -10:
                    enemyBulletGroup.remove(bullet)
        for powerUp in powerUpGroup:
            powerUp.move()
            if powerUp.rect.colliderect(player.rect):
                if isinstance(powerUp,Repair):
                    player.health += int(3 + player.performance//15)
                if isinstance(powerUp,BombDrop):
                    player.bombs += 1
                powerUpGroup.remove(powerUp)
        for bomb in bombGroup:
            if bomb.update():
                bombGroup.remove(bomb)
        teamCounter = 0
        teamEnemyModeOfAction = ["Straight","Right","Left"]
        for teamEnemy in teamEnemyGroup:
            memberLeft = len(teamEnemyGroup)
            if memberLeft <= 2:
                teamEnemy.shootInterval = 10
            teamEnemy.move()
            teamEnemy.shoot(enemyBulletGroup,teamEnemyModeOfAction[teamCounter%3],player)
            teamEnemy.update(player.performance)
            teamCounter += 1
            for bullet in playerBulletGroup:
                if teamEnemy.rect.colliderect(bullet.rect):
                    playerBulletGroup.remove(bullet)
                    teamEnemy.health -= bullet.power
                    if teamEnemy.health <= 0:
                        player.exp += teamEnemy.exp
                        if (random.randint(int(player.performance),100) >= 80):
                            spawnPowerUp(player,powerUpGroup,teamEnemy.rect.center)
                        explode(teamEnemy.rect.centerx,teamEnemy.rect.centery,
                                            teamEnemy.rect.size,explosionGroup)
                        teamEnemyGroup.remove(teamEnemy)
        for explosion in explosionGroup:
            if explosion.update():
                explosionGroup.remove(explosion)
        if player.health <= 0:
            #Explosion effect and gameOver screen
            if not gameOver:
                explode(player.rect.centerx,player.rect.centery,player.rect.size,explosionGroup)
            gameOver = True
            playerSpriteGroup.remove(player)
            endTimer -= 1
        ##Drawing and updating for sprite group
        backgroundGroup.draw(window)
        playerSpriteGroup.draw(window)
        playerBulletGroup.draw(window)
        enemyGroup.draw(window)
        teamEnemyGroup.draw(window)
        bombGroup.draw(window)
        enemyBulletGroup.draw(window)
        powerUpGroup.draw(window)
        preludeGroup.draw(window)
        explosionGroup.draw(window)
        ##Drawing UI, player health etc.
        for i in range(player.bombs):
            icon = pygame.transform.scale(pygame.image.load(os.path.join('Assets',
                        'PowerUps','bomb.png')).convert(),(12,30))
            icon.set_colorkey((255,255,255))
            window.blit(icon,(windowWidth//2 - 10*player.bombs + i*20,windowHeight - 40))
        playerHP = hpFont.render("Health: "+ str(player.health),False, (255,255,255))
        window.blit(playerHP,(20,windowHeight-50))
        if player.powerLevel == 3:
            playerEXP = hpFont.render("Max EXP",False, (255,255,255))
        else:
            playerEXP = hpFont.render("EXP: "+ str(player.exp) + "/100",
                                                    False, (255,255,255))
        window.blit(playerEXP,(420,windowHeight-50))
        pygame.display.update()
        clock.tick(gameSpeed)
    video.release()
    cv2.destroyAllWindows()
    pygame.mixer.music.stop()
    endInfinite(player.exp + (player.powerLevel-1)*100)
    return
titleScreen()
