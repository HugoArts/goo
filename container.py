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

    def create_element(self):
        """render the container sprite."""
        #the width is already set by the children, but we add margin. The height is the nextchild_pos y coordinate
        self.rect.width = self.rect.width + self.style['margin']
        self.rect.height = self.nextchild_pos[1] + self.style['margin']
        self.img = pygame.Surface((self.rect.size))

        self.img.fill(self.style['background_color'])
        pygame.draw.rect(self.img, self.style['border_color'], pygame.Rect((0,0), self.rect.size), self.style['border_width'])
