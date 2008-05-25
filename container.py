#! /usr/bin/env python

import goo
import pygame

class Container(goo.element.Element):
    """A basic container.

    The most basic of all containers. It draws a simple border around its
    elements and provides a background image. The box is not resizable,
    but it is nestable.
    """
    def __init__(self, parent, children):
        """initialize container"""
        goo.element.Element.__init__(self, parent)
        self.nextchild_pos = (self.style['margin'], self.style['margin'])

        children = [goo.parser.parse(node, self) for node in children]
        self.create()
        for child in children:
            child.arrange()

    def get_childpos(self, child):
        """get a suitable position for a child element.

        This is used when the child is arranging itself. The container gives it a suitable position.
        Note that the child may choose to adjust this for its style (e.g. alignment)
        """
        (x, y) = self.nextchild_pos
        self.nextchild_pos = (x, y + child.rect.height + self.style['margin'])
        return (x, y)

    def adjust(self, child):
        """adjust the container to accomodate a child.

        many container attributes (for example, the minimum container dimensions) depend on the children inside it.
        Therefore, this function should be called with the child after the child has been created.
        """
        if child.rect.width > self.rect.width:
            self.rect.width = child.rect.width
        self.rect.height += (child.rect.height + self.style['margin'])

    def create(self):
        """render the container sprite."""
        self.rect.width += self.style['margin']
        self.rect.height += self.style['margin']
        self.img = pygame.Surface((self.rect.size))

        self.img.fill(self.style['background_color'])
        pygame.draw.rect(self.img, self.style['border_color'], pygame.Rect((0,0), self.rect.size), self.style['border_width'])
        self.parent.adjust(self)


class HorizontalContainer(Container):
    """HorizontalContainer - similar to the basic container, but it arranges children horizontally"""

    def get_childpos(self, child):
        """get a suitable position for a child element.

        This is used when the child is arranging itself. The container gives it a suitable position.
        Note that the child may choose to adjust this for its style (e.g. alignment)
        """
        (x, y) = self.nextchild_pos
        self.nextchild_pos = x + child.rect.width + self.style['margin'], y)

    def adjust(self, child):
        """adjust the container to accomodate a child.

        many container attributes (for example, the minimum container dimensions) depend on the children inside it.
        Therefore, this function should be called with the child after the child has been created.
        """
        if child.rect.height > self.rect.height:
            self.rect.height = child.rect.height
        self.rect.width += (child.rect.width + self.style['margin'])
