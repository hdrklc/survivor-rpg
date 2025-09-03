#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Entities/Loot.py - Loot sınıfları
"""

from .base import BaseEntity
from kivy.graphics import Color, Ellipse


class LootOrb(BaseEntity):
    """XP orb'u"""
    
    def __init__(self, xp_value=1.0, **kwargs):
        super().__init__(**kwargs)
        self.radius = 4
        self.size = (self.radius * 2, self.radius * 2)
        self.color = (0.2, 1.0, 0.2, 1.0)  # Yeşil
        self.xp_value = xp_value
        self.collected = False
        self.magnet_speed = 150.0
        self.is_magnetized = False
        
    def _setup_graphics(self):
        """Loot grafiklerini ayarla"""
        with self.canvas:
            Color(0.2, 1.0, 0.2, 1.0)  # Yeşil
            self.graphic = Ellipse(pos=self.pos, size=self.size)
        self.bind(pos=self._update_graphics, size=self._update_graphics)
    
    def _update_graphics(self, *args):
        """Grafikleri güncelle"""
        if hasattr(self, 'graphic'):
            self.graphic.pos = self.pos
            self.graphic.size = self.size
    
    def update(self, dt: float):
        """Loot'u güncelle"""
        if not self.is_alive or self.collected:
            return
        
        # Magnet etkisi varsa hareket et
        if self.is_magnetized:
            self.move(dt)
    
    def magnetize_to(self, target_x: float, target_y: float):
        """Hedefe doğru çek"""
        self.is_magnetized = True
        self.set_velocity_towards(target_x, target_y, self.magnet_speed)
    
    def collect(self):
        """Topla"""
        self.collected = True
        self.kill()
    
    def is_collected(self) -> bool:
        """Toplandı mı?"""
        return self.collected
