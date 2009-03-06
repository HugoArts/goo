#! /usr/bin/env python

"""file containing classes for boxes of text"""

import base
import goo.draw
import gunge.event
import pygame
from itertools import chain


class StaticText(base.Control):
    """static box of text"""

    def __init__(self, parent, text, **attributes):
        """init StaticText"""
        self.text = text
        base.Control.__init__(self, parent, width="100", height="100", style="default_sizer", expand="True", **attributes)

    def arrange(self, area):
        """this does the job the create method would normally be doing.

        This is required since the content changes with the size of the element.
        """
        self.rect = base.Control.arrange(self, area)
        font = pygame.font.Font(self.style['font'], self.style['font_height'])
        lines = wrap_multiline(self.text, font, self.rect.width)
        self.img = goo.draw.alpha_surface(self.rect.size)

        for n, line in enumerate(lines):
            s = font.render(line, True, self.style['font_color'])
            self.img.blit(s, (self.style['padding'], self.style['padding'] + n * (font.size(line)[1] + 2)))
        return self.rect

    @gunge.event.bind(gunge.event.RENDER)
    def render(self, event):
        """render StaticText element"""
        base.Control.render(self, event)


def wrap_text(text, font, maxwidth):
    """wrap text.

    given a string with a specific pygame font object and a maximum width, return a list of strings that
    are as long as possible without exceeding the maximum lenght. Breaks up at whitespace if possible,
    otherwise starts breaking up words themselves.
    """
    text = text.lstrip()
    if font.size(text)[0] <= maxwidth:
        return [text]
    else:
        orig_text = text
        while font.size(text)[0] > maxwidth:
            split = text.rsplit(None, 1)[0]
            #start cutting words if splitting at whitespace doesn't cut it (pardon pun)
            text = split[:-1] if split == text else split
        return [text] + wrap_text(orig_text[len(text):], font, maxwidth)

def wrap_multiline(text, font, maxwidth):
    """wrap multiline text

    same as wrap_text, but split up at line boundaries first.
    """
    return list(chain(*(wrap_text(line, font, maxwidth) for line in text.splitlines())))
