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
    def __init__(self, parent, children, **attributes):
        """initialize container"""
        goo.element.Element.__init__(self, parent, **attributes)
        self.nextchild_pos = (self.style['margin'], self.style['margin'])

        children = [goo.parser.parse(node, self) for node in children if node.nodeType != 3]
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
        if child.rect.width + self.style['margin'] > self.rect.width:
            self.rect.width = child.rect.width + self.style['margin']
        self.rect.height += (child.rect.height + self.style['margin'])

    def create(self):
        """render the container sprite."""
        self.rect.width += self.style['margin']
        self.rect.height += self.style['margin']
        self.img = goo.draw.alpha_surface((self.rect.size))

        #the bottom one is the box border, the top one the box itself
        goo.draw.rounded_rect(self.img, pygame.Rect((0,0), self.rect.size), (self.style['background_color'], 0, self.style['border_radius']))
        goo.draw.rounded_rect(self.img, pygame.Rect((0,0), self.rect.size), self.style)
        self.parent.adjust(self)


class HrContainer(Container):
    """HorizontalContainer - similar to the basic container, but it arranges children horizontally"""

    def get_childpos(self, child):
        """get a suitable position for a child element.

        This is used when the child is arranging itself. The container gives it a suitable position.
        Note that the child may choose to adjust this for its style (e.g. alignment)
        """
        (x, y) = self.nextchild_pos
        self.nextchild_pos = (x + child.rect.width + self.style['margin'], y)
        return (x, y)

    def adjust(self, child):
        """adjust the container to accomodate a child.

        many container attributes (for example, the minimum container dimensions) depend on the children inside it.
        Therefore, this function should be called with the child after the child has been created.
        """
        if child.rect.height + self.style['margin'] > self.rect.height:
            self.rect.height = child.rect.height + self.style['margin']
        self.rect.width += (child.rect.width + self.style['margin'])


class Sizer(Container):
    """Sizer - similar to wxPython sizers.

    These are containers that don't have any decorations. This simple one is like the Container, but invisible.
    """
    def get_childpos(self, child):
        """return next child position.

        a sizer should not add margins around itself. To prevent that we alter get_childpos just a little
        """
        if self.nextchild_pos == (self.style['margin'], self.style['margin']):
            self.nextchild_pos = (0, 0)
        return Container.get_childpos(self, child)

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
