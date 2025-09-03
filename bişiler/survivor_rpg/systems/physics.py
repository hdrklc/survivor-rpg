#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Systems/Physics.py - Fizik ve çarpışma sistemi
"""

from typing import List, Optional
from entities.player import Player
from entities.enemy import Enemy
from entities.projectile import Projectile
from entities.loot import LootOrb


class PhysicsSystem:
    """Fizik ve çarpışma sistemi"""
    
    def __init__(self):
        pass
    
    def update(self, dt: float, player: Optional[Player], enemies: List[Enemy], 
               projectiles: List[Projectile], loot_orbs: List[LootOrb]):
        """Fizik sistemini güncelle"""
        
        if not player or not player.is_alive:
            return
        
        # Oyuncu - düşman çarpışması
        for enemy in enemies[:]:
            if enemy.is_alive and player.is_colliding_with(enemy):
                if player.take_damage(enemy.damage * dt):  # DPS hasarı
                    pass  # Hasar alındı
        
        # Mermi - düşman çarpışması
        for projectile in projectiles[:]:
            if not projectile.is_alive:
                continue
                
            for enemy in enemies[:]:
                if enemy.is_alive and projectile.is_colliding_with(enemy):
                    enemy.take_damage(projectile.damage)
                    projectile.hit_target()
                    break
        
        # Oyuncu - loot çarpışması
        player_x, player_y = player.get_center()
        magnet_range = player.get_magnet_range()
        
        for loot in loot_orbs[:]:
            if not loot.is_alive or loot.collected:
                continue
                
            distance = player.get_distance_to(loot)
            
            if distance <= magnet_range:
                # Magnet etkisi
                loot.magnetize_to(player_x, player_y)
                
            if distance <= (player.radius + loot.radius + 5):
                # Toplama
                player.collect_loot(loot.xp_value, 'xp')
                loot.collect()
