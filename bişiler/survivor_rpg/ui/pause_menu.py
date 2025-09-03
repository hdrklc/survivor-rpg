#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UI/PauseMenu.py - Pause menüsü
"""

from kivy.uix.widget import Widget
from kivy.event import EventDispatcher


class PauseMenu(Widget, EventDispatcher):
    """Pause menüsü"""
    
    __events__ = ('on_resume', 'on_main_menu', 'on_quit')
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def resume_game(self):
        """Oyunu devam ettir"""
        self.dispatch('on_resume')
    
    def go_to_main_menu(self):
        """Ana menüye dön"""
        self.dispatch('on_main_menu')
    
    def quit_game(self):
        """Oyundan çık"""
        self.dispatch('on_quit')
    
    def on_resume(self):
        pass
    
    def on_main_menu(self):
        pass
    
    def on_quit(self):
        pass
