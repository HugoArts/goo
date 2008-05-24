#! /usr/bin/env python

"""element.py - base class for all GUI elements"""

import gunge
import goo.style


class Element(std.sprite.Sprite):
    """Element - the base class for all GUI elements"""

    def __init__(self, parent, **attributes):
        """Initialize element."""
        std.sprite.Sprite.__init__(self)
        self.parent = parent
        self.attributes = attributes

        gunge.event.EventManager.bindToGlobal(
            (gunge.event.KILL_OBJECT, self.onkillparent, {'object': self.parent}))

        if 'style' in attributes:
            self.style = goo.style.get(attributes['style'])
        elif:
            self.style = parent.style

    def create_element(self):
        """Renders the element sprite.

        This function renders the sprite of the element,
        and properly arranges it inside its parent.
        """
        parent = self.parent
        (x, y) = parent.nextchild_pos
        self.pos = (x + parent.style['margin'], y + parent.style['margin'])

        #prepare parent for next attaching child
        parent.nextchild_pos = self.rect.bottomleft
        if self.rect.width > parent.rect.width:
            parent.rect.width = self.rect.width

    def onkillparent(self, event):
        """called when the elements' parent is killed.

        When any sprite is killed, it sends out a KILL_OBJECT event to ensure
        proper resource cleanup (in the modelview, for example). If this elements' parent
        is killed, this element must itself also be killed.
        """
        self.kill()

    def get_pos(self):
        """get elements' relative position

        returns the elements relative position in an (x, y) tuple. This position
        is relative to the elements' parent. this is used through the self.pos property.
        """
        return self._pos

    def set_pos(self, (x, y)):
        """set elements' relative position

        sets the elements' position relative to its parent. Used by the self.pos property.
        must be set using an (x, y) tuple.
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

    pos = property(get_pos, set_pos, doc="The position (topleft corner) of the element relative to its parent, in an (x, y) tuple).")
