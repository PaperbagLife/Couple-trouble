# This is a class file that contains the classes the main game will use
# The majority of the classes inherit from pygame's builtin sprite class

import pygame
import os
import random
import math

obstacles = ["airplane.png","bomb1.png","rock1.jpeg", "tree1.jpeg",
            "ufo.jpeg","car.png"]
obstacleScale = [(80,100),(100,100),(100,100),(100,100),(100,100),(50,100)]
obstacleVel = [15,0,0,0,15,8]

class Player(pygame.sprite.Sprite):
    #player ship, has a powerLevel for the bullets, which is leveled up through
    #gaining exp
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(os.path.join('Assets',
                                'Player','player.png')).convert()
        self.rect = self.image.get_rect()
        self.image.set_colorkey((102,204,255))
        self.rect.centerx = x
        self.rect.centery = y
        self.velocity = 16


def getScale(idx):
    return obstacleScale[idx]
    
class Obstacle(pygame.sprite.Sprite):
    #The obstacle class dropping from the sky.
    def __init__(self, x, idx, velocity = 10):
        pygame.sprite.Sprite.__init__(self)
        self.idx = idx
        self.image = pygame.transform.scale(pygame.image.load(os.path.join('Assets',
                        'Obstacles',obstacles[self.idx])).convert(), getScale(idx))
        self.rect = self.image.get_rect()
        self.image.set_colorkey((255,255,0))
        self.rect.centerx = x
        self.rect.bottom = 0
        self.velocity = velocity + obstacleVel[idx]
    def move(self):
        #return new top, in main should get rid of self based on self.top
        self.rect.centery += self.velocity
        return self.rect.top
    def collide(self,player):
        return self.rect.colliderect(player.rect)
    

class Background(pygame.sprite.Sprite):
    def __init__(self,filePath):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join('Assets',
                                        'Background',filePath)).convert()
        self.rect = self.image.get_rect()
        self.rect.left = 0
        self.rect.bottom = 800
    def move(self):
        self.rect.centery += 10
        if self.rect.top >= 0:
            self.rect.bottom = 800
        
        
class Button(pygame.sprite.Sprite):
    def __init__(self,x,y,filePath1,filePath2,action):
        pygame.sprite.Sprite.__init__(self)
        self.normalImage = pygame.image.load(os.path.join('Assets',
                                            'Background',filePath1)).convert()
        self.hoverImage = pygame.image.load(os.path.join('Assets',
                                            'Background',filePath2)).convert()
        self.image = pygame.image.load(os.path.join('Assets',
                                            'Background',filePath1)).convert()
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.action = action
        self.number = random.randint(1,100)
    def update(self,mousePos,click):
        
        if self.rect.left <= mousePos[0] <= self.rect.right and\
                            self.rect.top <= mousePos[1] <= self.rect.bottom:
            self.image = self.hoverImage
            if click[0]:
                print("click")
                self.action()
        else:
            self.image = self.normalImage
            
def getInterval(n):
    #return new interval update based on phase
    if n < 4:
        return 20
    return 100
    
    
class HeartBreak(pygame.sprite.Sprite):
    def __init__(self,x,y,scale):
        pygame.sprite.Sprite.__init__(self)
        exp0 = pygame.transform.scale(pygame.image.load(os.path.join('Assets','Player',
                            'Death','0.png')).convert(), scale)
        exp0.set_colorkey((102,204,255))
        exp1 = pygame.transform.scale(pygame.image.load(os.path.join('Assets','Player',
                            'Death','1.png')).convert(), scale)
        exp1.set_colorkey((102,204,255))
        exp2 = pygame.transform.scale(pygame.image.load(os.path.join('Assets','Player',
                            'Death','2.png')).convert(), scale)
        exp2.set_colorkey((102,204,255))
        exp3 = pygame.transform.scale(pygame.image.load(os.path.join('Assets','Player',
                            'Death','3.png')).convert(), scale)
        exp3.set_colorkey((102,204,255))
        self.images = [exp0,exp1,exp2,exp3]
        self.image = exp0
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.count = 0
        self.timeInt = 80
        self.xVel = 0
        self.yVel = 0
        self.calculated = False
        
    def update(self):
        if not self.calculated:
            if self.rect.centerx != 300:
                self.xVel = (300-self.rect.centerx)/50
            if self.rect.centery != 400:
                self.yVel = (400-self.rect.centery)/50
            self.calculated = True
        if self.count == 0:
            if self.rect.centerx < 298 or self.rect.centerx > 302:
                self.rect.centerx += self.xVel
            if self.rect.centery < 398 or self.rect.centery > 402:
                self.rect.centery += self.yVel
        self.timeInt -= 1
        if self.timeInt <= 0:
            self.count += 1
            self.timeInt = getInterval(self.count)
        if self.count < len(self.images):
            self.image = self.images[self.count]
        #Return True if it needs to be destroyed, ie reached the end of explosion
        return self.count == len(self.images)
        
class TitleScreen(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image1 = pygame.image.load(os.path.join('Assets',
                                        'Background','bg1.jpg')).convert()
        self.image0 = pygame.image.load(os.path.join('Assets',
                                        'Background','bg0.jpg')).convert()
        self.image = self.image1
        self.rect = self.image.get_rect()
        self.timer = 30
        self.toggle = False
    def update(self):
        if self.timer <= 0:
            self.toggle = not self.toggle
            if self.toggle:
                self.image = self.image1
            else:
                self.image = self.image0
            self.timer = 24
        self.timer -= 1
