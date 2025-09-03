#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Entities/Base.py - Temel varlık sınıfları
"""

from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.properties import ListProperty, NumericProperty, BooleanProperty
from typing import Tuple, Optional
import math


class BaseEntity(Widget):
    """Tüm oyun varlıkları için temel sınıf"""
    
    # Pozisyon ve hareket
    velocity = ListProperty([0.0, 0.0])
    speed = NumericProperty(0.0)
    
    # Boyut ve çarpışma
    radius = NumericProperty(10.0)
    
    # Durum
    is_alive = BooleanProperty(True)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (self.radius * 2, self.radius * 2)
        
        # Grafik bileşenlerini başlat
        self._setup_graphics()
        
    def _setup_graphics(self):
        """Grafik bileşenlerini ayarla (alt sınıflarda override edilmeli)"""
        pass
    
    def update(self, dt: float):
        """Varlığı güncelle (alt sınıflarda override edilmeli)"""
        pass
    
    def move(self, dt: float):
        """Temel hareket fonksiyonu"""
        if not self.is_alive:
            return
            
        # Pozisyonu güncelle
        self.x += self.velocity[0] * dt
        self.y += self.velocity[1] * dt
        
    def set_position(self, x: float, y: float):
        """Pozisyon ayarla"""
        self.pos = (x - self.radius, y - self.radius)
        
    def get_center(self) -> Tuple[float, float]:
        """Merkez pozisyonunu döndür"""
        return (self.x + self.radius, self.y + self.radius)
    
    def get_distance_to(self, other: 'BaseEntity') -> float:
        """Başka bir varlığa olan mesafe"""
        x1, y1 = self.get_center()
        x2, y2 = other.get_center()
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    
    def is_colliding_with(self, other: 'BaseEntity') -> bool:
        """Başka bir varlıkla çarpışıyor mu?"""
        distance = self.get_distance_to(other)
        return distance <= (self.radius + other.radius)
    
    def get_direction_to(self, target_x: float, target_y: float) -> Tuple[float, float]:
        """Hedef pozisyona olan yön vektörü (normalize edilmiş)"""
        x, y = self.get_center()
        dx = target_x - x
        dy = target_y - y
        
        distance = math.sqrt(dx*dx + dy*dy)
        if distance == 0:
            return (0, 0)
            
        return (dx / distance, dy / distance)
    
    def set_velocity_towards(self, target_x: float, target_y: float, speed: float):
        """Hedef pozisyona doğru hız ayarla"""
        direction_x, direction_y = self.get_direction_to(target_x, target_y)
        self.velocity = [direction_x * speed, direction_y * speed]
        self.speed = speed
    
    def kill(self):
        """Varlığı öldür"""
        self.is_alive = False
    
    def is_dead(self) -> bool:
        """Ölü mü?"""
        return not self.is_alive
    
    def is_out_of_bounds(self, screen_width: float, screen_height: float, 
                        margin: float = 200) -> bool:
        """Ekran sınırları dışında mı?"""
        x, y = self.get_center()
        return (x < -margin or x > screen_width + margin or 
                y < -margin or y > screen_height + margin)


# Mixin sınıfları (multiple inheritance yerine composition kullanacağız)
