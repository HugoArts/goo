#! /usr/bin/env python

"""element.py - base class for all GUI elements"""

import gunge
import goo


class Element(gunge.sprite.Sprite):
    """Element - the base class for all GUI elements"""

    def __init__(self, parent, **attributes):
        """Initialize element."""
        gunge.sprite.Sprite.__init__(self)
        if not isinstance(parent, goo.containers.Container):
            #TODO: create goo error
            raise RuntimeError("trying to attach element to non-container type '%s'" % type(parent).__name__)

        self.parent = parent
        self.attributes = attributes
        self.style = attributes.get('style', parent.style)
        self.id = attributes.get('id', None)

        gunge.event.EventManager.bindToGlobal(
            (gunge.event.KILL_OBJECT, self.onkillparent, {'object': self.parent}))

    def onkillparent(self, event):
        """called when the elements' parent is killed.

        When any sprite is killed, it sends out a KILL_OBJECT event to ensure
        proper resource cleanup (in the modelview, for example). If this elements' parent
        is killed, this element must itself also be killed.
        """
        self.kill()

    def create(self):
        """creates the element sprite and rect"""
        raise NotImplementedError("class '%s' does not implement create()" % type(self).__name__)

    def arrange(self):
        """arranges the element inside its parent"""
        self.pos = self.parent.get_childpos(self)

    def update(self):
        """update element (recalculate absolute position if parent has moved)"""
        self.rect.topleft = self.get_absolutepos()

    def get_absolutepos(self):
        """get elements' absolute position

        used for rendering on the screen. For relative position, use get_pos()
        """
        (x, y), (x_rel, y_rel) = self.parent.rect.topleft, self.pos
        return (x + x_rel, y + y_rel)

    def get_pos(self):
        """get elements' relative position

        returns the elements' position in an (x, y) tuple. This position
        is relative to the elements' parent. this is used through the self.pos property.
        """
        return self._pos

    def set_pos(self, (x, y)):
        """set elements' relative position

        sets the elements' position in an (x, y) tuple. This position
        is relative to the elements' parent. this is used through the self.pos property.
        """
        #test if this new position is within the parent
        parent_rect = self.parent.rect
        newrect = pygame.Rect((x + parent_rect.left, y + parent_rect.top), self.rect.size)
        if parent_rect.size != (0,0) and not parent_rect.contains(newrect):
            #TODO create goo.Error class
            #raise goo.Error("element position out of parent bounds: (%s, %s)" % (x, y))
            raise RuntimeError("element position out of parent bounds: (%s, %s)" % (x, y))

        #set new position relative and absolute
        self._pos = (x, y)
        self.rect = new_rect

    pos = property(get_pos, set_pos, doc="The position (topleft corner) of the element relative to its parent, in an (x, y) tuple).")
