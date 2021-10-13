import pygame
import math

pygame.init()
width, height = 960, 720
ctx = pygame.display.set_mode((width, height))

bgcolour = (15, 17, 27)
circlecolour = (255, 255, 255)
paddlecolour = (245, 111, 91)
multiplyer = 0.001
radius = 300
# x * x + y * y < r then inside circle

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
        self.x1 = 0
        self.y1 = 0
        self.x2 = 0
        self.y2 = 0
        self.center = pygame.math.Vector2(width / 2, height / 2)

    def findpoints(self):
        print()

    def draw(self):
        pygame.draw.polygon(ctx, self.colour, [(self.x, self.y), (self.x + self.paddlelength, self.y), (self.x + self.paddlelength, self.y + self.paddleheight), (self.x, self.y + self.paddleheight)])

        #pygame.draw.rect(ctx, self.colour, (self.x, self.y, self.paddlelength, self.paddleheight))

    def getCoordinates(self):
        self.x = self.r * math.cos(self.angle) + self.center.x - self.paddlelength / 2
        self.y = self.r * math.sin(self.angle) + self.center.y - self.paddleheight / 2

player = Paddle(radius, 100, 25, paddlecolour, 5)

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