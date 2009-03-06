#! /usr/bin/env python

"""implement a common radio button.

Only one radio button in a group can be checked. radio buttons with the same parent are considered to belong to the same group
"""

import base
import pygame
import gunge
import goo


class Radiobutton(base.Control):
    """radio button implementation. unchecks itself if a Radiobutton with the same parent is checked"""

    def __init__(self, parent, **attributes):
        self.checked = attributes.get('checked', False) == "True"
        self.description = attributes.get('description', '')
        self.icon = goo.img_loader['radio.png']
        self.mouse_over = False

        base.Control.__init__(self, parent, style="default_checkbox", **attributes)

    def create(self):
        """create the radio button surface"""
        font = pygame.font.Font(self.style['font'], self.style['font_height'])
        txtimg = font.render(self.description, True, self.style['font_color'])
        txtrect = txtimg.get_rect()

        self.img = goo.draw.alpha_surface((16 + txtrect.width + 2*self.style['padding'], max(12, txtrect.height) + 2*self.style['padding']))
        self.rect = self.img.get_rect()
        self.radio_rect = pygame.Rect((self.style['padding'] + 6,)*2, (12, 12))
        self.radio_rect.top = self.rect.height / 2.

        goo.draw.circle(self.img, self.style['background_color'], self.radio_rect, 6, 0)
        self.img.blit(txtimg, (16, self.style['padding']))

        goo.draw.circle(self.img, self.style['border_color'], self.radio_rect, 6, self.style['border_width'])

    @gunge.event.bind(goo.CHECKCHANGED, {'objecttype': lambda x: x is Radiobutton})
    def on_otherchecked(self, event):
        """if another button becomes checked, uncheck this box"""
        if event.objectid != self.id and event.parent is self.parent:
            self.checked = False

    @gunge.event.bind(pygame.MOUSEBUTTONUP, {'button': 1})
    def on_mouseup(self, event):
        """if the MOUSEUP collides with the radio button, check the button if not already checked and send out a CHECKCHANGED event"""
        if self.rect.collidepoint(event.pos):
            if not self.checked:
                self.checked = True
                event = pygame.event.Event(goo.CHECKCHANGED, {'objectid': self.id, 'objecttype': type(self), 'checked': self.checked, 'parent': self.parent})
                pygame.event.post(event)

    @gunge.event.bind(gunge.event.UPDATE)
    def update(self, event):
        """update the radio button. Bound to gunge.event.UPDATE"""
        base.Control.update(self, event)
        self.mouse_over = self.rect.collidepoint(pygame.mouse.get_pos())

        self.radio_rect.topleft = self.rect.topleft
        self.radio_rect.left += self.style['padding']
        self.radio_rect.centery = self.rect.centery

    @gunge.event.bind(gunge.event.RENDER)
    def render(self, event):
        """render the radio button. Bound to gunge.event.RENDER"""
        surface = event.display.screen
        if self.mouse_over:
            pygame.draw.rect(surface, self.style['hover_color'], self.rect, 0)
        base.Control.render(self, event)

        if self.checked:
            surface.blit(self.icon, (self.radio_rect.left + 3, self.radio_rect.top + 3))
