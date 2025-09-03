#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Graphics/ParticleSystem.py - Profesyonel parçacık efekt sistemi
"""

import math
import random
from typing import List, Tuple, Optional
from kivy.graphics import Color, Ellipse, Line, PushMatrix, PopMatrix, Scale
from kivy.clock import Clock


class Particle:
    """Tek bir parçacık"""
    
    def __init__(self, x: float, y: float, vel_x: float, vel_y: float,
                 color: Tuple[float, float, float, float], size: float,
                 lifetime: float, gravity: float = 0.0):
        self.x = x
        self.y = y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.color = list(color)
        self.size = size
        self.initial_size = size
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.gravity = gravity
        self.alive = True
        
        # Efekt özellikleri
        self.fade_out = True
        self.shrink = True
        self.spin = 0.0
        self.spin_speed = 0.0
    
    def update(self, dt: float):
        """Parçacığı güncelle"""
        if not self.alive:
            return
        
        # Pozisyon güncellemesi
        self.x += self.vel_x * dt
        self.y += self.vel_y * dt
        
        # Yerçekimi
        self.vel_y -= self.gravity * dt
        
        # Dönme
        self.spin += self.spin_speed * dt
        
        # Yaşam süresi
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.alive = False
            return
        
        # Yaşlanma efektleri
        age_ratio = 1.0 - (self.lifetime / self.max_lifetime)
        
        if self.fade_out:
            self.color[3] = 1.0 - age_ratio  # Alpha fade
        
        if self.shrink:
            self.size = self.initial_size * (1.0 - age_ratio * 0.8)


class ParticleEmitter:
    """Parçacık yayıcısı"""
    
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.particles: List[Particle] = []
        self.active = True
        
        # Yayıcı özellikleri
        self.emission_rate = 50.0  # saniyede parçacık sayısı
        self.emission_timer = 0.0
        self.burst_mode = False
        self.duration = -1.0  # -1 = sonsuz
        self.age = 0.0
        
        # Parçacık özellikleri
        self.particle_lifetime = (1.0, 2.0)  # min, max
        self.particle_size = (2.0, 4.0)
        self.particle_speed = (50.0, 100.0)
        self.particle_direction = (0.0, 360.0)  # derece
        self.particle_colors = [(1, 1, 1, 1)]
        self.gravity = 0.0
        self.spread_angle = 360.0  # derece
    
    def set_position(self, x: float, y: float):
        """Pozisyon ayarla"""
        self.x = x
        self.y = y
    
    def emit_burst(self, count: int):
        """Patlama halinde parçacık yay"""
        for _ in range(count):
            self._create_particle()
    
    def _create_particle(self):
        """Yeni parçacık oluştur"""
        # Rastgele özellikler
        lifetime = random.uniform(*self.particle_lifetime)
        size = random.uniform(*self.particle_size)
        speed = random.uniform(*self.particle_speed)
        
        # Yön hesaplama
        if self.spread_angle >= 360:
            angle = random.uniform(0, 2 * math.pi)
        else:
            base_angle = math.radians(self.particle_direction[0])
            spread = math.radians(self.spread_angle)
            angle = base_angle + random.uniform(-spread/2, spread/2)
        
        vel_x = math.cos(angle) * speed
        vel_y = math.sin(angle) * speed
        
        # Renk seçimi
        color = random.choice(self.particle_colors)
        
        # Parçacık oluştur
        particle = Particle(self.x, self.y, vel_x, vel_y, color, size, lifetime, self.gravity)
        
        # Rastgele efektler
        particle.spin_speed = random.uniform(-180, 180)  # derece/saniye
        
        self.particles.append(particle)
    
    def update(self, dt: float):
        """Yayıcıyı güncelle"""
        if not self.active:
            return
        
        self.age += dt
        
        # Süre kontrolü
        if self.duration > 0 and self.age >= self.duration:
            self.active = False
        
        # Yeni parçacık yayma
        if self.active and not self.burst_mode:
            self.emission_timer += dt
            particles_to_emit = int(self.emission_timer * self.emission_rate)
            if particles_to_emit > 0:
                self.emission_timer = 0.0
                for _ in range(particles_to_emit):
                    self._create_particle()
        
        # Mevcut parçacıkları güncelle
        for particle in self.particles[:]:
            particle.update(dt)
            if not particle.alive:
                self.particles.remove(particle)
    
    def render(self, canvas):
        """Parçacıkları render et"""
        for particle in self.particles:
            if not particle.alive:
                continue
            
            with canvas:
                Color(*particle.color)
                
                if particle.spin != 0:
                    PushMatrix()
                    # Rotation around particle center
                    # Note: Kivy rotation is in degrees
                    from kivy.graphics import Rotate
                    Rotate(angle=math.degrees(particle.spin), 
                          origin=(particle.x, particle.y))
                
                # Parçacığı çiz
                size = particle.size
                Ellipse(pos=(particle.x - size/2, particle.y - size/2), 
                       size=(size, size))
                
                if particle.spin != 0:
                    PopMatrix()
    
    def is_finished(self) -> bool:
        """Yayıcı bitti mi?"""
        return not self.active and len(self.particles) == 0


class ParticleSystem:
    """Ana parçacık sistem yöneticisi"""
    
    def __init__(self):
        self.emitters: List[ParticleEmitter] = []
        
    def create_explosion(self, x: float, y: float, intensity: float = 1.0) -> ParticleEmitter:
        """Patlama efekti oluştur"""
        emitter = ParticleEmitter(x, y)
        emitter.burst_mode = True
        emitter.particle_lifetime = (0.5, 1.5)
        emitter.particle_size = (3.0 * intensity, 8.0 * intensity)
        emitter.particle_speed = (80.0 * intensity, 150.0 * intensity)
        emitter.particle_colors = [
            (1.0, 0.8, 0.0, 1.0),  # Sarı
            (1.0, 0.4, 0.0, 1.0),  # Turuncu
            (1.0, 0.0, 0.0, 1.0),  # Kırmızı
        ]
        emitter.gravity = 100.0
        emitter.spread_angle = 360.0
        
        # Patlamayı başlat
        particle_count = int(20 * intensity)
        emitter.emit_burst(particle_count)
        emitter.active = False  # Sadece burst
        
        self.emitters.append(emitter)
        return emitter
    
    def create_heal_effect(self, x: float, y: float) -> ParticleEmitter:
        """İyileştirme efekti"""
        emitter = ParticleEmitter(x, y)
        emitter.emission_rate = 30.0
        emitter.duration = 1.0
        emitter.particle_lifetime = (1.0, 2.0)
        emitter.particle_size = (2.0, 4.0)
        emitter.particle_speed = (20.0, 50.0)
        emitter.particle_colors = [
            (0.0, 1.0, 0.0, 1.0),  # Yeşil
            (0.5, 1.0, 0.5, 1.0),  # Açık yeşil
            (1.0, 1.0, 1.0, 1.0),  # Beyaz
        ]
        emitter.gravity = -50.0  # Yukarı doğru
        emitter.spread_angle = 60.0
        emitter.particle_direction = (90.0, 90.0)  # Yukarı
        
        self.emitters.append(emitter)
        return emitter
    
    def create_damage_numbers(self, x: float, y: float, damage: int) -> ParticleEmitter:
        """Hasar sayıları efekti"""
        emitter = ParticleEmitter(x, y)
        emitter.burst_mode = True
        emitter.particle_lifetime = (1.5, 1.5)
        emitter.particle_size = (8.0, 8.0)
        emitter.particle_speed = (30.0, 60.0)
        emitter.particle_colors = [
            (1.0, 1.0, 0.0, 1.0) if damage >= 50 else (1.0, 0.5, 0.5, 1.0)
        ]
        emitter.gravity = -20.0  # Hafif yukarı
        emitter.spread_angle = 45.0
        emitter.particle_direction = (90.0, 90.0)
        
        # Tek parçacık (sayı için)
        emitter.emit_burst(1)
        emitter.active = False
        
        self.emitters.append(emitter)
        return emitter
    
    def create_level_up_effect(self, x: float, y: float) -> ParticleEmitter:
        """Level up efekti"""
        emitter = ParticleEmitter(x, y)
        emitter.burst_mode = True
        emitter.particle_lifetime = (2.0, 3.0)
        emitter.particle_size = (4.0, 8.0)
        emitter.particle_speed = (50.0, 120.0)
        emitter.particle_colors = [
            (1.0, 1.0, 0.0, 1.0),  # Altın
            (1.0, 0.8, 0.0, 1.0),  # Koyu altın
            (1.0, 1.0, 1.0, 1.0),  # Beyaz
        ]
        emitter.gravity = 50.0
        emitter.spread_angle = 360.0
        
        emitter.emit_burst(50)
        emitter.active = False
        
        self.emitters.append(emitter)
        return emitter
    
    def create_muzzle_flash(self, x: float, y: float, angle: float) -> ParticleEmitter:
        """Namlu alevi efekti"""
        emitter = ParticleEmitter(x, y)
        emitter.burst_mode = True
        emitter.particle_lifetime = (0.1, 0.3)
        emitter.particle_size = (2.0, 4.0)
        emitter.particle_speed = (100.0, 200.0)
        emitter.particle_colors = [
            (1.0, 1.0, 0.8, 1.0),  # Beyazımsı
            (1.0, 0.9, 0.0, 1.0),  # Sarı
        ]
        emitter.gravity = 0.0
        emitter.spread_angle = 30.0
        emitter.particle_direction = (math.degrees(angle), math.degrees(angle))
        
        emitter.emit_burst(8)
        emitter.active = False
        
        self.emitters.append(emitter)
        return emitter
    
    def update(self, dt: float):
        """Tüm parçacık sistemlerini güncelle"""
        for emitter in self.emitters[:]:
            emitter.update(dt)
            if emitter.is_finished():
                self.emitters.remove(emitter)
    
    def render(self, canvas):
        """Tüm parçacıkları render et"""
        for emitter in self.emitters:
            emitter.render(canvas)
    
    def clear(self):
        """Tüm parçacıkları temizle"""
        self.emitters.clear()
    
    def get_particle_count(self) -> int:
        """Toplam parçacık sayısı"""
        return sum(len(emitter.particles) for emitter in self.emitters)


# Global parçacık sistemi
particle_system = ParticleSystem()
