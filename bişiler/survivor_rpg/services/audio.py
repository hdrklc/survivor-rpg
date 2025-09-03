#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Services/Audio.py - Ses servisi
"""

from kivy.logger import Logger


class AudioService:
    """Ses servisi (basit implementasyon)"""
    
    def __init__(self):
        self.sfx_volume = 0.8
        self.music_volume = 0.7
        self.enabled = True
        
        Logger.info("AudioService: Ses servisi başlatıldı")
    
    def play_sfx(self, sound_name: str):
        """Ses efekti çal"""
        if self.enabled:
            # TODO: Gerçek ses çalma implementasyonu
            Logger.debug(f"AudioService: SFX çalınıyor: {sound_name}")
    
    def play_music(self, music_name: str):
        """Müzik çal"""
        if self.enabled:
            # TODO: Gerçek müzik çalma implementasyonu
            Logger.debug(f"AudioService: Müzik çalınıyor: {music_name}")
    
    def stop_music(self):
        """Müziği durdur"""
        Logger.debug("AudioService: Müzik durduruldu")
    
    def set_sfx_volume(self, volume: float):
        """SFX ses seviyesi"""
        self.sfx_volume = max(0.0, min(1.0, volume))
    
    def set_music_volume(self, volume: float):
        """Müzik ses seviyesi"""
        self.music_volume = max(0.0, min(1.0, volume))
