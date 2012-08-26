import random

import pygame 
from global_stuff import *
from pygame.locals import *

class Turtle():
    # keep the basic (gray-colored) shell and body surfaces as class variables
    shellSurface = None
    bodySurfaces = None
    
    MAX_STAT = 99
    
    LEAF_TIME = 30
    
    def __init__(self,speed,agility,endurance):
        self.speed=speed
        self.agility=agility
        self.endurance=endurance
        
        self.isRacing = False
        
        colorList = ['#168016','#9E7718','#C0C040','#7A1256','#C0C080',
                       '#124F63','#709516','#1C296C','#9B1B18','#303030']
        colorList=map(pygame.Color,colorList)
        
        shellColor = colorList[int(len(colorList)*self.endurance/(1.0*self.MAX_STAT+1))]
        bodyColor = colorList[int(len(colorList)*self.agility/(1.0*self.MAX_STAT+1))]
                
        myShellSurface = self.shellSurface.copy()
        myShellSurface.fill(shellColor,None,BLEND_MULT)
        
        self.surfaces=range(4)
        for i in range(2):
             self.surfaces[i]=self.bodySurfaces[i].copy()
             self.surfaces[i].fill(bodyColor,None,BLEND_MULT)
             self.surfaces[i].blit(myShellSurface,(0,0))
             
             #for flashing during leaf bonus
             self.surfaces[2+i]=self.surfaces[i].copy()
             self.surfaces[2+i].fill((255,255,255),None,BLEND_ADD)
                          
        
        self.xpos=SCREEN_WIDTH/2
        self.ypos=SCREEN_HEIGHT/2
        self.xspeed=0
        self.yspeed=0
                
        self.frame=0
        self.facingLeft=0   #1 if facing left
        self.frameDelay=int(70-60*self.speed/(1.0*self.MAX_STAT))
        self.frameCounter=random.randint(0,self.frameDelay)
        
        self.leafCounter = 0  #keep track of time left for Leaf boost
                
        self.objRect = None # placeholder for object on race track (related to agility)
    
    
    def tick(self):
        exhaustion = 1
        obstruction = 1
        if self.isRacing:
            # Are we exhausted?
            if self.xpos>0.2*(SCREEN_WIDTH-144)+(0.8*(SCREEN_WIDTH-144))*self.endurance/(1.0*self.MAX_STAT):
                exhaustion=0.4
            
            # Are we passing an obstruction?
            
            if self.objRect.colliderect(pygame.Rect(self.xpos,self.ypos, 32*3, 17*3)):
                obstruction=0.5 + 0.5*self.agility/(1.0*self.MAX_STAT)
                
            bonus=1
            if self.leafCounter>0:
                self.leafCounter-=1
                bonus=1.5            
            self.xpos=int(round(self.xpos+self.xspeed*bonus*exhaustion*obstruction + 2*bonus))
            
        self.frameDelay = int(70-60*self.speed*exhaustion/(1.0*self.MAX_STAT))
        self.frameCounter=(self.frameCounter-1)%self.frameDelay
        self.frame = 2*(self.leafCounter%2) + 2*self.frameCounter/self.frameDelay

    def startRacing(self):
        self.isRacing=True
        self.xspeed = 1+5*self.speed /(1.0*self.MAX_STAT)
    
    def stopRacing(self):
        self.isRacing=False
        self.xspeed = 0
        self.leafCounter=0
        self.raceTimeCounter=0
    
    def giveLeaf(self):
        self.leafCounter=self.LEAF_TIME
        
        
        