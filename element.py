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
        self.style = goo.style.get(attributes.get('style', "default"))
        self.id = attributes.get('id', None)
        self.handlers = {}

    def bind_handler(self, eventtype, handlerfunc, attr_filter=None):
        """bind event handlers to this element. This method is for the goo-specific way of handling events"""
        if eventtype not in self.handlers:
            self.handlers[eventtype] = []

        handler = Binder(eventtype, attr_filter, handlerfunc)
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
            if result == goo.NO_MATCH:
                #no match, next handler
                continue
            elif result == goo.SKIP:
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
        """creates the element sprite and rect

        this method is supposed to set up the element sprite and rect. This base method only creates a rect
        with the width and height specified in the attributes (default 0). call this in your derived method.
        You can always adjust the sizes if the element does not fit inside.
        """
        width = int(self.attributes.get("width", 0))
        height = int(self.attributes.get("height", 0))
        self.rect = pygame.Rect(0, 0, width, height)

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
            except AttributeError:
                continue
        return pygame.Rect(self.pos, self.rect.size)

    @gunge.event.bind(gunge.event.UPDATE)
    def update(self, event):
        """update element (recalculate absolute position if parent has moved)"""
        self.rect.topleft = self.get_absolutepos()
        gunge.sprite.Sprite.update(self, event)

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
        try:
            return self._pos
        except AttributeError:
            return None

    def set_pos(self, (x, y)):
        """set elements' relative position

        sets the elements' position in an (x, y) tuple. This position
        is relative to the elements' parent. this is used through the self.pos property.
        """
        #test if this new position is within the parent
        parent_rect = self.parent.rect
        new_rect = pygame.Rect((x + parent_rect.left, y + parent_rect.top), self.rect.size)
        #perform a boundary check, unless the parent size is 0 (meaning uninitialized)
        if parent_rect.size != (0,0) and (x < 0 or y < 0 or self.rect.right > parent_rect.right or self.rect.bottom > parent_rect.bottom):
                #TODO create goo.Error class
                #raise goo.Error("element position out of parent bounds: (%s, %s)" % (x, y))
                raise RuntimeError("element position out of parent bounds: (%s, %s), %s" % (x, y, self.id))

        #set new position relative and absolute
        self._pos = (x, y)
        self.rect = new_rect

    pos = property(get_pos, set_pos, doc="The position (topleft corner) of the element relative to its parent, in an (x, y) tuple).")


class Binder(gunge.event.Binder):
    """goo Binder that is slightly adapted to accomodate for goo event handling"""

    def __init__(self, eventtype, attr_filter, handler_func):
        gunge.event.Binder.__init__(self, eventtype, attr_filter, handler_func)

        self.func = handler_func

    def __call__(self, event):
        """returns goo.NO_MATCH if the filter does not match. If it does, the result of calling the handler is returned"""
        if self.filter_check(event):
            return self.func(event)
        return goo.NO_MATCH
