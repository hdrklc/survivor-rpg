#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UI/LevelUp.py - Level-up paneli
"""

from kivy.uix.widget import Widget
from kivy.event import EventDispatcher
from typing import List, Dict, Any


class LevelUpPanel(Widget, EventDispatcher):
    """Level-up yetenek seçim paneli"""
    
    __events__ = ('on_ability_selected',)
    
    def __init__(self, abilities: List[Dict[str, Any]], **kwargs):
        super().__init__(**kwargs)
        self.abilities = abilities
    
    def select_ability(self, index: int):
        """Yetenek seç"""
        if 0 <= index < len(self.abilities):
            self.dispatch('on_ability_selected', index)
    
    def on_ability_selected(self, index: int):
        """Yetenek seçildi eventi"""
        pass
