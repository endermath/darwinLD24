from global_stuff import *


class Turtle():
    def __init__(self,speed,agility,endurance):
        self.speed=speed
        self.agility=agility
        self.endurance=endurance
    
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

    