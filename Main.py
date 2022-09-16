
import pygame
import math 
from Engine import Engine
engine = Engine()
global screen
playing = True
engine.update_dt()
#setup pygame window
def draw():
    screen = pygame.display.set_mode((1540,820))
    screen.fill((255,255,255))
    return screen

def calculateDistances(velocity,angle,gravity,height):
    initialHoriVelocity = (velocity * math.cos(angle * 2 * math.pi/360))
    initialVertVelocity = (velocity * math.sin(angle * 2 * math.pi/360))
    finalVerticalVelocity = -1*(math.sqrt(initialVertVelocity**2 + 2 * gravity * height * -1))
    flightTime = (finalVerticalVelocity-initialVertVelocity)/gravity
    horiDistance = initialHoriVelocity * flightTime
    timeOfVertDistance = (velocity*-1)/gravity
    vertDistance = (velocity * timeOfVertDistance + 0.5*gravity*timeOfVertDistance**2)+height
    print(vertDistance)
    return (horiDistance,vertDistance)

def calculateScale(horiDistance,vertDistance,height):
    multi = max((math.ceil(vertDistance/800)),(math.ceil(height/800)),(math.ceil(horiDistance/1500)))
    tempXScales = [300,600,900,1200,1500]
    tempYScales = [200,400,600,800]
    xScales = [item * multi for item in tempXScales]
    xScales = [str(scale) for scale in xScales]
    yScales = [item * multi for item in tempYScales]
    yScales = [str(scale) for scale in yScales]
    return (xScales,yScales,multi)

def scaleValues(xVelocity,yVelocity,gravity,multi,height):
    xVelocity = xVelocity/multi
    yVelocity = yVelocity/multi
    gravity = gravity/multi
    height = height/multi
    return(xVelocity,yVelocity,gravity,height)

#calculate new positions of circle subroutine
def calculateCircle(X,Y,xVelocity,yVelocity,xAcceleration,yAcceleration,multi):
    NradianAngle = (math.atan(yVelocity/xVelocity))
    NcircleX = X +(xVelocity * engine.dt * multi)
    NcircleY = Y +(yVelocity * engine.dt * multi)
    NcircleXVelocity = xVelocity+(xAcceleration * engine.dt * multi)
    NcircleYVelocity = yVelocity+(yAcceleration * engine.dt * multi)
    return (NcircleX,NcircleY,NcircleXVelocity,NcircleYVelocity,NradianAngle)

def drawBg(screen):
    bgImage = pygame.image.load('Grid.png')
    screen.blit(bgImage,(0,20))

def drawYText(screen,scales):
    pygame.font.init()
    font = pygame.font.SysFont("Arial",20)
    count = 1
    for scale in scales:
        text = font.render(scale,True,(0,0,0),(255,255,255))
        textBox = text.get_rect()
        textBox.center = (30,820-200*count)
        screen.blit(text,textBox)
        count += 1

def drawXText(screen,scales):
    pygame.font.init()
    font = pygame.font.SysFont("Arial",20)
    count = 1
    for scale in scales:
        text = font.render(scale,True,(0,0,0),(255,255,255))
        textBox = text.get_rect()
        textBox.center = (300*count,800)
        screen.blit(text,textBox)
        count+=1

def drawValues(screen,circleX,circleY,circleXVelocity,circleYVelocity,multi,circleSize):
    tempFloatValues = [circleX,circleY - circleSize,circleXVelocity,circleYVelocity]
    floatValues = [(value * multi)for value in tempFloatValues]
    valueNames = ["circleX  =  ","circleY  =  ","circleXVelocity  =  ","circleYVelocity  =  "]
    roundedValues = [round(value,3)for value in floatValues]
    values = [str(value) for value in roundedValues]
    pygame.font.init()
    font=pygame.font.SysFont("Arial",20)
    for i in range(0,len(values)):
        text = font.render(valueNames[i],True,(0,0,0),(255,255,255))
        textBox = text.get_rect()
        textBox.center = (1300,(i+2)*20)
        screen.blit(text,textBox)
        text = font.render(values[i],True,(0,0,0),(255,255,255))
        textBox = text.get_rect()
        textBox.center = (1450,(i+2)*20)
        screen.blit(text,textBox)



#draw repositioned circle subroutine
def updateCircle(circleX,circleY,circleXVelocity,circleYVelocity,radianAngle,height,xScales,yScales,circleSize,multi):
    screen = draw()
    drawBg(screen)
    drawValues(screen,circleX,circleY,circleXVelocity,circleYVelocity,multi,circleSize)
    drawXText(screen,xScales)
    drawYText(screen,yScales)
    pygame.draw.rect(screen,(0,10,10),(0,820-height,20,height))
    pygame.draw.circle(screen,(255,0,0),(circleX,820-circleY),(circleSize))
    pygame.draw.line(screen,(0,255,0),(circleX,820-circleY),(circleX + circleXVelocity,820-circleY),width = 2)
    pygame.draw.line(screen,(0,0,255),(circleX,820-circleY),(circleX,820-(circleY + circleYVelocity)),width = 2)
    pygame.draw.line(screen,(255,0,255),(circleX,820-circleY),(circleX+circleXVelocity,820-(circleY + circleYVelocity)),width = 2)
    pygame.draw.polygon(screen,(0,255,00),points = [(circleX + circleXVelocity,820-circleY-5),(circleX + circleXVelocity,820-circleY+5),(circleX+circleXVelocity+7,820-circleY)])
    pygame.draw.polygon(screen,(255,0,255),points=[(circleX +circleXVelocity - (5*math.cos((180*math.pi/360)-radianAngle)),820-(circleY + circleYVelocity + (5*math.sin((180*math.pi/360)-radianAngle)))),(circleX +circleXVelocity + (5*math.cos((180*math.pi/360)-radianAngle)),820-(circleY + circleYVelocity - (5*math.sin((180*math.pi/360)-radianAngle)))),(circleX + circleXVelocity + 7*math.cos(radianAngle),(820-(circleY + circleYVelocity + 7*math.sin(radianAngle))))])
    if circleYVelocity > 0:
        pygame.draw.polygon(screen,(0,0,255),points=[(circleX-5,820-(circleY+circleYVelocity)),(circleX+5,820-(circleY+circleYVelocity)),(circleX,820-(circleY+circleYVelocity+7))])
    else:
        pygame.draw.polygon(screen,(0,0,255),points=[(circleX-5,820-(circleY+circleYVelocity)),(circleX+5,820-(circleY+circleYVelocity)),(circleX,820-(circleY+circleYVelocity-7))])
    pygame.display.update()

def calculateCircleSize(multi):
    circleSize = 20/multi
    return(circleSize)


#calculate velocity components subroutine
def calculateVelocities(angle,velocity):
    radianAngle =  (float(angle) * 2 *(math.pi))/360
    xVelocity = float(velocity) * (math.cos(radianAngle))
    yVelocity = float(velocity) * (math.sin(radianAngle))
    return (xVelocity,yVelocity,radianAngle)



#final adjustments subroutine
def finalAdjustments(Y,YVelocity,XVelocity,circleSize):
    remainingY = circleSize-Y
    timeRemaining = (remainingY/YVelocity)
    remainingX = timeRemaining * XVelocity
    return (remainingX,remainingY)

