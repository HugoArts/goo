#! /usr/bin/env python

"""draw functions used to draw the controls"""

import pygame, goo.style
import math

def alpha_surface(*args):
    """return a transparent surface

    return a surface with per-pixel alpha, cleared to (0, 0, 0, 0) (completely transparent).
    It takes the same arguments as pygame.Surface.
    """
    surface = pygame.Surface(*args)
    surface = surface.convert_alpha()
    surface.fill((0, 0, 0, 0))
    return surface

def circle(target_surf, color, pos, radius, width=0):
    """draw a circle

    drawing a circle with a width other than zero has weird results. Therefore this alternate method
    """
    alpha = color[3] if len(color) == 4 else 255
    colorkey = (0, 0, 0) if color[:3] != (0, 0, 0) else (255, 255, 255)
    s = pygame.Surface((radius*2+2, radius*2+2))
    s.fill(colorkey)
    pygame.draw.circle(s, color, (radius, radius), radius)
    if width > 0:
        pygame.draw.circle(s, colorkey, (radius, radius), radius - width)

    s.set_colorkey(colorkey)
    s.set_alpha(alpha)
    target_surf.blit(s, (pos[0] - radius, pos[1] - radius))

def rounded_rect(target_surf, rect, style):
    """draw a rounded rectangle

    the style argument can be either a tuple in the form of (color, width, radius) or a goo Style object 
    """
    #select best possible draw function
    if isinstance(style, goo.style.Style):
        color, width, radius = style['border_color'], style['border_width'], style['border_radius']
    else:
        color, width, radius = style
    draw_circle = pygame.draw.circle if width <= 1 else circle
    alpha = color[3] if len(color) == 4 else 255 
    colorkey = (0,0,0) if color[:3] != (0,0,0) else (255, 255, 255)
    r = rect

    #prepare the circle
    circ = pygame.Surface((radius*2, radius*2))
    circ.fill(colorkey)
    draw_circle(circ, color, (radius, radius), radius, width)

    #prepare the surface
    surf = pygame.Surface(r.size)
    surf.fill(colorkey)
    surf_rect = surf.get_rect()
    surf_rect.inflate_ip(-width+1, -width+1)

    #draw the rectangle and circle corners
    pygame.draw.rect(surf, color, surf_rect, width)
    surf.blit(circ, (0, 0), pygame.Rect((0, 0), (radius, radius)))
    surf.blit(circ, (0, r.h - radius), pygame.Rect((0, radius), (radius, radius)))
    surf.blit(circ, (r.w - radius, 0), pygame.Rect((radius, 0), (radius, radius)))
    surf.blit(circ, (r.w - radius, r.h - radius), pygame.Rect((radius, radius), (radius, radius)))

    surf.set_colorkey(colorkey)
    surf.set_alpha(alpha)
    target_surf.blit(surf, rect)
