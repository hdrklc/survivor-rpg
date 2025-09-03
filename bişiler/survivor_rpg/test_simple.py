#!/usr/bin/env python3
"""
Basit test versiyonu
"""

from kivy.app import App
from kivy.uix.label import Label
from kivy.logger import Logger

class TestApp(App):
    def build(self):
        Logger.info("Test: Uygulama başlatılıyor...")
        return Label(text='Test - Oyun Çalışıyor!', font_size='20sp')

if __name__ == '__main__':
    try:
        TestApp().run()
    except Exception as e:
        print(f"Hata: {e}")
        import traceback
        traceback.print_exc()
