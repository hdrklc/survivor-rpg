#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Systems/Spawn.py - Düşman spawn sistemi
"""

from typing import List, Dict
from entities.enhanced_enemies import EnhancedEnemy, EnemyFactory
from core.rng import GameRNG


class SpawnSystem:
    """Gelişmiş düşman spawn sistemi"""
    
    def __init__(self, rng: GameRNG):
        self.rng = rng
        self.spawn_timer = 0.0
        self.spawn_interval = 1.5  # Daha hızlı spawn
        self.wave_intensity = 1.0
        
    def update(self, dt: float, game_time: float, spawn_bounds: Dict) -> List[EnhancedEnemy]:
        """Gelişmiş spawn sistemi"""
        self.spawn_timer += dt
        
        # Dakika bazlı zorluk
        minute = int(game_time // 60)
        difficulty = EnemyFactory.get_difficulty_scale(minute)
        
        # Spawn hızı artışı
        current_interval = self.spawn_interval / (1.0 + minute * 0.1)
        
        new_enemies = []
        
        if self.spawn_timer >= current_interval:
            self.spawn_timer = 0.0
            
            # Çoklu spawn (daha sonraki dakikalarda)
            spawn_count = 1
            if minute >= 3:
                spawn_count = self.rng.random_int(1, 2)
            if minute >= 6:
                spawn_count = self.rng.random_int(2, 3)
            if minute >= 10:
                spawn_count = self.rng.random_int(3, 5)
            
            for _ in range(spawn_count):
                # Düşman türü seçimi
                enemy_type = EnemyFactory.get_random_enemy_type(minute)
                
                # Spawn pozisyonu
                spawn_x, spawn_y = self.rng.random_offscreen_position(
                    spawn_bounds.get('right', 800) - spawn_bounds.get('left', 0),
                    spawn_bounds.get('top', 600) - spawn_bounds.get('bottom', 0),
                    120
                )
                spawn_x += spawn_bounds.get('left', 0)
                spawn_y += spawn_bounds.get('bottom', 0)
                
                # Düşman oluştur
                enemy = EnemyFactory.create_enemy(enemy_type, spawn_x, spawn_y, difficulty)
                new_enemies.append(enemy)
        
        return new_enemies
