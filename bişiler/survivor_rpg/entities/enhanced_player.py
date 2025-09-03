#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Entities/EnhancedPlayer.py - Profesyonel oyuncu sınıfı
"""

import math
from typing import List, Dict, Any, Tuple
from kivy.graphics import Color, PushMatrix, PopMatrix, Rotate, Scale
from kivy.clock import Clock

from .base import BaseEntity
from core.state import PlayerStats
from graphics.sprite_manager import sprite_renderer
from graphics.particle_system import particle_system
from audio.sound_manager import sound_manager


class EnhancedPlayer(BaseEntity):
    """Profesyonel oyuncu sınıfı - gelişmiş grafikler ve efektler"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Temel özellikler
        self.radius = 16  # Daha büyük
        self.size = (self.radius * 2, self.radius * 2)
        
        # Hareket özellikleri
        self.max_speed = 180.0
        self.acceleration = 1000.0
        self.friction = 0.88
        self.target_velocity = [0.0, 0.0]
        
        # Sağlık özellikleri
        self.max_hp = 100.0
        self.current_hp = 100.0
        self.damage_immunity_time = 0.8  # Daha uzun bağışıklık
        self._damage_timer = 0.0
        
        # Oyuncu istatistikleri
        self.stats = PlayerStats()
        
        # Yetenekler
        self.abilities: List[Dict[str, Any]] = []
        
        # Gelişmiş saldırı sistemi
        self.last_attack_time = 0.0
        self.auto_fire_enabled = True
        self.combo_counter = 0
        self.combo_timer = 0.0
        self.combo_decay_time = 2.0
        
        # XP sistemi
        self._pending_level_up = False
        
        # Magnet sistemi
        self.magnet_range = 60.0
        
        # Görsel efektler
        self.rotation = 0.0
        self.scale = 1.0
        self.target_scale = 1.0
        self.glow_intensity = 0.0
        self.invulnerable_flash = 0.0
        
        # Animasyon
        self.idle_animation_time = 0.0
        self.movement_trail = []
        self.max_trail_length = 8
        
        # Ses pozisyonu
        self._update_audio_position()
        
        # Grafikleri ayarla
        self._setup_graphics()
    
    def _setup_graphics(self):
        """Profesyonel grafikler"""
        # Sprite renderer kullanacağız, canvas'ı boş bırak
        pass
    
    def _update_graphics(self, *args):
        """Grafik güncellemesi"""
        # Canvas'ı temizle ve yeniden çiz
        self.canvas.clear()
        
        with self.canvas:
            # Glow efekti
            if self.glow_intensity > 0.1:
                Color(0.5, 0.8, 1.0, self.glow_intensity * 0.3)
                from kivy.graphics import Ellipse
                glow_size = self.radius * 3 * self.glow_intensity
                glow_pos = (
                    self.center_x - glow_size / 2,
                    self.center_y - glow_size / 2
                )
                Ellipse(pos=glow_pos, size=(glow_size, glow_size))
            
            # Ana karakter transformasyonları
            PushMatrix()
            
            # Merkezi etrafında döndür
            if self.rotation != 0:
                Rotate(angle=self.rotation, origin=self.center)
            
            # Ölçeklendirme
            if self.scale != 1.0:
                Scale(self.scale, self.scale, 1.0)
                Scale(origin=self.center)
            
            # Invulnerability flash
            if self.invulnerable_flash > 0:
                flash_alpha = 0.5 + 0.5 * math.sin(self.invulnerable_flash * 20)
                Color(1, 1, 1, flash_alpha)
            else:
                Color(1, 1, 1, 1)
            
            # Ana sprite'ı render et
            sprite_renderer.render_sprite(
                self.canvas,
                'player',
                self.pos,
                self.size,
                color=(1, 1, 1, 1)
            )
            
            PopMatrix()
            
            # HP bar (oyuncunun üstünde)
            if self.current_hp < self.max_hp:
                self._draw_health_bar()
            
            # Combo göstergesi
            if self.combo_counter > 1:
                self._draw_combo_indicator()
    
    def _draw_health_bar(self):
        """Sağlık çubuğu çiz"""
        bar_width = 40
        bar_height = 4
        bar_x = self.center_x - bar_width / 2
        bar_y = self.center_y + self.radius + 8
        
        # Arkaplan
        Color(0.2, 0.2, 0.2, 0.8)
        from kivy.graphics import Rectangle
        Rectangle(pos=(bar_x, bar_y), size=(bar_width, bar_height))
        
        # HP bar
        hp_ratio = self.current_hp / self.max_hp if self.max_hp > 0 else 0
        hp_width = bar_width * hp_ratio
        
        # Renk gradyanı (yeşil -> sarı -> kırmızı)
        if hp_ratio > 0.6:
            r, g, b = 0.2, 1.0, 0.2  # Yeşil
        elif hp_ratio > 0.3:
            r, g, b = 1.0, 1.0, 0.2  # Sarı
        else:
            r, g, b = 1.0, 0.2, 0.2  # Kırmızı
        
        Color(r, g, b, 0.9)
        Rectangle(pos=(bar_x, bar_y), size=(hp_width, bar_height))
    
    def _draw_combo_indicator(self):
        """Combo göstergesi çiz"""
        # Basit text render (gerçek implementasyonda Label kullanılır)
        pass
    
    def set_movement_input(self, input_vector: Tuple[float, float]):
        """Hareket girişi"""
        self.target_velocity = [
            input_vector[0] * self.max_speed,
            input_vector[1] * self.max_speed
        ]
        
        # Hareket yönüne göre rotasyon
        if abs(input_vector[0]) > 0.1 or abs(input_vector[1]) > 0.1:
            target_rotation = math.degrees(math.atan2(input_vector[1], input_vector[0]))
            # Smooth rotation
            angle_diff = target_rotation - self.rotation
            if angle_diff > 180:
                angle_diff -= 360
            elif angle_diff < -180:
                angle_diff += 360
            
            self.rotation += angle_diff * 0.1  # Smooth rotation
    
    def update_movement(self, dt: float):
        """Gelişmiş hareket sistemi"""
        current_vx, current_vy = self.velocity
        target_vx, target_vy = self.target_velocity
        
        accel = self.acceleration * dt
        
        if target_vx != 0 or target_vy != 0:
            # Momentum ve hızlanma
            diff_x = target_vx - current_vx
            diff_y = target_vy - current_vy
            
            if abs(diff_x) > accel:
                diff_x = accel if diff_x > 0 else -accel
            if abs(diff_y) > accel:
                diff_y = accel if diff_y > 0 else -accel
                
            self.velocity = [current_vx + diff_x, current_vy + diff_y]
        else:
            # Sürtünme
            self.velocity = [current_vx * self.friction, current_vy * self.friction]
            
            if abs(self.velocity[0]) < 2.0:
                self.velocity[0] = 0
            if abs(self.velocity[1]) < 2.0:
                self.velocity[1] = 0
        
        # Hız sınırı
        speed = math.sqrt(self.velocity[0]**2 + self.velocity[1]**2)
        if speed > self.max_speed:
            self.velocity[0] = self.velocity[0] * self.max_speed / speed
            self.velocity[1] = self.velocity[1] * self.max_speed / speed
            
        self.speed = speed
        
        # Hareket trail efekti
        if speed > 50:  # Sadece hızlı hareket ederken
            self.movement_trail.append((self.center_x, self.center_y))
            if len(self.movement_trail) > self.max_trail_length:
                self.movement_trail.pop(0)
    
    def update_damage_timer(self, dt: float):
        """Hasar zamanlayıcısı"""
        if self._damage_timer > 0:
            self._damage_timer -= dt
            self.invulnerable_flash = self._damage_timer
            if self._damage_timer < 0:
                self._damage_timer = 0
                self.invulnerable_flash = 0
    
    def update_visual_effects(self, dt: float):
        """Görsel efekt güncellemeleri"""
        # İdle animasyon
        self.idle_animation_time += dt
        idle_bob = math.sin(self.idle_animation_time * 3.0) * 0.02
        self.target_scale = 1.0 + idle_bob
        
        # Ölçek yumuşak geçişi
        scale_diff = self.target_scale - self.scale
        self.scale += scale_diff * dt * 8.0
        
        # Glow efekti azalması
        if self.glow_intensity > 0:
            self.glow_intensity -= dt * 2.0
            if self.glow_intensity < 0:
                self.glow_intensity = 0
        
        # Combo timer
        if self.combo_counter > 0:
            self.combo_timer -= dt
            if self.combo_timer <= 0:
                self.combo_counter = max(0, self.combo_counter - 1)
                self.combo_timer = self.combo_decay_time
    
    def update(self, dt: float):
        """Ana güncelleme döngüsü"""
        if not self.is_alive:
            return
        
        # Temel güncellemeler
        self.update_movement(dt)
        self.move(dt)
        self.update_damage_timer(dt)
        self.update_visual_effects(dt)
        
        # Saldırı zamanlayıcısı
        self.last_attack_time += dt
        
        # İstatistik güncellemeleri
        self.max_speed = self.stats.get_total_speed() * 60
        self.max_hp = self.stats.get_max_hp()
        
        if self.current_hp > self.max_hp:
            self.current_hp = self.max_hp
        
        # Ses pozisyonu güncelle
        self._update_audio_position()
        
        # Grafikleri güncelle
        self._update_graphics()
    
    def _update_audio_position(self):
        """Ses pozisyonunu güncelle"""
        sound_manager.set_listener_position(self.center_x, self.center_y)
    
    def take_damage(self, amount: float) -> bool:
        """Gelişmiş hasar alma"""
        if self._damage_timer > 0 or not self.is_alive:
            return False
        
        # Kritik hasar kontrolü
        is_critical = False
        if hasattr(self, 'last_damage_source'):
            # Combo sistemi - art arda hasar alırsa daha az hasar
            combo_reduction = min(0.5, self.combo_counter * 0.1)
            amount *= (1.0 - combo_reduction)
        
        self.current_hp = max(0, self.current_hp - amount)
        self._damage_timer = self.damage_immunity_time
        self.stats.take_damage(amount)
        
        # Görsel efektler
        self.glow_intensity = 1.0
        self.target_scale = 1.3  # Damage büyütme efekti
        
        # Screen shake efekti (game manager'da yapılacak)
        
        # Parçacık efektleri
        particle_system.create_damage_numbers(self.center_x, self.center_y + 20, int(amount))
        
        # Ses efekti
        sound_manager.play_damage(self.center_x, self.center_y)
        
        if self.current_hp <= 0:
            self._trigger_death_effects()
            self.kill()
        
        return True
    
    def _trigger_death_effects(self):
        """Ölüm efektleri"""
        # Büyük patlama efekti
        particle_system.create_explosion(self.center_x, self.center_y, 2.0)
        sound_manager.play_explosion(self.center_x, self.center_y, 1.5)
    
    def heal(self, amount: float):
        """İyileştirme efektleri ile"""
        if not self.is_alive:
            return
        
        old_hp = self.current_hp
        self.current_hp = min(self.max_hp, self.current_hp + amount)
        actual_heal = self.current_hp - old_hp
        
        if actual_heal > 0:
            self.stats.heal(actual_heal)
            
            # İyileştirme efektleri
            self.glow_intensity = 0.8
            particle_system.create_heal_effect(self.center_x, self.center_y)
            sound_manager.play_pickup(self.center_x, self.center_y)
    
    def add_xp(self, amount: float):
        """XP ekleme efektleri ile"""
        if self.stats.add_xp(amount):
            self._pending_level_up = True
    
    def level_up(self):
        """Level atlama efektleri"""
        if self._pending_level_up:
            self.stats.level_up()
            self._pending_level_up = False
            
            # Muhteşem level up efektleri
            self.glow_intensity = 2.0
            self.target_scale = 1.5
            particle_system.create_level_up_effect(self.center_x, self.center_y)
            sound_manager.play_level_up()
            
            # Tam heal
            self.current_hp = self.max_hp
    
    def attack(self) -> bool:
        """Gelişmiş saldırı sistemi"""
        if self.can_attack() and self.auto_fire_enabled:
            self.last_attack_time = 0.0
            
            # Combo sistemi
            self.combo_counter += 1
            self.combo_timer = self.combo_decay_time
            
            # Muzzle flash efekti
            for i in range(self.get_projectile_count()):
                angle = (2 * math.pi * i) / self.get_projectile_count()
                flash_x = self.center_x + math.cos(angle) * 20
                flash_y = self.center_y + math.sin(angle) * 20
                particle_system.create_muzzle_flash(flash_x, flash_y, angle)
            
            # Ses efekti
            sound_manager.play_fire(self.center_x, self.center_y)
            
            return True
        return False
    
    def can_attack(self) -> bool:
        """Saldırabilir mi?"""
        if not self.auto_fire_enabled:
            return False
        attack_cooldown = 1.0 / self.stats.get_total_attack_speed()
        return self.last_attack_time >= attack_cooldown
    
    def get_attack_damage(self) -> float:
        """Combo bonusu ile hasar"""
        base_damage = self.stats.get_total_damage()
        combo_bonus = 1.0 + (self.combo_counter * 0.05)  # %5 bonus per combo
        return base_damage * combo_bonus
    
    def get_projectile_count(self) -> int:
        """Mermi sayısı"""
        count = 1
        for ability in self.abilities:
            if ability.get('type') == 'multishot':
                count += ability.get('bonus_projectiles', 1)
        return min(count, 12)  # Maksimum 12 mermi
    
    def add_ability(self, ability: Dict[str, Any]):
        """Yetenek ekleme efektleri ile"""
        self.abilities.append(ability)
        self._apply_ability_effects(ability)
        
        # Yetenek alma efekti
        self.glow_intensity = 1.5
        particle_system.create_heal_effect(self.center_x, self.center_y)
        sound_manager.play_pickup(self.center_x, self.center_y)
    
    def _apply_ability_effects(self, ability: Dict[str, Any]):
        """Yetenek etkilerini uygula"""
        ability_type = ability.get('type', '')
        
        if ability_type == 'speed':
            bonus = ability.get('bonus', 0.15)
            self.stats.speed_multiplier += bonus
        elif ability_type == 'damage':
            bonus = ability.get('bonus', 0.2)
            self.stats.damage_multiplier += bonus
        elif ability_type == 'health':
            bonus = ability.get('bonus', 0.25)
            old_max = self.stats.get_max_hp()
            self.stats.hp_multiplier += bonus
            new_max = self.stats.get_max_hp()
            hp_increase = new_max - old_max
            self.heal(hp_increase)
        elif ability_type == 'magnet':
            bonus = ability.get('bonus', 0.3)
            self.stats.magnet_range += self.stats.magnet_range * bonus
            self.magnet_range = self.stats.magnet_range
        elif ability_type == 'attack_speed':
            bonus = ability.get('bonus', 0.2)
            self.stats.attack_speed_multiplier += bonus
    
    def collect_loot(self, loot_value: float, loot_type: str = 'xp'):
        """Loot toplama efektleri ile"""
        if loot_type == 'xp':
            self.add_xp(loot_value)
            # Küçük parçacık efekti
            particle_system.create_heal_effect(self.center_x, self.center_y)
        elif loot_type == 'health':
            self.heal(loot_value)
    
    def get_status_info(self) -> Dict[str, Any]:
        """Gelişmiş durum bilgileri"""
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
            'combo_counter': self.combo_counter,
        }
    
    @property
    def level(self) -> int:
        return self.stats.level
