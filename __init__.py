#! /usr/bin/env python

"""Goo - XML based user interface working with gunge"""


__all__ = ['element', 'containers', 'controls', 'composite', 'style', 'parser', 'draw']

#temporary import
import pygame, gunge

#constants
TOPLEFT     = 1
TOPRIGHT    = 2
BOTTOMLEFT  = 4
BOTTOMRIGHT = 8

TOP    = TOPLEFT | TOPRIGHT
BOTTOM = BOTTOMLEFT | BOTTOMRIGHT
ALL    = TOP | BOTTOM

#prepare goo event types
BUTTONCLICK  = gunge.event.USEREVENT + 1
CHECKCHANGED = gunge.event.USEREVENT + 2

#event return types
NO_MATCH = 0
SKIP = 1

import goo.element
import goo.containers
import goo.controls
import goo.composite
import goo.style
import goo.parser
import goo.draw

#prepare image loader for goo internal resources
img_loader = gunge.media.ImageLoader("goo/images", False)
xml_loader = gunge.media.ResourceLoader(("goo/xml", "."), False)


#default styles
goo.style.add(goo.style.Style("default_titlebar",
    margin           = 5,
    padding          = 3,
    border_rounding  = TOP,
    border_color     = (0, 0, 0, 0),
    background_color = (0, 140, 215),))

goo.style.add(goo.style.Style("default_sizer",
    padding          = 0,
    border_color     = (0, 0, 0, 0),
    background_color = (0, 0, 0, 0)))

goo.style.add(goo.style.Style("default_frame",
    padding         = 0,
    margin          = 0))

goo.style.add(goo.style.Style("default_panel",
    border_rounding = 0))

goo.style.add(goo.style.Style("default_iconbutton",
    border_color     = (0, 0, 0, 0),
    hover_color      = (50, 190, 255, 100),
    clicked_color    = (200, 200, 200, 100),
    padding          = 0))

goo.style.add(goo.style.Style("default_checkbox",
    background_color = (255, 255, 255),
    border_color     = (153, 146, 146),
    hover_color      = (255, 255, 255),
    padding          = 2))

goo.style.add(goo.style.Style("default_text",
    background_color = (255, 255, 255),
    padding          = 2))


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

del pygame, gunge
