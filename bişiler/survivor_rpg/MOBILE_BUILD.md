# 📱 Survivor RPG - Mobil APK Oluşturma Rehberi

## 🔧 WSL2 Kurulumu (Windows)

### 1. WSL2'yi Etkinleştir
```powershell
# PowerShell'i yönetici olarak aç ve çalıştır:
wsl --install
# Bilgisayarı yeniden başlat
```

### 2. Ubuntu 22.04 Kur
```powershell
# Microsoft Store'dan "Ubuntu 22.04.3 LTS" indir ve kur
# Veya komut satırından:
wsl --install -d Ubuntu-22.04
```

### 3. Ubuntu'yu Başlat ve Kullanıcı Oluştur
- Ubuntu'yu aç
- Kullanıcı adı ve şifre oluştur

## 🏗️ Buildozer Kurulumu (Ubuntu içinde)

### 1. Sistem Paketlerini Kur
```bash
sudo apt update
sudo apt install -y python3-venv python3-pip git zip openjdk-17-jdk \
  zlib1g-dev libffi-dev libssl-dev autoconf libtool pkg-config cmake
```

### 2. Sanal Ortam Oluştur
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip Cython buildozer
```

### 3. Proje Dosyalarını Kopyala
```bash
# Windows dosyalarını WSL'e kopyala
cp -r /mnt/c/Users/hidir/Desktop/bişiler/survivor_rpg ~/
cd ~/survivor_rpg
```

## 📦 APK Oluşturma

### 1. İlk Derleme (Debug APK)
```bash
# Sanal ortamı aktif et
source .venv/bin/activate

# APK oluştur (ilk kez uzun sürer - Android SDK/NDK indirir)
buildozer -v android debug
```

### 2. APK Dosyasını Bul
```bash
# APK dosyası burada oluşur:
ls -la bin/
# survivorrpg-0.1.0-arm64-v8a-debug.apk
```

### 3. APK'yı Windows'a Kopyala
```bash
# APK'yı Windows masaüstüne kopyala
cp bin/*.apk /mnt/c/Users/hidir/Desktop/
```

## 📱 Telefona Yükleme

### Yöntem 1: USB ile
1. Telefonda "Geliştirici Seçenekleri"ni aç
2. "USB Hata Ayıklama"yı etkinleştir
3. Telefonu USB ile bağla
4. ```bash
   buildozer -v android debug deploy run
   ```

### Yöntem 2: APK Dosyası ile
1. APK dosyasını telefona kopyala (USB, email, vs.)
2. Telefonda "Bilinmeyen Kaynaklardan Yükleme"yi aç
3. APK'ya tıklayarak yükle

## 🔧 Sorun Giderme

### Java Sorunu
```bash
# Java sürümünü kontrol et
java -version
# Eğer Java 17 değilse:
sudo update-alternatives --config java
```

### Buildozer Cache Temizleme
```bash
buildozer android clean
rm -rf .buildozer/
```

### Bellek Sorunu
```bash
# WSL2'ye daha fazla RAM ver
# Windows'ta ~/.wslconfig dosyası oluştur:
[wsl2]
memory=8GB
processors=4
```

## 🚀 Play Store için AAB

AAB (Android App Bundle) oluşturmak için:

```bash
# buildozer.spec dosyasında şu satırı aktif et:
# android.release_artifact = aab

# Release AAB oluştur:
buildozer android release
```

## 📋 Önemli Notlar

- İlk derleme 30-60 dakika sürebilir (Android SDK/NDK indirme)
- APK boyutu ~50-100MB olabilir
- Oyun landscape modda optimize edilmiş
- Android 7.0+ (API 24+) gerekli
- ARM64 ve ARM32 mimarilerini destekler

## 🎮 Test Etme

APK yüklendikten sonra:
- Touch kontrolleri test et
- Level up kartlarının görünürlüğünü kontrol et
- Performansı gözlemle
- Ses efektlerini test et

