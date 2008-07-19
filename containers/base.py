#! /usr/bin/env python

"""containers.py - elements that can contain other elements

containers can (obviously) contain other elements, including other containers. Different containers
may draw different borders or backgrounds, and can also arrange their children differently
"""

import goo.element, goo.parser, goo.draw
import pygame

class Container(goo.element.Element):
    """A basic container.

    The most basic of all containers. It draws a simple border around its
    elements and provides a background image. The box is not resizable,
    but it is nestable.
    """
    def __init__(self, parent, children, size=(0, 0), **attributes):
        """initialize container"""
        goo.element.Element.__init__(self, parent, **attributes)
        self.rect.size = size if size == (0, 0) else tuple(int(e) for e in size.split(','))
        if not (hasattr(self, 'min_width') and hasattr(self, 'min_height')):
            self.min_width, self.min_height = (0, self.style['padding'] - self.style['margin'])

        self.children = [goo.parser.parse(node, self) for node in children if node.nodeType not in (3, 8)]
        self.children = filter(lambda x: x is not None, self.children)
        self.create()
        self.arrange_children()

    def arrange_children(self):
        """arrange the children of this container

        calls the arrange function for each of the containers children, with a rectangle as argument.
        Within that rectangle, the child is free to position itself. When done, the child must return a rectangle
        representing the actual space it is occupying, so that the container can give a suitable area to the next child
        """
        self.nextchild_pos = [self.style['padding'], self.style['padding']]
        for i, child in enumerate(self.children):
            width = self.rect.width - self.nextchild_pos[0] - self.style['padding']

            height = self.rect.height - self.nextchild_pos[1] - sum(c.rect.height for c in self.children[i+1:])
            height -= (len(self.children[i+1:]) * self.style['margin']) + self.style['padding']

            area = child.arrange(pygame.Rect(self.nextchild_pos, (width, height)))
            self.nextchild_pos[1] = (area.bottom + self.style['margin'])

    def adjust(self, child):
        """adjust the container to accomodate a child.

        many container attributes (for example, the minimum container dimensions) depend on the children inside it.
        Therefore, this function should be called with the child after the child has been created.
        """
        if child.rect.width + self.style['padding'] > self.min_width:
            self.min_width = child.rect.width + self.style['padding']
        self.min_height += (child.rect.height + self.style['margin'])

    def create(self):
        """render the container sprite."""
        self.min_width += self.style['padding']
        self.min_height += self.style['padding']
        if self.rect.width < self.min_width:
            self.rect.width = self.min_width
        if self.rect.height < self.min_height:
            self.rect.height = self.min_height

        self.parent.adjust(self)

    def render(self, surface):
        """render container decorations to the screen"""
        #the bottom one is the box border, the top one the box itself
        goo.draw.rounded_rect(surface, self.rect, (self.style['background_color'], 0, self.style['border_radius'], self.style['border_rounding']))
        goo.draw.rounded_rect(surface, self.rect, self.style)


class HrContainer(Container):
    """HorizontalContainer - similar to the basic container, but it arranges children horizontally"""

    def __init__(self, parent, children, size=(0, 0), **attributes):
        """initialize HrContainer"""
        goo.element.Element.__init__(self, parent, **attributes)
        self.min_width, self.min_height = (self.style['padding'] - self.style['margin'], 0)
        Container.__init__(self, parent, children, size, **attributes)

    def arrange_children(self):
        """arrange the children of this container

        calls the arrange function for each of the containers children, with a rectangle as argument.
        Within that rectangle, the child is free to position itself. When done, the child must return a rectangle
        representing the actual space it is occupying, so that the container can give a suitable area to the next child
        """
        self.nextchild_pos = [self.style['padding'], self.style['padding']]
        for i, child in enumerate(self.children):
            height = self.rect.height - self.nextchild_pos[1] - self.style['padding']

            width = self.rect.width - self.nextchild_pos[0] - sum(c.rect.width for c in self.children[i+1:])
            width -= (len(self.children[i+1:]) * self.style['margin']) + self.style['padding']

            area = child.arrange(pygame.Rect(self.nextchild_pos, (width, height)))
            self.nextchild_pos[0] = (area.right + self.style['margin'])

    def adjust(self, child):
        """adjust the container to accomodate a child.

        many container attributes (for example, the minimum container dimensions) depend on the children inside it.
        Therefore, this function should be called with the child after the child has been created.
        """
        if child.rect.height + self.style['padding'] > self.min_height:
            self.min_height = child.rect.height + self.style['padding']
        self.min_width += (child.rect.width + self.style['margin'])


