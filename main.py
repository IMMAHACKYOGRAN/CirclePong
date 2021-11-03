import pygame
import math
from pygame.constants import K_a, K_d, K_SPACE
import pygame.gfxdraw
import sys

pygame.init()
width, height = 960, 720
ctx = pygame.display.set_mode((width, height))
pygame.font.init()
text = pygame.font.SysFont('arial', 255)

bgcolour = (15, 17, 27)
circlecolour = (255, 255, 255)
paddlecolour = (245, 111, 91)
ballcolour = (148, 178, 136)
multiplyer = 0.001
radius = 300
keys = [False, #left
        False, #right
        False] #interact

class Ball:
    def __init__(self, origin, r):
        self.origin = origin
        self.speed = 0
        self.r = r
        self.angle = 0
        self.pos = pygame.math.Vector2(origin.x, origin.y)
        self.lastpos = pygame.math.Vector2(0, 0)

    def move(self):
        self.lastpos.x = self.pos.x
        self.lastpos.y = self.pos.y
        self.pos.x += math.sin(self.angle) * self.speed
        self.pos.y += math.cos(self.angle) * self.speed
    
    def draw(self):
        pygame.draw.circle(ctx, ballcolour, self.pos, self.r)
    
    def inbounds(self):
        if math.sqrt(math.pow(self.pos.x - player.center.x, 2) + math.pow(self.pos.y - player.center.y, 2)) > radius:
            player.init()

    def changeVels(self):
        if player.isColliding(self.pos, self.r, player.points):
            while player.isColliding(self.pos, self.r, player.points):
                self.pos.x -= math.sin(self.angle) * self.speed
                self.pos.y -= math.cos(self.angle) * self.speed
            self.angle = player.angle - 2 * (self.angle)
            print(self.angle)
            player.score += 1

class Paddle:
    def __init__(self, r, paddlelength, paddleheight, colour, sens):
        self.angle = 0
        self.score = 0
        self.r = r
        self.paddlelength = paddlelength
        self.paddleheight = paddleheight
        self.colour = colour
        self.sens = sens * multiplyer
        self.x = 0
        self.y = 0
        self.normal = (0, 0)
        self.depth = sys.float_info.max
        self.center = pygame.math.Vector2(width / 2, height / 2)
        self.points = []

    def projectVerticies(self, verticies, axis):
        min = sys.float_info.max
        max = sys.float_info.min

        for i in range(len(verticies)):
            v = verticies[i]
            projection = dot(v, axis)
            if projection < min: min = projection
            if projection > max: max = projection
            
        return min, max

    def projectCircle(self, pos, r, axis):
        direction = customNomalize(axis)
        DAR = (direction[0] * r, direction[1] * r)
        p1 = (pos[0] + DAR[0], pos[1] + DAR[1])
        p2 = (pos[0] - DAR[0], pos[1] - DAR[1])

        min = dot(p1, axis)
        max = dot(p2, axis)

        #Failsafe for if the value are somehow swaped
        if min > max:
            a = min
            min = max
            max = a

        return min, max

    def getClosestPoint(self, circlepos, verticies):
        r = -1
        minDist = sys.float_info.max
        for i in range(len(verticies)):
            v = verticies[i]
            dist = (math.sqrt(math.pow(v[0], 2) + math.pow(circlepos.x, 2)), math.sqrt(math.pow(v[1], 2) + math.pow(circlepos.y, 2)))

            if(dist[0] < minDist and dist[1] < minDist):
                minDist = dist
                r = i

            return r

    def findCenter(self, verticies):
        sx = 0
        sy = 0
        for i in range(len(verticies)):
            v = verticies[i]
            sx += v[0]
            sy += v[1]
        
        return (sx / len(verticies), sy / len(verticies))

    def isColliding(self, circlepos, circler, verticies):
        self.normal = (0, 0)
        self.depth = sys.float_info.max
        axis = (0, 0)
        axisDepth = 0

        for i in range(len(verticies)):
            a = verticies[i]
            b = verticies[(i + 1) % len(verticies)]
            edge = (b[0] - a[0], b[1] - a[1])
            axis = (-edge[1], edge[0])

            cv = self.projectCircle(circlepos, circler, axis)
            pv = self.projectVerticies(verticies, axis)

            if pv[0] >= cv[1] or cv[0] >= pv[1]:
                return False

            axisDepth = min(cv[1] - pv[0], pv[1] - cv[0])

            if axisDepth < self.depth:
                self.depth = axisDepth
                self.normal = axis

        cpi = self.getClosestPoint(circlepos, verticies)       
        cpv = verticies[cpi]

        axis = (cpv[0] - circlepos[0], cpv[1] - circlepos[1])

        cv = self.projectCircle(circlepos, circler, axis)
        pv = self.projectVerticies(verticies, axis)

        if pv[0] >= cv[1] or cv[0] >= pv[1]:
            return False

        axisDepth = min(cv[1] - pv[0], pv[1] - cv[0])

        if axisDepth < self.depth:
            self.depth = axisDepth
            self.normal = axis

        self.depth /= math.sqrt(self.normal[0] * self.normal[0] + self.normal[1] * self.normal[1])
        self.normal = customNomalize(self.normal)

        polygonCenter = self.findCenter(verticies)

        direction = (polygonCenter[0] - circlepos.x, polygonCenter[1] - circlepos.y)

        if dot(direction, self.normal) < 0:
            self.normal[0] - 2 * self.normal[0]
            self.normal[1] - 2 * self.normal[1]
        
        return True

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

        if keys[2] == True:
            ball.speed = 0.1

    def rotatepoint(self, point, angle, origin):
        x = math.cos(angle) * (point[0] - origin.x) - math.sin(angle) * (point[1] - origin.y) + origin.x
        y = math.sin(angle) * (point[0] - origin.x) + math.cos(angle) * (point[1] - origin.y) + origin.y
        return x, y

    def updatePoints(self):
        self.points = [
            self.rotatepoint((self.x, self.y), self.angle, self.center), 
            self.rotatepoint((self.x + self.paddlelength, self.y), self.angle, self.center), 
            self.rotatepoint((self.x + self.paddlelength, self.y + self.paddleheight), self.angle, self.center), 
            self.rotatepoint((self.x, self.y + self.paddleheight), self.angle, self.center)]

    def draw(self):
        pygame.gfxdraw.aapolygon(ctx, self.points, self.colour)
        pygame.draw.polygon(ctx, self.colour, self.points)

    def getCoordinates(self): # Converts Polar coordinate to cartiesian.
        self.x = self.r * math.cos(self.angle / radius + radius) + self.center.x - self.paddlelength / 2
        self.y = self.r * math.sin(self.angle / radius + radius) + self.center.y

    def init(self):
        self.angle = 0
        self.score = 0
        self.x = 0
        self.y = 0
        self.normal = (0, 0)
        self.depth = sys.float_info.max
        self.center = pygame.math.Vector2(width / 2, height / 2)
        ball.angle = 0
        ball.speed = 0
        ball.pos = pygame.math.Vector2(ball.origin.x, ball.origin.y)
        ball.lastpos = pygame.math.Vector2(0, 0)

player = Paddle(radius, 150, 25, paddlecolour, 2)
ball = Ball(player.center, 10)

#Custom normalize function cuz python is bad and doesnt have one built in
def customNomalize(v):
    length = math.sqrt(math.pow(v[0], 2) + math.pow(v[1], 2))
    return (v[0] / length, v[1] / length)

#Custom dot product function cuz python is bad and doesnt have one built in
def dot(a, b):
    return a[0] * b[0] + a[1] * b[1]

def render():
    ctx.fill(bgcolour)
    pygame.gfxdraw.aacircle(ctx, math.floor(player.center.x), math.floor(player.center.y), radius, circlecolour)
    renderscore = text.render(str(player.score), True, (255, 255, 255))
    ctx.blit(renderscore, (width / 2 - text.get_linesize() / 4, height / 2 - text.get_height() / 2))
    player.draw()
    ball.draw()

def update():
    player.getCoordinates()
    player.updatePoints()
    player.move()
    ball.move()
    ball.changeVels()
    ball.inbounds()
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
            if event.key == K_SPACE:
                keys[2] = True

                
        if event.type == pygame.KEYUP:
            if event.key == K_a:
                keys[0] = False
            if event.key == K_d:
                keys[1] = False
            if event.key == K_SPACE:
                keys[2] = False

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
https://www.youtube.com/watch?v=vWs33LVrs74
"""
