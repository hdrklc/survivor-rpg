#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UI/HUD.py - Oyun içi HUD
"""

from kivy.uix.widget import Widget
from kivy.properties import StringProperty, NumericProperty
from typing import Optional
from entities.player import Player


class HUD(Widget):
    """Heads-Up Display"""
    
    # Properties for binding with KV
    time_text = StringProperty("00:00")
    hp_percent = NumericProperty(100.0)
    xp_percent = NumericProperty(0.0)
    player_level = NumericProperty(1)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.player: Optional[Player] = None
    
    def bind_player(self, player: Player):
        """Oyuncuya bağla"""
        self.player = player
        self.update_player_stats()
    
    def update_time(self, game_time: float):
        """Zamanı güncelle"""
        minutes = int(game_time // 60)
        seconds = int(game_time % 60)
        self.time_text = f"{minutes:02d}:{seconds:02d}"
    
    def update_player_stats(self):
        """Oyuncu istatistiklerini güncelle"""
        if not self.player:
            return
        
        status = self.player.get_status_info()
        self.hp_percent = status['hp_percent']
        self.xp_percent = status['xp_percent']
        self.player_level = status['level']
    
    def pause_game(self):
        """Oyunu duraklat"""
        # GameManager'dan çağrılacak
        pass
