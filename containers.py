#! /usr/bin/env python

"""containers.py - elements that can contain other elements

containers can (obviously) contain other elements, including other containers. Different containers
may draw different borders or backgrounds, and can also arrange their children differently
"""

import goo
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
        self.min_width, self.min_height = (0, 0)

        self.children = [goo.parser.parse(node, self) for node in children if node.nodeType != 3]
        self.create()
        self.arrange_children()

    def arrange_children(self):
        """arrange the children of this container

        calls the arrange function for each of the containers children, with a rectangle as argument.
        Within that rectangle, the child is free to position itself. When done, the child must return a rectangle
        representing the actual space it is occupying, so that the container can give a suitable area to the next child
        """
        self.nextchild_pos = [self.style['margin'], self.style['margin']]
        for i, child in enumerate(self.children):
            width = self.rect.width - self.nextchild_pos[0] - self.style['margin']

            height = self.rect.height - self.nextchild_pos[1] - sum(c.rect.height for c in self.children[i+1:])
            height -= ((len(self.children[i+1:]) + 1) * self.style['margin'])

            area = child.arrange(pygame.Rect(self.nextchild_pos, (width, height)))
            self.nextchild_pos[1] = (area.bottom + self.style['margin'])

    def adjust(self, child):
        """adjust the container to accomodate a child.

        many container attributes (for example, the minimum container dimensions) depend on the children inside it.
        Therefore, this function should be called with the child after the child has been created.
        """
        if child.rect.width + self.style['margin'] > self.min_width:
            self.min_width = child.rect.width + self.style['margin']
        self.min_height += (child.rect.height + self.style['margin'])

    def create(self):
        """render the container sprite."""
        self.min_width += self.style['margin']
        self.min_height += self.style['margin']
        if self.rect.width < self.min_width:
            self.rect.width = self.min_width
        if self.rect.height < self.min_height:
            self.rect.height = self.min_height

        self.parent.adjust(self)

    def render(self, surface):
        """render container decorations to the screen"""
        #the bottom one is the box border, the top one the box itself
        goo.draw.rounded_rect(surface, self.rect, (self.style['background_color'], 0, self.style['border_radius']))
        goo.draw.rounded_rect(surface, self.rect, self.style)


class HrContainer(Container):
    """HorizontalContainer - similar to the basic container, but it arranges children horizontally"""

    def arrange_children(self):
        """arrange the children of this container

        calls the arrange function for each of the containers children, with a rectangle as argument.
        Within that rectangle, the child is free to position itself. When done, the child must return a rectangle
        representing the actual space it is occupying, so that the container can give a suitable area to the next child
        """
        self.nextchild_pos = [self.style['margin'], self.style['margin']]
        for i, child in enumerate(self.children):
            height = self.rect.height - self.nextchild_pos[1] - self.style['margin']

            width = self.rect.width - self.nextchild_pos[0] - sum(c.rect.width for c in self.children[i+1:])
            width -= ((len(self.children[i+1:]) + 1) * self.style['margin'])

            area = child.arrange(pygame.Rect(self.nextchild_pos, (width, height)))
            self.nextchild_pos[0] = (area.right + self.style['margin'])

    def adjust(self, child):
        """adjust the container to accomodate a child.

        many container attributes (for example, the minimum container dimensions) depend on the children inside it.
        Therefore, this function should be called with the child after the child has been created.
        """
        if child.rect.height + self.style['margin'] > self.min_height:
            self.min_height = child.rect.height + self.style['margin']
        self.min_width += (child.rect.width + self.style['margin'])


class Sizer(Container):
    """Sizer - similar to wxPython sizers.

    These are containers that don't have any decorations. This simple one is like the Container, but invisible.
    """
    def arrange_children(self):
        """arrange the children of this container

        calls the arrange function for each of the containers children, with a rectangle as argument.
        Within that rectangle, the child is free to position itself. When done, the child must return a rectangle
        representing the actual space it is occupying, so that the container can give a suitable area to the next child
        """
        self.nextchild_pos = [0, 0]
        for i, child in enumerate(self.children):
            width = self.rect.width - self.nextchild_pos[0]

            height = self.rect.height - self.nextchild_pos[1] - sum(c.rect.height for c in self.children[i+1:])
            height -= (len(self.children[i+1:]) * self.style['margin'])

            area = child.arrange(pygame.Rect(self.nextchild_pos, (width, height)))
            self.nextchild_pos[1] = (area.bottom + self.style['margin'])

    def adjust(self, child):
        """adjust for parent. Same as a container, except don't count margins"""
        if child.rect.width > self.rect.width:
            self.rect.width = child.rect.width
        self.rect.height += (child.rect.height + self.style['margin'])

    def create(self):
        """adjust margin sizes

        in the Container, margins are adjusted and the container is drawn. Since this Sizer is invisible,
        Only the margins are adjusted. Of course the parent is also adjusted for this sizer.
        """
        self.rect.height -= self.style['margin']
        self.parent.adjust(self)

    def render(self, surface):
        """does nothing

        since the Sizer is invisible, this method does nothing
        """
        pass


class HrSizer(HrContainer):
    """HrSizer - a horizontal sizer

    this is the Horizontal version of the sizer. It works the same as the Horizontal container,
    but without the decorations.
    """
    def arrange_children(self):
        """arrange the children of this container

        calls the arrange function for each of the containers children, with a rectangle as argument.
        Within that rectangle, the child is free to position itself. When done, the child must return a rectangle
        representing the actual space it is occupying, so that the container can give a suitable area to the next child
        """
        self.nextchild_pos = [0, 0]
        for i, child in enumerate(self.children):
            height = self.rect.height - self.nextchild_pos[1]

            width = self.rect.width - self.nextchild_pos[0] - sum(c.rect.width for c in self.children[i+1:])
            width -= ((len(self.children[i+1:])) * self.style['margin'])

            area = child.arrange(pygame.Rect(self.nextchild_pos, (width, height)))
            self.nextchild_pos[0] = (area.right + self.style['margin'])

    def get_childpos(self, child):
        """return next child position.

        a sizer should not add margins around itself. To prevent that we alter get_childpos just a little
        """
        if self.nextchild_pos == (self.style['margin'], self.style['margin']):
            self.nextchild_pos = (0, 0)
        return HrContainer.get_childpos(self, child)

    def adjust(self, child):
        """adjust for child. same as HrContainer, but without margin"""
        if child.rect.height > self.rect.height:
            self.rect.height = child.rect.height
        self.rect.width += (child.rect.width + self.style['margin'])

    def create(self):
        """adjust margin sizes

        in the Container, margins are adjusted and the container is drawn. Since this Sizer is invisible,
        Only the margins are adjusted. Of course the parent is also adjusted for this sizer.
        """
        self.rect.width -= self.style['margin']
        self.parent.adjust(self)

    def render(self, surface):
        """does nothing

        since the Sizer is invisible, this method does nothing
        """
        pass
