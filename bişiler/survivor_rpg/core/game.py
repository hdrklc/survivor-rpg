#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Core/Game.py - Ana oyun döngüsü ve sahne yönetimi
"""

import random
from typing import Dict, List, Optional
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.logger import Logger
from kivy.properties import NumericProperty, ListProperty, BooleanProperty

from .state import GameState, GameScene
from .rng import GameRNG
from entities.enhanced_player import EnhancedPlayer
from entities.enhanced_enemies import EnhancedEnemy, EnemyFactory
from entities.projectile import Projectile
from entities.loot import LootOrb
from graphics.sprite_manager import sprite_renderer
from graphics.particle_system import particle_system
from audio.sound_manager import sound_manager
from systems.physics import PhysicsSystem
from systems.spawn import SpawnSystem
from systems.combat import CombatSystem
from systems.movement import MovementSystem
from systems.abilities import AbilitySystem
from ui.hud import HUD
from ui.levelup import LevelUpPanel
from ui.pause_menu import PauseMenu
from ui.game_over import GameOverScreen
from services.save import SaveService
from services.audio import AudioService


class GameScreen(Widget):
    """Ana oyun ekranı - varlıkların çizildiği alan"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.entities = []
        
        # Parçacık render'ı için canvas binding
        self.bind(size=self._update_canvas, pos=self._update_canvas)
        
    def _update_canvas(self, *args):
        """Canvas güncellemesi"""
        # Parçacık sistemini render et
        particle_system.render(self.canvas)
        
    def add_entity(self, entity):
        """Ekrana varlık ekle"""
        self.entities.append(entity)
        self.add_widget(entity)
        
    def remove_entity(self, entity):
        """Ekrandan varlık kaldır"""
        if entity in self.entities:
            self.entities.remove(entity)
            self.remove_widget(entity)


class GameManager(Widget):
    """Ana oyun yöneticisi - tüm sistemleri koordine eder"""
    
    # Oyun durumu
    current_scene = NumericProperty(1)  # GameScene.GAME = 1
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
        self.audio_service = AudioService()
        
        # Varlık listeleri
        self.player: Optional[EnhancedPlayer] = None
        self.enemies: List[EnhancedEnemy] = []
        self.projectiles: List[Projectile] = []
        self.loot_orbs: List[LootOrb] = []
        
        # Sistemler
        self.physics_system = PhysicsSystem()
        self.spawn_system = SpawnSystem(self.rng)
        self.combat_system = CombatSystem()
        self.movement_system = MovementSystem()
        self.ability_system = AbilitySystem()
        
        # UI bileşenleri
        self.game_screen = GameScreen()
        self.hud = HUD()
        self.level_up_panel = None
        self.pause_menu = None
        self.game_over_screen = None
        
        # Joystick kontrolleri
        self._joystick_anchor = None
        self._joystick_touch_id = None
        
        # Oyunu başlat
        self._initialize_game()
        
    def _initialize_game(self):
        """Oyunu başlat"""
        Logger.info("GameManager: Oyun başlatılıyor...")
        
        # Ekranları ekle
        self.add_widget(self.game_screen)
        self.add_widget(self.hud)
        
        # Oyuncuyu oluştur
        self.player = EnhancedPlayer()
        self.player.pos = [self.width/2, self.height/2]
        self.game_screen.add_entity(self.player)
        
        # HUD'ı güncelle
        self.hud.bind_player(self.player)
        
        # Oyun durumunu başlat
        self.state.start_new_run(self.rng.generate_seed())
        
        Logger.info("GameManager: Oyun başlatıldı!")
        
    def update(self, dt):
        """Ana oyun döngüsü (60 FPS)"""
        if self.is_paused or self.current_scene != 1:  # GameScene.GAME
            return
            
        # Zamanı güncelle
        self.game_time += dt
        self.state.game_time = self.game_time
        
        # Joystick kontrolü
        if self.joystick_active and self.player:
            self.player.set_movement_input(self.joystick_pos)
        
        # Sistemleri güncelle
        self._update_systems(dt)
        
        # Parçacık sistemini güncelle
        particle_system.update(dt)
        
        # UI'ı güncelle
        self._update_ui(dt)
        
        # Level-up kontrolü
        if self.player and self.player.needs_level_up():
            self._trigger_level_up()
            
        # Oyun bitişi kontrolü
        if self.player and self.player.is_dead():
            self._trigger_game_over()
            
    def _update_systems(self, dt):
        """Tüm sistemleri güncelle"""
        
        # Hareket sistemi
        self.movement_system.update(dt, self.player, self.enemies, self.projectiles)
        
        # Spawn sistemi
        new_enemies = self.spawn_system.update(dt, self.game_time, self.get_spawn_bounds())
        for enemy in new_enemies:
            self.enemies.append(enemy)
            self.game_screen.add_entity(enemy)
        
        # Düşman AI güncellemesi
        if self.player and self.player.is_alive:
            player_pos = (self.player.center_x, self.player.center_y)
            for enemy in self.enemies:
                if enemy.is_alive:
                    enemy.update_ai(dt, player_pos, self.enemies)
            
        # Yetenek sistemi (auto-fire)
        if self.player:
            new_projectiles = self.ability_system.update(dt, self.player, self.enemies)
            for projectile in new_projectiles:
                self.projectiles.append(projectile)
                self.game_screen.add_entity(projectile)
        
        # Fizik sistemi (çarpışma tespiti)
        self.physics_system.update(dt, self.player, self.enemies, self.projectiles, self.loot_orbs)
        
        # Savaş sistemi (hasar hesaplama)
        new_loot = self.combat_system.update(dt, self.player, self.enemies, self.projectiles)
        for loot in new_loot:
            self.loot_orbs.append(loot)
            self.game_screen.add_entity(loot)
        
        # Ölü varlıkları temizle
        self._cleanup_dead_entities()
        
    def _update_ui(self, dt):
        """UI'ı güncelle"""
        if self.hud:
            self.hud.update_time(self.game_time)
            
    def _trigger_level_up(self):
        """Level-up panelini göster"""
        if self.level_up_panel:
            return  # Zaten açık
            
        self.is_paused = True
        abilities = self.ability_system.get_random_abilities(3, self.player.abilities)
        
        self.level_up_panel = LevelUpPanel(abilities)
        self.level_up_panel.bind(on_ability_selected=self._on_ability_selected)
        self.add_widget(self.level_up_panel)
        
    def _on_ability_selected(self, panel, ability_index):
        """Yetenek seçildiğinde"""
        selected_ability = panel.abilities[ability_index]
        self.player.add_ability(selected_ability)
        self.player.level_up()
        
        # Panel'i kapat
        self.remove_widget(self.level_up_panel)
        self.level_up_panel = None
        self.is_paused = False
        
    def _trigger_game_over(self):
        """Oyun bitişi ekranını göster"""
        self.current_scene = 4  # GameScene.GAME_OVER
        
        # İstatistikleri hesapla
        survival_time = self.format_time(self.game_time)
        final_level = self.player.level if self.player else 1
        coins_earned = self.state.coins_earned
        
        # Kaydet
        self.save_service.add_meta_currency(coins_earned)
        self.save_service.save_game_data()
        
        # Game over ekranını göster
        self.game_over_screen = GameOverScreen(
            survival_time=survival_time,
            final_level=final_level,
            coins_earned=coins_earned
        )
        self.game_over_screen.bind(on_restart=self._restart_game)
        self.game_over_screen.bind(on_main_menu=self._go_to_main_menu)
        self.add_widget(self.game_over_screen)
        
    def _cleanup_dead_entities(self):
        """Ölü varlıkları temizle"""
        # Düşmanlar
        for enemy in self.enemies[:]:
            if enemy.is_dead():
                self.enemies.remove(enemy)
                self.game_screen.remove_entity(enemy)
                
        # Mermiler
        for projectile in self.projectiles[:]:
            if projectile.is_dead():
                self.projectiles.remove(projectile)
                self.game_screen.remove_entity(projectile)
                
        # Loot
        for loot in self.loot_orbs[:]:
            if loot.is_collected():
                self.loot_orbs.remove(loot)
                self.game_screen.remove_entity(loot)
    
    def get_spawn_bounds(self):
        """Spawn sınırlarını döndür"""
        margin = 100
        return {
            'left': -margin,
            'right': self.width + margin,
            'top': self.height + margin,
            'bottom': -margin,
            'center_x': self.width / 2,
            'center_y': self.height / 2
        }
    
    def format_time(self, seconds):
        """Zamanı formatla"""
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes:02d}:{secs:02d}"
    
    # Touch/Joystick kontrolleri
    def on_touch_down(self, touch):
        """Dokunma başlangıcı"""
        # Sol alt çeyrek - joystick alanı
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
        """Dokunma hareketi"""
        if (self._joystick_touch_id == touch.uid and 
            self.joystick_active):
            self._update_joystick(touch.x, touch.y)
            return True
            
        return super().on_touch_move(touch)
    
    def on_touch_up(self, touch):
        """Dokunma bitişi"""
        if self._joystick_touch_id == touch.uid:
            self.joystick_active = False
            self.joystick_pos = [0.0, 0.0]
            self._joystick_touch_id = None
            self._joystick_anchor = None
            return True
            
        return super().on_touch_up(touch)
    
    def _update_joystick(self, touch_x, touch_y):
        """Joystick pozisyonunu güncelle"""
        if not self._joystick_anchor:
            return
            
        anchor_x, anchor_y = self._joystick_anchor
        dx = touch_x - anchor_x
        dy = touch_y - anchor_y
        
        # Mesafeyi sınırla (max 60 piksel)
        max_distance = 60
        distance = (dx*dx + dy*dy) ** 0.5
        
        if distance > max_distance:
            dx = dx * max_distance / distance
            dy = dy * max_distance / distance
            
        # Normalize et (-1 ile 1 arası)
        self.joystick_pos = [dx / max_distance, dy / max_distance]
    
    # Oyun kontrolleri
    def pause_game(self):
        """Oyunu duraklat"""
        if self.current_scene == 1:  # GameScene.GAME
            self.is_paused = True
            if not self.pause_menu:
                self.pause_menu = PauseMenu()
                self.pause_menu.bind(on_resume=self._resume_game)
                self.pause_menu.bind(on_main_menu=self._go_to_main_menu)
                self.pause_menu.bind(on_quit=self._quit_game)
                self.add_widget(self.pause_menu)
    
    def resume_game(self):
        """Oyunu devam ettir"""
        self._resume_game()
    
    def _resume_game(self, *args):
        """Oyunu devam ettir (internal)"""
        self.is_paused = False
        if self.pause_menu:
            self.remove_widget(self.pause_menu)
            self.pause_menu = None
    
    def _restart_game(self, *args):
        """Oyunu yeniden başlat"""
        # Tüm varlıkları temizle
        self._clear_all_entities()
        
        # Oyunu yeniden başlat
        self.game_time = 0.0
        self.current_scene = 1  # GameScene.GAME
        self.is_paused = False
        
        if self.game_over_screen:
            self.remove_widget(self.game_over_screen)
            self.game_over_screen = None
            
        self._initialize_game()
    
    def _go_to_main_menu(self, *args):
        """Ana menüye dön"""
        # TODO: Ana menü implementasyonu
        Logger.info("GameManager: Ana menüye dönülüyor...")
        
    def _quit_game(self, *args):
        """Oyundan çık"""
        self.save_game()
        Logger.info("GameManager: Oyundan çıkılıyor...")
        # App.get_running_app().stop()
    
    def _clear_all_entities(self):
        """Tüm varlıkları temizle"""
        for enemy in self.enemies[:]:
            self.game_screen.remove_entity(enemy)
        for projectile in self.projectiles[:]:
            self.game_screen.remove_entity(projectile)
        for loot in self.loot_orbs[:]:
            self.game_screen.remove_entity(loot)
            
        if self.player:
            self.game_screen.remove_entity(self.player)
            
        self.enemies.clear()
        self.projectiles.clear()
        self.loot_orbs.clear()
        self.player = None
    
    def save_game(self):
        """Oyunu kaydet"""
        self.save_service.save_game_data()
        Logger.info("GameManager: Oyun kaydedildi.")
