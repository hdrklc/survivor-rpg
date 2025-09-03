#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Entities/Player.py - Oyuncu sınıfı
"""

import math
from typing import List, Dict, Any, Tuple
from kivy.graphics import Color, Ellipse
from kivy.clock import Clock

from .base import BaseEntity
from core.state import PlayerStats


class Player(BaseEntity):
    """Ana oyuncu karakteri"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Temel özellikler
        self.radius = 12
        self.size = (self.radius * 2, self.radius * 2)
        
        # Hareket özellikleri
        self.max_speed = 150.0
        self.acceleration = 800.0
        self.friction = 0.85
        self.target_velocity = [0.0, 0.0]
        
        # Sağlık özellikleri
        self.max_hp = 100.0
        self.current_hp = 100.0
        self.damage_immunity_time = 0.5
        self._damage_timer = 0.0
        
        # Oyuncu istatistikleri
        self.stats = PlayerStats()
        
        # Yetenekler
        self.abilities: List[Dict[str, Any]] = []
        
        # Saldırı sistemi
        self.last_attack_time = 0.0
        self.auto_fire_enabled = True
        
        # XP sistemi
        self._pending_level_up = False
        
        # Magnet sistemi
        self.magnet_range = 50.0
        
        # Grafikleri ayarla
        self._setup_graphics()
        
    def _setup_graphics(self):
        """Oyuncu grafiklerini ayarla"""
        with self.canvas:
            # Ana karakter (mavi daire)
            Color(0.2, 0.8, 1.0, 1.0)
            self.body = Ellipse(pos=self.pos, size=self.size)
            
            # İç nokta (beyaz)
            Color(1, 1, 1, 0.8)
            inner_size = (self.radius, self.radius)
            inner_pos = (self.x + self.radius/2, self.y + self.radius/2)
            self.inner = Ellipse(pos=inner_pos, size=inner_size)
            
        self.bind(pos=self._update_graphics, size=self._update_graphics)
    
    def _update_graphics(self, *args):
        """Grafikleri güncelle"""
        if hasattr(self, 'body'):
            self.body.pos = self.pos
            self.body.size = self.size
            
        if hasattr(self, 'inner'):
            inner_size = (self.radius, self.radius)
            inner_pos = (self.x + self.radius/2, self.y + self.radius/2)
            self.inner.pos = inner_pos
            self.inner.size = inner_size
    
    def set_movement_input(self, input_vector: Tuple[float, float]):
        """Hareket girişi ayarla"""
        self.target_velocity = [
            input_vector[0] * self.max_speed,
            input_vector[1] * self.max_speed
        ]
    
    def update_movement(self, dt: float):
        """Hareket güncellemesi"""
        current_vx, current_vy = self.velocity
        target_vx, target_vy = self.target_velocity
        
        accel = self.acceleration * dt
        
        if target_vx != 0 or target_vy != 0:
            diff_x = target_vx - current_vx
            diff_y = target_vy - current_vy
            
            if abs(diff_x) > accel:
                diff_x = accel if diff_x > 0 else -accel
            if abs(diff_y) > accel:
                diff_y = accel if diff_y > 0 else -accel
                
            self.velocity = [current_vx + diff_x, current_vy + diff_y]
        else:
            self.velocity = [current_vx * self.friction, current_vy * self.friction]
            
            if abs(self.velocity[0]) < 1.0:
                self.velocity[0] = 0
            if abs(self.velocity[1]) < 1.0:
                self.velocity[1] = 0
        
        speed = math.sqrt(self.velocity[0]**2 + self.velocity[1]**2)
        if speed > self.max_speed:
            self.velocity[0] = self.velocity[0] * self.max_speed / speed
            self.velocity[1] = self.velocity[1] * self.max_speed / speed
            
        self.speed = speed
    
    def update_damage_timer(self, dt: float):
        """Hasar zamanlayıcısı"""
        if self._damage_timer > 0:
            self._damage_timer -= dt
            if self._damage_timer < 0:
                self._damage_timer = 0
    
    def update(self, dt: float):
        """Oyuncuyu güncelle"""
        if not self.is_alive:
            return
            
        # Hareket güncellemesi
        self.update_movement(dt)
        self.move(dt)
        
        # Hasar zamanlayıcısı
        self.update_damage_timer(dt)
        
        # Saldırı zamanlayıcısı
        self.last_attack_time += dt
        
        # İstatistikleri güncelle
        self.max_speed = self.stats.get_total_speed() * 50
        self.max_hp = self.stats.get_max_hp()
        
        if self.current_hp > self.max_hp:
            self.current_hp = self.max_hp
    
    def take_damage(self, amount: float) -> bool:
        """Hasar al"""
        if self._damage_timer > 0 or not self.is_alive:
            return False
            
        self.current_hp = max(0, self.current_hp - amount)
        self._damage_timer = self.damage_immunity_time
        self.stats.take_damage(amount)
        
        if self.current_hp <= 0:
            self.kill()
            
        return True
    
    def heal(self, amount: float):
        """İyileştir"""
        if not self.is_alive:
            return
        self.current_hp = min(self.max_hp, self.current_hp + amount)
        self.stats.heal(amount)
    
    def add_xp(self, amount: float):
        """XP ekle"""
        if self.stats.add_xp(amount):
            self._pending_level_up = True
    
    def needs_level_up(self) -> bool:
        """Level atlaması gerekiyor mu?"""
        return self._pending_level_up
    
    def level_up(self):
        """Level atla"""
        if self._pending_level_up:
            self.stats.level_up()
            self._pending_level_up = False
    
    def add_ability(self, ability: Dict[str, Any]):
        """Yetenek ekle"""
        self.abilities.append(ability)
        self._apply_ability_effects(ability)
    
    def _apply_ability_effects(self, ability: Dict[str, Any]):
        """Yetenek etkilerini uygula"""
        ability_type = ability.get('type', '')
        
        if ability_type == 'speed':
            bonus = ability.get('bonus', 0.1)
            self.stats.speed_multiplier += bonus
        elif ability_type == 'damage':
            bonus = ability.get('bonus', 0.1)
            self.stats.damage_multiplier += bonus
        elif ability_type == 'health':
            bonus = ability.get('bonus', 0.2)
            old_max = self.stats.get_max_hp()
            self.stats.hp_multiplier += bonus
            new_max = self.stats.get_max_hp()
            hp_increase = new_max - old_max
            self.heal(hp_increase)
        elif ability_type == 'magnet':
            bonus = ability.get('bonus', 0.2)
            self.stats.magnet_range += self.stats.magnet_range * bonus
            self.magnet_range = self.stats.magnet_range
        elif ability_type == 'attack_speed':
            bonus = ability.get('bonus', 0.15)
            self.stats.attack_speed_multiplier += bonus
    
    def can_attack(self) -> bool:
        """Saldırabilir mi?"""
        if not self.auto_fire_enabled:
            return False
        attack_cooldown = 1.0 / self.stats.get_total_attack_speed()
        return self.last_attack_time >= attack_cooldown
    
    def attack(self) -> bool:
        """Saldırı yap"""
        if self.can_attack():
            self.last_attack_time = 0.0
            return True
        return False
    
    def get_attack_damage(self) -> float:
        """Saldırı hasarını hesapla"""
        return self.stats.get_total_damage()
    
    def get_projectile_count(self) -> int:
        """Mermi sayısını hesapla"""
        count = 1
        for ability in self.abilities:
            if ability.get('type') == 'multishot':
                count += ability.get('bonus_projectiles', 1)
        return count
    
    def get_magnet_range(self) -> float:
        """Magnet menzilini döndür"""
        return self.magnet_range
    
    def collect_loot(self, loot_value: float, loot_type: str = 'xp'):
        """Loot topla"""
        if loot_type == 'xp':
            self.add_xp(loot_value)
        elif loot_type == 'health':
            self.heal(loot_value)
    
    def get_status_info(self) -> Dict[str, Any]:
        """Durum bilgilerini döndür"""
        return {
            'hp': self.current_hp,
            'max_hp': self.max_hp,
            'hp_percent': (self.current_hp / self.max_hp) * 100 if self.max_hp > 0 else 0,
            'level': self.stats.level,
            'xp': self.stats.current_xp,
            'xp_to_next': self.stats.xp_to_next_level,
            'xp_percent': (self.stats.current_xp / self.stats.xp_to_next_level) * 100 if self.stats.xp_to_next_level > 0 else 0,
            'damage': self.stats.get_total_damage(),
            'speed': self.stats.get_total_speed(),
            'attack_speed': self.stats.get_total_attack_speed(),
            'abilities_count': len(self.abilities),
        }
    
    def flash_damage(self, duration: float = 0.1):
        """Hasar flash efekti"""
        # Basit flash efekti
        pass
    
    @property
    def level(self) -> int:
        """Mevcut level"""
        return self.stats.level