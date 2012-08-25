
from global_stuff import *

class Player():
    def __init__(self):
        self.xpos=SCREEN_WIDTH/2
        self.ypos=SCREEN_HEIGHT/2
        self.xspeed=0
        self.yspeed=0
        
        self.frame=0
        self.frameCounter=0
        self.frameDelay=20
        
    def tick(self):
        self.xpos=self.xpos+self.xspeed
        self.ypos=self.ypos+self.yspeed
        self.frameCounter=(self.frameCounter-1)%self.frameDelay
        self.frame = 2*self.frameCounter/self.frameDelay
        
    def right(self):
        self.xspeed=2
    def left(self):
        self.xspeed=-2
    