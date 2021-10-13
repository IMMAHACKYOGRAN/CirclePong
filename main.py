import pygame
import math

pygame.init()
width, height = 960, 720
ctx = pygame.display.set_mode((width, height))

bgcolour = (15, 17, 27)
circlecolour = (255, 255, 255)
paddlecolour = (245, 111, 91)
multiplyer = 0.0001
radius = 300
# x * x + y * y < r then inside circle

class Paddle:
    def __init__(self, r, paddlelength, paddleheight, colour, sens):
        self.angle = 0 # POLAR COORDINATE
        self.facing = 0 # WHERE IT IS LOOKING, NOT THE SAME AS WHERE IT IS
        self.r = r
        self.paddlelength = paddlelength
        self.paddleheight = paddleheight
        self.colour = colour
        self.sens = sens * multiplyer
        self.x = 0
        self.y = 0
        self.center = pygame.math.Vector2(width / 2, height / 2)

    def rotatepoint(self, point, angle, origin):
        x = math.cos(angle) * (point[0] - origin.x) - math.sin(angle) * (point[1] - origin.y) + origin.x
        y = math.sin(angle) * (point[0] - origin.x) + math.cos(angle) * (point[1] - origin.y) + origin.y
        return x, y

    def draw(self):
        print(self.angle)
        pygame.draw.polygon(ctx, self.colour, 
        [self.rotatepoint((self.x, self.y), self.angle, self.center), 
        self.rotatepoint((self.x + self.paddlelength, self.y), self.angle, self.center), 
        self.rotatepoint((self.x + self.paddlelength, self.y + self.paddleheight), self.angle, self.center), 
        self.rotatepoint((self.x, self.y + self.paddleheight), self.angle, self.center)])

        #pygame.draw.rect(ctx, self.colour, (self.x, self.y, self.paddlelength, self.paddleheight))

    def getCoordinates(self):
        self.x = self.r * math.cos(self.angle / radius + radius) + self.center.x - self.paddlelength / 2
        self.y = self.r * math.sin(self.angle / radius + radius) + self.center.yS

player = Paddle(radius, 150, 25, paddlecolour, 5)

def render():
    ctx.fill(bgcolour)
    pygame.draw.circle(ctx, circlecolour, player.center, radius, 3)

def update():    
    if player.angle >= player.sens:
        player.angle -= player.sens
    else:
        player.angle = math.pi * 2
    player.getCoordinates()
    render()
    
    player.draw()

while True:

    update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
    pygame.display.flip()

""" 
============={bibliography}============= 
https://stackoverflow.com/questions/4465931/rotate-rectangle-around-a-point/13208761
https://www.w3schools.com/python/python_tuples.asp
https://www.pygame.org/docs/
https://www.pygame.org/docs/ref/draw.html#pygame.draw.polygon
"""