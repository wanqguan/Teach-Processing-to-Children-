
import cairo
import pygame
import sys

from pygame.math import Vector2
from noise import pnoise2 as noise
from math import sin, cos, pi
from random import random
from copy import deepcopy


def Prandom(*arg):
    if len(arg) == 1:
        return random() * arg[0]
    else:
        a, b = arg
        return a + random() * (b - a)


def Pconstrain(amt, low, high):
    if amt < low:
        return low
    if amt > high:
        return high
    return amt


def Pmap(value, start1, stop1, start2, stop2):
    k = (stop2 - start2) / (stop1 - start1)
    return start2 + (value - start1) * k


def fill(*arg):
    if len(arg) == 3:
        ctx.set_source_rgb(*arg)
    elif len(arg) == 4:
        ctx.set_source_rgba(*arg)


def translate(x, y):
    ctx.translate(x/width, y/height)


def rotate(angle):
    ctx.rotate(angle)


def pushMatrix():
    ctx.save()


def popMatrix():
    ctx.restore()


def strokeWeight(k):
    ctx.set_line_width(k)


def circle(x, y, r):
    ctx.arc(x/width, y/height, r/width, 0.0, 2.0 * pi)
    ctx.stroke()


def rect(x, y, a, b):
    x /= width
    y /= height
    a /= width
    b /= height
    ctx.rectangle(x, y, a, b)
    ctx.stroke()


def line(x1, y1, x2, y2):
    ctx.move_to(x1/width, y1/height)
    ctx.line_to(x2/width, y2/height)
    ctx.stroke()


def background(*c):
    fill(*c)
    ctx.rectangle(0, 0, 1, 1)  # Rectangle(x0, y0, x1, y1)
    ctx.fill()


class PVector(Vector2):
    def __init__(self, x, y):
        super().__init__(x, y)

    def mult(self, k):
        self.__imul__(k)

    def get(self):
        return deepcopy(self)

    def limit(self, k):
        if self.length() > k:
            self.scale_to_length(k)

    def mag(self):
        return self.magnitude()

    def heading2D(self):
        return self.angle_to(PVector(0, 1))

    def add(self, *arg):
        if len(arg) == 1:
            self.__iadd__(arg[0])  # 这里对self赋值失败
            return self.get()
        elif len(arg) == 2:
            tmp = arg[0] + arg[1]
            return PVector(tmp.x, tmp.y)

    def sub(self, *arg):
        if len(arg) == 1:
            self -= arg[0]
            return self.get()
        elif len(arg) == 2:
            tmp = arg[0] - arg[1]
            return PVector(tmp.x, tmp.y)


class FlowField():
    def __init__(self, r):
        self.resolution = r
        # Determine the number of columns and rows based on sketch's width and height
        self.cols = width // r  # Attention
        self.rows = height // r
        self.field = []
        self.init()

    def init(self):
        self.field = []
        xoff = 0
        xrand = Prandom(0, 1)
        yrand = Prandom(0, 1)
        for i in range(self.cols):
            yoff = 0
            tmp = []
            for j in range(self.rows):
                theta = Pmap(noise(xoff+xrand, yoff+yrand), 0, 1, 0, 2 * pi)
                assert theta < 2 * pi
                # Polar to cartesian coordinate transformation to get x and y components of the vector
                tmp.append(PVector(cos(theta), sin(theta)))
                yoff += 0.01
            self.field.append(tmp)
            xoff += 0.01

    def display(self):
        # fill(0, 1, 0)
        for i in range(self.cols):
            for j in range(self.rows):
                self.drawVector(
                    self.field[i][j], i * self.resolution, j * self.resolution, self.resolution - 2)

    def drawVector(self, v, x, y, scayl):
        pushMatrix()
        translate(x, y)
        rotate(v.heading2D())
        leg = v.mag()*scayl
        line(0, 0, leg, 0)
        arrowsize = 4
        line(leg, 0, leg-arrowsize, +arrowsize/2)
        line(leg, 0, leg-arrowsize, -arrowsize/2)
        popMatrix()

    def lookup(self, lookup):
        column = int(Pconstrain(lookup.x / self.resolution, 0, self.cols - 1))
        row = int(Pconstrain(lookup.y / self.resolution, 0, self.rows - 1))
        return self.field[column][row].get()


class Vehicle(object):
    """ generated source for class Vehicle """

    def __init__(self, l, ms, mf):
        """ generated source for method __init__ """
        self.location = l.get()
        self.r = 3.0
        self.maxspeed = ms
        self.maxforce = mf
        self.acceleration = PVector(0, 0)
        self.velocity = PVector(0, 0)

    def run(self):
        """ generated source for method run """
        self.update()
        self.borders()
        self.display()

    #  Implementing Reynolds' flow field following algorithm
    #  http://www.red3d.com/cwr/steer/FlowFollow.html
    def follow(self, flow):
        """ generated source for method follow """
        #  What is the vector at that spot in the flow field?
        desired = flow.lookup(self.location)
        #  Scale it up by maxspeed
        desired.mult(self.maxspeed)
        #  Steering is desired minus velocity
        steer = PVector.sub(desired, self.velocity)
        steer.limit(self.maxforce)
        #  Limit to maximum steering force
        self.applyForce(steer)

    def applyForce(self, force):
        """ generated source for method applyForce """
        #  We could add mass here if we want A = F / M
        self.acceleration.add(force)

    #  Method to update location
    def update(self):
        """ generated source for method update """
        #  Update velocity
        self.velocity.add(self.acceleration)
        #  Limit speed
        self.velocity.limit(self.maxspeed)
        self.location.add(self.velocity)
        #  Reset accelertion to 0 each cycle
        self.acceleration.mult(0)

    def display(self):
        """ generated source for method display """
        #  Draw a triangle rotated in the direction of velocity
        circle(self.location.x, self.location.y, 5)

    #  Wraparound
    def borders(self):
        """ generated source for method borders """
        if self.location.x < -self.r:
            self.location.x = width + self.r
        if self.location.y < -self.r:
            self.location.y = height + self.r
        if self.location.x > width + self.r:
            self.location.x = -self.r
        if self.location.y > height + self.r:
            self.location.y = -self.r


def input(events):
    global mousePressed, mouseX, mouseY
    for event in events:
        if event.type == pygame.QUIT:
            sys.exit(0)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouseX, mouseY = pygame.mouse.get_pos()
            mousePressed = True
        else:
            mousePressed = False


width, height = 600, 600
mouseX, mouseY = 0, 0
mousePressed = False

debug = True
flowfield = FlowField(20)
vehicles = []
for i in range(120):
    vehicles.append(Vehicle(PVector(Prandom(width), Prandom(
        height)), Prandom(2, 5), Prandom(0.1, 0.5)))


def update():
    input(pygame.event.get())
    background(1, 1, 1)
    fill(1, 0, 0)
    strokeWeight(0.003)
    # flowfield.display()
    for v in vehicles:
        v.follow(flowfield)
        v.run()
    if mousePressed:
        flowfield.init()
        circle(mouseX, mouseY, 20)


def main():
    global ctx
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)

    pygame.init()
    pygame.display.set_mode((width, height))
    screen = pygame.display.get_surface()

    ctx = cairo.Context(surface)
    ctx.scale(width, height)

    while True:
        update()
        # Create PyGame surface from Cairo Surface
        buf = surface.get_data()
        image = pygame.image.frombuffer(buf, (width, height), "ARGB")
        # Tranfer to Screen
        screen.blit(image, (0, 0))
        pygame.display.flip()


if __name__ == "__main__":
    main()
