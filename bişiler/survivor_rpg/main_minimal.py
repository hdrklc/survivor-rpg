#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Survivor RPG - Minimal çalışan versiyon
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
from kivy.properties import ListProperty, NumericProperty

# Kivy ayarları
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '600')
Config.set('graphics', 'resizable', True)

class SimplePlayer(Widget):
    """Basit oyuncu"""
    
    velocity = ListProperty([0.0, 0.0])
    speed = NumericProperty(150.0)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size = (32, 32)
        self.pos = (400, 300)
        
        with self.canvas:
            Color(0.2, 0.8, 1.0, 1.0)  # Mavi
            self.graphic = Ellipse(pos=self.pos, size=self.size)
        
        self.bind(pos=self.update_graphics)
    
    def update_graphics(self, *args):
        self.graphic.pos = self.pos
    
    def update(self, dt):
        # Hareket
        self.x += self.velocity[0] * dt
        self.y += self.velocity[1] * dt
        
        # Ekran sınırları
        self.x = max(0, min(self.x, 800 - self.width))
        self.y = max(0, min(self.y, 600 - self.height))
    
    def set_velocity(self, vx, vy):
        self.velocity = [vx * self.speed, vy * self.speed]

class SimpleGame(Widget):
    """Basit oyun"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Oyuncu oluştur
        self.player = SimplePlayer()
        self.add_widget(self.player)
        
        # Joystick
        self.joystick_pos = [0.0, 0.0]
        self.joystick_active = False
        self._joystick_anchor = None
        self._joystick_touch_id = None
        
        Logger.info("SimpleGame: Basit oyun başlatıldı!")
    
    def update(self, dt):
        # Joystick kontrolü
        if self.joystick_active:
            self.player.set_velocity(self.joystick_pos[0], self.joystick_pos[1])
        else:
            self.player.set_velocity(0, 0)
        
        # Oyuncuyu güncelle
        self.player.update(dt)
    
    def on_touch_down(self, touch):
        # Sol yarı - joystick
        if touch.x < self.width * 0.5:
            self._joystick_anchor = (touch.x, touch.y)
            self._joystick_touch_id = touch.uid
            self.joystick_active = True
            self._update_joystick(touch.x, touch.y)
            return True
        return False
    
    def on_touch_move(self, touch):
        if self._joystick_touch_id == touch.uid and self.joystick_active:
            self._update_joystick(touch.x, touch.y)
            return True
        return False
    
    def on_touch_up(self, touch):
        if self._joystick_touch_id == touch.uid:
            self.joystick_active = False
            self.joystick_pos = [0.0, 0.0]
            self._joystick_touch_id = None
            self._joystick_anchor = None
            return True
        return False
    
    def _update_joystick(self, touch_x, touch_y):
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

class SurvivorRPGApp(App):
    def build(self):
        Logger.info("SurvivorRPG: Minimal oyun başlatılıyor...")
        
        self.game = SimpleGame()
        Clock.schedule_interval(self.game.update, 1/60.0)
        
        return self.game

if __name__ == '__main__':
    SurvivorRPGApp().run()
