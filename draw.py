#! /usr/bin/env python

"""draw functions used to draw the controls"""

import pygame

def rounded_rect(target_surf, rect, color, width, radius):
    """draw a rounded rectangle

    radius is the amount of rounding at the edges, and width is the thickness of the edges
    if the width argument is 0, the rectangle will be filled.
    """
    #set a colorkey to prevent drawing the background
    colorkey = (0,0,0) if color != (0,0,0) else (255, 255, 255)
    #prepare the circle
    r = rect
    circle = pygame.Surface((radius*2, radius*2))
    circle.convert_alpha()
    circle.fill(colorkey)
    pygame.draw.circle(circle, color, (radius, radius), radius, width)
    #prepare the surface
    surf = pygame.Surface(r.size)
    surf.convert_alpha()
    surf.fill(colorkey)
    surf_rect = surf.get_rect()
    surf_rect.inflate_ip(-width+1, -width+1)

    #draw the rectangle and circle corners
    pygame.draw.rect(surf, color, surf_rect, width)
    surf.blit(circle, (0, 0), pygame.Rect((0, 0), (radius, radius)))
    surf.blit(circle, (0, r.h - radius), pygame.Rect((0, radius), (radius, radius)))
    surf.blit(circle, (r.w - radius, 0), pygame.Rect((radius, 0), (radius, radius)))
    surf.blit(circle, (r.w - radius, r.h - radius), pygame.Rect((radius, radius), (radius, radius)))
    surf.set_colorkey(colorkey)

    target_surf.blit(surf, rect)
