#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Systems/Abilities.py - Yetenek sistemi
"""

import math
from typing import List, Optional, Dict, Any
from entities.player import Player
from entities.enemy import Enemy
from entities.projectile import Projectile


class AbilitySystem:
    """Yetenek sistemi"""
    
    def __init__(self):
        self.available_abilities = [
            {
                'id': 'multishot',
                'name': 'Çoklu Atış',
                'description': '+1 mermi sayısı',
                'type': 'multishot',
                'bonus_projectiles': 1
            },
            {
                'id': 'damage',
                'name': 'Güç Artışı',
                'description': '+20% hasar',
                'type': 'damage',
                'bonus': 0.2
            },
            {
                'id': 'speed',
                'name': 'Hız Artışı',
                'description': '+15% hareket hızı',
                'type': 'speed',
                'bonus': 0.15
            },
            {
                'id': 'health',
                'name': 'Sağlık Artışı',
                'description': '+25% maksimum HP',
                'type': 'health',
                'bonus': 0.25
            },
            {
                'id': 'magnet',
                'name': 'Manyetik Alan',
                'description': '+30% çekim alanı',
                'type': 'magnet',
                'bonus': 0.3
            },
            {
                'id': 'attack_speed',
                'name': 'Hızlı Atış',
                'description': '+20% saldırı hızı',
                'type': 'attack_speed',
                'bonus': 0.2
            }
        ]
    
    def update(self, dt: float, player: Optional[Player], enemies: List[Enemy]) -> List[Projectile]:
        """Yetenek sistemini güncelle"""
        
        new_projectiles = []
        
        if not player or not player.is_alive:
            return new_projectiles
        
        # Auto-fire sistemi
        if player.can_attack() and player.attack():
            # Mermiler oluştur
            projectile_count = player.get_projectile_count()
            damage = player.get_attack_damage()
            
            player_x, player_y = player.get_center()
            
            # Dairesel yayılım
            for i in range(projectile_count):
                angle = (2 * math.pi * i) / projectile_count
                
                projectile = Projectile(damage=damage)
                projectile.set_position(player_x, player_y)
                
                # Hız vektörü
                speed = 200.0
                vel_x = math.cos(angle) * speed
                vel_y = math.sin(angle) * speed
                projectile.velocity = [vel_x, vel_y]
                
                new_projectiles.append(projectile)
        
        return new_projectiles
    
    def get_random_abilities(self, count: int, current_abilities: List[Dict]) -> List[Dict]:
        """Rastgele yetenekler seç"""
        import random
        
        # Mevcut yetenekleri filtrele (aynısından sadece 3 tane)
        current_counts = {}
        for ability in current_abilities:
            ability_id = ability.get('id', '')
            current_counts[ability_id] = current_counts.get(ability_id, 0) + 1
        
        available = []
        for ability in self.available_abilities:
            if current_counts.get(ability['id'], 0) < 3:
                available.append(ability.copy())
        
        if len(available) <= count:
            return available
        
        return random.sample(available, count)
