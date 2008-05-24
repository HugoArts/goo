#! /usr/bin/env python

import goo
import pygame

class Container(goo.element.Element):
    """A basic container.

    The most basic of all containers. It draws a simple border around its
    elements and provides a background image. The box is not resizable,
    but it is nestable.
    """
    def __init__(self, parent, children, **attributes):
        """initialize container"""
        goo.element.Element.__init__(self, parent, **attributes)
        self.nextchild_pos = (0,0)

        for node in children:
            goo.parser.parse(node, self)
        self.create_element()

    def create_element(self, style, position):
        """render the container sprite."""
        #TODO we'll need to rewrite this crap for sure. I'm not sure how yet

        #for now, we'll assume we already know its size
        self.img = pygame.Surface(self.size).convert_alpha()
        self.rect = pygame.Rect(self.pos, self.size)

        self.img.fill(self.style['container_background_color'])
        pygame.draw.rect(self.img, self.style['container_border_color'], pygame.Rect((0,0), self.size), self.style['container_border_width'])
