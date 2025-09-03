#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Entities/Enemy.py - Düşman sınıfları
"""

from .base import BaseEntity
from kivy.graphics import Color, Ellipse


class Enemy(BaseEntity):
    """Temel düşman sınıfı"""
    
    def __init__(self, enemy_type="slime", **kwargs):
        super().__init__(**kwargs)
        self.radius = 8
        self.size = (self.radius * 2, self.radius * 2)
        self.color = (1.0, 0.2, 0.2, 1.0)  # Kırmızı
        self.max_hp = 20.0
        self.current_hp = 20.0
        self.enemy_type = enemy_type
        self.damage = 5.0
        self.move_speed = 30.0
        self.target_pos = [0, 0]
        
    def _setup_graphics(self):
        """Düşman grafiklerini ayarla"""
        with self.canvas:
            Color(1.0, 0.2, 0.2, 1.0)  # Kırmızı
            self.graphic = Ellipse(pos=self.pos, size=self.size)
        self.bind(pos=self._update_graphics, size=self._update_graphics)
    
    def _update_graphics(self, *args):
        """Grafikleri güncelle"""
        if hasattr(self, 'graphic'):
            self.graphic.pos = self.pos
            self.graphic.size = self.size
    
    def update(self, dt: float):
        """Düşmanı güncelle"""
        if not self.is_alive:
            return
        
        # Hedefe doğru hareket et
        self.set_velocity_towards(self.target_pos[0], self.target_pos[1], self.move_speed)
        self.move(dt)
        
        # Hasar zamanlayıcısını güncelle (basit implementasyon)
        pass
    
    def set_target(self, x: float, y: float):
        """Hedef pozisyon ayarla"""
        self.target_pos = [x, y]
    
    def take_damage(self, amount: float) -> bool:
        """Hasar al"""
        if not self.is_alive:
            return False
        self.current_hp = max(0, self.current_hp - amount)
        if self.current_hp <= 0:
            self.kill()
        return True
