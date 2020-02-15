# This is a class file that contains the classes the main game will use
# The majority of the classes inherit from pygame's builtin sprite class

import pygame
import os
import random
import math

obstacles = ["obs1.png"]

class Player(pygame.sprite.Sprite):
    #player ship, has a powerLevel for the bullets, which is leveled up through
    #gaining exp
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(os.path.join('Assets',
                                'Obstacles','tree.png')).convert()
        self.rect = self.image.get_rect()
        self.image.set_colorkey((255,239,16))
        self.rect.centerx = x
        self.rect.centery = y
        self.velocity = 16
        
class Obstacle(pygame.sprite.Sprite):
    #The obstacle class dropping from the sky.
    def __init__(self, x, idx, velocity = 10):
        pygame.sprite.Sprite.__init__(self)
        self.idx = idx
        self.image = pygame.image.load(os.path.join('Assets',
                        'Obstacles',obstacles[self.idx])).convert()
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = 0
        self.velocity = velocity
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
        self.rect.centery += 1
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
