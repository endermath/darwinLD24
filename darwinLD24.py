
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

statsFontObj = pygame.font.Font('freesansbold.ttf',9)
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

# Scale 3x
def scale3x(surf):
     r=surf.get_rect()
     return pygame.transform.scale(surf,(r.w*3,r.h*3))

darwinSurface=[1,2,3,4]
darwinSurface[0]=pygame.transform.scale(spriteSheetSurface.subsurface(pygame.Rect(0,0,16,16)),(48,48))
darwinSurface[1]=pygame.transform.scale(spriteSheetSurface.subsurface(pygame.Rect(16,0,16,16)),(48,48))
darwinSurface[2]=pygame.transform.flip(darwinSurface[0],True,False)
darwinSurface[3]=pygame.transform.flip(darwinSurface[1],True,False)

ridingDarwinSurface=scale3x(spriteSheetSurface.subsurface(pygame.Rect(16,16,16,16)))

boneSurface=pygame.transform.scale(spriteSheetSurface.subsurface(pygame.Rect(4*16,0,16,16)),(48,48))
stoneSurface=pygame.transform.scale(spriteSheetSurface.subsurface(pygame.Rect(5*16,0,16,16)),(48,48))
cactusSurface=pygame.transform.scale(spriteSheetSurface.subsurface(pygame.Rect(0,16,16,16)),(48,48))

objTypeSurfaces=[stoneSurface,boneSurface,cactusSurface]

desertSurfaces = [1,2]
desertSurfaces[0]=pygame.transform.scale(spriteSheetSurface.subsurface(pygame.Rect(6*16,0,16,16)),(48,48))
desertSurfaces[1]=pygame.transform.scale(spriteSheetSurface.subsurface(pygame.Rect(7*16,0,16,16)),(48,48))


goalSurface=scale3x(spriteSheetSurface.subsurface(pygame.Rect(4*16,4*16,16,16*3)))

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


# Load sound effects
selectSound = pygame.mixer.Sound("selectsound.wav")
breedSound = pygame.mixer.Sound("breedsound.wav")
countdownSound = pygame.mixer.Sound("countdown1.wav")
startSound = pygame.mixer.Sound("startsound.wav")
leafBonusSound=pygame.mixer.Sound("leafbonus.wav")

#
unlockedNewSpecies=False

sandRandomizer=random.Random()    # used to randomize the sand/desert tiles


# Reset the game
def resetGame():
     global gameOver, victory, raceNumber, turtleList, leafCounter
     
     turtleList = []
     for i in range(10):
          v = int(5+i*Turtle.MAX_STAT/10.0)
          turtleList.append(Turtle(10,v,10))
     
     turtleList.append(Turtle(random.randint(1,15),random.randint(1,15),random.randint(1,15)))
     turtleList.append(Turtle(random.randint(1,15),random.randint(1,15),random.randint(1,15)))
     
     gameOver=False
     victory=False
     
     raceNumber=0
     victories=0
     leafCounter=1  #start with one leaf

def drawSand():
     sandRandomizer.seed(928374)
     for x in range(0,SCREEN_WIDTH-1,48):
          for y in range(0,SCREEN_HEIGHT-1,48):
               windowSurface.blit(desertSurfaces[sandRandomizer.randint(0,1)],(x,y))


def doTitle():
     done=False
     mainMenuCounter=18   #animate Darwin

     # Play title music
     pygame.mixer.music.load("bu-the-bananas-elves.it")
     pygame.mixer.music.play(-1)

     # Prepare title text
     titleSurface=range(3)
     titleSurface[0]=bigFontObj.render("DARWIN'S",True,TEXT_COLOR)
     titleSurface[1]=bigFontObj.render("TURTLE RACE",True,TEXT_COLOR)
     titleSurface[2]=bigFontObj.render("CHALLANGE",True,TEXT_COLOR)

     while not done:
          mainMenuCounter = (mainMenuCounter-1)%24
          
          drawSand()

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
          fpsClock.tick(FPS)


def doSelect():
     global gameOver   #need to modify these global variables
     # Initialize Turtle Selection Screen
     selectedTurtle=0
     
     # Play select/breed screen music
     pygame.mixer.music.load("bu-tasty-and-lively.it")
     #pygame.mixer.music.play(-1)

     # Position the turtles in the list on screen
     total=len(turtleList)
     rtotal = min(5,total)
     for a in range(total):
          r = a/5
          c = a%5
          turtleList[5*r+c].xpos=(SCREEN_WIDTH-(rtotal*96+(rtotal-1)*16))/2+(96+16)*c
          turtleList[5*r+c].ypos=200+(17*3+16)*r

     # Prepare text to be displayed
     selectTurtleSurface=titleFontObj.render("SELECT YOUR TURTLE",True,TEXT_COLOR)
     w=selectTurtleSurface.get_rect().width*3
     h=selectTurtleSurface.get_rect().height*3
     selectTurtleSurface=pygame.transform.scale(selectTurtleSurface,(w,h))
     
     done=False
     while not done:
          
          # Clear Screen
          windowSurface.fill((200,200,240)) #(130,130,230))
          
          # Display message
          w=selectTurtleSurface.get_rect().width
          windowSurface.blit(selectTurtleSurface, ((SCREEN_WIDTH-w)/2,32))
          pygame.draw.line(windowSurface,(0,0,0), (16,80),(SCREEN_WIDTH-16,80),3)
          
          # Draw turtles
          for t in turtleList:
               windowSurface.blit(t.surfaces[t.frame],(t.xpos,t.ypos))
          pygame.draw.rect(windowSurface, (0,0,0), pygame.Rect(
               (SCREEN_WIDTH-(96*5+16*4))/2-16, turtleList[0].ypos-16,
               (96*5+16*4)+16*2, 17*3*4+3*16+2*16), 3)
          
          # Draw selection square
          sc=random.randint(150,250)
          selectColor = (sc,sc,sc)
          t=turtleList[selectedTurtle]
          cursorRect=pygame.Rect(t.xpos-3,t.ypos-3,96+6,17*3+6)
          pygame.draw.rect(windowSurface, selectColor, cursorRect, 3)
          
          # Draw selected turtle above
          windowSurface.blit(t.surfaces[t.frame],(240,112))
          
          # Display turtle statistics
          t=turtleList[selectedTurtle]
          statsy=88
          spdTextSurface=scale3x(statsFontObj.render("SPEED: "+str(t.speed),True,TEXT_COLOR))
          agiTextSurface=scale3x(statsFontObj.render("AGILITY: "+str(t.agility),True,TEXT_COLOR))
          endTextSurface=scale3x(statsFontObj.render("ENDURANCE: "+str(t.endurance),True,TEXT_COLOR))
          
          windowSurface.blit(spdTextSurface, (380,statsy))
          windowSurface.blit(agiTextSurface, (380,statsy+32))
          windowSurface.blit(endTextSurface, (380,statsy+64))
          
          for t in turtleList:
               t.tick()
               
          for event in pygame.event.get():
               if event.type==QUIT:
                    sys.exit()
               elif event.type==KEYDOWN:
                    if event.key==K_LEFT:
                         if selectedTurtle-1>=0:
                              selectedTurtle-=1
                              selectSound.play()
                    elif event.key==K_RIGHT:
                         if selectedTurtle+1<len(turtleList):
                              selectedTurtle+=1
                              selectSound.play()
                    elif event.key==K_UP:
                         if selectedTurtle-5>=0:
                              selectedTurtle-=5
                              selectSound.play()
                    elif event.key==K_DOWN:
                         if selectedTurtle+5<len(turtleList):
                              selectedTurtle+=5
                              selectSound.play()
                    elif event.key==K_RETURN:
                         selectSound.play()
                         done=True
                    elif event.key==K_ESCAPE:
                         done=True
                         gameOver=True

          pygame.display.update()
          fpsClock.tick(FPS)

     return turtleList[selectedTurtle]
          
          #selectSurface=
          #windowSurface.fill((80,80,170))
     

def doRace(turtle):
     global leafCounter, raceNumber
     
     raceNumber += 1
     
     NUMBER_OF_RACERS=3
     
     # Randomize turtles to race against
     minS=1+2*(raceNumber-1)
     maxS=1+10*raceNumber
     racingTurtles=[]
     for i in range(NUMBER_OF_RACERS):
          racingTurtles.append(Turtle(random.randint(minS,maxS),random.randint(minS,maxS),random.randint(minS,maxS)))
               
     playerIndex = random.choice(range(NUMBER_OF_RACERS))
     racingTurtles[playerIndex]=turtle            # add player's turtle

     LANE_Y = 3*48
     LANE_HEIGHT=48+32
     
     
     # Randomize obstructive objects on the race tracks
     objSurfaces=[] 
     objRects = []
     for i in range(NUMBER_OF_RACERS):
          x=random.randint(32+96, SCREEN_WIDTH-144)
          objRects.append(pygame.Rect(x,LANE_Y+LANE_HEIGHT*i, 48,48))
          objSurfaces.append(random.choice(objTypeSurfaces))

     # setup racing turtles
     for i in range(NUMBER_OF_RACERS):
          t=racingTurtles[i]
          t.xpos = 16
          t.ypos = LANE_Y+LANE_HEIGHT*i
          t.objRect = objRects[i]       #let the turtle know where the obstruction is

     countdown = 3
     countdownSound.play()
     countdown_counter=20
     timeClock = None
     started=False
     finished=False
     won=False
     done=False
     while not done:
          
          # Draw sand background
          drawSand()
          
          # Draw obstructive objects
          for i in range(NUMBER_OF_RACERS):
               r=objRects[i]
               windowSurface.blit(objSurfaces[i], (r.x,r.y))
               
          # First do a countdown
          if countdown>=0:
               countdown_counter-=1
               if countdown_counter<0:
                    countdown_counter=20
                    countdown-=1
                    if countdown>0:
                         countdownSound.play()

               readySurf=scale3x(titleFontObj.render("GET READY!",True,TEXT_COLOR))
               readyRect=readySurf.get_rect()
               readyY=-96+(SCREEN_HEIGHT-readyRect.h)/2
               windowSurface.blit(readySurf,((SCREEN_WIDTH-readyRect.w)/2,readyY))
               
               if countdown>0:
                    st=str(countdown)
               else:
                    st="GO!"
               countSurface=scale3x(titleFontObj.render(st,True,TEXT_COLOR))
               countRect=countSurface.get_rect()
               windowSurface.blit(countSurface,((SCREEN_WIDTH-countRect.w)/2,readyY+96))

          if countdown<=0 and not started:
               started=True
               startSound.play()
               for t in racingTurtles:
                    t.startRacing()
               timeClock = pygame.time.get_ticks()  #keep track of time
               

          # Draw starting line
          pygame.draw.line(windowSurface,(240,10,10),(16+96, LANE_Y-48), (16+96,LANE_Y+LANE_HEIGHT*NUMBER_OF_RACERS),3)
          
          # Draw goal strip
          windowSurface.blit(goalSurface,(SCREEN_WIDTH-48,LANE_Y-48))
          windowSurface.blit(goalSurface,(SCREEN_WIDTH-48,LANE_Y-48+48*3))
          
               
          # Draw turtles
          for t in racingTurtles:
               windowSurface.blit(t.surfaces[t.frame],(t.xpos,t.ypos))

          # Draw Darwin on top of the last (the player's) turtles
          windowSurface.blit(ridingDarwinSurface,(turtle.xpos+6*3, turtle.ypos-9*3))
          
          # display a line
          FOOTER_Y=SCREEN_HEIGHT-64
          pygame.draw.line(windowSurface, (0,0,0), (16,FOOTER_Y),(SCREEN_WIDTH-16,FOOTER_Y),3)
          # race number
          raceCounterSurf=scale3x(statsFontObj.render("RACE NO.: "+str(raceNumber),True,TEXT_COLOR))
          windowSurface.blit(raceCounterSurf, (16,FOOTER_Y+9))
          # leaf counter
          leafCounterSurface=scale3x(statsFontObj.render(str(leafCounter),True,TEXT_COLOR))
          windowSurface.blit(leafCounterSurface, (300,FOOTER_Y+9) )
          # time clock
          if timeClock==None:
               tim=0
          else:
               if not finished:
                    tim=int(round((pygame.time.get_ticks()-timeClock)/100.0))
          clockSurface=scale3x(statsFontObj.render("TIME: "+str(tim),True,TEXT_COLOR))
          windowSurface.blit(clockSurface, (500,FOOTER_Y+9))

                    
          # Check if somebody won
          if not finished:
               for t in racingTurtles:
                    t.tick()
               for t in racingTurtles:
                    if t.xpos>SCREEN_WIDTH-96:
                         finished=True
                         finishCounter=FPS*3
                         # stop racing
                         for t in racingTurtles:
                              t.stopRacing()
                         # Was it you?
                         if turtle.xpos>SCREEN_WIDTH-96:
                              won=True
                         else:
                              won=False
          else:
          # If finished, announce victory or loss
               if won:
                    finMsgObj=scale3x(titleFontObj.render("YOU WIN!",True,TEXT_COLOR))
               else:
                    finMsgObj=scale3x(titleFontObj.render("YOU LOSE",True,TEXT_COLOR))
               
               wi=finMsgObj.get_rect().w
               windowSurface.blit(finMsgObj,((SCREEN_WIDTH-wi)/2,readyY))
               finishCounter-=1
               if finishCounter<=0:
                    done=True
          
          # Check for key presses
          for event in pygame.event.get():
               if event.type==QUIT:
                    sys.exit()
               elif event.type==KEYDOWN:
                    if event.key==K_SPACE and not finished:
                         if leafCounter>0:
                              turtle.giveLeaf()
                              leafBonusSound.play()
                              leafCounter-=1
                    elif event.key==K_ESCAPE:
                         gameOver=True
                         done=True
                
          pygame.display.update()
          fpsClock.tick(FPS)

     
     leafCounter+=1
     
     return won 


def doBreeding():
     pass
     

def doQuit():
     # Do you wish to quit? Show message. Wait for Y/N
     pass

# Main loop
while True:
     resetGame()
     doTitle()
     pygame.mixer.music.fadeout(1000)
     while not gameOver:
          turtle=doSelect()     #returns the selected turtle
          pygame.mixer.music.fadeout(1000)
          if doRace(turtle):    #returns True if race was won
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
         
    