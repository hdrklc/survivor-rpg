#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Services/Save.py - Kayıt/yükleme servisi
"""

import json
import os
from typing import Dict, Any
from kivy.logger import Logger


class SaveService:
    """Kayıt/yükleme servisi"""
    
    def __init__(self, save_file: str = "survivor_save.json"):
        self.save_file = save_file
        self.data = {}
        self.load_game_data()
    
    def save_game_data(self):
        """Oyun verilerini kaydet"""
        try:
            with open(self.save_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
            Logger.info(f"SaveService: Veri kaydedildi: {self.save_file}")
        except Exception as e:
            Logger.error(f"SaveService: Kaydetme hatası: {e}")
    
    def load_game_data(self):
        """Oyun verilerini yükle"""
        try:
            if os.path.exists(self.save_file):
                with open(self.save_file, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
                Logger.info(f"SaveService: Veri yüklendi: {self.save_file}")
            else:
                self.data = self._get_default_data()
                Logger.info("SaveService: Varsayılan veri oluşturuldu")
        except Exception as e:
            Logger.error(f"SaveService: Yükleme hatası: {e}")
            self.data = self._get_default_data()
    
    def _get_default_data(self) -> Dict[str, Any]:
        """Varsayılan kayıt verisi"""
        return {
            'meta_currency': 0,
            'perma_upgrades': {
                'atk_lvl': 0,
                'hp_lvl': 0,
                'speed_lvl': 0,
                'magnet_lvl': 0,
                'xp_lvl': 0
            },
            'settings': {
                'sfx_volume': 0.8,
                'music_volume': 0.7,
                'vibration': True,
                'auto_fire': True
            },
            'stats': {
                'total_runs': 0,
                'best_time': 0.0,
                'highest_level': 1,
                'total_enemies': 0
            }
        }
    
    def get_meta_currency(self) -> int:
        """Meta para miktarını al"""
        return self.data.get('meta_currency', 0)
    
    def add_meta_currency(self, amount: int):
        """Meta para ekle"""
        current = self.get_meta_currency()
        self.data['meta_currency'] = current + amount
    
    def spend_meta_currency(self, amount: int) -> bool:
        """Meta para harca"""
        current = self.get_meta_currency()
        if current >= amount:
            self.data['meta_currency'] = current - amount
            return True
        return False
    
    def get_setting(self, key: str, default=None):
        """Ayar al"""
        return self.data.get('settings', {}).get(key, default)
    
    def set_setting(self, key: str, value):
        """Ayar kaydet"""
        if 'settings' not in self.data:
            self.data['settings'] = {}
        self.data['settings'][key] = value
