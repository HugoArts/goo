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
        base.Control.__init__(self, parent, width="50", height="90", style="default_sizer", expand="True", **attributes)

    def arrange(self, area):
        """this does the job the create method would normally be doing.

        This is required since the content changes with the size of the element.
        """
        self.rect = base.Control.arrange(self, area)
        self.font = self.style.font()
        lines = wrap_multiline(self.text, self.font, self.rect.width)
        self.img = goo.draw.alpha_surface(self.rect.size)

        for n, line in enumerate(lines):
            s = self.font.render(line, True, self.style['font_color'])
            self.img.blit(s, (self.style['padding'], self.style['padding'] + n * (self.font.get_linesize())))
        return self.rect

    @gunge.event.bind(gunge.event.RENDER)
    def render(self, event):
        """render StaticText element"""
        base.Control.render(self, event)


class TextCtrl(base.Control):
    """editable text control box"""

    def __init__(self, parent, text, **attributes):
        """init TextCtrl"""
        self.text = text
        self.cursor_pos = None
        self.blink_count = 0
        self.cursor_blink = False
        base.Control.__init__(self, parent, style="default_text", **attributes)

    @gunge.event.bind(pygame.MOUSEBUTTONDOWN, {'button': 1})
    def on_mousedown(self, event):
        """event handler for mouse click"""
        if self.rect.collidepoint(event.pos):
            self.cursor_pos = 1 + find_cursorpos(event.pos[0] - (self.rect.left + self.style['padding']), self.text, self.font)
        else:
            self.cursor_pos = None

    @gunge.event.bind(pygame.KEYDOWN, {'unicode': lambda x: unicode.isalnum(x) or unicode.isspace(x)})
    def on_textentered(self, event):
        if self.cursor_pos is not None:
            self.text = ''.join((self.text[:self.cursor_pos], event.unicode, self.text[self.cursor_pos:]))
            self.cursor_pos += 1
            self.render_text()

    @gunge.event.bind(pygame.KEYDOWN, {'key': set((pygame.K_BACKSPACE, pygame.K_DELETE))})
    def on_deletekey(self, event):
        """deletes one key to the left or right of the cursor"""
        if self.cursor_pos is not None:
            if event.key is pygame.K_DELETE and self.cursor_pos < len(self.text):
                self.text = self.text[:self.cursor_pos] + self.text[self.cursor_pos + 1:]
                self.render_text()
            elif event.key is pygame.K_BACKSPACE and self.cursor_pos > 0:
                self.text = self.text[:self.cursor_pos - 1] + self.text[self.cursor_pos:]
                self.cursor_pos -= 1
                self.render_text()
            print event.unicode

    @gunge.event.bind(pygame.KEYDOWN, {'key': set((pygame.K_RIGHT, pygame.K_LEFT))})
    def on_movekey(self, event):
        """moves cursor one space right"""
        if self.cursor_pos is not None:
            if event.key == pygame.K_RIGHT and self.cursor_pos < len(self.text):
                self.cursor_pos += 1
            elif event.key == pygame.K_LEFT and self.cursor_pos > 0:
                self.cursor_pos -= 1

    def create(self):
        """create the rectangle of the TextCtrl

        this processes the 'numlines' and 'charwidth' attributes, as well as the normal
        'width' and 'height' attributes. Note that width and height override the TextCtrl specific attributes.
        Also note that the charwidth attributes is only accurate for fixed-width fonts. It approximates otherwise
        by using the width of a lone "a" character.
        """
        base.Control.create(self)
        self.font = self.style.font()
        if self.rect.height == 0:
            self.rect.height = int(self.attributes.get("numlines", 1)) * self.font.get_linesize()
        if self.rect.width == 0:
            self.rect.width = int(self.attributes.get("charwidth", 20)) * self.font.size("a")[0]
        self.rect.width += self.style['padding'] * 2
        self.rect.height += self.style['padding'] * 2
        self.render_text()

    def render_text(self):
        """render text inside the TextCtrl"""
        lines = wrap_text(self.text, self.font, self.rect.width)
        self.img = goo.draw.alpha_surface(self.rect.size)

        for n, line in enumerate(lines):
            if n * self.font.get_linesize() > self.rect.height:
                break
            s = self.font.render(line, True, self.style['font_color'])
            self.img.blit(s, (self.style['padding'], self.style['padding'] + n * (self.font.get_linesize())))

    @gunge.event.bind(gunge.event.UPDATE)
    def update(self, event):
        """update TextCtrl"""
        base.Control.update(self, event)
        self.blink_count += 1
        if self.blink_count > 14:
            self.cursor_blink = not self.cursor_blink
            self.blink_count = 0

    @gunge.event.bind(gunge.event.RENDER)
    def render(self, event):
        """render TextCtrl"""
        surface = event.display.screen
        goo.draw.rounded_rect(surface, self.rect, (self.style["background_color"], 0, self.style["border_radius"], self.style["border_rounding"]))
        goo.draw.rounded_rect(surface, self.rect, self.style)
        if self.cursor_pos is not None and self.cursor_blink:
            x = self.rect.left + self.style["padding"] + self.font.size(self.text[:self.cursor_pos])[0]
            y = self.rect.centery
            pygame.draw.line(surface, (0,0,0), (x, y + self.font.get_linesize() // 2), (x, y - self.font.get_linesize() // 2))
        base.Control.render(self, event)


def wrap_text(text, font, maxwidth):
    """wrap text

    given a string with a specific pygame font object and a maximum width, return a list of strings that
    are as long as possible without exceeding the maximum length. Breaks up at whitespace if possible,
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

def find_cursorpos(cursor_x, text, font):
    """binary search for the position of the cursor"""
    if cursor_x >= font.size(text)[0]:
        return len(text) - 1
    if cursor_x <= 0:
        return -1

    half = len(text) // 2
    n = int(round(half / 2.))
    while 1:
        char_start = font.size(text[:half])[0]
        char_end = font.size(text[:half + 1])[0]
        if char_start < cursor_x <= char_end or len(text) == 1:
            return half
        elif cursor_x > char_end:
            half += n
            n = int(round(n / 2.))
        elif cursor_x <= char_start:
            half -= n
            n = int(round(n / 2.))
