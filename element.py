#! /usr/bin/env python

"""element.py - base class for all GUI elements"""

import stdtools as std
import goo.style


class Element(std.sprite.Sprite):
    """Element - the base class for all GUI elements"""

    def __init__(self, parent):
        """Initialize element."""
        std.sprite.Sprite.__init__(self)
        self.parent = parent

    def create_element(self, style, position):
        """Renders the element sprite.

        This function renders the sprite of the element, using the specified style,
        and properly arranges it inside its parent.
        """
        #this will do something later, like arrange the element in its' parent correctly
        raise NotImplementedError("Class '%s' does not implement a create_element method" % type(self).__name__)

    def get_pos(self):
        """get the elements' relative position

        returns the elements relative position in an (x, y) tuple. This position
        is relative to the elements' parent. this is used through the self.pos property.
        An elements' position is the location of its topleft corner
        """
        return self._pos

    def set_pos(self, (x, y)):
        """set elements' relative position

        sets the elements' position relative to its parent. Used by the self.pos property.
        must be set using an (x, y) tuple. The position is the location of the top left of the element.
        """
        #test if this new position is within the parent
        parent_rect = self.parent.rect
        newrect = pygame.Rect((x + parent_rect.left, y + parent_rect.top), self.rect.size)
        if not parent_rect.contains(newrect):
            #TODO create Goo.Error class
            #raise Goo.Error("element position out of parent bounds: (%s, %s)" % (x, y))
            raise RuntimeError("element position out of parent bounds: (%s, %s)" % (x, y))

        #set new position relative and absolute
        self._pos = (x, y)
        self.rect = new_rect

    pos = property(get_pos, set_pos, doc="The position of the element relative to its parent, in an (x, y) tuple).")
