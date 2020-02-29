from __future__ import print_function

import sys
import math

import cairo
import pygame

width, height = 600, 600
mouseX, mouseY = 0, 0
mousePressed = False


def draw(surface):
    ctx = cairo.Context(surface)
    ctx.scale(width, height)

    # background

    ctx.set_source_rgb(1, 1, 1)
    ctx.rectangle(0, 0, 1, 1)  # Rectangle(x0, y0, x1, y1)
    ctx.fill()

    ctx.set_source_rgb(1, 0, 0)
    ctx.set_line_width(0.001)
    ctx.arc(0.5, 0.5, 0.25, 0.0, 2.0 * math.pi)
    ctx.stroke()

    if mousePressed:
        ctx.arc(mouseX, mouseY, 0.1, 0.0, 2.0 * math.pi)
        ctx.stroke()


def input(events):
    global mousePressed, mouseX, mouseY
    for event in events:
        if event.type == pygame.QUIT:
            sys.exit(0)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouseX, mouseY = pygame.mouse.get_pos()
            mouseX /= width
            mouseY /= height
            mousePressed = True
        else:
            mousePressed = False


def main():
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)

    pygame.init()
    pygame.display.set_mode((width, height))
    screen = pygame.display.get_surface()

    while True:
        input(pygame.event.get())
        draw(surface)
        # Create PyGame surface from Cairo Surface
        buf = surface.get_data()
        image = pygame.image.frombuffer(buf, (width, height), "ARGB")
        # Tranfer to Screen
        screen.blit(image, (0, 0))
        pygame.display.flip()


if __name__ == "__main__":
    main()
