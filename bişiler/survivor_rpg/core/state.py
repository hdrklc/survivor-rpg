#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Core/State.py - Oyun durumu ve sahne yönetimi
"""

from enum import IntEnum
from dataclasses import dataclass, field
from typing import Dict, List, Any


class GameScene(IntEnum):
    """Oyun sahneleri"""
    MAIN_MENU = 0
    GAME = 1
    PAUSE = 2
    LEVEL_UP = 3
    GAME_OVER = 4
    SETTINGS = 5


@dataclass
class PlayerStats:
    """Oyuncu istatistikleri"""
    # Temel özellikler
    max_hp: float = 100.0
    current_hp: float = 100.0
    base_damage: float = 10.0
    base_speed: float = 3.0
    base_attack_speed: float = 1.0
    
    # Level sistemi
    level: int = 1
    current_xp: float = 0.0
    xp_to_next_level: float = 15.0
    
    # Bonus değerleri (yetenek bonusları)
    damage_multiplier: float = 1.0
    speed_multiplier: float = 1.0
    attack_speed_multiplier: float = 1.0
    hp_multiplier: float = 1.0
    
    # Özel özellikler
    crit_chance: float = 0.05  # %5
    crit_multiplier: float = 1.5  # 1.5x
    magnet_range: float = 50.0
    
    def get_total_damage(self) -> float:
        """Toplam hasar hesapla"""
        return self.base_damage * self.damage_multiplier
    
    def get_total_speed(self) -> float:
        """Toplam hız hesapla"""
        return self.base_speed * self.speed_multiplier
    
    def get_total_attack_speed(self) -> float:
        """Toplam saldırı hızı hesapla"""
        return self.base_attack_speed * self.attack_speed_multiplier
    
    def get_max_hp(self) -> float:
        """Maksimum HP hesapla"""
        return self.max_hp * self.hp_multiplier
    
    def is_dead(self) -> bool:
        """Oyuncu öldü mü?"""
        return self.current_hp <= 0
    
    def heal(self, amount: float):
        """Oyuncuyu iyileştir"""
        self.current_hp = min(self.current_hp + amount, self.get_max_hp())
    
    def take_damage(self, amount: float):
        """Hasar al"""
        self.current_hp = max(0, self.current_hp - amount)
    
    def add_xp(self, amount: float) -> bool:
        """XP ekle, level atladıysa True döndür"""
        self.current_xp += amount
        
        if self.current_xp >= self.xp_to_next_level:
            return True
        return False
    
    def level_up(self):
        """Level atla"""
        self.current_xp -= self.xp_to_next_level
        self.level += 1
        
        # XP gereksinimi artışı (tasarım dokümanından)
        self.xp_to_next_level = 10 + 5 * self.level + 1.25 * (self.level ** 2)
        
        # Level başına küçük stat artışı
        self.damage_multiplier += 0.02  # +2% hasar
        self.speed_multiplier += 0.02   # +2% hız


@dataclass
class RunStats:
    """Tek koşu istatistikleri"""
    seed: int = 0
    start_time: float = 0.0
    current_time: float = 0.0
    
    # İstatistikler
    enemies_killed: int = 0
    damage_dealt: float = 0.0
    damage_taken: float = 0.0
    xp_gained: float = 0.0
    coins_collected: int = 0
    
    # En yüksek değerler
    highest_level: int = 1
    longest_survival: float = 0.0
    
    def get_survival_time(self) -> float:
        """Hayatta kalma süresi"""
        return self.current_time - self.start_time
    
    def add_kill(self, enemy_type: str = None):
        """Düşman öldürme sayacı"""
        self.enemies_killed += 1
    
    def add_damage_dealt(self, amount: float):
        """Verilen hasar sayacı"""
        self.damage_dealt += amount
    
    def add_damage_taken(self, amount: float):
        """Alınan hasar sayacı"""
        self.damage_taken += amount
    
    def add_xp(self, amount: float):
        """XP sayacı"""
        self.xp_gained += amount
    
    def add_coins(self, amount: int):
        """Coin sayacı"""
        self.coins_collected += amount


@dataclass 
class MetaProgression:
    """Kalıcı meta ilerleme"""
    # Meta para
    total_coins: int = 0
    lifetime_coins: int = 0
    
    # Kalıcı yükseltmeler (0-5 seviye)
    permanent_upgrades: Dict[str, int] = field(default_factory=lambda: {
        'attack_bonus': 0,      # Her seviye +3% hasar
        'health_bonus': 0,      # Her seviye +5% HP
        'speed_bonus': 0,       # Her seviye +3% hız
        'magnet_bonus': 0,      # Her seviye +20% çekim alanı
        'xp_bonus': 0,          # Her seviye +10% XP
    })
    
    # İstatistikler
    total_runs: int = 0
    total_playtime: float = 0.0
    best_survival_time: float = 0.0
    highest_level_reached: int = 1
    total_enemies_killed: int = 0
    
    def get_upgrade_cost(self, upgrade_name: str) -> int:
        """Yükseltme maliyeti hesapla"""
        current_level = self.permanent_upgrades.get(upgrade_name, 0)
        base_costs = {
            'attack_bonus': 50,
            'health_bonus': 60,
            'speed_bonus': 40,
            'magnet_bonus': 30,
            'xp_bonus': 70,
        }
        base_cost = base_costs.get(upgrade_name, 50)
        # Her seviye %50 daha pahalı
        return int(base_cost * (1.5 ** current_level))
    
    def can_afford_upgrade(self, upgrade_name: str) -> bool:
        """Yükseltmeyi alabilir mi?"""
        if self.permanent_upgrades.get(upgrade_name, 0) >= 5:
            return False  # Max seviye
        cost = self.get_upgrade_cost(upgrade_name)
        return self.total_coins >= cost
    
    def buy_upgrade(self, upgrade_name: str) -> bool:
        """Yükseltme satın al"""
        if not self.can_afford_upgrade(upgrade_name):
            return False
            
        cost = self.get_upgrade_cost(upgrade_name)
        self.total_coins -= cost
        self.permanent_upgrades[upgrade_name] += 1
        return True
    
    def get_upgrade_bonus(self, upgrade_name: str) -> float:
        """Yükseltme bonusu hesapla"""
        level = self.permanent_upgrades.get(upgrade_name, 0)
        bonus_per_level = {
            'attack_bonus': 0.03,   # 3%
            'health_bonus': 0.05,   # 5%
            'speed_bonus': 0.03,    # 3%
            'magnet_bonus': 0.20,   # 20%
            'xp_bonus': 0.10,       # 10%
        }
        return level * bonus_per_level.get(upgrade_name, 0.0)


class GameState:
    """Ana oyun durumu sınıfı"""
    
    def __init__(self):
        # Mevcut sahne
        self.current_scene = GameScene.MAIN_MENU
        self.previous_scene = GameScene.MAIN_MENU
        
        # Oyuncu durumu
        self.player_stats = PlayerStats()
        
        # Mevcut koşu
        self.current_run = RunStats()
        
        # Meta ilerleme
        self.meta_progression = MetaProgression()
        
        # Oyun ayarları
        self.settings = {
            'music_volume': 0.7,
            'sfx_volume': 0.8,
            'vibration': True,
            'auto_fire': True,
            'graphics_quality': 'medium'  # low, medium, high
        }
        
        # Geçici durumlar
        self.game_time = 0.0
        self.is_paused = False
        self.coins_earned = 0  # Bu koşuda kazanılan
        
    def start_new_run(self, seed: int):
        """Yeni koşu başlat"""
        # Koşu istatistiklerini sıfırla
        self.current_run = RunStats()
        self.current_run.seed = seed
        self.current_run.start_time = 0.0
        
        # Oyuncu istatistiklerini sıfırla
        self.player_stats = PlayerStats()
        
        # Meta bonusları uygula
        self._apply_meta_bonuses()
        
        # Oyun durumu
        self.current_scene = GameScene.GAME
        self.game_time = 0.0
        self.is_paused = False
        self.coins_earned = 0
        
    def end_run(self):
        """Koşu bitişi"""
        # İstatistikleri güncelle
        survival_time = self.current_run.get_survival_time()
        
        self.meta_progression.total_runs += 1
        self.meta_progression.total_playtime += survival_time
        
        if survival_time > self.meta_progression.best_survival_time:
            self.meta_progression.best_survival_time = survival_time
            
        if self.player_stats.level > self.meta_progression.highest_level_reached:
            self.meta_progression.highest_level_reached = self.player_stats.level
            
        self.meta_progression.total_enemies_killed += self.current_run.enemies_killed
        
        # Kazanılan coinleri ekle
        self.meta_progression.total_coins += self.coins_earned
        self.meta_progression.lifetime_coins += self.coins_earned
        
    def _apply_meta_bonuses(self):
        """Meta bonusları oyuncuya uygula"""
        # Kalıcı yükseltme bonusları
        attack_bonus = self.meta_progression.get_upgrade_bonus('attack_bonus')
        health_bonus = self.meta_progression.get_upgrade_bonus('health_bonus')
        speed_bonus = self.meta_progression.get_upgrade_bonus('speed_bonus')
        magnet_bonus = self.meta_progression.get_upgrade_bonus('magnet_bonus')
        
        # Bonusları uygula
        self.player_stats.damage_multiplier += attack_bonus
        self.player_stats.hp_multiplier += health_bonus
        self.player_stats.speed_multiplier += speed_bonus
        self.player_stats.magnet_range += self.player_stats.magnet_range * magnet_bonus
        
        # HP'yi yeniden hesapla ve doldur
        self.player_stats.current_hp = self.player_stats.get_max_hp()
        
    def change_scene(self, new_scene: GameScene):
        """Sahne değiştir"""
        self.previous_scene = self.current_scene
        self.current_scene = new_scene
        
    def toggle_pause(self):
        """Pause durumunu değiştir"""
        if self.current_scene == GameScene.GAME:
            self.is_paused = not self.is_paused
            
    def get_current_minute(self) -> int:
        """Mevcut dakika (spawn ve ölçekleme için)"""
        return int(self.game_time // 60)
    
    def to_dict(self) -> Dict[str, Any]:
        """Save için dict'e çevir"""
        return {
            'meta_progression': {
                'total_coins': self.meta_progression.total_coins,
                'permanent_upgrades': self.meta_progression.permanent_upgrades.copy(),
                'total_runs': self.meta_progression.total_runs,
                'total_playtime': self.meta_progression.total_playtime,
                'best_survival_time': self.meta_progression.best_survival_time,
                'highest_level_reached': self.meta_progression.highest_level_reached,
                'total_enemies_killed': self.meta_progression.total_enemies_killed,
            },
            'settings': self.settings.copy()
        }
    
    def from_dict(self, data: Dict[str, Any]):
        """Save'den yükle"""
        if 'meta_progression' in data:
            meta_data = data['meta_progression']
            self.meta_progression.total_coins = meta_data.get('total_coins', 0)
            self.meta_progression.permanent_upgrades.update(
                meta_data.get('permanent_upgrades', {})
            )
            self.meta_progression.total_runs = meta_data.get('total_runs', 0)
            self.meta_progression.total_playtime = meta_data.get('total_playtime', 0.0)
            self.meta_progression.best_survival_time = meta_data.get('best_survival_time', 0.0)
            self.meta_progression.highest_level_reached = meta_data.get('highest_level_reached', 1)
            self.meta_progression.total_enemies_killed = meta_data.get('total_enemies_killed', 0)
            
        if 'settings' in data:
            self.settings.update(data['settings'])
