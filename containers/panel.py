#! /usr/bin/env python

"""panel.py - a container used inside Frames (though it can be used outside as well)

the panel has no rounded borders and is a simple light grey color. Otherwise, it behaves like
a standard container, arranging its children vertically.
"""

import base


class Panel(base.Container):
    """Simple container used inside Frames. Has no rounded corners and grey background"""
    def __init__(self, parent, children, size=(0, 0), **attributes):
        base.Container.__init__(self, parent, children, style="default_panel", **attributes)
