#! /usr/bin/env python

"""Goo - XML based user interface working with gunge"""


__all__ = ['element', 'composite', 'controls', 'containers', 'style', 'parser', 'draw']

import goo.element
import goo.composite
import goo.controls
import goo.containers
import goo.style
import goo.parser
import goo.draw


import pygame, gunge.event

BUTTONCLICK = gunge.event.USEREVENT + 1

class NullParent:
    """A dummy parent.

    This parent has some dummy attributes so that top-level windows don't get burned
    when they try to access their parent.
    """
    style = goo.style.get()
    rect  = pygame.Rect((0, 0), (0, 0))

    @classmethod
    def adjust(cls, child):
        """this at the moment does nothing at all.

        A (top-level) container will call this method, so it must be available.
        """
        pass

    @classmethod
    def get_childpos(cls, child):
        """returns (10, 10)"""
        return (10, 10)

del pygame
