#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Systems/Movement.py - Hareket sistemi
"""

from typing import List, Optional
from entities.player import Player
from entities.enemy import Enemy
from entities.projectile import Projectile


class MovementSystem:
    """Hareket sistemi"""
    
    def __init__(self):
        pass
    
    def update(self, dt: float, player: Optional[Player], enemies: List[Enemy], 
               projectiles: List[Projectile]):
        """Hareket sistemini güncelle"""
        
        # Oyuncu hareketi
        if player and player.is_alive:
            player.update(dt)
        
        # Düşman hareketi
        if player and player.is_alive:
            player_x, player_y = player.get_center()
            for enemy in enemies:
                if enemy.is_alive:
                    enemy.set_target(player_x, player_y)
                    enemy.update(dt)
        
        # Mermi hareketi
        for projectile in projectiles:
            if projectile.is_alive:
                projectile.update(dt)
