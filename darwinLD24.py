
import pygame,sys,os,random,math

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
pygame.display.set_caption("Darwin's Turtle Race Challenge")
pygame.display.set_icon(pygame.image.load(os.path.join(basedir,'icon.png')))
windowSurface=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT)) #,FULLSCREEN | DOUBLEBUF | HWSURFACE)
pygame.mouse.set_visible(False)

#statsFontObj = pygame.font.Font(None,9*3) #'freesansbold.ttf'
#titleFontObj = pygame.font.Font(None,16*3)
#bigFontObj = pygame.font.Font(None,24*3)

#scoreSurface = fontObj.render('155', False, (0,0,0))
#w=scoreSurface.get_rect().width*3
#h=scoreSurface.get_rect().height*3
#scoreSurface = pygame.transform.scale(scoreSurface,(w,h))

# Load resources
fontSurface=pygame.image.load(os.path.join(basedir,'font.png'))
alphabet="0123456789!/:.'? ABCDEFGHIJKLMNOPQRSTUVWXYZ?????"

FONT_WIDTH=15
def renderMsg(msg, xpos, ypos, scaleFactor=3, color=TEXT_COLOR):
     if xpos==-1:        #-1 as xpos means we want to center it
          xpos = (SCREEN_WIDTH-len(msg)*FONT_WIDTH*scaleFactor)/2
     for c in msg:
          i=alphabet.index(c)
          x=(i%16)*16
          y=(i/16)*16
          surf=scale(fontSurface.subsurface(pygame.Rect(x,y,16,16)),scaleFactor)
          surf.fill(color,None,BLEND_MULT)
          windowSurface.blit(surf,(xpos,ypos))
          xpos+=FONT_WIDTH*scaleFactor
     

spriteSheetSurface=pygame.image.load(os.path.join(basedir,'spritesheet.png'))
#spriteSheetSurface.set_colorkey((255,255,255))  #white will be interpreted as transparent
#spriteSheetSurface=spriteSheetSurface.convert() #convert color format to that of the display

# Scale
def scale(surf,sf=3):
     r=surf.get_rect()
     return pygame.transform.scale(surf,(r.w*sf,r.h*sf))
def scale3x(surf):
     return scale(surf)
     
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
selectSound = pygame.mixer.Sound(os.path.join(basedir,"selectsound.wav"))
breedSound = pygame.mixer.Sound(os.path.join(basedir,"breedsound.wav"))
countdownSound = pygame.mixer.Sound(os.path.join(basedir,"countdown1.wav"))
startSound = pygame.mixer.Sound(os.path.join(basedir,"startsound.wav"))
leafBonusSound=pygame.mixer.Sound(os.path.join(basedir,"leafbonus.wav"))
lostRaceSound=pygame.mixer.Sound(os.path.join(basedir,"lostrace.wav"))
winGameSound=pygame.mixer.Sound(os.path.join(basedir,"win.ogg"))

#
unlockedNewSpecies=False

sandRandomizer=random.Random()    # used to randomize the sand/desert tiles


# Reset the game
def resetGame():
     global gameOver, victory, raceNumber, turtleList, leafCounter, losses, victories, selectedTurtle,totalRacingTime
     
     turtleList = []
#     for i in range(10):
#          v = int(5+i*Turtle.MAX_STAT/10.0)
#          turtleList.append(Turtle(10,v,10))
     
     turtleList.append(Turtle(random.randint(1,15),random.randint(1,15),random.randint(1,15)))
     turtleList.append(Turtle(random.randint(1,15),random.randint(1,15),random.randint(1,15)))
     
     selectedTurtle = 0
     
     gameOver=False
     victory=False
     
     raceNumber=0
     totalRacingTime =0 
     losses=0
     victories=0
     leafCounter=1  #start with one leaf

def drawSand():
     sandRandomizer.seed(928374)
     for x in range(0,SCREEN_WIDTH-1,48):
          for y in range(0,SCREEN_HEIGHT-1,48):
               windowSurface.blit(desertSurfaces[sandRandomizer.randint(0,1)],(x,y))


def doTitle():
     done=False
     mainMenuCounter=14   #animate Darwin

     # Play title music
     pygame.mixer.music.load(os.path.join(basedir,"bu-the-bananas-elves.it"))
     pygame.mixer.music.play(-1)

     # Prepare title text
     #titleSurface=range(3)
     #titleSurface[0]=bigFontObj.render("DARWIN'S",True,TEXT_COLOR)
     #titleSurface[1]=bigFontObj.render("TURTLE RACE",True,TEXT_COLOR)
     #titleSurface[2]=bigFontObj.render("CHALLENGE",True,TEXT_COLOR)
     
     t=Turtle(random.randint(1,Turtle.MAX_STAT),random.randint(1,Turtle.MAX_STAT),random.randint(1,Turtle.MAX_STAT))
     while not done:
          mainMenuCounter = (mainMenuCounter-1)%24
          
          drawSand()

          #for i in range(3):
          #     surf=titleSurface[i]
          #     w=surf.get_rect().width
          #     h=surf.get_rect().height
          #     windowSurface.blit(surf,((SCREEN_WIDTH-w)/2,32+i*24*3))
          renderMsg("DARWIN'S",-1,32,scaleFactor=3)
          renderMsg("TURTLE RACE",-1,32+24*3,scaleFactor=3)
          renderMsg("CHALLENGE",-1,32+2*24*3,scaleFactor=3)
          
          if mainMenuCounter>11:
               windowSurface.blit(darwinSurface[0],(40,186))
          else:
               windowSurface.blit(darwinSurface[1],(40,186))
          
          windowSurface.blit(pygame.transform.flip(t.surfaces[t.frame],True,False),(SCREEN_WIDTH-112,186))
          
          step=24
          renderMsg("INSTRUCTIONS:", -1, 240, scaleFactor=1)
          renderMsg("HELP DARWIN PROVE HIS THEORY", -1, 240+step, scaleFactor=1)
          renderMsg("BY BREEDING THE PERFECT RACING TURTLE", -1, 240+step*2, scaleFactor=1)
          
          renderMsg("CONTROLS:",-1,240+step*4, scaleFactor=1)
          renderMsg("ARROW KEYS AND RETURN TO SELECT", -1, 240+step*5, scaleFactor=1)
          renderMsg("SPACE TO BOOST DURING RACE",-1, 240+step*6, scaleFactor=1)
          renderMsg("RETURN TO BEGIN",-1, 240+step*7, scaleFactor=1)
          
          renderMsg("BY ENDERMATH 2012",-1, 240+step*9, scaleFactor=1)
          
          t.tick()
          
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


def doSelect(textMessage, previouslySelectedTurtle=None, listOfTurtles=[], discardCursor=False):
     global gameOver,selectedTurtle   #need to modify these global variables
     # Initialize Turtle Selection Screen
     if previouslySelectedTurtle==None:
          selectedTurtle=0
     
     if listOfTurtles==[]:
          listOfTurtles=turtleList
     
     # Position the turtles in the list on screen
     total=len(listOfTurtles)
     rtotal = min(5,total)
     for a in range(total):
          r = a/5
          c = a%5
          listOfTurtles[5*r+c].xpos=(SCREEN_WIDTH-(rtotal*96+(rtotal-1)*16))/2+(96+16)*c
          listOfTurtles[5*r+c].ypos=184+(17*3+16)*r

     # Prepare text to be displayed
     #selectTurtleSurface=titleFontObj.render(textMessage,True,TEXT_COLOR)
     
     selectCounter=0  #for flashing cursor
     done=False
     while not done:
          
          # Clear Screen
          windowSurface.fill(BG_COLOR) #(130,130,230))
          
          # Display message
#          w=selectTurtleSurface.get_width()
#          windowSurface.blit(selectTurtleSurface, ((SCREEN_WIDTH-w)/2,32))
          renderMsg(textMessage, -1, 16, scaleFactor=2)
          pygame.draw.line(windowSurface,(0,0,0), (16,58),(SCREEN_WIDTH-16,58),3)


          
          # Draw turtles
          for t in listOfTurtles:
               windowSurface.blit(t.surfaces[t.frame],(t.xpos,t.ypos))
               # mark previously selected turtle with a square (during breeding menu)
               if t==previouslySelectedTurtle:
                    cursorRect=pygame.Rect(t.xpos-3,t.ypos-3,96+6-3,17*3+6)                    
                    pygame.draw.rect(windowSurface, (225,20,20), cursorRect, 3 )
          pygame.draw.rect(windowSurface, (0,0,0), pygame.Rect(
               (SCREEN_WIDTH-(96*5+16*4))/2-16, listOfTurtles[0].ypos-16,
               (96*5+16*4)+16*2, 17*3*4+3*16+2*16), 3)
          
          # Draw selection square
          selectCounter = (selectCounter+1)%50
          sc=150+2*selectCounter
          if discardCursor:
               selectColor = (240,10,10)
          else:
               selectColor = (sc,sc,sc/2)
          t=listOfTurtles[selectedTurtle]
          cursorRect=pygame.Rect(t.xpos-3,t.ypos-3,96+6-3,17*3+6)
          pygame.draw.rect(windowSurface, selectColor, cursorRect, 3)
          
          if discardCursor:
               pygame.draw.line(windowSurface, selectColor, cursorRect.topright, cursorRect.bottomleft,3)
               pygame.draw.line(windowSurface, selectColor, cursorRect.topleft, cursorRect.bottomright,3)
               
               
          
          # Draw selected turtle above
          windowSurface.blit(t.surfaces[t.frame],(140,88))
          
          # Display turtle statistics
          t=listOfTurtles[selectedTurtle]
          statsy=72
          #spdTextSurface=statsFontObj.render("SPEED: "+str(t.speed),True,TEXT_COLOR)
          #agiTextSurface=statsFontObj.render("AGILITY: "+str(t.agility),True,TEXT_COLOR)
          #endTextSurface=statsFontObj.render("ENDURANCE: "+str(t.endurance),True,TEXT_COLOR)
          #windowSurface.blit(spdTextSurface, (380,statsy))
          #windowSurface.blit(agiTextSurface, (380,statsy+32))
          #windowSurface.blit(endTextSurface, (380,statsy+64))
          renderMsg("SPEED:     "+str(t.speed), 280,statsy, scaleFactor=1)
          renderMsg("AGILITY:   "+str(t.agility), 280,statsy+32, scaleFactor=1)
          renderMsg("ENDURANCE: "+str(t.endurance), 280,statsy+64, scaleFactor=1)
          
          
          for t in listOfTurtles:
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
                         if selectedTurtle+1<len(listOfTurtles):
                              selectedTurtle+=1
                              selectSound.play()
                    elif event.key==K_UP:
                         if selectedTurtle-5>=0:
                              selectedTurtle-=5
                              selectSound.play()
                    elif event.key==K_DOWN:
                         if selectedTurtle+5<len(listOfTurtles):
                              selectedTurtle+=5
                              selectSound.play()
                    elif event.key==K_RETURN:
                         selectSound.play()
                         done=True
#                    elif event.key==K_ESCAPE:
#                         done=True
#                         gameOver=True

          pygame.display.update()
          fpsClock.tick(FPS)

     return listOfTurtles[selectedTurtle]




def doRace(turtle):
     global leafCounter, raceNumber, losses, gameOver, victories, totalRacingTime
     
     raceNumber += 1
     
     NUMBER_OF_RACERS=3
     
     # Randomize turtles to race against
     minS=max(1, 1+2*(raceNumber-1))
     maxS=min(Turtle.MAX_STAT, 1+4*raceNumber)
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
     gotLeaves=False  #keeps track of whether we got a chance to get leaves
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

               #readySurf=titleFontObj.render("GET READY!",True,TEXT_COLOR)
               #readyY=-96*2+(SCREEN_HEIGHT-readySurf.get_height())/2
               #windowSurface.blit(readySurf,((SCREEN_WIDTH-readySurf.get_width())/2,readyY))
               readyY=-96*2+(SCREEN_HEIGHT-48)/2
               renderMsg("GET READY!",-1,readyY)
               
               if countdown>0:
                    st=str(countdown)
               else:
                    st="GO!"
               #countSurface=titleFontObj.render(st,True,TEXT_COLOR)
               #windowSurface.blit(countSurface,((SCREEN_WIDTH-countSurface.get_width())/2,readyY+64))
               renderMsg(st,-1,readyY+64)

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
          #raceCounterSurf=statsFontObj.render("LOST/RACES: "+str(losses)+"/"+str(raceNumber),True,TEXT_COLOR)
          #windowSurface.blit(raceCounterSurf, (16,FOOTER_Y+9))
          renderMsg(" WON: "+str(victories),16,FOOTER_Y+9,scaleFactor=1)
          renderMsg("LOST: "+str(losses),16,FOOTER_Y+9+16,scaleFactor=1)
          # leaf counter
          #leafCounterSurface=statsFontObj.render("LEAVES: "+str(leafCounter),True,TEXT_COLOR)
          #windowSurface.blit(leafCounterSurface, (364,FOOTER_Y+9) )
          renderMsg("LEAF BOOSTS: "+str(leafCounter), -1, FOOTER_Y+9, scaleFactor=1)
          
          # time clock
          if timeClock==None:
               tim=0
          else:
               if not finished:
                    tim=round((pygame.time.get_ticks()-timeClock)/100.0,1)
          #clockSurface=statsFontObj.render("TIME: "+str(tim),True,TEXT_COLOR)
          #windowSurface.blit(clockSurface, (500,FOOTER_Y+9))
          renderMsg("TIME: "+str(tim), 472,FOOTER_Y+9, scaleFactor=1)
          
                    
          # Check if somebody won
          if not finished:
               for t in racingTurtles:
                    t.tick()
               for t in racingTurtles:
                    if t.xpos>SCREEN_WIDTH-96:
                         finished=True
                         totalRacingTime += tim     #add duration of this race to totalRacingTime
                         finishCounter=FPS*2
                         # stop racing
                         for t in racingTurtles:
                              t.stopRacing()
                         # Was it you?
                         if turtle.xpos>SCREEN_WIDTH-96:
                              won=True
                              victories+=1
                              pygame.mixer.music.load(os.path.join(basedir,'wonrace.xm'))
                              pygame.mixer.music.play(1)
                              #if len(turtleList)<MAX_TURTLES_OWNED:
                              #     turtleList.append(Turtle(random.randint(minS,maxS),random.randint(minS,maxS),random.randint(minS,maxS)))
                         else:
                              lostRaceSound.play()
                              won=False
                              losses+=1
          else:
          # If finished, announce victory or loss
               if won:
                    #finMsgObj=titleFontObj.render("YOU WIN!",True,TEXT_COLOR)
                    finMsg = "YOU WIN!"
               else:
                    if losses>=MAX_LOSSES:
                         #finMsgObj=titleFontObj.render("GAME OVER",True,TEXT_COLOR)
                         finMsg = "GAME OVER"
                         gameOver=True
                    else:
                         #finMsgObj=titleFontObj.render("YOU LOSE",True,TEXT_COLOR)
                         finMsg = "YOU LOSE"
               
               #wi=finMsgObj.get_rect().w
               #windowSurface.blit(finMsgObj,((SCREEN_WIDTH-wi)/2,readyY))
               renderMsg(finMsg,-1,readyY)
               
               # found leaves?
               if not gameOver:     # if we lost the race and are gameover we dont get leaves...
                    if not gotLeaves:  #and also now if we already got them
                         gotLeaves=True
                         r=random.randint(1,5)
                         
                         if r==5:
                              leafCounter+=2
                              leafMsg="YOU FOUND TWO LEAVES!"
                         elif r>1:
                              leafCounter+=1
                              leafMsg="YOU FOUND A LEAF."
                         else:
                              leafMsg="YOU FOUND NOTHING."
                    renderMsg(leafMsg,-1,readyY+48,scaleFactor=1) #but display msg
                    
               
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
#                    elif event.key==K_ESCAPE:
#                         gameOver=True
#                         done=True
                
          pygame.display.update()
          fpsClock.tick(FPS)

     
     if won:
          racingTurtles.remove(turtle)
          return racingTurtles               #return opponents so we can claim our prize
     else:
          return None
          


def mutate(a,b,d):
     if random.randint(1,2)==1:
          mean = (2*a+b)/3.0
     else:
          mean = (a+2*b)/3.0
     sigma=d/3.0
     c = random.gauss(mean,sigma)
     #only allow positive variations
     if c<mean:
          c=mean + (mean-c)
     c=int(round(c))
     c=max(1,c)
     c=min(Turtle.MAX_STAT,c)
     return c
     
def doBreeding(turtle1,turtle2):
     d=math.sqrt((turtle1.speed - turtle2.speed)**2+(turtle1.agility-turtle2.agility)**2+
       (turtle1.endurance-turtle2.endurance)**2)
     sp=mutate(turtle1.speed,turtle2.speed,d)
     ag=mutate(turtle1.agility,turtle2.agility,d)
     en=mutate(turtle1.endurance,turtle2.endurance,d)
     t=Turtle(sp,ag,en)
     turtleList.append(t)
     t.flash()
     breedSound.play()
     return sp==Turtle.MAX_STAT and ag==Turtle.MAX_STAT and en==Turtle.MAX_STAT
     
def doGameCompleted():
     pygame.mixer.music.stop()
     winGameSound.play()
     
     done=False
     t=Turtle(Turtle.MAX_STAT,Turtle.MAX_STAT,Turtle.MAX_STAT)
     while not done:
          windowSurface.fill(BG_COLOR)
          
          renderMsg("CONGRATULATIONS!!!", -1, 16, scaleFactor=2)
          pygame.draw.line(windowSurface,(0,0,0), (16,58),(SCREEN_WIDTH-16,58),3)

          step=24
          renderMsg("YOU HAVE BRED THE PERFECT", -1, 58+step*1, scaleFactor=1)
          renderMsg("RACING TURTLE!!", -1, 58+step*2, scaleFactor=1)
          renderMsg("NOW DARWIN WILL GO DOWN IN HISTORY", -1, 58+step*3, scaleFactor=1)
          renderMsg("AS THE BEST TURTLE RACER", -1, 58+step*4, scaleFactor=1)
          renderMsg("IN ALL OF GALAPAGOS ISLANDS", -1, 58+step*5, scaleFactor=1)
          
          windowSurface.blit(t.surfaces[t.frame], ((SCREEN_WIDTH-96)/2,58+step*6))
          t.flash()

          renderMsg("SPEED:     "+str(t.speed), -1, 58+step*9, scaleFactor=1)
          renderMsg("AGILITY:   "+str(t.agility), -1, 58+step*10, scaleFactor=1)
          renderMsg("ENDURANCE: "+str(t.endurance), -1, 58+step*11, scaleFactor=1)
                                       
          renderMsg("NUMBER OF RACES: "+str(raceNumber),-1,58+step*12,scaleFactor=1)
          renderMsg("TOTAL RACING TIME: "+str(totalRacingTime),-1,58+step*13,scaleFactor=1)
          
          renderMsg("PRESS RETURN TO RESTART GAME", -1, 58+step*15, scaleFactor=1)
          
          t.tick()
          
          for event in pygame.event.get():
               if event.type==QUIT:
                    sys.exit()
               elif event.type==KEYDOWN:
                    if event.key==K_RETURN:
                         done = True
          
          pygame.display.update()
          fpsClock.tick(FPS)

def doQuit():
     # Do you wish to quit? Show message. Wait for Y/N
     pass

# Main loop
while True:
     resetGame()
     doTitle()
     pygame.mixer.music.fadeout(1000)
     while not gameOver:
          # Play select/breed screen music
          pygame.mixer.music.load(os.path.join(basedir,"bu-tasty-and-lively.it"))
          pygame.mixer.music.play(-1)
          turtle=doSelect("SELECT RACE TURTLE")     #returns the selected turtle
          pygame.mixer.music.fadeout(1000)
          result=doRace(turtle)    #returns True if race was won
          if gameOver:
               break
          pygame.mixer.music.load(os.path.join(basedir,"bu-tasty-and-lively.it"))
          pygame.mixer.music.play(-1)
          if result:
               while len(turtleList)>=MAX_TURTLES_OWNED:
                    t=doSelect("DISCARD ONE TURTLE", discardCursor=True)
                    turtleList.remove(t)
               turtleList.append(doSelect("SELECT YOUR PRIZE",None,result))
               
          
          while len(turtleList)>=MAX_TURTLES_OWNED:
               t=doSelect("DISCARD ONE TURTLE", discardCursor=True)
               turtleList.remove(t)
          
          turtle1=None
          turtle2=None
          while turtle1==turtle2:
               turtle1=doSelect("BREED TWO TURTLES")
               turtle2=doSelect("BREED TWO TURTLES",turtle1)
          
          if doBreeding(turtle1,turtle2):  #bred new species?
               victory=True
               unlockedNewSpecies=True               
               gameOver=True
          
     if victory:
          doGameCompleted()     
     
          

          

#     windowSurface.blit(darwinSurface[frameOffset+player.frame],(player.xpos,player.ypos),None,BLEND_SUB)
#     elif gameState==STATE_RACE:
#          player.tick()
               
#          windowSurface.blit(darwinSurface[player.frame],(player.xpos,player.ypos))
         
    