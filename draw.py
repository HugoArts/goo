#! /usr/bin/env python

"""draw functions used to draw the controls"""

import pygame, goo.style

def alpha_surface(*args):
    """return a transparent surface

    return a surface with per-pixel alpha, cleared to (0, 0, 0, 0) (completely transparent).
    It takes the same arguments as pygame.Surface.
    """
    surface = pygame.Surface(*args)
    surface = surface.convert_alpha()
    surface.fill((0, 0, 0, 0))
    return surface

def rounded_rect(target_surf, rect, style):
    """draw a rounded rectangle

    the style argument can be either a tuple in the form of (color, width, radius) or a goo Style object 
    """
    if isinstance(style, goo.style.Style):
        color, width, radius = style['border_color'], style['border_width'], style['border_radius']
    else:
        color, width, radius = style
    alpha = color[3] if len(color) == 4 else 255 
    colorkey = (0,0,0) if color != (0,0,0) else (255, 255, 255)
    r = rect

    #prepare the circle
    circle = pygame.Surface((radius*2, radius*2))
    circle.fill(colorkey)
    pygame.draw.circle(circle, color, (radius, radius), radius, width)

    #prepare the surface
    surf = pygame.Surface(r.size)
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
    surf.set_alpha(alpha)
    target_surf.blit(surf, rect)
