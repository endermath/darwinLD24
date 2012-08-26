import random

from global_stuff import *
from pygame.locals import *

class Turtle():
    # keep the basic (gray-colored) shell and body surfaces as class variables
    shellSurface = None
    bodySurfaces = None
    
    MAX_STAT = 100
    
    LEAF_TIME = 40
    
    def __init__(self,speed,agility,endurance):
        self.speed=speed
        self.agility=agility
        self.endurance=endurance
        
        self.isRacing = False
        
        shellColor = (random.randint(100,250),random.randint(100,250),random.randint(100,250))
        bodyColor = (random.randint(100,250),random.randint(100,250),random.randint(100,250))
        
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
        self.frameDelay=int(30-20*self.speed/(1.0*self.MAX_STAT))
        self.frameCounter=random.randint(0,self.frameDelay)
        
        self.leafCounter = 0  #keep track of time left for Leaf boost
        
    def tick(self):
        if self.isRacing:
            bonus=1
            if self.leafCounter>0:
                self.leafCounter-=1
                bonus=1.5
            self.xpos=int(round(self.xpos+self.xspeed*bonus + 2*bonus))
            
        self.frameCounter=(self.frameCounter-1)%self.frameDelay
        self.frame = 2*(self.leafCounter%2) + 2*self.frameCounter/self.frameDelay

    def startRacing(self):
        self.isRacing=True
        self.xspeed = 1+10*self.speed /(1.0*self.MAX_STAT)
    
    def stopRacing(self):
        self.isRacing=False
        self.xspeed = 0
        self.leafCounter=0
    
    def giveLeaf(self):
        self.leafCounter=self.LEAF_TIME
        
        
        