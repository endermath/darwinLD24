
import pygame,sys,os

from pygame.locals import *
from global_stuff import *

from player import *

# Set base path (so that it also works with pyinstaller)
if getattr(sys, 'frozen', None):
     basedir = sys._MEIPASS
else:
     basedir = os.path.dirname(__file__)

pygame.init()
fpsClock=pygame.time.Clock()
pygame.display.set_caption("Darwin's Adventure")
pygame.display.set_icon(pygame.image.load(os.path.join(basedir,'icon.png')))
windowSurface=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT),FULLSCREEN | DOUBLEBUF | HWSURFACE)
pygame.mouse.set_visible(False)


# load resources
    
spriteSheetSurface=pygame.image.load(os.path.join(basedir,'spritesheet.png'))
spriteSheetSurface.set_colorkey((255,255,255))  #white will be interpreted as transparent
spriteSheetSurface=spriteSheetSurface.convert() #convert color format to that of the display

darwinSurface=[1,2,3,4]
darwinSurface[0]=pygame.transform.scale(spriteSheetSurface.subsurface(pygame.Rect(0,0,16,16)),(48,48))
darwinSurface[1]=pygame.transform.scale(spriteSheetSurface.subsurface(pygame.Rect(16,0,16,16)),(48,48))
darwinSurface[2]=pygame.transform.flip(darwinSurface[0],True,False)
darwinSurface[3]=pygame.transform.flip(darwinSurface[1],True,False)


# Create player

player = Player()

# Main loop
while True:
     windowSurface.fill((80,80,170))

#     frameOffset=0
#     if player.xspeed<0:
#          frameOffset=2    
#     windowSurface.blit(darwinSurface[frameOffset+player.frame],(player.xpos,player.ypos),None,BLEND_SUB)
     
     player.tick()
     
     frameOffset=0
     if player.xspeed<0:
          frameOffset=2
     
     windowSurface.blit(darwinSurface[frameOffset+player.frame],(player.xpos,player.ypos))
    
     for event in pygame.event.get():
          if event.type==QUIT:
               sys.exit()
          elif event.type==KEYDOWN:
               if event.key==K_RIGHT:
                    player.right()
               elif event.key==K_LEFT:
                    player.left()
               elif event.key==K_ESCAPE:
                    sys.exit()
          
                
     pygame.display.update()
     fpsClock.tick(80)
    