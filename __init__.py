#! /usr/bin/env python

"""Goo - XML based user interface working with gunge"""


__all__ = ['element', 'parser', 'style', 'containers']

import goo.element
import goo.containers
import goo.style
import goo.parser

class NullParent:
    """A dummy parent.

    This parent has some dummy attributes so that top-level windows don't get burned
    when they try to access their parent.
    """
    @classmethod
    def adjust(cls, child):
        """this at the moment does nothing at all.

        A (top-level) container will call this method, so it must be available.
        """
        pass
