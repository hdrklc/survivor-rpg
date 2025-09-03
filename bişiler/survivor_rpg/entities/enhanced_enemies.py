#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Entities/EnhancedEnemies.py - Profesyonel düşman sınıfları
"""

import math
import random
from typing import Tuple, Optional, List
from kivy.graphics import Color, PushMatrix, PopMatrix, Rotate

from .base import BaseEntity
from graphics.sprite_manager import sprite_renderer
from graphics.particle_system import particle_system
from audio.sound_manager import sound_manager


class EnhancedEnemy(BaseEntity):
    """Gelişmiş düşman temel sınıfı"""
    
    def __init__(self, enemy_type: str = "slime", **kwargs):
        super().__init__(**kwargs)
        
        self.enemy_type = enemy_type
        self.radius = 12
        self.size = (self.radius * 2, self.radius * 2)
        
        # Temel özellikler
        self.max_hp = 30.0
        self.current_hp = 30.0
        self.damage = 8.0
        self.move_speed = 40.0
        self.xp_value = 1.0
        
        # AI özellikleri
        self.target_pos = [0, 0]
        self.ai_state = "chase"  # chase, attack, flee, patrol
        self.ai_timer = 0.0
        self.detection_range = 200.0
        self.attack_range = 25.0
        
        # Görsel efektler
        self.rotation = 0.0
        self.scale = 1.0
        self.flash_timer = 0.0
        self.death_animation_timer = 0.0
        
        # Hareket özellikleri
        self.acceleration = 300.0
        self.friction = 0.8
        self.avoid_distance = 30.0  # Diğer düşmanlardan kaçınma
        
        # Özel yetenekler
        self.special_cooldown = 0.0
        self.special_ability_timer = random.uniform(3.0, 8.0)
        
        # Ses efektleri
        self.hurt_sound_cooldown = 0.0
        
        self._setup_enemy_type()
        self._setup_graphics()
    
    def _setup_enemy_type(self):
        """Düşman türüne göre özellikler"""
        if self.enemy_type == "slime":
            self.max_hp = 25.0
            self.damage = 6.0
            self.move_speed = 35.0
            self.xp_value = 1.0
            self.radius = 10
        elif self.enemy_type == "goblin":
            self.max_hp = 40.0
            self.damage = 12.0
            self.move_speed = 55.0
            self.xp_value = 2.0
            self.radius = 12
            self.detection_range = 250.0
        elif self.enemy_type == "skeleton":
            self.max_hp = 60.0
            self.damage = 15.0
            self.move_speed = 45.0
            self.xp_value = 3.0
            self.radius = 14
            self.attack_range = 35.0
        elif self.enemy_type == "orc":
            self.max_hp = 100.0
            self.damage = 25.0
            self.move_speed = 30.0
            self.xp_value = 5.0
            self.radius = 18
            self.attack_range = 40.0
        
        self.current_hp = self.max_hp
        self.size = (self.radius * 2, self.radius * 2)
    
    def _setup_graphics(self):
        """Grafik ayarları"""
        # Sprite renderer kullanacağız
        pass
    
    def _update_graphics(self):
        """Grafik güncellemesi"""
        self.canvas.clear()
        
        with self.canvas:
            # Flash efekti (hasar aldığında)
            if self.flash_timer > 0:
                flash_intensity = self.flash_timer / 0.2
                Color(1, 1, 1, flash_intensity)
            else:
                Color(1, 1, 1, 1)
            
            # Transformasyonlar
            PushMatrix()
            
            if self.rotation != 0:
                Rotate(angle=self.rotation, origin=self.center)
            
            # Ölüm animasyonu
            if self.death_animation_timer > 0:
                death_scale = 1.0 + (self.death_animation_timer * 2.0)
                from kivy.graphics import Scale
                Scale(death_scale, death_scale, 1.0)
                Scale(origin=self.center)
            
            # Sprite render
            sprite_renderer.render_sprite(
                self.canvas,
                self.enemy_type,
                self.pos,
                self.size
            )
            
            PopMatrix()
            
            # HP bar (düşük HP'de)
            if self.current_hp < self.max_hp * 0.8:
                self._draw_health_bar()
    
    def _draw_health_bar(self):
        """Sağlık çubuğu"""
        bar_width = self.radius * 1.5
        bar_height = 3
        bar_x = self.center_x - bar_width / 2
        bar_y = self.center_y + self.radius + 6
        
        # Arkaplan
        Color(0.1, 0.1, 0.1, 0.8)
        from kivy.graphics import Rectangle
        Rectangle(pos=(bar_x, bar_y), size=(bar_width, bar_height))
        
        # HP
        hp_ratio = self.current_hp / self.max_hp if self.max_hp > 0 else 0
        hp_width = bar_width * hp_ratio
        
        if hp_ratio > 0.5:
            Color(0.2, 0.8, 0.2, 0.9)  # Yeşil
        elif hp_ratio > 0.25:
            Color(0.8, 0.8, 0.2, 0.9)  # Sarı
        else:
            Color(0.8, 0.2, 0.2, 0.9)  # Kırmızı
        
        Rectangle(pos=(bar_x, bar_y), size=(hp_width, bar_height))
    
    def update_ai(self, dt: float, player_pos: Tuple[float, float], 
                  other_enemies: List['EnhancedEnemy']):
        """Gelişmiş AI sistemi"""
        self.ai_timer += dt
        
        player_x, player_y = player_pos
        distance_to_player = math.sqrt(
            (player_x - self.center_x)**2 + (player_y - self.center_y)**2
        )
        
        # Durum makinesi
        if self.ai_state == "chase":
            if distance_to_player <= self.attack_range:
                self.ai_state = "attack"
                self.ai_timer = 0.0
            elif distance_to_player > self.detection_range:
                self.ai_state = "patrol"
                self.ai_timer = 0.0
        
        elif self.ai_state == "attack":
            if distance_to_player > self.attack_range * 1.5:
                self.ai_state = "chase"
            elif self.ai_timer > 1.0:  # Saldırı aralığı
                self._perform_attack(player_pos)
                self.ai_timer = 0.0
        
        elif self.ai_state == "patrol":
            if distance_to_player <= self.detection_range:
                self.ai_state = "chase"
            else:
                # Rastgele dolaşma
                if self.ai_timer > 2.0:
                    angle = random.uniform(0, 2 * math.pi)
                    distance = random.uniform(50, 100)
                    self.target_pos = [
                        self.center_x + math.cos(angle) * distance,
                        self.center_y + math.sin(angle) * distance
                    ]
                    self.ai_timer = 0.0
        
        # Hareket hesaplama
        self._calculate_movement(player_pos, other_enemies)
        
        # Özel yetenek
        self.special_cooldown -= dt
        if self.special_cooldown <= 0:
            self._use_special_ability(player_pos)
            self.special_cooldown = self.special_ability_timer
    
    def _calculate_movement(self, player_pos: Tuple[float, float], 
                          other_enemies: List['EnhancedEnemy']):
        """Hareket hesaplama (flocking behavior)"""
        if self.ai_state == "chase" or self.ai_state == "attack":
            target_x, target_y = player_pos
        else:
            target_x, target_y = self.target_pos
        
        # Hedefe doğru yön
        dx = target_x - self.center_x
        dy = target_y - self.center_y
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance > 1.0:
            move_x = (dx / distance) * self.move_speed
            move_y = (dy / distance) * self.move_speed
        else:
            move_x = move_y = 0.0
        
        # Diğer düşmanlardan kaçınma (separation)
        avoid_x = avoid_y = 0.0
        avoid_count = 0
        
        for enemy in other_enemies:
            if enemy == self or not enemy.is_alive:
                continue
            
            enemy_dx = enemy.center_x - self.center_x
            enemy_dy = enemy.center_y - self.center_y
            enemy_distance = math.sqrt(enemy_dx*enemy_dx + enemy_dy*enemy_dy)
            
            if enemy_distance < self.avoid_distance and enemy_distance > 0:
                # Uzaklaşma kuvveti
                avoid_strength = (self.avoid_distance - enemy_distance) / self.avoid_distance
                avoid_x -= (enemy_dx / enemy_distance) * avoid_strength * 50
                avoid_y -= (enemy_dy / enemy_distance) * avoid_strength * 50
                avoid_count += 1
        
        if avoid_count > 0:
            avoid_x /= avoid_count
            avoid_y /= avoid_count
        
        # Final hareket vektörü
        final_x = move_x + avoid_x
        final_y = move_y + avoid_y
        
        # Hız sınırı
        final_speed = math.sqrt(final_x*final_x + final_y*final_y)
        if final_speed > self.move_speed:
            final_x = (final_x / final_speed) * self.move_speed
            final_y = (final_y / final_speed) * self.move_speed
        
        self.velocity = [final_x, final_y]
        
        # Rotasyon (hareket yönüne doğru)
        if final_speed > 5:
            target_rotation = math.degrees(math.atan2(final_y, final_x))
            angle_diff = target_rotation - self.rotation
            if angle_diff > 180:
                angle_diff -= 360
            elif angle_diff < -180:
                angle_diff += 360
            self.rotation += angle_diff * 0.1
    
    def _perform_attack(self, player_pos: Tuple[float, float]):
        """Saldırı gerçekleştir"""
        # Saldırı efektleri
        if self.enemy_type == "goblin":
            # Hızlı saldırı
            particle_system.create_muzzle_flash(
                self.center_x, self.center_y,
                math.atan2(player_pos[1] - self.center_y, player_pos[0] - self.center_x)
            )
        elif self.enemy_type == "skeleton":
            # Kemik fırlatma efekti
            pass
        elif self.enemy_type == "orc":
            # Güçlü saldırı efekti
            particle_system.create_explosion(self.center_x, self.center_y, 0.5)
        
        sound_manager.play_sound('fire', 0.3, (self.center_x, self.center_y))
    
    def _use_special_ability(self, player_pos: Tuple[float, float]):
        """Özel yetenek kullan"""
        if self.enemy_type == "slime":
            # Bölünme yeteneği (düşük HP'de)
            if self.current_hp < self.max_hp * 0.3:
                self._split_slime()
        elif self.enemy_type == "goblin":
            # Hız patlaması
            self.move_speed *= 1.5
            # 2 saniye sonra normal hıza dön
            def reset_speed(dt):
                self.move_speed /= 1.5
            from kivy.clock import Clock
            Clock.schedule_once(reset_speed, 2.0)
        elif self.enemy_type == "skeleton":
            # Teleport (oyuncunun arkasına)
            player_x, player_y = player_pos
            angle = random.uniform(0, 2 * math.pi)
            teleport_distance = 60
            new_x = player_x + math.cos(angle) * teleport_distance
            new_y = player_y + math.sin(angle) * teleport_distance
            self.center_x = new_x
            self.center_y = new_y
            particle_system.create_explosion(new_x, new_y, 0.3)
        elif self.enemy_type == "orc":
            # Öfke modu (daha fazla hasar, daha hızlı)
            self.damage *= 1.3
            self.move_speed *= 1.2
            self.scale = 1.2
    
    def _split_slime(self):
        """Slime bölünmesi"""
        # İki küçük slime oluştur (game manager'da yapılacak)
        self.xp_value = 0.5  # Bölündüğünde daha az XP
    
    def update(self, dt: float):
        """Ana güncelleme"""
        if not self.is_alive:
            # Ölüm animasyonu
            self.death_animation_timer += dt
            if self.death_animation_timer > 0.5:
                return  # Animasyon bitti
        
        # Flash efekti azalması
        if self.flash_timer > 0:
            self.flash_timer -= dt
            if self.flash_timer < 0:
                self.flash_timer = 0
        
        # Ses cooldown
        if self.hurt_sound_cooldown > 0:
            self.hurt_sound_cooldown -= dt
        
        # Hareket
        self.move(dt)
        
        # Grafik güncellemesi
        self._update_graphics()
    
    def take_damage(self, amount: float) -> bool:
        """Hasar alma efektleri ile"""
        if not self.is_alive:
            return False
        
        self.current_hp = max(0, self.current_hp - amount)
        
        # Görsel efektler
        self.flash_timer = 0.2
        self.scale = 1.2  # Geçici büyütme
        
        # Parçacık efektleri
        blood_color = (0.8, 0.2, 0.2, 1.0)  # Kırmızı
        if self.enemy_type == "slime":
            blood_color = (0.2, 0.8, 0.2, 1.0)  # Yeşil
        elif self.enemy_type == "skeleton":
            blood_color = (0.9, 0.9, 0.9, 1.0)  # Beyaz
        
        # Kan efekti
        emitter = particle_system.create_explosion(self.center_x, self.center_y, 0.3)
        if emitter and hasattr(emitter, 'particle_colors'):
            emitter.particle_colors = [blood_color]
        
        # Hasar sayısı
        particle_system.create_damage_numbers(
            self.center_x, self.center_y + 15, int(amount)
        )
        
        # Ses efekti
        if self.hurt_sound_cooldown <= 0:
            sound_manager.play_damage(self.center_x, self.center_y)
            self.hurt_sound_cooldown = 0.3
        
        if self.current_hp <= 0:
            self._trigger_death_effects()
            self.kill()
        
        return True
    
    def _trigger_death_effects(self):
        """Ölüm efektleri"""
        # Büyük patlama
        particle_system.create_explosion(self.center_x, self.center_y, 1.0)
        sound_manager.play_explosion(self.center_x, self.center_y, 0.8)
        
        # XP orb oluşturma (game manager'da yapılacak)
    
    def get_xp_value(self) -> float:
        """XP değeri"""
        return self.xp_value
    
    def get_damage(self) -> float:
        """Hasar değeri"""
        return self.damage
    
    def is_dead(self) -> bool:
        """Ölü mü?"""
        return not self.is_alive or self.current_hp <= 0


class EnemyFactory:
    """Düşman fabrikası"""
    
    @staticmethod
    def create_enemy(enemy_type: str, x: float, y: float, 
                    difficulty_scale: float = 1.0) -> EnhancedEnemy:
        """Düşman oluştur"""
        enemy = EnhancedEnemy(enemy_type)
        enemy.center_x = x
        enemy.center_y = y
        
        # Zorluk ölçeklendirmesi
        enemy.max_hp *= difficulty_scale
        enemy.current_hp = enemy.max_hp
        enemy.damage *= difficulty_scale
        enemy.xp_value *= difficulty_scale
        
        return enemy
    
    @staticmethod
    def get_random_enemy_type(minute: int) -> str:
        """Dakikaya göre rastgele düşman türü"""
        if minute < 2:
            return random.choice(['slime'])
        elif minute < 5:
            return random.choice(['slime', 'goblin'])
        elif minute < 8:
            return random.choice(['slime', 'goblin', 'skeleton'])
        else:
            return random.choice(['slime', 'goblin', 'skeleton', 'orc'])
    
    @staticmethod
    def get_difficulty_scale(minute: int) -> float:
        """Zorluk ölçeklendirmesi"""
        # Her dakika %12 daha zor
        return 1.0 + (minute * 0.12)
