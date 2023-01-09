import sys
import pygame
import numpy as np
import cv2
import random
import os, math

# Configuration
pygame.init()
fps = 60
fpsClock = pygame.time.Clock()
width, height = 640, 480
screen = pygame.display.set_mode((width, height))
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PINK = (255,192,203)
PURPLE=(162,25,255)

font = pygame.font.SysFont('Arial', 40)

objects = []

class Button():
    def __init__(self, x, y, width, height, buttonText='Button', onclickFunction=None, onePress=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.onePress = onePress
        self.alreadyPressed = False

        self.fillColors = {
            'normal': '#ffffff',
            'hover': '#666666',
            'pressed': '#333333',
        }
        
        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.buttonSurf = font.render(buttonText, True, (20, 20, 20))
        
        objects.append(self)
        
    def process(self):
        mousePos = pygame.mouse.get_pos()
        self.buttonSurface.fill(self.fillColors['normal'])
        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.fillColors['hover'])
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.buttonSurface.fill(self.fillColors['pressed'])
                if self.onePress:
                    self.onclickFunction()
                elif not self.alreadyPressed:
                    self.onclickFunction()
                    self.alreadyPressed = True
            else:
                self.alreadyPressed = False
                
        self.buttonSurface.blit(self.buttonSurf, [
        self.buttonRect.width/2 - self.buttonSurf.get_rect().width/2,
        self.buttonRect.height/2 - self.buttonSurf.get_rect().height/2
        ])
        screen.blit(self.buttonSurface, self.buttonRect)    
        
def myFunction():
    
    def getline(canvas,x0,y0,x1,y1,color):
        # |기울기|<1 --> y =  (x-x0) * (y1-y0) / (x1-x0) +y0
        # |기울기|>1 --> x = (y-y0) * (x1-x0)/(y1-y0) +x0
        if(abs(x1-x0)<abs(y1-y0)): #|기울기|>1인 경우
            if(y1==y0):
                y = y0
                if(x0<x1):
                    for x in range(x0,x1+1):
                        canvas[int(y),int(x)] = color
                else:
                    for x in range(x0,x1-1,-1):
                        canvas[int(y),int(x)] = color
            else:
                if(y0<y1):
                    for y in range(y0,y1+1):
                        x = (y-y0) * (x1-x0)/(y1-y0) +x0
                        canvas[int(y),int(x)] = color
                else:
                    for y in range(y0,y1-1,-1):
                        x = (y-y0) * (x1-x0)/(y1-y0) +x0
                        canvas[int(y),int(x)] = color
    
        else:#|기울기|<=1인 경우
            if(x1==x0):
                x = x0
                if(y0<y1):
                    for y in range(y0,y1+1):
                        canvas[int(y),int(x)] = color
                else:
                    for y in range(y0,y1-1,-1):
                        canvas[int(y),int(x)] = color
            
            else:
                if(x0<x1):
                    for x in range(x0,x1+1):
                        y =  (x-x0) * (y1-y0) / (x1-x0) +y0
                        canvas[int(y),int(x)] = color
                        
                else:
                    for x in range(x0,x1-1,-1):
                        y =  (x-x0) * (y1-y0) / (x1-x0) +y0
                        canvas[int(y),int(x)] = color
                        
    def deg2rad(deg):
        rad = deg*np.pi/180.0
        return rad
    
    def makeTmat(a,b):
        Tmat = np.eye(3,3)
        Tmat[0,2] = a
        Tmat[1,2] = b
        return Tmat
        
    def makeRmat(degree):
        rad = deg2rad(degree)
        c = np.cos(rad)
        s = np.sin(rad)
        Rmat = np.eye(3,3)
        Rmat[0,0] = c
        Rmat[0,1] = -s
        Rmat[1,0] = s
        Rmat[1,1] = c
        
        return Rmat

    def drawPolygon(canvas,pts,color):
        num = pts.shape[0]
        for i in range(num-1):
            getline(canvas,pts[i,0],pts[i,1],pts[i+1,0],pts[i+1,1],color)   
        getline(canvas,pts[0,0],pts[0,1],pts[-1,0],pts[-1,1],color)   


    def Next(p,theta):
        next = p @makeTmat(200,0)@makeTmat(0,35)@makeRmat(theta)@makeTmat(0,-35)
        return next

    def Re_point(Q,point):
        Q = Q @ point
        Q = np.delete(Q,2,axis=0)
        Q = Q.T
        Q = Q.astype('int')
        return Q
    
    def main():
        width,height = 1200,1200
        color = (0, 0, 255)
        canvas = np.zeros((height,width,3),dtype='uint8')
        rect=[]
        rect.append((0,0))
        rect.append((200,0))
        rect.append((200,70))
        rect.append((0,70))
        rect = np.array(rect)
        
        point = rect.copy()
        l = np.ones(4)
        point = point.T
        point = np.append(point,[l],axis=0)

        
        while True:
            canvas = np.zeros((height,width,3),dtype='uint8')
            theta = random.randint(-40,70)
            P = makeTmat(200,750)@makeRmat(-90)
            Q1 = Next(P,theta)
            Q2 = Next(Q1,random.randint(10,60))
            Q3 = Next(Q2,random.randint(20,60))
            Q4 = Next(Q3,random.randint(-30,50))
        
            P = Re_point(P,point)
            Q1 = Re_point(Q1,point)
            Q2 = Re_point(Q2,point)
            Q3 = Re_point(Q3,point)
            Q4 = Re_point(Q4,point)
            
            drawPolygon(canvas,P,color)
            drawPolygon(canvas,Q1,color)
            drawPolygon(canvas,Q2,color)
            drawPolygon(canvas,Q3,color)
            drawPolygon(canvas,Q4,color)
            
            cv2.imshow("dispWindow",canvas)
            if cv2.waitKey(100)==27:
                break
            
    if __name__ =="__main__":
        main()

def myFunction1():
    
    def Rmat(degree):
        radian = np.deg2rad(degree)
        c = np.cos(radian)
        s = np.sin(radian)
        R = np.array([[c,-s,0],[s,c,0],[0,0,1]])
        return R

    def Tmat(a,b):
        H = np.eye(3)
        H[0,2] = a
        H[1,2] = b
        return H

    def remove3thDim(pp):
        q = pp[0:2, :].T
        return q

    poly = np.array([[0,0,1],[100,0,1],[100,20,1],[0,20,1]])     
    poly = poly.T

    def makeRect(width,height):
        newbox = np.array([[0,0,1],[100,0,1],[100,20,1],[0,20,1]])
        return newbox

    cor = np.array([10,10,1])

    def main():
        
        pygame.init()

        screen = pygame.display.set_mode((width, height))

        pygame.display.set_caption("Robort arm_keyboard")

        clock = pygame.time.Clock()
 

        done = False

        degree1 = -90
        degree2 = 30
        degree3 = 40
        
        
        base = makeRect(120,120)
        baseH = Tmat(width/2-100,height-50)
        basePart = remove3thDim(baseH @ base.T)
        
        firstArmL = 120
        secondArmL = 120
        thirdArmL = 120    
        
        firstArmB = makeRect(firstArmL, 20)
        secondArmB = makeRect(secondArmL, 20)
        thirdArmB = makeRect(thirdArmL, 20)
        
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
            
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                degree1 += -1     
            if keys[pygame.K_RIGHT]:
                degree1 += +1  
            if keys[pygame.K_UP]:
                degree2 += -1       
            if keys[pygame.K_DOWN]:
                degree2 += +1       
            if keys[pygame.K_x]:
                degree3 += -1     
            if keys[pygame.K_y]:
                degree3 += +1 
            if keys[pygame.K_w]:
                thirdArmL += 1
            if keys[pygame.K_z]:
                thirdArmL += -1
                               

            if degree1 > -10:
                degree1 = -10
            elif degree1 < -170:
                degree1 = -170
                
            FirstH = baseH @ Tmat(50,0) @ Rmat(degree1) @ Tmat(-10,-10)
            SecondH = FirstH @ Tmat(firstArmL, 0) @ Tmat(-10, 10) @ Rmat(degree2) @ Tmat(-10,-10)
            ThirdH = SecondH @ Tmat(secondArmL, 0) @ Tmat(-10, 10) @ Rmat(degree3) @ Tmat(-10,-10)
            
            
            firstPart = remove3thDim(FirstH @ firstArmB.T)
            secondPart = remove3thDim(SecondH @ secondArmB.T)
            thirdPart = remove3thDim(ThirdH @ thirdArmB.T)
            
            
            
            screen.fill((60,0,100))
            
            pygame.draw.polygon(screen, BLACK, basePart,0)
            pygame.draw.polygon(screen, (210,145,255), firstPart, 0)
            pygame.draw.polygon(screen, PURPLE, secondPart, 0)
            pygame.draw.polygon(screen, PINK, thirdPart, 0)
            
            font = pygame.font.SysFont('Arial', 20)
            
            text1 = font.render("press up and down key -> move 2 joint", True,WHITE)
            text2 = font.render("press right and left key -> move 3 joint", True,WHITE)
            text3 = font.render("press x and y -> move 1 joint", True,WHITE)
            
            screen.blit(text3,(10,10))
            screen.blit(text1,(10,40))
            screen.blit(text2,(10,70))
            
            pygame.display.flip()
            clock.tick(60)
        
    if __name__ == "__main__" :
        main()      
        pygame. quit()
        
                
              
Button(30, 30, 400, 100, 'CONTROL MODE1', myFunction)
Button(30, 140, 400, 100, 'CONTROL MODE2', myFunction1)




while True:
    screen.fill((20, 20, 20))
    text1 = font.render("CONTROL MODE1 -> AUTO", True,WHITE)
    text2 = font.render("CONTROL MODE2 -> KEYBOARD", True,WHITE)  
    screen.blit(text1,(10,250))
    screen.blit(text2,(10,300))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    for object in objects:
        object.process()
    pygame.display.flip()
    fpsClock.tick(fps)
        