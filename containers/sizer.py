#! /usr/bin/env python

"""sizer.py - a container without any decorations"""

import base

class Sizer(base.Container):
    """Sizer - similar to wxPython sizers.

    These are containers that don't have any decorations. This simple one is like the Container, but invisible.
    """
    def __init__(self, parent, children, style="default_sizer", **attributes):
        base.Container.__init__(self, parent, children, style=style, **attributes)


class HrSizer(base.HrContainer):
    """HrSizer - a horizontal sizer

    this is the Horizontal version of the sizer. It works the same as the Horizontal container,
    but without the decorations.
    """
    def __init__(self, parent, pos, style="default_sizer", **attributes):
        base.HrContainer.__init__(self, parent, pos, style=style, **attributes)
