#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Core/RNG.py - Rastgele sayı üretimi ve seed yönetimi
"""

import random
import time
from typing import List, Dict, Any, Tuple
import math


class GameRNG:
    """Oyun rastgele sayı üreticisi"""
    
    def __init__(self, seed: int = None):
        self.seed = seed or self._generate_time_seed()
        self.random = random.Random(self.seed)
        
    def _generate_time_seed(self) -> int:
        """Zamana dayalı seed üret"""
        return int(time.time() * 1000000) % (2**31)
    
    def generate_seed(self) -> int:
        """Yeni seed üret"""
        return self._generate_time_seed()
    
    def set_seed(self, seed: int):
        """Seed'i değiştir"""
        self.seed = seed
        self.random = random.Random(seed)
    
    def random_float(self) -> float:
        """0.0 - 1.0 arası rastgele float"""
        return self.random.random()
    
    def random_range(self, min_val: float, max_val: float) -> float:
        """Belirtilen aralıkta rastgele float"""
        return self.random.uniform(min_val, max_val)
    
    def random_int(self, min_val: int, max_val: int) -> int:
        """Belirtilen aralıkta rastgele int"""
        return self.random.randint(min_val, max_val)
    
    def random_bool(self, probability: float = 0.5) -> bool:
        """Belirtilen olasılıkla True/False"""
        return self.random.random() < probability
    
    def random_offscreen_position(self, screen_width: float, screen_height: float,
                                margin: float = 100) -> Tuple[float, float]:
        """Ekran dışında rastgele pozisyon"""
        side = self.random.randint(0, 3)
        
        if side == 0:  # Sol
            x = -margin
            y = self.random.uniform(-margin, screen_height + margin)
        elif side == 1:  # Sağ
            x = screen_width + margin
            y = self.random.uniform(-margin, screen_height + margin)
        elif side == 2:  # Üst
            x = self.random.uniform(-margin, screen_width + margin)
            y = screen_height + margin
        else:  # Alt
            x = self.random.uniform(-margin, screen_width + margin)
            y = -margin
            
        return (x, y)
    
    def weighted_choice(self, choices: Dict[str, float]) -> str:
        """Ağırlıklı rastgele seçim"""
        if not choices:
            return None
            
        items = list(choices.items())
        total_weight = sum(weight for _, weight in items)
        
        if total_weight <= 0:
            return self.random.choice(list(choices.keys()))
        
        r = self.random.uniform(0, total_weight)
        cumulative = 0
        
        for item, weight in items:
            cumulative += weight
            if r <= cumulative:
                return item
                
        return items[-1][0]
    
    def random_choice(self, items: List[Any]) -> Any:
        """Listeden rastgele seç"""
        if not items:
            return None
        return self.random.choice(items)