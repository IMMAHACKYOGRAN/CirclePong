import pygame
import math
from pygame.constants import K_a, K_d
import pygame.gfxdraw
import numpy as mathbutbetter

pygame.init()
width, height = 960, 720
ctx = pygame.display.set_mode((width, height))

bgcolour = (15, 17, 27)
circlecolour = (255, 255, 255)
paddlecolour = (245, 111, 91)
ballcolour = (148, 178, 136)
multiplyer = 0.001
radius = 300
keys = [False, # Left
        False] # Right
#play = False

class Ball:
    def __init__(self, origin, r):
        self.origin = origin
        self.speed = 1
        self.r = r
        self.pos = pygame.math.Vector2(origin.x, origin.y)
        self.vel = pygame.math.Vector2(0, -0.1)
        self.left = self.pos.x - self.r / 2
        self.right = self.pos.x + self.r / 2
        self.top = self.pos.y + self.r / 2
        self.bottom = self.pos.y - self.r / 2
        
    def getVels(self):
        pass

    def move(self):
        self.pos.x += self.vel.x
        self.pos.y += self.vel.y
    
    def draw(self):
        pygame.draw.circle(ctx, ballcolour, self.pos, self.r)
    
    def inbounds(self):
        if math.sqrt(math.pow(self.pos.x - player.center.x, 2) + math.pow(self.pos.y - player.center.y, 2)) > radius:
            pass

class Paddle:
    def __init__(self, r, paddlelength, paddleheight, colour, sens):
        self.angle = 0
        self.r = r
        self.paddlelength = paddlelength
        self.paddleheight = paddleheight
        self.colour = colour
        self.sens = sens * multiplyer
        self.x = 0
        self.y = 0
        self.center = pygame.math.Vector2(width / 2, height / 2)
        self.points = [
            self.rotatepoint((self.x, self.y), self.angle, self.center), 
            self.rotatepoint((self.x + self.paddlelength, self.y), self.angle, self.center), 
            self.rotatepoint((self.x + self.paddlelength, self.y + self.paddleheight), self.angle, self.center), 
            self.rotatepoint((self.x, self.y + self.paddleheight), self.angle, self.center)]

    def getCollision(self):
        #update points
        self.points = [
            self.rotatepoint((self.x, self.y), self.angle, self.center), 
            self.rotatepoint((self.x + self.paddlelength, self.y), self.angle, self.center), 
            self.rotatepoint((self.x + self.paddlelength, self.y + self.paddleheight), self.angle, self.center), 
            self.rotatepoint((self.x, self.y + self.paddleheight), self.angle, self.center)]

        #find closest vertex to circle
        pointDists = []
        for point in self.points:
            dist = math.sqrt(math.pow(ball.pos.x - point[0], 2) + math.pow(ball.pos.y - point[1], 2))
            pointDists.append(dist)
        
        closestPoint = min(pointDists)
        #if distance to closest point on edge is less than ball.r {return true}
            #print("BALL HAS COLLIDED WITH THE PONG")

    def move(self):
        if keys[0] == True:
            if self.angle >= self.sens:
                self.angle -= self.sens
            else:
                self.angle = math.pi * 2 - self.sens

        if keys[1] == True:
            if self.angle <= math.pi * 2:
                self.angle += self.sens
            else:
                self.angle = 0 + self.sens

    def rotatepoint(self, point, angle, origin):
        x = math.cos(angle) * (point[0] - origin.x) - math.sin(angle) * (point[1] - origin.y) + origin.x
        y = math.sin(angle) * (point[0] - origin.x) + math.cos(angle) * (point[1] - origin.y) + origin.y
        return x, y

    def draw(self):
        pygame.gfxdraw.aapolygon(ctx, 
        [self.rotatepoint((self.x, self.y), self.angle, self.center), 
        self.rotatepoint((self.x + self.paddlelength, self.y), self.angle, self.center), 
        self.rotatepoint((self.x + self.paddlelength, self.y + self.paddleheight), self.angle, self.center), 
        self.rotatepoint((self.x, self.y + self.paddleheight), self.angle, self.center)], self.colour)

        pygame.draw.polygon(ctx, self.colour, 
        [self.rotatepoint((self.x, self.y), self.angle, self.center), #top left point
        self.rotatepoint((self.x + self.paddlelength, self.y), self.angle, self.center), #top right point
        self.rotatepoint((self.x + self.paddlelength, self.y + self.paddleheight), self.angle, self.center), #bottom right point 
        self.rotatepoint((self.x, self.y + self.paddleheight), self.angle, self.center)]) #bottom left point

        #pygame.draw.aaline(ctx, (255, 255, 0), ball.pos, (self.closestPoint, self.closestPoint))

    def getCoordinates(self): # Converts Polar coordinate to cartiesian.
        self.x = self.r * math.cos(self.angle / radius + radius) + self.center.x - self.paddlelength / 2
        self.y = self.r * math.sin(self.angle / radius + radius) + self.center.y

player = Paddle(radius, 150, 25, paddlecolour, 2)
ball = Ball(player.center, 10)

def render():
    ctx.fill(bgcolour)
    pygame.gfxdraw.aacircle(ctx, math.floor(player.center.x), math.floor(player.center.y), radius, circlecolour)
    player.draw()
    ball.draw()

def update():
    player.getCoordinates()
    player.move()
    ball.move()
    ball.inbounds()
    player.getCollision()
    render()

while True:

    update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == K_a:
                keys[0] = True
            if event.key == K_d:
                keys[1] = True
                
        if event.type == pygame.KEYUP:
            if event.key == K_a:
                keys[0] = False
            if event.key == K_d:
                keys[1] = False

    pygame.display.flip()

"""
============={bibliography}============= 
https://stackoverflow.com/questions/4465931/rotate-rectangle-around-a-point/13208761
https://www.w3schools.com/python/python_tuples.asp
https://www.pygame.org/docs/
https://www.pygame.org/docs/ref/draw.html#pygame.draw.polygon
https://www.youtube.com/watch?v=4y_nmpv-9lI
https://www.reddit.com/r/gamedev/comments/xtry1/circlepolygon_collison_using_sat/
https://www.youtube.com/watch?v=59BTXB-kFNs
https://www.youtube.com/watch?v=-EsWKT7Doww
https://www.youtube.com/watch?v=RBya4M6SWwk
https://stackoverflow.com/questions/3499026/find-a-minimum-value-in-an-array-of-floats
https://www.w3schools.com/python/python_arrays.asp
"""