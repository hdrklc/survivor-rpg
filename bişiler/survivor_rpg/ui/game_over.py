#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UI/GameOver.py - Game over ekranı
"""

from kivy.uix.widget import Widget
from kivy.event import EventDispatcher
from kivy.properties import StringProperty, NumericProperty


class GameOverScreen(Widget, EventDispatcher):
    """Game over ekranı"""
    
    __events__ = ('on_restart', 'on_main_menu')
    
    survival_time = StringProperty("00:00")
    final_level = NumericProperty(1)
    coins_earned = NumericProperty(0)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def restart_game(self):
        """Oyunu yeniden başlat"""
        self.dispatch('on_restart')
    
    def go_to_main_menu(self):
        """Ana menüye dön"""
        self.dispatch('on_main_menu')
    
    def on_restart(self):
        pass
    
    def on_main_menu(self):
        pass
