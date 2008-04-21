#! /usr/bin/env python

"""element.py - base class for all GUI elements"""

import stdtools as std

class Element(std.sprite.Sprite):
    """Element - the base class for all GUI elements"""

    def __init__(self, style):
        std.sprite.Sprite.__init__(self)
        self.style = style
