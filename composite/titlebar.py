#! /usr/bin/env python

"""titlebar.py - a window titlebar attached to a frame"""

import base
import gunge.event
import pygame
import goo

class TitleBar(base.Composite):
    """a window titlebar, must have a Frame as parent"""

    def __init__(self, parent, children, **attributes):
        """init TitleBar"""
        #if not isinstance(parent, Frame):
        #    raise RuntimeError("parent of titlebar is not a TopLevelWindow")
        base.Composite.__init__(self, parent, children, "titlebar.xml", **attributes)

        self.dragging = False
        self.bind(
            (goo.BUTTONCLICK, self.on_minimize, {'objectid': 'mini_window'}),
            (goo.BUTTONCLICK, self.on_maximize, {'objectid': 'maxi_window'}),
            (goo.BUTTONCLICK, self.on_close,    {'objectid': 'exit_window'}))

    @gunge.event.bind(pygame.MOUSEBUTTONDOWN, {'button': 1})
    def on_mousedown(self, event):
        """start dragging if mouseclick on titlebar"""
        if self.rect.collidepoint(event.pos):
            self.dragging = True
            return gunge.event.HANDLE_STOP

    @gunge.event.bind(pygame.MOUSEBUTTONUP, {'button': 1})
    def on_mouseup(self, event):
        """stop dragging"""
        self.dragging = False

    @gunge.event.bind(pygame.MOUSEMOTION)
    def on_motion(self, event):
        """drag the parent window"""
        if self.dragging:
            (x, y) = self.parent.pos
            self.parent.pos = (x + event.rel[0], y + event.rel[1])

    def on_minimize(self, event):
        """minimize the window"""
        pass

    def on_maximize(self, event):
        """maximize the window"""
        pass

    def on_close(self, event):
        """close window"""
        self.parent.kill()
