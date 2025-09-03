#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Systems/Combat.py - Savaş sistemi
"""

from typing import List, Optional
from entities.player import Player
from entities.enemy import Enemy
from entities.projectile import Projectile
from entities.loot import LootOrb


class CombatSystem:
    """Savaş sistemi"""
    
    def __init__(self):
        pass
    
    def update(self, dt: float, player: Optional[Player], enemies: List[Enemy], 
               projectiles: List[Projectile]) -> List[LootOrb]:
        """Savaş sistemini güncelle"""
        
        new_loot = []
        
        # Ölen düşmanlardan loot oluştur
        for enemy in enemies[:]:
            if enemy.is_dead():
                # XP orb oluştur
                loot = LootOrb(xp_value=1.0)
                enemy_x, enemy_y = enemy.get_center()
                loot.set_position(enemy_x, enemy_y)
                new_loot.append(loot)
        
        return new_loot
