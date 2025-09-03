#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Entities/Projectile.py - Mermi sınıfları
"""

from .base import BaseEntity
from kivy.graphics import Color, Ellipse


class Projectile(BaseEntity):
    """Temel mermi sınıfı"""
    
    def __init__(self, damage=10.0, **kwargs):
        super().__init__(**kwargs)
        self.radius = 3
        self.size = (self.radius * 2, self.radius * 2)
        self.color = (1.0, 1.0, 0.5, 1.0)  # Sarımsı
        self.damage = damage
        self.lifetime = 2.0  # 2 saniye yaşam süresi
        self.age = 0.0
        
    def _setup_graphics(self):
        """Mermi grafiklerini ayarla"""
        with self.canvas:
            Color(1.0, 1.0, 0.5, 1.0)  # Sarı
            self.graphic = Ellipse(pos=self.pos, size=self.size)
        self.bind(pos=self._update_graphics, size=self._update_graphics)
    
    def _update_graphics(self, *args):
        """Grafikleri güncelle"""
        if hasattr(self, 'graphic'):
            self.graphic.pos = self.pos
            self.graphic.size = self.size
    
    def update(self, dt: float):
        """Mermiyi güncelle"""
        if not self.is_alive:
            return
        
        # Hareket et
        self.move(dt)
        
        # Yaşlanma
        self.age += dt
        if self.age >= self.lifetime:
            self.kill()
    
    def hit_target(self):
        """Hedefe çarptı"""
        self.kill()
