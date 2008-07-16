#! /usr/bin/env python

"""element.py - base class for all GUI elements"""

import gunge
import goo
import pygame


class Element(gunge.sprite.Sprite):
    """Element - the base class for all GUI elements"""

    def __init__(self, parent, **attributes):
        """Initialize element."""
        gunge.sprite.Sprite.__init__(self)
        if not isinstance(parent, (goo.containers.Container, goo.NullParent)):
            #TODO: create goo error
            raise RuntimeError("trying to attach element to non-container type '%s'" % type(parent).__name__)

        self.parent = parent
        self.attributes = attributes
        self.style = goo.style.get(attributes['style'] if attributes.has_key('style') else "default")
        self.id = attributes.get('id', None)
        self.handlers = {}

        gunge.event.EventManager.bindToGlobal(
            (gunge.event.KILL_OBJECT, self.onkillparent, {'object': self.parent}))

    def onkillparent(self, event):
        """called when the elements' parent is killed.

        When any sprite is killed, it sends out a KILL_OBJECT event to ensure
        proper resource cleanup (in the modelview, for example). If this elements' parent
        is killed, this element must itself also be killed.
        """
        self.kill()

    def bind_handler(self, eventtype, handlerfunc, attr_filter=None):
        """bind event handlers to this element. This method is for the goo-specific way of handling events"""
        if eventtype not in self.handlers:
            self.handlers[eventtype] = []

        handler = gunge.event.EventBinder(handlerfunc, attr_filter)
        self.handlers[eventtype].append(handler)
        return handler

    def bind(self, *args):
        """shorthand method for binding multiple handlers at once"""
        for bind_args in args:
            self.bind_handler(*bind_args)

    def process_event(self, event):
        """handle events in the goo-specific way.

        this means that we look for handlers bound using self.bind. If one is found, this is called and we're done.
        If not, we look for handlers in the parent of this element. You can also force the processing to continue by returning
        something evaluating to True from your handler
        """
        for handler in self.handlers.get(event.type, []):
            result = handler(event)
            if result == gunge.event.NO_MATCH:
                #no match, next handler
                continue
            elif result == gunge.event.SKIP:
                #match, and upstream send requested
                break
            else:
                #match, no upstream send requested. done
                return
        if not isinstance(self.parent, goo.NullParent):
            self.parent.process_event(event)
        else:
            pygame.event.post(event)

    def create(self):
        """creates the element sprite and rect"""
        raise NotImplementedError("class '%s' does not implement create()" % type(self).__name__)

    def arrange(self, area):
        """arranges the element inside its parent

        the argument passed in is the area the element has been allotted, as a pygame.Rect. The actual area occupied must
        be returned, so that the parent can place other elements correctly. Note that the position of the area rectangle
        is relative to the parent, so basically what must be returned after arranging is pygame.Rect(self.pos, self.rect.size)
        """
        self.pos = area.topleft
        for attr, arg in self.attributes.items():
            try:
                getattr(goo.style, attr)(self, area, arg)
            except AttributeError, e:
                continue
        return pygame.Rect(self.pos, self.rect.size)

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
        new_rect = pygame.Rect((x + parent_rect.left, y + parent_rect.top), self.rect.size)
        if parent_rect.size != (0,0) and not parent_rect.contains(new_rect):
            #TODO create goo.Error class
            #raise goo.Error("element position out of parent bounds: (%s, %s)" % (x, y))
            raise RuntimeError("element position out of parent bounds: (%s, %s), %s" % (x, y, self))

        #set new position relative and absolute
        self._pos = (x, y)
        self.rect = new_rect

    pos = property(get_pos, set_pos, doc="The position (topleft corner) of the element relative to its parent, in an (x, y) tuple).")
