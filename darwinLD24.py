
import pygame,sys,os

from pygame.locals import *
from global_stuff import *

# Set base path (so that it also works with pyinstaller)
if getattr(sys, 'frozen', None):
     basedir = sys._MEIPASS
else:
     basedir = os.path.dirname(__file__)

pygame.init()
fpsClock=pygame.time.Clock()
pygame.display.set_caption("Darwin's Adventure")
pygame.display.set_icon(pygame.image.load(os.path.join(basedir,'icon.png')))
windowSurface=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

# load resources
spriteSheetSurface=pygame.image.load(os.path.join(basedir,'spritesheet.png'))
spriteSheetSurface=spriteSheetSurface.convert() #convert color format to that of the display

darwinSurface=[1,2,3,4]
darwinSurface[0]=spriteSheetSurface.subsurface(pygame.Rect(0,0,16,16))
darwinSurface[1]=spriteSheetSurface.subsurface(pygame.Rect(16,0,16,16))
darwinSurface[2]=pygame.transform.flip(darwinSurface[0],True,False)
darwinSurface[3]=pygame.transform.flip(darwinSurface[1],True,False)



# Main loop
while True:
    for event in pygame.event.get():
        if event.type==QUIT:
            sys.exit()
        elif event.type==KEYDOWN:
            sys.exit()
    pygame.display.update()
    fpsClock.tick(40)
    