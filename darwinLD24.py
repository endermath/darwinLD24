
import pygame,sys,os,random

from pygame.locals import *
from global_stuff import *

from turtle import *

# Set base path (so that it also works with pyinstaller)
if getattr(sys, 'frozen', None):
     basedir = sys._MEIPASS
else:
     basedir = os.path.dirname(__file__)

# Initialize pygame and window
pygame.init()
fpsClock=pygame.time.Clock()
pygame.display.set_caption("Darwin's Adventure")
pygame.display.set_icon(pygame.image.load(os.path.join(basedir,'icon.png')))
windowSurface=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT)) #,FULLSCREEN | DOUBLEBUF | HWSURFACE)
pygame.mouse.set_visible(False)

scoreFontObj = pygame.font.Font('freesansbold.ttf',10)
titleFontObj = pygame.font.Font('freesansbold.ttf',16)
bigFontObj = pygame.font.Font('freesansbold.ttf',24)

#scoreSurface = fontObj.render('155', False, (0,0,0))
#w=scoreSurface.get_rect().width*3
#h=scoreSurface.get_rect().height*3
#scoreSurface = pygame.transform.scale(scoreSurface,(w,h))

# Load resources
spriteSheetSurface=pygame.image.load(os.path.join(basedir,'spritesheet.png'))
#spriteSheetSurface.set_colorkey((255,255,255))  #white will be interpreted as transparent
#spriteSheetSurface=spriteSheetSurface.convert() #convert color format to that of the display

darwinSurface=[1,2,3,4]
darwinSurface[0]=pygame.transform.scale(spriteSheetSurface.subsurface(pygame.Rect(0,0,16,16)),(48,48))
darwinSurface[1]=pygame.transform.scale(spriteSheetSurface.subsurface(pygame.Rect(16,0,16,16)),(48,48))
darwinSurface[2]=pygame.transform.flip(darwinSurface[0],True,False)
darwinSurface[3]=pygame.transform.flip(darwinSurface[1],True,False)

boneSurface=pygame.transform.scale(spriteSheetSurface.subsurface(pygame.Rect(4*16,0,16,16)),(48,48))
stoneSurface=pygame.transform.scale(spriteSheetSurface.subsurface(pygame.Rect(5*16,0,16,16)),(48,48))

desertSurfaces = [1,2]
desertSurfaces[0]=pygame.transform.scale(spriteSheetSurface.subsurface(pygame.Rect(6*16,0,16,16)),(48,48))
desertSurfaces[1]=pygame.transform.scale(spriteSheetSurface.subsurface(pygame.Rect(7*16,0,16,16)),(48,48))

cactusSurface=pygame.transform.scale(spriteSheetSurface.subsurface(pygame.Rect(0,16,16,16)),(48,48))

# Build turtle icons
turtleShellSurface = pygame.transform.scale(
                     spriteSheetSurface.subsurface(
                     pygame.Rect(pygame.Rect(64,32,32,17))),(96,17*3))
turtleBodySurfaces = []
turtleBodySurfaces.append(pygame.transform.scale(
                         spriteSheetSurface.subsurface(
                         pygame.Rect(pygame.Rect(96,32,32,17))),(96,17*3)))
turtleBodySurfaces.append(pygame.transform.scale(
                         spriteSheetSurface.subsurface(
                         pygame.Rect(pygame.Rect(0,64,32,17))),(96,17*3)))

Turtle.shellSurface = turtleShellSurface
Turtle.bodySurfaces = turtleBodySurfaces


#defaultLegColor = pygame.Color('#114400')
#defaultShellColor = pygame.Color('#226600')

# 114400 = 888888 x 228800
# 226600 = CCCCCC x 228800

#turtleSurfaces=blueLeg
#turtleSurfaces.append(pygame.transform.scale(spriteSheetSurface.subsurface(pygame.Rect(0,32,32,17)),(96,17*3)))
#turtleSurfaces.append(pygame.transform.scale(spriteSheetSurface.subsurface(pygame.Rect(32,32,32,17)),(96,17*3)))



pygame.mixer.music.load("bu-the-bananas-elves.it")

#
unlockedNewSpecies=False

# Reset the game
def resetGame():
     global gameOver, victory, racenumber, turtleList
     pygame.mixer.music.stop()
     pygame.mixer.music.rewind()
     pygame.mixer.music.play(-1)
     
     turtleList = []
     turtleList.append(Turtle(random.randint(1,25),random.randint(1,25),random.randint(1,25)))
     turtleList.append(Turtle(random.randint(1,25),random.randint(1,25),random.randint(1,25)))
     turtleList.append(Turtle(random.randint(1,25),random.randint(1,25),random.randint(1,25)))
     
     gameOver=False
     victory=False
     
     raceNumber=0

def doTitle():
     done=False
     sandRandomizer=random.Random()    # used to randomize the sand/desert tiles
     mainMenuCounter=25   #animate Darwin

     # Prepare title text
     titleSurface=range(3)
     titleSurface[0]=bigFontObj.render("DARWIN'S",False,TEXT_COLOR)
     titleSurface[1]=bigFontObj.render("TURTLE RACE",False,TEXT_COLOR)
     titleSurface[2]=bigFontObj.render("CHALLANGE",False,TEXT_COLOR)

     while not done:
          mainMenuCounter = (mainMenuCounter-1)%24
          sandRandomizer.seed(928374)
          for x in range(0,SCREEN_WIDTH-1,48):
               for y in range(0,SCREEN_HEIGHT-1,48):
                    windowSurface.blit(desertSurfaces[sandRandomizer.randint(0,1)],(x,y))

          for i in range(3):
               w=titleSurface[i].get_rect().width*3
               h=titleSurface[i].get_rect().height*3
               surf = pygame.transform.scale(titleSurface[i],(w,h))
               windowSurface.blit(surf,((SCREEN_WIDTH-w)/2,32+i*24*3))

          if mainMenuCounter>11:
               windowSurface.blit(darwinSurface[0],(10,186))
          else:
               windowSurface.blit(darwinSurface[1],(10,186))

          # RETURN to start, ESC to quit
          for event in pygame.event.get():
               if event.type==QUIT:
                    sys.exit()
               elif event.type==KEYDOWN:
                    if event.key==K_RETURN:
                         done=True
                    elif event.key==K_ESCAPE:
                         sys.exit()
                
          pygame.display.update()
          fpsClock.tick(80)


def doSelect():
     global gameOver   #need to modify these global variables
     # Initialize Turtle Selection Screen
     selectedTurtle=0
     
     # Position the turtles in the list on screen
     total=len(turtleList)
     rtotal = min(5,total)
     for a in range(total):
          r = a/5
          c = a%5
          turtleList[5*r+c].xpos=(SCREEN_WIDTH-(rtotal*96+(rtotal-1)*16))/2+(96+16)*c
          turtleList[5*r+c].ypos=200+(17*3+16)*r

     # Prepare text to be displayed
     selectTurtleSurface=titleFontObj.render("SELECT YOUR TURTLE",False,TEXT_COLOR)
     w=selectTurtleSurface.get_rect().width*3
     h=selectTurtleSurface.get_rect().height*3
     selectTurtleSurface=pygame.transform.scale(selectTurtleSurface,(w,h))
     
     done=False
     while not done:
          
          # Clear Screen
          windowSurface.fill((130,130,230))
          
          # Display message
          w=selectTurtleSurface.get_rect().width
          windowSurface.blit(selectTurtleSurface, ((SCREEN_WIDTH-w)/2,40))
          
          # Draw turtles
          for t in turtleList:
               windowSurface.blit(t.surfaces[t.frame],(t.xpos,t.ypos))
          
          # Draw selection square
          sc=random.randint(150,250)
          selectColor = (sc,sc,sc)
          t=turtleList[selectedTurtle]
          cursorRect=pygame.Rect(t.xpos-3,t.ypos-3,96+6,17*3+6)
          pygame.draw.rect(windowSurface, selectColor, cursorRect, 3)
          
          
          for t in turtleList:
               t.tick()
               
          for event in pygame.event.get():
               if event.type==QUIT:
                    sys.exit()
               elif event.type==KEYDOWN:
                    if event.key==K_LEFT:
                         selectedTurtle=max(0,selectedTurtle-1)
                    elif event.key==K_RIGHT:
                         selectedTurtle=min(len(turtleList)-1,selectedTurtle+1)                         
                    elif event.key==K_UP:
                         if selectedTurtle-5>0:
                              selectedTurtle-=5
                    elif event.key==K_DOWN:
                         if selectedTurtle+5<len(turtleList):
                              selectedTurtle+=5
                    elif event.key==K_RETURN:
                         done=True
                    elif event.key==K_ESCAPE:
                         done=True
                         gameOver=True

          pygame.display.update()
          fpsClock.tick(80)

     return turtleList[selectedTurtle]
          
          #selectSurface=
          #windowSurface.fill((80,80,170))
     

def doRace():
     done=False
     while not done:
          for event in pygame.event.get():
               if event.type==QUIT:
                    sys.exit()
               elif event.type==KEYDOWN:
                    if event.key==K_SPACE:
                         player.down()
                    elif event.key==K_ESCAPE:
                         gameOver=True
                         done=True
                
          pygame.display.update()
          fpsClock.tick(80)



def doBreeding():
     pass
     

def doQuit():
     # Do you wish to quit? Show message. Wait for Y/N
     pass

# Main loop
while True:
     resetGame()
     doTitle()
     while not gameOver:
          doSelect()
          if doRace():    #returns True if race was won
               pass
               #won
          else:
               pass
               #lost
          if doBreeding():  #bred new species?
               victory=True
               unlockedNewSpecies=True               
               gameOver=True
          
     if victory:
          # show victory message
          pass
     
     
          

          

#     windowSurface.blit(darwinSurface[frameOffset+player.frame],(player.xpos,player.ypos),None,BLEND_SUB)
#     elif gameState==STATE_RACE:
#          player.tick()
               
#          windowSurface.blit(darwinSurface[player.frame],(player.xpos,player.ypos))
         
    