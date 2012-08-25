import random

from global_stuff import *
from pygame.locals import *

class Turtle():
    # keep the basic (gray-colored) shell and body surfaces as class variables
    shellSurface = None
    bodySurfaces = None
    def __init__(self,speed,agility,endurance):
        self.speed=speed
        self.agility=agility
        self.endurance=endurance
        
        shellColor = (random.randint(100,250),random.randint(100,250),random.randint(100,250))
        bodyColor = (random.randint(100,250),random.randint(100,250),random.randint(100,250))
        
        myShellSurface = self.shellSurface.copy()
        myShellSurface.fill(shellColor,None,BLEND_MULT)

        self.surfaces=range(2)
        for i in range(2):
             self.surfaces[i]=self.bodySurfaces[i].copy()
             self.surfaces[i].fill(bodyColor,None,BLEND_MULT)
             self.surfaces[i].blit(myShellSurface,(0,0))

        
        self.xpos=SCREEN_WIDTH/2
        self.ypos=SCREEN_HEIGHT/2
        self.xspeed=0
        self.yspeed=0
                
        self.frame=0
        self.facingLeft=0   #1 if facing left
        self.frameCounter=0
        self.frameDelay=20
        
    def tick(self):
        self.xpos=self.xpos+self.xspeed
        self.ypos=self.ypos+self.yspeed
        self.frameCounter=(self.frameCounter-1)%self.frameDelay
        self.frame = 2*self.facingLeft + 2*self.frameCounter/self.frameDelay

    