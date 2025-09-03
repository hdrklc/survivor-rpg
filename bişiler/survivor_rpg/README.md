# 🎮 Survivor RPG

Vampire Survivors tarzında 2D survival oyunu. Python ve Kivy ile geliştirilmiştir.

## 🚀 Hızlı Başlangıç

### 1. Gereksinimleri Kurun

```bash
pip install -r requirements.txt
```

### 2. Oyunu Çalıştırın

```bash
cd survivor_rpg
python main.py
```

## 🎯 Oyun Özellikleri

- ⏱️ **10-15 dakikalık** hızlı koşular
- 🎮 **Tek parmak** joystick kontrolü
- 🔫 **Otomatik ateş** sistemi
- 📈 **Level-up** yetenek seçimi
- 💰 **Meta progression** sistemi
- 📱 **Android** desteği

## 🕹️ Kontroller

- **Sol alt çeyrek**: Joystick (hareket)
- **Sağ üst**: Pause butonu
- **Otomatik ateş**: Sürekli aktif

## 🛠️ Geliştirme

### Proje Yapısı

```
survivor_rpg/
├── main.py              # Ana uygulama
├── app.kv               # Kivy UI tanımları
├── core/                # Temel sistemler
│   ├── game.py          # Ana oyun döngüsü
│   ├── state.py         # Oyun durumu
│   └── rng.py           # Rastgele sayı üretici
├── entities/            # Oyun varlıkları
│   ├── player.py        # Oyuncu
│   ├── enemy.py         # Düşmanlar
│   ├── projectile.py    # Mermiler
│   └── loot.py          # Loot sistemleri
├── systems/             # Oyun sistemleri
│   ├── physics.py       # Fizik ve çarpışma
│   ├── spawn.py         # Düşman spawn
│   ├── combat.py        # Savaş sistemi
│   ├── movement.py      # Hareket sistemi
│   └── abilities.py     # Yetenek sistemi
├── ui/                  # Kullanıcı arayüzü
│   ├── hud.py           # Oyun içi HUD
│   ├── levelup.py       # Level-up paneli
│   ├── pause_menu.py    # Pause menüsü
│   └── game_over.py     # Game over ekranı
└── services/            # Servisler
    ├── save.py          # Kayıt sistemi
    └── audio.py         # Ses sistemi
```

### Android Build

```bash
# buildozer.spec dosyasını düzenleyin
buildozer android debug
```

## 🎨 Oyun Mekanikleri

### Yetenekler
- **Çoklu Atış**: Daha fazla mermi
- **Güç Artışı**: Daha fazla hasar
- **Hız Artışı**: Daha hızlı hareket
- **Sağlık Artışı**: Daha fazla HP
- **Manyetik Alan**: Daha geniş loot toplama
- **Hızlı Atış**: Daha hızlı saldırı

### Düşmanlar
- **Slime**: Temel düşman, yavaş
- **Daha fazlası yakında...**

## 📝 Yapılacaklar

- [ ] Daha fazla düşman türü
- [ ] Boss savaşları
- [ ] Ses efektleri
- [ ] Parçacık efektleri
- [ ] Daha fazla yetenek
- [ ] Meta shop sistemi

## 🐛 Bilinen Sorunlar

- Henüz ses sistemi implementasyonu yok
- Grafik optimizasyonları gerekli

## 📄 Lisans

Bu proje eğitim amaçlıdır.
