from __future__ import print_function

# import math
import sys
import math

import cairo
import pygame

width, height = 600, 600


def drawCircle(cr, x, y, r):
    cr.arc(x, y, r, 0.0, 2.0 * math.pi)
    cr.stroke()
    if r > 0.004:
        drawCircle(cr, x + r, y, r / 2)
        drawCircle(cr, x - r, y, r / 2)
        drawCircle(cr, x, y + r, r / 2)
        drawCircle(cr, x, y - r, r / 2)


def draw(surface):
    ctx = cairo.Context(surface)
    ctx.scale(width, height)

    # background

    ctx.set_source_rgb(1, 1, 1)
    ctx.rectangle(0, 0, 1, 1)  # Rectangle(x0, y0, x1, y1)
    ctx.fill()

    ctx.set_source_rgb(1, 0, 0)
    ctx.set_line_width(0.001)
    drawCircle(ctx, 0.5, 0.5, 0.25)


def input(events):
    for event in events:
        if event.type == pygame.QUIT:
            sys.exit(0)
        else:
            print(event)


def main():
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)

    pygame.init()
    pygame.display.set_mode((width, height))
    screen = pygame.display.get_surface()

    draw(surface)

    # Create PyGame surface from Cairo Surface
    buf = surface.get_data()
    image = pygame.image.frombuffer(buf, (width, height), "ARGB")
    # Tranfer to Screen
    screen.blit(image, (0, 0))
    pygame.display.flip()

    while True:
        input(pygame.event.get())


if __name__ == "__main__":
    main()
