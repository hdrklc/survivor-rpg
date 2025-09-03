# Survivor RPG - WSL2 ve Ubuntu Kurulum Script'i
# PowerShell'i yönetici olarak çalıştırın!

Write-Host "🎮 Survivor RPG - WSL2 Kurulum" -ForegroundColor Cyan
Write-Host "===============================" -ForegroundColor Cyan

# WSL2 kurulu mu kontrol et
$wslStatus = wsl --status 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "📦 WSL2 kuruluyor..." -ForegroundColor Yellow
    wsl --install
    Write-Host "⚠️  Bilgisayarınızı yeniden başlatın ve bu script'i tekrar çalıştırın!" -ForegroundColor Red
    pause
    exit
}

# Ubuntu kurulu mu kontrol et
$ubuntuCheck = wsl -l -v | Select-String "Ubuntu"
if (-not $ubuntuCheck) {
    Write-Host "🐧 Ubuntu 22.04 kuruluyor..." -ForegroundColor Yellow
    wsl --install -d Ubuntu-22.04
}

Write-Host "✅ WSL2 ve Ubuntu hazır!" -ForegroundColor Green

# Proje dosyalarını WSL'e kopyala
Write-Host "📁 Proje dosyaları WSL'e kopyalanıyor..." -ForegroundColor Blue
$currentPath = Get-Location
wsl -d Ubuntu-22.04 -- bash -c "mkdir -p ~/survivor_rpg"
wsl -d Ubuntu-22.04 -- bash -c "cp -r /mnt/c/Users/$env:USERNAME/Desktop/bişiler/survivor_rpg/* ~/survivor_rpg/"

Write-Host "🏗️  Buildozer kurulumu başlatılıyor..." -ForegroundColor Blue
wsl -d Ubuntu-22.04 -- bash -c "cd ~/survivor_rpg && chmod +x build_mobile.sh && ./build_mobile.sh"

Write-Host "🎉 Kurulum tamamlandı!" -ForegroundColor Green
Write-Host "APK dosyası WSL içinde ~/survivor_rpg/bin/ klasöründe oluştu" -ForegroundColor Cyan

# APK'yı Windows'a kopyala
Write-Host "📱 APK Windows masaüstüne kopyalanıyor..." -ForegroundColor Blue
wsl -d Ubuntu-22.04 -- bash -c "cp ~/survivor_rpg/bin/*.apk /mnt/c/Users/$env:USERNAME/Desktop/ 2>/dev/null || echo 'APK henüz oluşmadı'"

Write-Host "✅ İşlem tamamlandı! APK dosyası masaüstünde" -ForegroundColor Green

