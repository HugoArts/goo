#! /usr/bin/env python

"""frame.py - a frame is a top-level-window, with a titlebar and everythin"""

import base


class Frame(base.Composite):
    """A top level window with a title bar and optionally a statusbar and/or menubar"""
    def __init__(self, parent, children, **attributes):
        base.Composite.__init__(self, parent, children, "frame.xml", **attributes)
        #make sure titlebar has right parent
        self.children[0].children[0].parent = self
