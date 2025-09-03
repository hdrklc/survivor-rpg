#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Audio/SoundManager.py - Profesyonel ses yönetim sistemi
"""

import os
import math
from typing import Dict, Optional, Tuple
from kivy.logger import Logger
try:
    from kivy.core.audio import SoundLoader
except ImportError:
    SoundLoader = None


class AudioClip:
    """Ses klip sınıfı"""
    
    def __init__(self, file_path: str, volume: float = 1.0):
        self.file_path = file_path
        self.volume = volume
        self.sound = None
        self.loaded = False
        
        self._load_sound()
    
    def _load_sound(self):
        """Ses dosyasını yükle"""
        if not SoundLoader:
            Logger.warning("AudioClip: SoundLoader mevcut değil")
            return
        
        try:
            if os.path.exists(self.file_path):
                self.sound = SoundLoader.load(self.file_path)
                if self.sound:
                    self.sound.volume = self.volume
                    self.loaded = True
                    Logger.info(f"AudioClip: Ses yüklendi: {self.file_path}")
                else:
                    Logger.warning(f"AudioClip: Ses yüklenemedi: {self.file_path}")
            else:
                Logger.warning(f"AudioClip: Dosya bulunamadı: {self.file_path}")
        except Exception as e:
            Logger.error(f"AudioClip: Yükleme hatası: {e}")
    
    def play(self, volume: float = None):
        """Ses çal"""
        if not self.loaded or not self.sound:
            return
        
        try:
            if volume is not None:
                self.sound.volume = volume * self.volume
            else:
                self.sound.volume = self.volume
            
            self.sound.play()
        except Exception as e:
            Logger.error(f"AudioClip: Çalma hatası: {e}")
    
    def stop(self):
        """Ses durdur"""
        if self.loaded and self.sound:
            try:
                self.sound.stop()
            except Exception as e:
                Logger.error(f"AudioClip: Durdurma hatası: {e}")
    
    def set_volume(self, volume: float):
        """Ses seviyesi ayarla"""
        self.volume = max(0.0, min(1.0, volume))
        if self.loaded and self.sound:
            self.sound.volume = self.volume


class ProceduralAudio:
    """Procedural ses üretimi"""
    
    @staticmethod
    def generate_tone(frequency: float, duration: float, sample_rate: int = 44100) -> bytes:
        """Basit ton üret"""
        import struct
        import math
        
        samples = int(sample_rate * duration)
        data = []
        
        for i in range(samples):
            t = float(i) / sample_rate
            # Sinüs dalgası
            sample = int(32767 * math.sin(2 * math.pi * frequency * t))
            # Fade out efekti
            fade = 1.0 - (i / samples)
            sample = int(sample * fade)
            data.append(struct.pack('<h', sample))
        
        return b''.join(data)
    
    @staticmethod
    def generate_explosion_sound(duration: float = 0.5) -> bytes:
        """Patlama sesi üret"""
        import struct
        import random
        
        sample_rate = 22050
        samples = int(sample_rate * duration)
        data = []
        
        for i in range(samples):
            # Rastgele gürültü (white noise)
            sample = random.randint(-32767, 32767)
            
            # Envelope (zarf)
            t = float(i) / samples
            if t < 0.1:  # Attack
                envelope = t / 0.1
            else:  # Decay
                envelope = (1.0 - t) / 0.9
            
            # Düşük frekans filtresi (bass boost)
            envelope *= (1.0 - t * 0.5)
            
            sample = int(sample * envelope * 0.3)  # Volume control
            data.append(struct.pack('<h', sample))
        
        return b''.join(data)
    
    @staticmethod
    def generate_pickup_sound(pitch: float = 1.0) -> bytes:
        """Pickup sesi üret"""
        import struct
        import math
        
        sample_rate = 22050
        duration = 0.2
        samples = int(sample_rate * duration)
        data = []
        
        base_freq = 440.0 * pitch
        
        for i in range(samples):
            t = float(i) / sample_rate
            
            # Rising pitch
            freq = base_freq * (1.0 + t * 2.0)
            
            # Sinüs + harmonikler
            sample1 = math.sin(2 * math.pi * freq * t)
            sample2 = math.sin(2 * math.pi * freq * 2 * t) * 0.5
            sample3 = math.sin(2 * math.pi * freq * 3 * t) * 0.25
            
            combined = (sample1 + sample2 + sample3) / 1.75
            
            # Envelope
            envelope = (1.0 - t) ** 0.5
            
            sample = int(32767 * combined * envelope * 0.4)
            data.append(struct.pack('<h', sample))
        
        return b''.join(data)


class SoundManager:
    """Ana ses yöneticisi"""
    
    def __init__(self):
        self.audio_clips: Dict[str, AudioClip] = {}
        self.master_volume = 1.0
        self.sfx_volume = 0.8
        self.music_volume = 0.7
        self.enabled = True
        
        # Ses havuzu (sound pooling)
        self.sound_pools: Dict[str, list] = {}
        self.max_pool_size = 5
        
        # 3D ses özellikleri
        self.listener_pos = [0.0, 0.0]
        self.max_distance = 500.0
        
        self._load_default_sounds()
        
        Logger.info("SoundManager: Ses sistemi başlatıldı")
    
    def _load_default_sounds(self):
        """Varsayılan sesleri yükle"""
        # Procedural sesler oluştur
        self._create_procedural_sounds()
        
        # Asset klasöründen ses dosyalarını yükle
        self._load_audio_files()
    
    def _create_procedural_sounds(self):
        """Procedural sesler oluştur"""
        try:
            # Geçici ses dosyaları oluştur
            import tempfile
            import wave
            
            temp_dir = tempfile.gettempdir()
            
            # Patlama sesi
            explosion_data = ProceduralAudio.generate_explosion_sound(0.5)
            explosion_path = os.path.join(temp_dir, "explosion.wav")
            self._save_wav_file(explosion_path, explosion_data, 22050)
            self.audio_clips['explosion'] = AudioClip(explosion_path, 0.6)
            
            # Pickup sesi
            pickup_data = ProceduralAudio.generate_pickup_sound(1.2)
            pickup_path = os.path.join(temp_dir, "pickup.wav")
            self._save_wav_file(pickup_path, pickup_data, 22050)
            self.audio_clips['pickup'] = AudioClip(pickup_path, 0.4)
            
            # Level up sesi
            levelup_data = ProceduralAudio.generate_pickup_sound(1.8)
            levelup_path = os.path.join(temp_dir, "levelup.wav")
            self._save_wav_file(levelup_path, levelup_data, 22050)
            self.audio_clips['levelup'] = AudioClip(levelup_path, 0.7)
            
            # Hasar sesi
            damage_data = ProceduralAudio.generate_tone(150.0, 0.1)
            damage_path = os.path.join(temp_dir, "damage.wav")
            self._save_wav_file(damage_path, damage_data, 44100)
            self.audio_clips['damage'] = AudioClip(damage_path, 0.3)
            
            # Ateş sesi
            fire_data = ProceduralAudio.generate_explosion_sound(0.1)
            fire_path = os.path.join(temp_dir, "fire.wav")
            self._save_wav_file(fire_path, fire_data, 22050)
            self.audio_clips['fire'] = AudioClip(fire_path, 0.2)
            
        except Exception as e:
            Logger.error(f"SoundManager: Procedural ses hatası: {e}")
    
    def _save_wav_file(self, file_path: str, audio_data: bytes, sample_rate: int):
        """WAV dosyası kaydet"""
        try:
            import wave
            
            with wave.open(file_path, 'wb') as wav_file:
                wav_file.setnchannels(1)  # Mono
                wav_file.setsampwidth(2)  # 16-bit
                wav_file.setframerate(sample_rate)
                wav_file.writeframes(audio_data)
                
        except Exception as e:
            Logger.error(f"SoundManager: WAV kaydetme hatası: {e}")
    
    def _load_audio_files(self):
        """Ses dosyalarını yükle"""
        # Assets klasöründen ses dosyalarını yükle
        audio_dir = "assets/audio"
        if os.path.exists(audio_dir):
            for filename in os.listdir(audio_dir):
                if filename.endswith(('.wav', '.ogg', '.mp3')):
                    name = os.path.splitext(filename)[0]
                    file_path = os.path.join(audio_dir, filename)
                    self.audio_clips[name] = AudioClip(file_path)
    
    def play_sound(self, sound_name: str, volume: float = 1.0, 
                   position: Optional[Tuple[float, float]] = None):
        """Ses çal"""
        if not self.enabled:
            return
        
        if sound_name not in self.audio_clips:
            Logger.warning(f"SoundManager: Ses bulunamadı: {sound_name}")
            return
        
        # 3D ses hesaplama
        final_volume = volume * self.sfx_volume * self.master_volume
        
        if position:
            distance = self._calculate_distance(position, self.listener_pos)
            if distance > self.max_distance:
                return  # Çok uzak, ses çalma
            
            # Mesafe bazlı ses azalması
            distance_factor = 1.0 - (distance / self.max_distance)
            final_volume *= distance_factor
        
        # Ses havuzundan al veya yeni oluştur
        clip = self.audio_clips[sound_name]
        clip.play(final_volume)
    
    def play_sound_3d(self, sound_name: str, x: float, y: float, volume: float = 1.0):
        """3D pozisyonlu ses çal"""
        self.play_sound(sound_name, volume, (x, y))
    
    def set_listener_position(self, x: float, y: float):
        """Dinleyici pozisyonu ayarla"""
        self.listener_pos = [x, y]
    
    def _calculate_distance(self, pos1: Tuple[float, float], pos2: Tuple[float, float]) -> float:
        """İki nokta arası mesafe"""
        dx = pos1[0] - pos2[0]
        dy = pos1[1] - pos2[1]
        return math.sqrt(dx*dx + dy*dy)
    
    def play_explosion(self, x: float, y: float, intensity: float = 1.0):
        """Patlama sesi çal"""
        volume = 0.6 * intensity
        self.play_sound_3d('explosion', x, y, volume)
    
    def play_pickup(self, x: float, y: float):
        """Pickup sesi çal"""
        self.play_sound_3d('pickup', x, y, 0.4)
    
    def play_level_up(self):
        """Level up sesi çal"""
        self.play_sound('levelup', 0.8)
    
    def play_damage(self, x: float, y: float):
        """Hasar sesi çal"""
        self.play_sound_3d('damage', x, y, 0.5)
    
    def play_fire(self, x: float, y: float):
        """Ateş sesi çal"""
        self.play_sound_3d('fire', x, y, 0.3)
    
    def set_master_volume(self, volume: float):
        """Ana ses seviyesi"""
        self.master_volume = max(0.0, min(1.0, volume))
    
    def set_sfx_volume(self, volume: float):
        """Efekt ses seviyesi"""
        self.sfx_volume = max(0.0, min(1.0, volume))
    
    def set_music_volume(self, volume: float):
        """Müzik ses seviyesi"""
        self.music_volume = max(0.0, min(1.0, volume))
    
    def enable_audio(self, enabled: bool):
        """Ses sistemini aç/kapat"""
        self.enabled = enabled
    
    def stop_all_sounds(self):
        """Tüm sesleri durdur"""
        for clip in self.audio_clips.values():
            clip.stop()
    
    def cleanup(self):
        """Temizlik"""
        self.stop_all_sounds()
        
        # Geçici dosyaları temizle
        import tempfile
        temp_dir = tempfile.gettempdir()
        temp_files = ['explosion.wav', 'pickup.wav', 'levelup.wav', 'damage.wav', 'fire.wav']
        
        for filename in temp_files:
            file_path = os.path.join(temp_dir, filename)
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
            except Exception as e:
                Logger.error(f"SoundManager: Temizlik hatası: {e}")


# Global ses yöneticisi
sound_manager = SoundManager()
