#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Survivor RPG - Profesyonel versiyon
Tüm özelliklerle birlikte
"""

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.graphics import Color, Ellipse, Rectangle, PushMatrix, PopMatrix, Rotate, Scale, Line
from kivy.graphics.texture import Texture
from kivy.clock import Clock
from kivy.properties import ListProperty, NumericProperty
from kivy.logger import Logger
from kivy.core.window import Window
import math
import random
import struct
import tempfile
import os

class ParticleSystem:
    """Parçacık efekt sistemi"""
    
    def __init__(self):
        self.particles = []
    
    def add_explosion(self, x, y, color=(1,0.5,0,1), count=15):
        """Patlama efekti ekle"""
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(50, 150)
            lifetime = random.uniform(0.5, 1.2)
            
            particle = {
                'x': x, 'y': y,
                'vx': math.cos(angle) * speed,
                'vy': math.sin(angle) * speed,
                'color': list(color),
                'lifetime': lifetime,
                'max_lifetime': lifetime,
                'size': random.uniform(3, 8)
            }
            self.particles.append(particle)
    
    def add_blood(self, x, y, count=8):
        """Kan efekti"""
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(30, 80)
            lifetime = random.uniform(0.3, 0.8)
            
            particle = {
                'x': x, 'y': y,
                'vx': math.cos(angle) * speed,
                'vy': math.sin(angle) * speed,
                'color': [0.8, 0.1, 0.1, 1.0],  # Kırmızı kan
                'lifetime': lifetime,
                'max_lifetime': lifetime,
                'size': random.uniform(2, 5)
            }
            self.particles.append(particle)
    
    def add_muzzle_flash(self, x, y, angle):
        """Namlu alevi"""
        for _ in range(5):
            spread = random.uniform(-0.3, 0.3)
            flash_angle = angle + spread
            speed = random.uniform(100, 200)
            lifetime = random.uniform(0.1, 0.2)
            
            particle = {
                'x': x, 'y': y,
                'vx': math.cos(flash_angle) * speed,
                'vy': math.sin(flash_angle) * speed,
                'color': [1.0, 1.0, 0.8, 1.0],  # Beyazımsı
                'lifetime': lifetime,
                'max_lifetime': lifetime,
                'size': random.uniform(2, 4)
            }
            self.particles.append(particle)
    
    def add_level_up(self, x, y):
        """Level up efekti"""
        for _ in range(30):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(80, 200)
            lifetime = random.uniform(1.0, 2.0)
            
            particle = {
                'x': x, 'y': y,
                'vx': math.cos(angle) * speed,
                'vy': math.sin(angle) * speed,
                'color': [1.0, 1.0, 0.0, 1.0],  # Altın
                'lifetime': lifetime,
                'max_lifetime': lifetime,
                'size': random.uniform(4, 10)
            }
            self.particles.append(particle)
    
    def update(self, dt):
        """Parçacıkları güncelle"""
        for particle in self.particles[:]:
            particle['x'] += particle['vx'] * dt
            particle['y'] += particle['vy'] * dt
            particle['vy'] -= 100 * dt  # Yerçekimi
            particle['lifetime'] -= dt
            
            # Fade out
            age_ratio = 1.0 - (particle['lifetime'] / particle['max_lifetime'])
            particle['color'][3] = 1.0 - age_ratio
            
            if particle['lifetime'] <= 0:
                self.particles.remove(particle)
    
    def render(self, canvas):
        """Parçacıkları çiz"""
        # Canvas'ı temizle önce
        canvas.clear()
        
        for particle in self.particles:
            with canvas:
                Color(*particle['color'])
                size = particle['size']
                Ellipse(
                    pos=(particle['x'] - size/2, particle['y'] - size/2),
                    size=(size, size)
                )

class SoundManager:
    """Basit ses yöneticisi"""
    
    def __init__(self):
        self.enabled = True
        self.sounds = {}
        self._create_procedural_sounds()
    
    def _create_procedural_sounds(self):
        """Procedural sesler oluştur"""
        try:
            # Basit ses efektleri oluştur (placeholder)
            self.sounds = {
                'shoot': True,
                'hit': True,
                'explosion': True,
                'levelup': True
            }
            Logger.info("SoundManager: Sesler oluşturuldu")
        except Exception as e:
            Logger.warning(f"SoundManager: Ses oluşturma hatası: {e}")
    
    def play(self, sound_name):
        """Ses çal"""
        if self.enabled and sound_name in self.sounds:
            Logger.debug(f"SoundManager: {sound_name} çalınıyor")

class EnhancedPlayer(Widget):
    """Gelişmiş oyuncu"""
    
    velocity = ListProperty([0.0, 0.0])
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size = (32, 32)
        self.pos = (400, 300)
        self.speed = 200.0
        self.hp = 100.0
        self.max_hp = 100.0
        self.level = 1
        self.xp = 0.0
        self.xp_to_next = 100.0
        
        # Animasyon
        self.rotation = 0.0
        self.scale_factor = 1.0
        self.target_scale = 1.0
        self.glow_intensity = 0.0
        self.flash_timer = 0.0
        
        # Yetenekler
        self.abilities = []
        self.damage_multiplier = 1.0
        self.speed_multiplier = 1.0
        self.attack_speed_multiplier = 1.0
        
        self._setup_graphics()
        self.bind(pos=self.update_graphics)
    
    def _setup_graphics(self):
        """Gelişmiş grafikler"""
        # Grafikleri update_graphics'te yapacağız
        pass
    
    def update_graphics(self, *args):
        """Grafik güncelleme"""
        self.canvas.clear()
        
        with self.canvas:
            # Glow efekti
            if self.glow_intensity > 0.1:
                Color(0.5, 0.8, 1.0, self.glow_intensity * 0.5)
                glow_size = 48 + self.glow_intensity * 20
                glow_pos = (self.x - glow_size/2 + 16, self.y - glow_size/2 + 16)
                Ellipse(pos=glow_pos, size=(glow_size, glow_size))
            
            # Flash efekti
            flash_alpha = 1.0
            if self.flash_timer > 0:
                flash_alpha = 0.5 + 0.5 * math.sin(self.flash_timer * 30)
            
            # Transformasyonlar
            PushMatrix()
            
            # Rotasyon
            if self.rotation != 0:
                Rotate(angle=self.rotation, origin=(self.center_x, self.center_y))
            
            # Ölçeklendirme
            if self.scale_factor != 1.0:
                Scale(self.scale_factor, self.scale_factor, 1.0)
                Scale(origin=(self.center_x, self.center_y))
            
            # Dış halka (zırh)
            Color(0.8, 0.8, 1.0, flash_alpha)
            Ellipse(pos=self.pos, size=self.size)
            
            # Ana gövde
            Color(0.2, 0.8, 1.0, flash_alpha)
            inner_size = (24, 24)
            inner_pos = (self.x + 4, self.y + 4)
            Ellipse(pos=inner_pos, size=inner_size)
            
            # Merkez nokta
            Color(1.0, 1.0, 1.0, flash_alpha)
            center_size = (8, 8)
            center_pos = (self.x + 12, self.y + 12)
            self.center_dot = Ellipse(pos=center_pos, size=center_size)
            
            # Level göstergesi (çevresinde halka)
            if self.level > 1:
                Color(1.0, 1.0, 0.0, 0.7)
                Line(circle=(self.center_x, self.center_y, 20), width=2)
            
            PopMatrix()
    
    def update(self, dt):
        """Güncelleme"""
        # Hareket
        self.x += self.velocity[0] * dt
        self.y += self.velocity[1] * dt
        
        # Ekran sınırları
        self.x = max(0, min(self.x, 800 - self.width))
        self.y = max(0, min(self.y, 600 - self.height))
        
        # Animasyonlar
        self.target_scale = 1.0 + 0.1 * math.sin(Clock.get_time() * 3)
        scale_diff = self.target_scale - self.scale_factor
        self.scale_factor += scale_diff * dt * 5
        
        if self.glow_intensity > 0:
            self.glow_intensity -= dt * 2
        
        if self.flash_timer > 0:
            self.flash_timer -= dt
        
        # Hareket yönüne göre rotasyon
        if abs(self.velocity[0]) > 10 or abs(self.velocity[1]) > 10:
            target_rotation = math.degrees(math.atan2(self.velocity[1], self.velocity[0]))
            angle_diff = target_rotation - self.rotation
            if angle_diff > 180:
                angle_diff -= 360
            elif angle_diff < -180:
                angle_diff += 360
            self.rotation += angle_diff * dt * 3
        
        self.update_graphics()
    
    def set_movement(self, vx, vy):
        """Hareket ayarla"""
        total_speed = self.speed * self.speed_multiplier
        self.velocity = [vx * total_speed, vy * total_speed]
    
    def take_damage(self, damage):
        """Hasar al"""
        self.hp -= damage
        self.flash_timer = 0.3
        self.glow_intensity = 1.0
        return self.hp > 0
    
    def add_xp(self, amount):
        """XP ekle"""
        self.xp += amount
        if self.xp >= self.xp_to_next:
            return self.level_up()
        return False
    
    def level_up(self):
        """Level atla"""
        self.xp -= self.xp_to_next
        self.level += 1
        self.xp_to_next *= 1.2
        self.glow_intensity = 2.0
        
        # Stat artışları
        self.max_hp += 10
        self.hp = self.max_hp  # Tam heal
        
        return True
    
    def get_damage(self):
        """Toplam hasar"""
        return 20 * self.damage_multiplier
    
    def get_attack_speed(self):
        """Saldırı hızı"""
        return 2.0 * self.attack_speed_multiplier

class EnhancedEnemy(Widget):
    """Gelişmiş düşman"""
    
    def __init__(self, enemy_type="basic", **kwargs):
        super().__init__(**kwargs)
        self.enemy_type = enemy_type
        self.alive = True
        self.flash_timer = 0.0
        self.rotation = 0.0
        self.scale_factor = 1.0
        
        # Tür özelliklerini ayarla
        self._setup_enemy_type()
        self._setup_graphics()
        self.bind(pos=self.update_graphics)
    
    def _setup_enemy_type(self):
        """Düşman türü özelliklerini ayarla"""
        if self.enemy_type == "basic":
            self.size = (20, 20)
            self.hp = 30.0
            self.max_hp = 30.0
            self.speed = 50.0
            self.damage = 15.0
            self.xp_value = 5.0
            self.color = (1.0, 0.2, 0.2, 1.0)  # Kırmızı
            
        elif self.enemy_type == "fast":
            self.size = (16, 16)
            self.hp = 20.0
            self.max_hp = 20.0
            self.speed = 80.0
            self.damage = 10.0
            self.xp_value = 3.0
            self.color = (1.0, 0.5, 0.0, 1.0)  # Turuncu
            
        elif self.enemy_type == "tank":
            self.size = (28, 28)
            self.hp = 80.0
            self.max_hp = 80.0
            self.speed = 25.0
            self.damage = 25.0
            self.xp_value = 15.0
            self.color = (0.5, 0.2, 0.8, 1.0)  # Mor
            
        elif self.enemy_type == "shooter":
            self.size = (18, 18)
            self.hp = 25.0
            self.max_hp = 25.0
            self.speed = 40.0
            self.damage = 12.0
            self.xp_value = 8.0
            self.color = (0.2, 0.8, 0.2, 1.0)  # Yeşil
            self.shoot_timer = 0.0
            self.shoot_cooldown = 2.0
    
    def _setup_graphics(self):
        """Grafik ayarları"""
        pass  # update_graphics'te yapılacak
    
    def update_graphics(self, *args):
        """Grafik güncelleme"""
        self.canvas.clear()
        
        with self.canvas:
            # Flash efekti
            flash_alpha = 1.0
            if self.flash_timer > 0:
                flash_alpha = 0.5 + 0.5 * math.sin(self.flash_timer * 20)
            
            # Transformasyonlar
            PushMatrix()
            
            if self.rotation != 0:
                Rotate(angle=self.rotation, origin=(self.center_x, self.center_y))
            
            if self.scale_factor != 1.0:
                Scale(self.scale_factor, self.scale_factor, 1.0)
                Scale(origin=(self.center_x, self.center_y))
            
            # Ana gövde
            r, g, b, a = self.color
            Color(r, g, b, a * flash_alpha)
            Ellipse(pos=self.pos, size=self.size)
            
            # Tür özel efektleri
            if self.enemy_type == "tank":
                # Zırh detayları
                Color(0.8, 0.8, 0.8, flash_alpha * 0.8)
                Line(circle=(self.center_x, self.center_y, self.width/2 - 2), width=2)
                
            elif self.enemy_type == "fast":
                # Hız çizgileri
                Color(1.0, 1.0, 0.0, flash_alpha * 0.6)
                for i in range(3):
                    angle = self.rotation + (i - 1) * 30
                    start_x = self.center_x - math.cos(math.radians(angle)) * 15
                    start_y = self.center_y - math.sin(math.radians(angle)) * 15
                    end_x = self.center_x - math.cos(math.radians(angle)) * 25
                    end_y = self.center_y - math.sin(math.radians(angle)) * 25
                    Line(points=[start_x, start_y, end_x, end_y], width=2)
                    
            elif self.enemy_type == "shooter":
                # Silah
                Color(0.3, 0.3, 0.3, flash_alpha)
                gun_x = self.center_x + math.cos(math.radians(self.rotation)) * 12
                gun_y = self.center_y + math.sin(math.radians(self.rotation)) * 12
                Ellipse(pos=(gun_x - 3, gun_y - 3), size=(6, 6))
            
            # HP bar (düşük HP'de)
            if self.hp < self.max_hp * 0.7:
                hp_ratio = self.hp / self.max_hp
                bar_width = self.width
                bar_height = 3
                bar_x = self.x
                bar_y = self.y + self.height + 5
                
                # Arkaplan
                Color(0.2, 0.2, 0.2, 0.8)
                Rectangle(pos=(bar_x, bar_y), size=(bar_width, bar_height))
                
                # HP
                if hp_ratio > 0.5:
                    Color(0.2, 0.8, 0.2, 0.9)
                elif hp_ratio > 0.25:
                    Color(0.8, 0.8, 0.2, 0.9)
                else:
                    Color(0.8, 0.2, 0.2, 0.9)
                
                Rectangle(pos=(bar_x, bar_y), size=(bar_width * hp_ratio, bar_height))
            
            PopMatrix()
    
    def update(self, dt, player_pos, projectiles):
        """Güncelleme"""
        if not self.alive:
            return []
        
        # Flash timer
        if self.flash_timer > 0:
            self.flash_timer -= dt
        
        # AI davranışı
        new_projectiles = []
        
        if self.enemy_type == "shooter":
            self.shoot_timer += dt
            if self.shoot_timer >= self.shoot_cooldown:
                # Oyuncuya ateş et
                new_projectiles.append(self._create_enemy_projectile(player_pos))
                self.shoot_timer = 0.0
        
        # Oyuncuya doğru hareket
        dx = player_pos[0] - self.center_x
        dy = player_pos[1] - self.center_y
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance > 1:
            # Hareket
            move_speed = self.speed
            if self.enemy_type == "shooter" and distance < 150:
                # Shooter uzak durmaya çalışır
                move_speed = -self.speed * 0.5
            
            self.x += (dx / distance) * move_speed * dt
            self.y += (dy / distance) * move_speed * dt
            
            # Rotasyon
            self.rotation = math.degrees(math.atan2(dy, dx))
        
        # Animasyon
        if self.enemy_type == "fast":
            self.scale_factor = 1.0 + 0.2 * math.sin(Clock.get_time() * 8)
        else:
            self.scale_factor = 1.0 + 0.05 * math.sin(Clock.get_time() * 2)
        
        self.update_graphics()
        return new_projectiles
    
    def _create_enemy_projectile(self, player_pos):
        """Düşman mermisi oluştur"""
        return EnemyProjectile(
            self.center_x, self.center_y,
            player_pos[0], player_pos[1],
            damage=8.0
        )
    
    def take_damage(self, damage):
        """Hasar al"""
        self.hp -= damage
        self.flash_timer = 0.2
        self.scale_factor = 1.3
        
        if self.hp <= 0:
            self.alive = False
            return True
        return False

class EnhancedProjectile(Widget):
    """Gelişmiş mermi"""
    
    def __init__(self, start_x, start_y, target_x, target_y, damage=20.0, **kwargs):
        super().__init__(**kwargs)
        self.size = (8, 8)
        self.pos = (start_x - 4, start_y - 4)
        self.damage = damage
        self.alive = True
        self.lifetime = 3.0
        self.age = 0.0
        self.trail = []
        
        # Yön hesapla
        dx = target_x - start_x
        dy = target_y - start_y
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance > 0:
            speed = 400.0
            self.velocity = [(dx/distance) * speed, (dy/distance) * speed]
            self.angle = math.atan2(dy, dx)
        else:
            self.velocity = [0, 0]
            self.angle = 0
        
        self._setup_graphics()
        self.bind(pos=self.update_graphics)
    
    def _setup_graphics(self):
        pass  # update_graphics'te yapılacak
    
    def update_graphics(self, *args):
        """Grafik güncelleme"""
        self.canvas.clear()
        
        with self.canvas:
            # Trail efekti
            if len(self.trail) > 1:
                for i, (tx, ty) in enumerate(self.trail):
                    alpha = (i + 1) / len(self.trail) * 0.3
                    Color(1.0, 1.0, 0.5, alpha)
                    Ellipse(pos=(tx - 2, ty - 2), size=(4, 4))
            
            # Ana mermi
            Color(1.0, 1.0, 0.2, 1.0)
            Ellipse(pos=self.pos, size=self.size)
            
            # Glow efekti
            Color(1.0, 1.0, 0.8, 0.5)
            glow_size = (12, 12)
            glow_pos = (self.x - 2, self.y - 2)
            Ellipse(pos=glow_pos, size=glow_size)
    
    def update(self, dt):
        """Güncelleme"""
        if not self.alive:
            return
        
        # Trail güncelle
        self.trail.append((self.center_x, self.center_y))
        if len(self.trail) > 5:
            self.trail.pop(0)
        
        # Hareket
        self.x += self.velocity[0] * dt
        self.y += self.velocity[1] * dt
        
        # Yaşlanma
        self.age += dt
        if self.age >= self.lifetime:
            self.alive = False
        
        # Ekran dışı kontrolü
        if (self.x < -50 or self.x > 850 or 
            self.y < -50 or self.y > 650):
            self.alive = False
        
        self.update_graphics()

class EnemyProjectile(Widget):
    """Düşman mermisi"""
    
    def __init__(self, start_x, start_y, target_x, target_y, damage=8.0, **kwargs):
        super().__init__(**kwargs)
        self.size = (6, 6)
        self.pos = (start_x - 3, start_y - 3)
        self.damage = damage
        self.alive = True
        self.lifetime = 2.0
        self.age = 0.0
        
        # Yön hesapla
        dx = target_x - start_x
        dy = target_y - start_y
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance > 0:
            speed = 200.0
            self.velocity = [(dx/distance) * speed, (dy/distance) * speed]
        else:
            self.velocity = [0, 0]
        
        with self.canvas:
            Color(0.8, 0.2, 0.2, 1.0)  # Kırmızı düşman mermisi
            self.graphic = Ellipse(pos=self.pos, size=self.size)
        
        self.bind(pos=self.update_graphics)
    
    def update_graphics(self, *args):
        if hasattr(self, 'graphic'):
            self.graphic.pos = self.pos
    
    def update(self, dt):
        if not self.alive:
            return
        
        self.x += self.velocity[0] * dt
        self.y += self.velocity[1] * dt
        
        self.age += dt
        if self.age >= self.lifetime:
            self.alive = False
        
        if (self.x < -50 or self.x > 850 or 
            self.y < -50 or self.y > 650):
            self.alive = False

class AbilityCard(Widget):
    """Yetenek kartı"""
    
    def __init__(self, ability_data, **kwargs):
        super().__init__(**kwargs)
        self.ability = ability_data
        self.size = (220, 140)
        
        # Grafikleri bind ile güncelleyeceğiz
        self.bind(pos=self.update_graphics, size=self.update_graphics)
        
        # Metin widget'larını oluştur
        self.title = Label(
            text=ability_data['name'],
            color=(1, 1, 0, 1),  # Altın sarısı
            font_size='18sp',
            size_hint=(None, None),
            size=(200, 35),
            bold=True
        )
        
        self.desc = Label(
            text=ability_data['description'],
            color=(1, 1, 1, 1),  # Beyaz
            font_size='14sp',
            size_hint=(None, None),
            size=(200, 80),
            text_size=(200, None),
            halign='center',
            valign='middle'
        )
        
        self.add_widget(self.title)
        self.add_widget(self.desc)
        
        # İlk grafik çizimi
        self.update_graphics()
    
    def update_graphics(self, *args):
        """Grafikleri güncelle"""
        self.canvas.before.clear()
        
        with self.canvas.before:
            # Kart arkaplanı (daha açık)
            Color(0.15, 0.25, 0.45, 0.95)
            Rectangle(pos=self.pos, size=self.size)
            
            # Ana kenarlık (beyaz)
            Color(1.0, 1.0, 1.0, 0.9)
            Line(rectangle=(self.x, self.y, self.width, self.height), width=3)
            
            # İç kenarlık (altın)
            Color(1.0, 0.8, 0.2, 0.7)
            Line(rectangle=(self.x + 3, self.y + 3, self.width - 6, self.height - 6), width=2)
            
            # Başlık arkaplanı
            Color(0.1, 0.2, 0.4, 0.8)
            Rectangle(pos=(self.x + 5, self.y + 100), size=(self.width - 10, 35))
        
        # Metin pozisyonlarını güncelle
        self.title.pos = (self.x + 10, self.y + 100)
        self.title.text_size = (200, None)
        self.title.halign = 'center'
        
        self.desc.pos = (self.x + 10, self.y + 20)
        self.desc.text_size = (200, 80)

class ParticleWidget(Widget):
    """Parçacık efektleri için widget"""
    
    def __init__(self, particle_system, **kwargs):
        super().__init__(**kwargs)
        self.particle_system = particle_system
    
    def update_particles(self):
        """Parçacıkları güncelle ve çiz"""
        self.particle_system.render(self.canvas)

class ProfessionalGame(Widget):
    """Profesyonel oyun sınıfı"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Sistemler
        self.particle_system = ParticleSystem()
        self.sound_manager = SoundManager()
        
        # Parçacık widget'ı
        self.particle_widget = ParticleWidget(self.particle_system)
        self.add_widget(self.particle_widget)
        
        # Oyuncu
        self.player = EnhancedPlayer()
        self.add_widget(self.player)
        
        # Varlıklar
        self.enemies = []
        self.projectiles = []
        self.enemy_projectiles = []
        
        # Timers
        self.enemy_spawn_timer = 0.0
        self.attack_timer = 0.0
        self.game_time = 0.0
        self.difficulty_scale = 1.0
        
        # Joystick
        self.joystick_active = False
        self.joystick_pos = [0.0, 0.0]
        self._joystick_anchor = None
        self._joystick_touch_id = None
        
        # Mouse/Touch kontrolleri (mobil uyumlu)
        self.mouse_active = False
        self.mouse_pos = [0.0, 0.0]
        self._mouse_touch_id = None
        
        # UI
        self.paused = False
        self.level_up_cards = []
        self.setup_ui()
        
        # Yetenekler database
        self.abilities_db = [
            {'name': 'Çoklu Atış', 'description': '+2 mermi sayısı', 'type': 'multishot', 'value': 2},
            {'name': 'Güç Artışı', 'description': '+30% hasar', 'type': 'damage', 'value': 0.3},
            {'name': 'Hız Boost', 'description': '+25% hareket hızı', 'type': 'speed', 'value': 0.25},
            {'name': 'Hızlı Ateş', 'description': '+40% saldırı hızı', 'type': 'attack_speed', 'value': 0.4},
            {'name': 'Zırh', 'description': '+50 maksimum HP', 'type': 'health', 'value': 50},
            {'name': 'Berserker', 'description': 'Düşük HP\'de +50% hasar', 'type': 'berserker', 'value': 0.5}
        ]
        
        Logger.info("ProfessionalGame: Profesyonel oyun başlatıldı!")
    
    def _update_mouse_movement(self, mouse_x, mouse_y):
        """Mouse pozisyonuna göre hareket vektörü hesapla"""
        # Oyuncu merkez pozisyonu
        player_center_x = self.player.center_x
        player_center_y = self.player.center_y
        
        # Mouse ile oyuncu arasındaki mesafe
        dx = mouse_x - player_center_x
        dy = mouse_y - player_center_y
        distance = math.sqrt(dx*dx + dy*dy)
        
        # Minimum mesafe (dead zone)
        dead_zone = 50
        if distance < dead_zone:
            return 0.0, 0.0
        
        # Hareket vektörünü normalize et
        move_x = dx / distance
        move_y = dy / distance
        
        # Mesafeye göre hız ayarla (uzaksa daha hızlı)
        speed_factor = min(1.0, (distance - dead_zone) / 200.0)
        
        return move_x * speed_factor, move_y * speed_factor
    
    def setup_ui(self):
        """UI elementleri"""
        # Arka plan efekti
        with self.canvas.before:
            Color(0.05, 0.05, 0.15, 1.0)  # Koyu mavi arkaplan
            Rectangle(pos=(0, 0), size=(800, 600))
            
            # Grid pattern
            Color(0.1, 0.1, 0.3, 0.3)
            for i in range(0, 801, 50):
                Line(points=[i, 0, i, 600], width=1)
            for i in range(0, 601, 50):
                Line(points=[0, i, 800, i], width=1)
        
        # Zaman
        self.time_label = Label(
            text="00:00",
            pos=(10, 560),
            size=(100, 30),
            color=(1, 1, 1, 1),
            font_size='18sp'
        )
        self.add_widget(self.time_label)
        
        # HP bar
        self.hp_bg = Widget()
        with self.hp_bg.canvas:
            Color(0.2, 0.2, 0.2, 0.8)
            Rectangle(pos=(10, 530), size=(200, 20))
        self.add_widget(self.hp_bg)
        
        self.hp_bar = Widget()
        with self.hp_bar.canvas:
            Color(0.2, 0.8, 0.2, 0.9)
            self.hp_rect = Rectangle(pos=(10, 530), size=(200, 20))
        self.add_widget(self.hp_bar)
        
        # XP bar
        self.xp_bg = Widget()
        with self.xp_bg.canvas:
            Color(0.2, 0.2, 0.2, 0.8)
            Rectangle(pos=(10, 505), size=(200, 15))
        self.add_widget(self.xp_bg)
        
        self.xp_bar = Widget()
        with self.xp_bar.canvas:
            Color(1.0, 1.0, 0.0, 0.9)
            self.xp_rect = Rectangle(pos=(10, 505), size=(0, 15))
        self.add_widget(self.xp_bar)
        
        # Level
        self.level_label = Label(
            text="Level 1",
            pos=(220, 520),
            size=(100, 30),
            color=(1, 1, 0, 1),
            font_size='16sp'
        )
        self.add_widget(self.level_label)
        
        # Stats
        self.stats_label = Label(
            text="Düşmanlar: 0 | Mermiler: 0",
            pos=(10, 480),
            size=(300, 20),
            color=(0.8, 0.8, 0.8, 1),
            font_size='12sp'
        )
        self.add_widget(self.stats_label)
    
    def update(self, dt):
        """Ana oyun döngüsü"""
        if self.paused:
            return
        
        self.game_time += dt
        self.difficulty_scale = 1.0 + (self.game_time / 60.0) * 0.5  # Her dakika %50 daha zor
        
        # Kontrol sistemi (mouse/touch)
        move_x, move_y = 0.0, 0.0
        
        # Mouse kontrol (masaüstü)
        if self.mouse_active:
            move_x, move_y = self.mouse_pos[0], self.mouse_pos[1]
        
        # Joystick kontrol (mobil - sol yarı ekran)
        elif self.joystick_active:
            move_x, move_y = self.joystick_pos[0], self.joystick_pos[1]
        
        self.player.set_movement(move_x, move_y)
        
        # Oyuncuyu güncelle
        self.player.update(dt)
        
        # Düşman spawn
        spawn_rate = max(0.5, 2.0 - (self.game_time / 30.0))  # Giderek hızlanan spawn
        self.enemy_spawn_timer += dt
        if self.enemy_spawn_timer >= spawn_rate:
            self.spawn_enemy()
            self.enemy_spawn_timer = 0.0
        
        # Otomatik ateş
        attack_speed = 1.0 / self.player.get_attack_speed()
        self.attack_timer += dt
        if self.attack_timer >= attack_speed:
            self.auto_attack()
            self.attack_timer = 0.0
        
        # Düşmanları güncelle
        player_pos = (self.player.center_x, self.player.center_y)
        for enemy in self.enemies[:]:
            new_enemy_projectiles = enemy.update(dt, player_pos, self.projectiles)
            for proj in new_enemy_projectiles:
                self.enemy_projectiles.append(proj)
                self.add_widget(proj)
            
            if not enemy.alive:
                # Ölüm efektleri
                self.particle_system.add_explosion(enemy.center_x, enemy.center_y)
                self.particle_system.add_blood(enemy.center_x, enemy.center_y)
                self.sound_manager.play('explosion')
                
                # XP ver
                if self.player.add_xp(enemy.xp_value):
                    self.trigger_level_up()
                
                self.remove_widget(enemy)
                self.enemies.remove(enemy)
        
        # Mermileri güncelle
        for projectile in self.projectiles[:]:
            projectile.update(dt)
            if not projectile.alive:
                self.remove_widget(projectile)
                self.projectiles.remove(projectile)
        
        # Düşman mermilerini güncelle
        for proj in self.enemy_projectiles[:]:
            proj.update(dt)
            if not proj.alive:
                self.remove_widget(proj)
                self.enemy_projectiles.remove(proj)
        
        # Çarpışma kontrolü
        self.check_collisions(dt)
        
        # Parçacık sistemi
        self.particle_system.update(dt)
        self.particle_widget.update_particles()
        
        # UI güncelle
        self.update_ui()
    
    def spawn_enemy(self):
        """Gelişmiş düşman spawn"""
        # Tür seçimi (zorluk bazlı)
        enemy_types = ["basic"]
        if self.game_time > 30:
            enemy_types.append("fast")
        if self.game_time > 60:
            enemy_types.append("tank")
        if self.game_time > 90:
            enemy_types.append("shooter")
        
        enemy_type = random.choice(enemy_types)
        
        # Pozisyon
        side = random.randint(0, 3)
        if side == 0:  # Sol
            x, y = -40, random.randint(0, 600)
        elif side == 1:  # Sağ
            x, y = 840, random.randint(0, 600)
        elif side == 2:  # Üst
            x, y = random.randint(0, 800), 640
        else:  # Alt
            x, y = random.randint(0, 800), -40
        
        enemy = EnhancedEnemy(enemy_type=enemy_type)
        enemy.pos = (x, y)
        
        # Zorluk ölçeklendirmesi
        enemy.hp *= self.difficulty_scale
        enemy.max_hp = enemy.hp
        enemy.damage *= self.difficulty_scale
        enemy.speed *= min(2.0, 1.0 + (self.difficulty_scale - 1.0) * 0.5)
        
        self.enemies.append(enemy)
        self.add_widget(enemy)
    
    def auto_attack(self):
        """Gelişmiş otomatik saldırı"""
        if not self.enemies:
            return
        
        # En yakın düşmanları bul
        targets = []
        for enemy in self.enemies:
            if enemy.alive:
                distance = math.sqrt(
                    (enemy.center_x - self.player.center_x)**2 + 
                    (enemy.center_y - self.player.center_y)**2
                )
                targets.append((enemy, distance))
        
        if not targets:
            return
        
        # Mesafeye göre sırala
        targets.sort(key=lambda x: x[1])
        
        # Mermi sayısı (yeteneklere göre)
        projectile_count = 1
        for ability in self.player.abilities:
            if ability['type'] == 'multishot':
                projectile_count += ability['value']
        
        # Mermiler oluştur
        for i in range(min(projectile_count, len(targets))):
            target_enemy = targets[i][0]
            
            projectile = EnhancedProjectile(
                self.player.center_x,
                self.player.center_y,
                target_enemy.center_x,
                target_enemy.center_y,
                damage=self.player.get_damage()
            )
            
            self.projectiles.append(projectile)
            self.add_widget(projectile)
            
            # Muzzle flash efekti
            angle = math.atan2(
                target_enemy.center_y - self.player.center_y,
                target_enemy.center_x - self.player.center_x
            )
            self.particle_system.add_muzzle_flash(
                self.player.center_x, self.player.center_y, angle
            )
        
        self.sound_manager.play('shoot')
    
    def check_collisions(self, dt):
        """Gelişmiş çarpışma kontrolü"""
        # Oyuncu mermisi - düşman
        for projectile in self.projectiles[:]:
            for enemy in self.enemies[:]:
                if (projectile.alive and enemy.alive and 
                    self.is_colliding(projectile, enemy)):
                    
                    if enemy.take_damage(projectile.damage):
                        # Düşman öldü
                        pass
                    else:
                        # Hit efekti
                        self.particle_system.add_blood(enemy.center_x, enemy.center_y, 3)
                        self.sound_manager.play('hit')
                    
                    projectile.alive = False
        
        # Düşman mermisi - oyuncu
        for proj in self.enemy_projectiles[:]:
            if (proj.alive and self.is_colliding(proj, self.player)):
                if not self.player.take_damage(proj.damage):
                    # Oyuncu öldü
                    self.game_over()
                proj.alive = False
        
        # Oyuncu - düşman (temas hasarı)
        for enemy in self.enemies:
            if enemy.alive and self.is_colliding(self.player, enemy):
                contact_damage = enemy.damage * dt * 0.5  # DPS
                if not self.player.take_damage(contact_damage):
                    self.game_over()
    
    def is_colliding(self, obj1, obj2):
        """Çarpışma tespiti"""
        dx = obj1.center_x - obj2.center_x
        dy = obj1.center_y - obj2.center_y
        distance = math.sqrt(dx*dx + dy*dy)
        return distance < (obj1.width/2 + obj2.width/2)
    
    def trigger_level_up(self):
        """Level up tetikle"""
        self.paused = True
        self.particle_system.add_level_up(self.player.center_x, self.player.center_y)
        self.sound_manager.play('levelup')
        
        # Önceki kartları temizle
        for card in self.level_up_cards:
            self.remove_widget(card)
        self.level_up_cards.clear()
        
        # 3 rastgele yetenek seç
        available_abilities = random.sample(self.abilities_db, min(3, len(self.abilities_db)))
        
        # Arkaplan overlay ekle
        self.levelup_overlay = Widget()
        with self.levelup_overlay.canvas:
            Color(0.0, 0.0, 0.0, 0.7)  # Yarı saydam siyah
            Rectangle(pos=(0, 0), size=(800, 600))
        self.add_widget(self.levelup_overlay)
        
        # Level up başlığı
        self.levelup_title = Label(
            text="LEVEL UP!",
            pos=(300, 450),
            size=(200, 50),
            color=(1, 1, 0, 1),
            font_size='24sp'
        )
        self.add_widget(self.levelup_title)
        
        # Talimat metni
        self.levelup_instruction = Label(
            text="Bir yetenek seçin:",
            pos=(300, 400),
            size=(200, 30),
            color=(1, 1, 1, 1),
            font_size='16sp'
        )
        self.add_widget(self.levelup_instruction)
        
        # Kartları oluştur ve merkeze yerleştir
        card_width = 220
        card_spacing = 240
        total_width = len(available_abilities) * card_spacing - 20
        start_x = (800 - total_width) / 2  # Ekranın ortasında başla
        
        for i, ability in enumerate(available_abilities):
            card = AbilityCard(ability)
            card.pos = (start_x + i * card_spacing, 230)  # Y pozisyonunu ortaladık
            self.level_up_cards.append(card)
            self.add_widget(card)
        
        # Tıklama eventi ekle
        self.bind(on_touch_down=self.on_ability_card_touch)
        
        Logger.info(f"Level up: {len(self.level_up_cards)} kart oluşturuldu")
    
    def on_ability_card_touch(self, instance, touch):
        """Yetenek kartı tıklama"""
        if not self.level_up_cards:
            return False
        
        Logger.info(f"Tıklama pozisyonu: {touch.pos}")
        
        for i, card in enumerate(self.level_up_cards):
            Logger.info(f"Kart {i} pozisyonu: {card.pos}, boyutu: {card.size}")
            if card.collide_point(*touch.pos):
                Logger.info(f"Kart {i} seçildi: {card.ability['name']}")
                
                # Yeteneği uygula
                self.apply_ability(card.ability)
                
                # UI elementlerini kaldır
                for c in self.level_up_cards:
                    self.remove_widget(c)
                self.level_up_cards.clear()
                
                if hasattr(self, 'levelup_overlay'):
                    self.remove_widget(self.levelup_overlay)
                if hasattr(self, 'levelup_title'):
                    self.remove_widget(self.levelup_title)
                if hasattr(self, 'levelup_instruction'):
                    self.remove_widget(self.levelup_instruction)
                
                self.paused = False
                self.unbind(on_touch_down=self.on_ability_card_touch)
                return True
        
        Logger.info("Hiçbir kart seçilmedi")
        return False
    
    def apply_ability(self, ability):
        """Yetenek uygula"""
        self.player.abilities.append(ability)
        
        if ability['type'] == 'damage':
            self.player.damage_multiplier += ability['value']
        elif ability['type'] == 'speed':
            self.player.speed_multiplier += ability['value']
        elif ability['type'] == 'attack_speed':
            self.player.attack_speed_multiplier += ability['value']
        elif ability['type'] == 'health':
            self.player.max_hp += ability['value']
            self.player.hp = self.player.max_hp  # Tam heal
        
        Logger.info(f"Yetenek alındı: {ability['name']}")
    
    def update_ui(self):
        """UI güncelle"""
        # Zaman
        minutes = int(self.game_time // 60)
        seconds = int(self.game_time % 60)
        self.time_label.text = f"{minutes:02d}:{seconds:02d}"
        
        # HP bar
        hp_ratio = self.player.hp / self.player.max_hp
        self.hp_bar.canvas.clear()
        with self.hp_bar.canvas:
            if hp_ratio > 0.6:
                Color(0.2, 0.8, 0.2, 0.9)
            elif hp_ratio > 0.3:
                Color(0.8, 0.8, 0.2, 0.9)
            else:
                Color(0.8, 0.2, 0.2, 0.9)
            Rectangle(pos=(10, 530), size=(200 * hp_ratio, 20))
        
        # XP bar
        xp_ratio = self.player.xp / self.player.xp_to_next
        self.xp_bar.canvas.clear()
        with self.xp_bar.canvas:
            Color(1.0, 1.0, 0.0, 0.9)
            Rectangle(pos=(10, 505), size=(200 * xp_ratio, 15))
        
        # Level
        self.level_label.text = f"Level {self.player.level}"
        
        # Stats
        alive_enemies = sum(1 for enemy in self.enemies if enemy.alive)
        active_projectiles = len(self.projectiles)
        self.stats_label.text = f"Düşmanlar: {alive_enemies} | Mermiler: {active_projectiles}"
    
    def game_over(self):
        """Oyun bitti"""
        Logger.info("Game Over!")
        # TODO: Game over ekranı
    
    # Touch/Mouse kontrolleri
    def on_touch_down(self, touch):
        # Level up kartları varsa onları kontrol et
        if self.level_up_cards:
            return super().on_touch_down(touch)
        
        # Mobil: Sol yarı joystick, sağ yarı mouse kontrol
        # Masaüstü: Her yer mouse kontrol
        if touch.x < 400:  # Sol yarı - joystick (mobil)
            self._joystick_anchor = (touch.x, touch.y)
            self._joystick_touch_id = touch.uid
            self.joystick_active = True
            self._update_joystick(touch.x, touch.y)
            return True
        else:  # Sağ yarı veya tüm ekran - mouse kontrol
            self._mouse_touch_id = touch.uid
            self.mouse_active = True
            self._update_mouse_control(touch.x, touch.y)
            return True
    
    def on_touch_move(self, touch):
        if self._joystick_touch_id == touch.uid and self.joystick_active:
            self._update_joystick(touch.x, touch.y)
            return True
        elif self._mouse_touch_id == touch.uid and self.mouse_active:
            self._update_mouse_control(touch.x, touch.y)
            return True
        return False
    
    def on_touch_up(self, touch):
        if self._joystick_touch_id == touch.uid:
            self.joystick_active = False
            self.joystick_pos = [0.0, 0.0]
            self._joystick_touch_id = None
            return True
        elif self._mouse_touch_id == touch.uid:
            self.mouse_active = False
            self.mouse_pos = [0.0, 0.0]
            self._mouse_touch_id = None
            return True
        return False
    
    def _update_mouse_control(self, touch_x, touch_y):
        """Mouse kontrol güncelleme"""
        move_x, move_y = self._update_mouse_movement(touch_x, touch_y)
        self.mouse_pos = [move_x, move_y]
    
    def _update_joystick(self, touch_x, touch_y):
        if not self._joystick_anchor:
            return
        
        anchor_x, anchor_y = self._joystick_anchor
        dx = touch_x - anchor_x
        dy = touch_y - anchor_y
        
        max_distance = 80
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance > max_distance:
            dx = dx * max_distance / distance
            dy = dy * max_distance / distance
        
        self.joystick_pos = [dx / max_distance, dy / max_distance]

class SurvivorRPGApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Survivor RPG - Professional Edition"
    
    def build(self):
        Logger.info("SurvivorRPG: Profesyonel versiyon başlatılıyor...")
        
        self.game = ProfessionalGame()
        Clock.schedule_interval(self.game.update, 1/60.0)
        
        return self.game

if __name__ == '__main__':
    SurvivorRPGApp().run()