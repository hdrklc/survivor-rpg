#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Survivor RPG - Güvenli ana uygulama dosyası
"""

import os
import sys
from pathlib import Path
import traceback

# Proje kök dizinini Python path'e ekle
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.logger import Logger
from kivy.uix.label import Label

# Kivy ayarları
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '600')
Config.set('graphics', 'resizable', True)
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

class SurvivorRPGApp(App):
    """Ana uygulama sınıfı"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Survivor RPG - Professional"
        self.game_manager = None
        
    def build(self):
        """Uygulamayı başlat"""
        Logger.info("SurvivorRPG: Uygulama başlatılıyor...")
        
        try:
            # GameManager'ı import et
            from core.game import GameManager
            Logger.info("SurvivorRPG: GameManager import edildi")
            
            # Oyun yöneticisini oluştur
            self.game_manager = GameManager()
            Logger.info("SurvivorRPG: GameManager oluşturuldu")
            
            # Ana oyun döngüsünü başlat (60 FPS)
            Clock.schedule_interval(self.game_manager.update, 1/60.0)
            Logger.info("SurvivorRPG: Oyun döngüsü başlatıldı")
            
            return self.game_manager
            
        except Exception as e:
            Logger.error(f"SurvivorRPG: Build hatası: {e}")
            Logger.error(f"Traceback: {traceback.format_exc()}")
            
            # Hata durumunda basit label döndür
            return Label(
                text=f'Oyun Yüklenirken Hata:\n{str(e)[:200]}...',
                font_size='16sp',
                text_size=(None, None),
                halign='center',
                valign='middle'
            )
    
    def on_pause(self):
        """Uygulama duraklatıldığında"""
        if self.game_manager and hasattr(self.game_manager, 'pause_game'):
            self.game_manager.pause_game()
        return True
    
    def on_resume(self):
        """Uygulama devam ettirildiğinde"""
        if self.game_manager and hasattr(self.game_manager, 'resume_game'):
            self.game_manager.resume_game()
    
    def on_stop(self):
        """Uygulama kapatıldığında"""
        if self.game_manager and hasattr(self.game_manager, 'save_game'):
            try:
                self.game_manager.save_game()
            except Exception as e:
                Logger.error(f"Save hatası: {e}")
        Logger.info("SurvivorRPG: Uygulama kapatılıyor...")

if __name__ == '__main__':
    try:
        Logger.info("SurvivorRPG: Ana uygulama başlatılıyor...")
        app = SurvivorRPGApp()
        app.run()
    except Exception as e:
        Logger.error(f"SurvivorRPG: Kritik hata: {e}")
        print(f"HATA: {e}")
        print("Traceback:")
        traceback.print_exc()
        input("Çıkmak için Enter'a basın...")
        sys.exit(1)
