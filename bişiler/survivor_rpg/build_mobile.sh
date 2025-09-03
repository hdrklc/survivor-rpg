#!/bin/bash
# Survivor RPG - Mobil APK Build Script

echo "🎮 Survivor RPG - Mobil APK Oluşturma"
echo "====================================="

# Renk kodları
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Hata durumunda çık
set -e

echo -e "${BLUE}📦 Sistem paketleri kontrol ediliyor...${NC}"

# Gerekli paketleri kontrol et
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 bulunamadı. Lütfen kurun.${NC}"
    exit 1
fi

if ! command -v java &> /dev/null; then
    echo -e "${YELLOW}⚠️  Java bulunamadı. Kurulum yapılıyor...${NC}"
    sudo apt update
    sudo apt install -y openjdk-17-jdk
fi

echo -e "${GREEN}✅ Sistem paketleri hazır${NC}"

# Sanal ortam oluştur
echo -e "${BLUE}🔧 Sanal ortam hazırlanıyor...${NC}"

if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    echo -e "${GREEN}✅ Sanal ortam oluşturuldu${NC}"
else
    echo -e "${YELLOW}⚠️  Sanal ortam zaten mevcut${NC}"
fi

# Sanal ortamı aktif et
source .venv/bin/activate

# Buildozer kurulumu
echo -e "${BLUE}🏗️  Buildozer kuruluyor...${NC}"
pip install --upgrade pip
pip install Cython==0.29.33
pip install buildozer

echo -e "${GREEN}✅ Buildozer kuruldu${NC}"

# Buildozer spec kontrolü
if [ ! -f "buildozer.spec" ]; then
    echo -e "${RED}❌ buildozer.spec dosyası bulunamadı!${NC}"
    exit 1
fi

echo -e "${BLUE}🔨 APK oluşturuluyor... (Bu işlem uzun sürebilir)${NC}"

# APK oluştur
buildozer -v android debug

if [ $? -eq 0 ]; then
    echo -e "${GREEN}🎉 APK başarıyla oluşturuldu!${NC}"
    echo -e "${GREEN}📁 APK konumu: $(pwd)/bin/${NC}"
    ls -la bin/*.apk
    
    echo -e "${BLUE}📱 Telefona yüklemek için:${NC}"
    echo "1. USB ile: buildozer android debug deploy run"
    echo "2. Manuel: APK dosyasını telefona kopyala ve yükle"
    
else
    echo -e "${RED}❌ APK oluşturma başarısız!${NC}"
    exit 1
fi

