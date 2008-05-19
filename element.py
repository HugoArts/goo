#! /usr/bin/env python

"""element.py - base class for all GUI elements"""

import stdtools as std
import gui.style

class Element(std.sprite.Sprite):
    """Element - the base class for all GUI elements"""

    def __init__(self, style=None):
        """initialize the element."""
        std.sprite.Sprite.__init__(self)
        self.style = style

        #assign default style if none is set
        if self.style is None:
            self.style = gui.style.Style()

    def create_element(self):
        """create the element.

        This must be called before the element can be rendered to the
        screen. It renders the element surface. Must be implemented by
        derived classes
        """
        raise NotImplementedError("create_element is not implemented in class '%s'" % type(self).__name__)

    def hide(self, value=True):
        """hide/unhide the GUI Element.

        Passing in True hides the element, preventing it from
        rendering or responding to events. False unhides again.
        """
        self.hidden = value
