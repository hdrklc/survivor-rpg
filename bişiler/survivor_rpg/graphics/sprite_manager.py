#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Graphics/SpriteManager.py - Profesyonel sprite yönetim sistemi
"""

import os
from typing import Dict, Tuple, Optional
from kivy.graphics import Rectangle, PushMatrix, PopMatrix, Rotate, Color
from kivy.graphics.texture import Texture
from kivy.core.image import Image
from kivy.logger import Logger
import math


class SpriteSheet:
    """Sprite sheet yönetimi"""
    
    def __init__(self, image_path: str, sprite_width: int, sprite_height: int):
        self.image_path = image_path
        self.sprite_width = sprite_width
        self.sprite_height = sprite_height
        self.texture = None
        self.sprites: Dict[str, Texture] = {}
        
        self._load_texture()
    
    def _load_texture(self):
        """Texture'ı yükle"""
        try:
            if os.path.exists(self.image_path):
                image = Image(self.image_path)
                self.texture = image.texture
                Logger.info(f"SpriteSheet: Texture yüklendi: {self.image_path}")
            else:
                Logger.warning(f"SpriteSheet: Dosya bulunamadı: {self.image_path}")
                self._create_fallback_texture()
        except Exception as e:
            Logger.error(f"SpriteSheet: Texture yükleme hatası: {e}")
            self._create_fallback_texture()
    
    def _create_fallback_texture(self):
        """Fallback texture oluştur"""
        # 32x32 renkli kare oluştur
        data = []
        for y in range(32):
            for x in range(32):
                # Gradient efekti
                r = int(255 * (x / 31))
                g = int(255 * (y / 31))
                b = 128
                a = 255
                data.extend([r, g, b, a])
        
        self.texture = Texture.create(size=(32, 32))
        self.texture.blit_buffer(bytes(data), colorfmt='rgba', bufferfmt='ubyte')
    
    def get_sprite(self, name: str, x: int, y: int) -> Texture:
        """Sprite'ı al"""
        if name in self.sprites:
            return self.sprites[name]
        
        if not self.texture:
            return None
        
        # Sprite'ı kes
        sprite_texture = self.texture.get_region(
            x * self.sprite_width,
            y * self.sprite_height,
            self.sprite_width,
            self.sprite_height
        )
        
        self.sprites[name] = sprite_texture
        return sprite_texture


class AnimatedSprite:
    """Animasyonlu sprite"""
    
    def __init__(self, sprite_sheet: SpriteSheet, frames: list, fps: float = 10.0):
        self.sprite_sheet = sprite_sheet
        self.frames = frames  # [(name, x, y), ...]
        self.fps = fps
        self.frame_duration = 1.0 / fps
        self.current_frame = 0
        self.time_since_frame = 0.0
        self.playing = True
        self.loop = True
        
        # Frame texture'larını önceden yükle
        self.frame_textures = []
        for name, x, y in frames:
            texture = sprite_sheet.get_sprite(name, x, y)
            self.frame_textures.append(texture)
    
    def update(self, dt: float):
        """Animasyonu güncelle"""
        if not self.playing or not self.frame_textures:
            return
        
        self.time_since_frame += dt
        
        if self.time_since_frame >= self.frame_duration:
            self.time_since_frame = 0.0
            self.current_frame += 1
            
            if self.current_frame >= len(self.frame_textures):
                if self.loop:
                    self.current_frame = 0
                else:
                    self.current_frame = len(self.frame_textures) - 1
                    self.playing = False
    
    def get_current_texture(self) -> Optional[Texture]:
        """Mevcut frame'in texture'ını al"""
        if not self.frame_textures:
            return None
        return self.frame_textures[self.current_frame]
    
    def play(self):
        """Animasyonu başlat"""
        self.playing = True
    
    def pause(self):
        """Animasyonu duraklat"""
        self.playing = False
    
    def reset(self):
        """Animasyonu başa sar"""
        self.current_frame = 0
        self.time_since_frame = 0.0


class SpriteRenderer:
    """Gelişmiş sprite render sistemi"""
    
    def __init__(self):
        self.sprite_sheets: Dict[str, SpriteSheet] = {}
        self._load_default_sprites()
    
    def _load_default_sprites(self):
        """Varsayılan sprite'ları yükle"""
        # Oyuncu sprite'ları
        self._create_player_sprites()
        
        # Düşman sprite'ları
        self._create_enemy_sprites()
        
        # Efekt sprite'ları
        self._create_effect_sprites()
        
        # UI sprite'ları
        self._create_ui_sprites()
    
    def _create_player_sprites(self):
        """Oyuncu sprite'larını oluştur"""
        # Procedural olarak güzel oyuncu sprite'ı oluştur
        data = []
        size = 32
        center = size // 2
        
        for y in range(size):
            for x in range(size):
                # Merkeze olan mesafe
                dist = math.sqrt((x - center)**2 + (y - center)**2)
                
                if dist <= 12:  # Ana gövde
                    # Mavi gradient
                    intensity = 1.0 - (dist / 12)
                    r = int(50 + intensity * 100)
                    g = int(150 + intensity * 100)
                    b = int(255)
                    a = 255
                elif dist <= 14:  # Kenar çizgisi
                    r, g, b, a = 255, 255, 255, 255
                else:  # Şeffaf
                    r, g, b, a = 0, 0, 0, 0
                
                data.extend([r, g, b, a])
        
        texture = Texture.create(size=(size, size))
        texture.blit_buffer(bytes(data), colorfmt='rgba', bufferfmt='ubyte')
        
        # Fake sprite sheet oluştur
        class FakeSheet:
            def __init__(self, tex):
                self.texture = tex
            def get_sprite(self, name, x, y):
                return self.texture
        
        self.sprite_sheets['player'] = FakeSheet(texture)
    
    def _create_enemy_sprites(self):
        """Düşman sprite'larını oluştur"""
        enemies = {
            'slime': (100, 255, 100),    # Yeşil slime
            'goblin': (255, 100, 100),   # Kırmızı goblin
            'skeleton': (200, 200, 200), # Gri iskelet
            'orc': (150, 100, 50),       # Kahverengi orc
        }
        
        for enemy_name, (base_r, base_g, base_b) in enemies.items():
            data = []
            size = 24
            center = size // 2
            
            for y in range(size):
                for x in range(size):
                    dist = math.sqrt((x - center)**2 + (y - center)**2)
                    
                    if dist <= 10:  # Ana gövde
                        intensity = 1.0 - (dist / 10)
                        r = int(base_r * intensity)
                        g = int(base_g * intensity)
                        b = int(base_b * intensity)
                        a = 255
                        
                        # Göz efekti
                        if 6 <= x <= 8 and 8 <= y <= 10:
                            r, g, b = 255, 0, 0  # Kırmızı göz
                        elif 16 <= x <= 18 and 8 <= y <= 10:
                            r, g, b = 255, 0, 0  # Kırmızı göz
                            
                    elif dist <= 12:  # Kenar
                        r = int(base_r * 0.5)
                        g = int(base_g * 0.5) 
                        b = int(base_b * 0.5)
                        a = 255
                    else:
                        r, g, b, a = 0, 0, 0, 0
                    
                    data.extend([r, g, b, a])
            
            texture = Texture.create(size=(size, size))
            texture.blit_buffer(bytes(data), colorfmt='rgba', bufferfmt='ubyte')
            
            class FakeSheet:
                def __init__(self, tex):
                    self.texture = tex
                def get_sprite(self, name, x, y):
                    return self.texture
            
            self.sprite_sheets[enemy_name] = FakeSheet(texture)
    
    def _create_effect_sprites(self):
        """Efekt sprite'larını oluştur"""
        effects = {
            'explosion': [(255, 255, 0), (255, 150, 0), (255, 50, 0)],
            'heal': [(0, 255, 0), (150, 255, 150), (255, 255, 255)],
            'damage': [(255, 0, 0), (255, 100, 100), (255, 150, 150)],
        }
        
        for effect_name, colors in effects.items():
            textures = []
            
            for frame, (r, g, b) in enumerate(colors):
                data = []
                size = 16
                center = size // 2
                
                for y in range(size):
                    for x in range(size):
                        dist = math.sqrt((x - center)**2 + (y - center)**2)
                        max_radius = 6 + frame * 2  # Genişleyen efekt
                        
                        if dist <= max_radius:
                            intensity = 1.0 - (dist / max_radius)
                            final_r = int(r * intensity)
                            final_g = int(g * intensity)
                            final_b = int(b * intensity)
                            alpha = int(255 * intensity * (1.0 - frame * 0.3))
                        else:
                            final_r = final_g = final_b = alpha = 0
                        
                        data.extend([final_r, final_g, final_b, alpha])
                
                texture = Texture.create(size=(size, size))
                texture.blit_buffer(bytes(data), colorfmt='rgba', bufferfmt='ubyte')
                textures.append(texture)
            
            class FakeSheet:
                def __init__(self, texs):
                    self.textures = texs
                    self.current = 0
                def get_sprite(self, name, x, y):
                    return self.textures[self.current % len(self.textures)]
            
            self.sprite_sheets[effect_name] = FakeSheet(textures)
    
    def _create_ui_sprites(self):
        """UI sprite'larını oluştur"""
        # Modern UI elementleri
        ui_elements = {
            'button': (70, 130, 180),     # Steel blue
            'panel': (40, 40, 60),        # Dark gray
            'health_bar': (220, 20, 60),  # Crimson
            'mana_bar': (30, 144, 255),   # Dodger blue
            'xp_bar': (255, 215, 0),      # Gold
        }
        
        for ui_name, (r, g, b) in ui_elements.items():
            data = []
            width, height = 64, 16 if 'bar' in ui_name else 64
            
            for y in range(height):
                for x in range(width):
                    # Gradient efekti
                    if 'bar' in ui_name:
                        intensity = 0.7 + 0.3 * (1.0 - y / height)  # Dikey gradient
                    else:
                        center_x, center_y = width // 2, height // 2
                        dist = math.sqrt((x - center_x)**2 + (y - center_y)**2)
                        max_dist = math.sqrt(center_x**2 + center_y**2)
                        intensity = 0.5 + 0.5 * (1.0 - dist / max_dist)
                    
                    final_r = int(r * intensity)
                    final_g = int(g * intensity)
                    final_b = int(b * intensity)
                    alpha = 255
                    
                    # Kenar vurgusu
                    if x == 0 or x == width-1 or y == 0 or y == height-1:
                        final_r = min(255, final_r + 50)
                        final_g = min(255, final_g + 50)
                        final_b = min(255, final_b + 50)
                    
                    data.extend([final_r, final_g, final_b, alpha])
            
            texture = Texture.create(size=(width, height))
            texture.blit_buffer(bytes(data), colorfmt='rgba', bufferfmt='ubyte')
            
            class FakeSheet:
                def __init__(self, tex):
                    self.texture = tex
                def get_sprite(self, name, x, y):
                    return self.texture
            
            self.sprite_sheets[ui_name] = FakeSheet(texture)
    
    def render_sprite(self, canvas, sprite_name: str, pos: Tuple[float, float], 
                     size: Tuple[float, float], rotation: float = 0.0, 
                     color: Tuple[float, float, float, float] = (1, 1, 1, 1)):
        """Sprite'ı render et"""
        
        if sprite_name not in self.sprite_sheets:
            Logger.warning(f"SpriteRenderer: Sprite bulunamadı: {sprite_name}")
            return
        
        sheet = self.sprite_sheets[sprite_name]
        texture = sheet.get_sprite(sprite_name, 0, 0)
        
        if not texture:
            return
        
        with canvas:
            Color(*color)
            
            if rotation != 0.0:
                PushMatrix()
                # Rotation merkezi
                center_x = pos[0] + size[0] / 2
                center_y = pos[1] + size[1] / 2
                Rotate(angle=rotation, origin=(center_x, center_y))
            
            Rectangle(texture=texture, pos=pos, size=size)
            
            if rotation != 0.0:
                PopMatrix()
    
    def get_sprite_sheet(self, name: str) -> Optional[SpriteSheet]:
        """Sprite sheet'i al"""
        return self.sprite_sheets.get(name)


# Global sprite renderer
sprite_renderer = SpriteRenderer()
