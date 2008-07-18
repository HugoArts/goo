#! /usr/bin/env python

"""base - base control class"""

import goo.element


class Control(goo.element.Element):
    """Base class for all controls"""
    
    def __init__(self, parent, **attributes):
        """initialize the control
        
        all this currently does is create the element.
        """
        goo.element.Element.__init__(self, parent, **attributes)
        self.create()
