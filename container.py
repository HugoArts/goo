#! /usr/bin/env python

import element
import pygame

class Container(element.Element):
    """A basic container.

    The most basic of all containers. It draws a simple border around its
    elements and provides a background image. The box is not resizable,
    but it is nestable.
    """
    def __init__(self, style=None, pos=(0,0), size=(0,0)):
        element.Element.__init__(self, style, pos)
        self.size = size
        self.create_element()

    def create_element(self):
        #for now, we'll assume we already know its size
        self.img = pygame.Surface(self.size).convert_alpha()
        self.rect = pygame.Rect(self.pos, self.size)

        self.img.fill(self.style['container_background_color'])
        pygame.draw.rect(self.img, self.style['container_border_color'], pygame.Rect((0,0), self.size), self.style['container_border_width'])
