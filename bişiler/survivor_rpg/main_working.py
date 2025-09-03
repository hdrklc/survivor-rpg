#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Survivor RPG - Çalışan versiyon (eski sistemlerle)
"""

import os
import sys
from pathlib import Path

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.logger import Logger
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse
from kivy.properties import ListProperty, NumericProperty, BooleanProperty

# Kivy ayarları
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '600')
Config.set('graphics', 'resizable', True)

# Eski basit sistemleri import et
from entities.player import Player
from entities.enemy import Enemy
from entities.projectile import Projectile
from entities.loot import LootOrb
from systems.physics import PhysicsSystem
from systems.spawn import SpawnSystem
from systems.combat import CombatSystem
from systems.movement import MovementSystem
from systems.abilities import AbilitySystem
from ui.hud import HUD
from core.state import GameState
from core.rng import GameRNG
from services.save import SaveService

class WorkingGameScreen(Widget):
    """Çalışan oyun ekranı"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.entities = []
        
    def add_entity(self, entity):
        self.entities.append(entity)
        self.add_widget(entity)
        
    def remove_entity(self, entity):
        if entity in self.entities:
            self.entities.remove(entity)
            self.remove_widget(entity)

class WorkingGameManager(Widget):
    """Çalışan oyun yöneticisi"""
    
    # Oyun durumu
    current_scene = NumericProperty(1)  # GAME
    game_time = NumericProperty(0.0)
    is_paused = BooleanProperty(False)
    
    # Joystick
    joystick_pos = ListProperty([0.0, 0.0])
    joystick_active = BooleanProperty(False)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Temel bileşenler
        self.state = GameState()
        self.rng = GameRNG()
        self.save_service = SaveService()
        
        # Varlık listeleri
        self.player = None
        self.enemies = []
        self.projectiles = []
        self.loot_orbs = []
        
        # Sistemler
        self.physics_system = PhysicsSystem()
        self.spawn_system = SpawnSystem(self.rng)
        self.combat_system = CombatSystem()
        self.movement_system = MovementSystem()
        self.ability_system = AbilitySystem()
        
        # UI
        self.game_screen = WorkingGameScreen()
        self.hud = HUD()
        
        # Joystick kontrolleri
        self._joystick_anchor = None
        self._joystick_touch_id = None
        
        self._initialize_game()
        
    def _initialize_game(self):
        """Oyunu başlat"""
        Logger.info("WorkingGameManager: Oyun başlatılıyor...")
        
        # Ekranları ekle
        self.add_widget(self.game_screen)
        self.add_widget(self.hud)
        
        # Oyuncuyu oluştur
        self.player = Player()
        self.player.pos = [self.width/2 - 16, self.height/2 - 16]
        self.game_screen.add_entity(self.player)
        
        # HUD'ı bağla
        self.hud.bind_player(self.player)
        
        # Oyun durumunu başlat
        self.state.start_new_run(self.rng.generate_seed())
        
        Logger.info("WorkingGameManager: Oyun başlatıldı!")
        
    def update(self, dt):
        """Ana oyun döngüsü"""
        if self.is_paused or self.current_scene != 1:
            return
            
        # Zamanı güncelle
        self.game_time += dt
        self.state.game_time = self.game_time
        
        # Joystick kontrolü
        if self.joystick_active and self.player:
            self.player.set_movement_input(self.joystick_pos)
        
        # Sistemleri güncelle
        self._update_systems(dt)
        
        # UI'ı güncelle
        self._update_ui(dt)
        
        # Level-up kontrolü
        if self.player and self.player.needs_level_up():
            self._trigger_level_up()
            
        # Oyun bitişi kontrolü
        if self.player and self.player.is_dead():
            Logger.info("WorkingGameManager: Oyuncu öldü!")
            
    def _update_systems(self, dt):
        """Sistemleri güncelle"""
        
        # Hareket sistemi
        self.movement_system.update(dt, self.player, self.enemies, self.projectiles)
        
        # Spawn sistemi
        new_enemies = self.spawn_system.update(dt, self.game_time, self.get_spawn_bounds())
        for enemy in new_enemies:
            self.enemies.append(enemy)
            self.game_screen.add_entity(enemy)
            
        # Yetenek sistemi (auto-fire)
        if self.player:
            new_projectiles = self.ability_system.update(dt, self.player, self.enemies)
            for projectile in new_projectiles:
                self.projectiles.append(projectile)
                self.game_screen.add_entity(projectile)
        
        # Fizik sistemi
        self.physics_system.update(dt, self.player, self.enemies, self.projectiles, self.loot_orbs)
        
        # Savaş sistemi
        new_loot = self.combat_system.update(dt, self.player, self.enemies, self.projectiles)
        for loot in new_loot:
            self.loot_orbs.append(loot)
            self.game_screen.add_entity(loot)
        
        # Temizlik
        self._cleanup_dead_entities()
        
    def _update_ui(self, dt):
        """UI güncelle"""
        if self.hud:
            self.hud.update_time(self.game_time)
            self.hud.update_player_stats()
            
    def _trigger_level_up(self):
        """Level-up"""
        abilities = self.ability_system.get_random_abilities(3, self.player.abilities)
        if abilities:
            # İlk yeteneği otomatik ver (demo için)
            self.player.add_ability(abilities[0])
            self.player.level_up()
            Logger.info(f"WorkingGameManager: Level {self.player.level}! Yetenek: {abilities[0]['name']}")
    
    def _cleanup_dead_entities(self):
        """Ölü varlıkları temizle"""
        for enemy in self.enemies[:]:
            if enemy.is_dead():
                self.enemies.remove(enemy)
                self.game_screen.remove_entity(enemy)
                
        for projectile in self.projectiles[:]:
            if projectile.is_dead():
                self.projectiles.remove(projectile)
                self.game_screen.remove_entity(projectile)
                
        for loot in self.loot_orbs[:]:
            if loot.is_collected():
                self.loot_orbs.remove(loot)
                self.game_screen.remove_entity(loot)
    
    def get_spawn_bounds(self):
        """Spawn sınırları"""
        margin = 100
        return {
            'left': -margin,
            'right': self.width + margin,
            'top': self.height + margin,
            'bottom': -margin,
            'center_x': self.width / 2,
            'center_y': self.height / 2
        }
    
    # Touch kontrolleri
    def on_touch_down(self, touch):
        # Sol yarı - joystick
        if (touch.x < self.width * 0.5 and 
            touch.y < self.height * 0.5 and 
            not self.is_paused):
            
            self._joystick_anchor = (touch.x, touch.y)
            self._joystick_touch_id = touch.uid
            self.joystick_active = True
            self._update_joystick(touch.x, touch.y)
            return True
            
        return super().on_touch_down(touch)
    
    def on_touch_move(self, touch):
        if (self._joystick_touch_id == touch.uid and 
            self.joystick_active):
            self._update_joystick(touch.x, touch.y)
            return True
            
        return super().on_touch_move(touch)
    
    def on_touch_up(self, touch):
        if self._joystick_touch_id == touch.uid:
            self.joystick_active = False
            self.joystick_pos = [0.0, 0.0]
            self._joystick_touch_id = None
            self._joystick_anchor = None
            return True
            
        return super().on_touch_up(touch)
    
    def _update_joystick(self, touch_x, touch_y):
        """Joystick güncelle"""
        if not self._joystick_anchor:
            return
            
        anchor_x, anchor_y = self._joystick_anchor
        dx = touch_x - anchor_x
        dy = touch_y - anchor_y
        
        max_distance = 60
        distance = (dx*dx + dy*dy) ** 0.5
        
        if distance > max_distance:
            dx = dx * max_distance / distance
            dy = dy * max_distance / distance
            
        self.joystick_pos = [dx / max_distance, dy / max_distance]
    
    def save_game(self):
        """Oyunu kaydet"""
        self.save_service.save_game_data()

class SurvivorRPGApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Survivor RPG - Working Version"
        self.game_manager = None
        
    def build(self):
        Logger.info("SurvivorRPG: Çalışan versiyon başlatılıyor...")
        
        try:
            self.game_manager = WorkingGameManager()
            Clock.schedule_interval(self.game_manager.update, 1/60.0)
            return self.game_manager
        except Exception as e:
            Logger.error(f"SurvivorRPG: Hata: {e}")
            import traceback
            traceback.print_exc()
            
            from kivy.uix.label import Label
            return Label(text=f'Hata: {str(e)}', font_size='16sp')
    
    def on_stop(self):
        if self.game_manager:
            self.game_manager.save_game()

if __name__ == '__main__':
    SurvivorRPGApp().run()
