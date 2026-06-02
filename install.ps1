# Qishloq xo'jaligi roboti - Windows PowerShell O'rnatish Skripti
# Foydalanish: .\install.ps1

param(
    [switch]$SkipPython = $false
)

Write-Host "╔════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  🌾 Aziz Robo - PowerShell O'rnatish Skripti           ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# 1. Python tekshirish
Write-Host "📍 Python tekshirilmoqda..." -ForegroundColor Yellow
$pythonPath = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonPath) {
    Write-Host "❌ Python topilmadi!" -ForegroundColor Red
    Write-Host "Iltimos, Python 3.8+ o'rnating: https://www.python.org/downloads/" -ForegroundColor Red
    Write-Host "MUHIM: Setup-da 'Add Python to PATH' ustun qilish kerak!" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

$pythonVersion = & python --version 2>&1
Write-Host "✅ Python topildi: $pythonVersion" -ForegroundColor Green
Write-Host ""

# 2. Virtual environment yaratamiz
Write-Host "📍 Virtual environment o'rnatilmoqda..." -ForegroundColor Yellow
if (-not (Test-Path "venv")) {
    & python -m venv venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Virtual environment yaratib bo'lmadi!" -ForegroundColor Red
        exit 1
    }
    Write-Host "✅ Virtual environment yaratildi" -ForegroundColor Green
} else {
    Write-Host "✅ Virtual environment allaqachon mavjud" -ForegroundColor Green
}
Write-Host ""

# 3. Virtual environment faollashtirish
Write-Host "📍 Virtual environment faollashtirilyapti..." -ForegroundColor Yellow
$activateScript = ".\venv\Scripts\Activate.ps1"
if (-not (Test-Path $activateScript)) {
    Write-Host "❌ Virtual environment faol qila olmadi" -ForegroundColor Red
    exit 1
}

# PowerShell execution policy tekshirish
$policy = Get-ExecutionPolicy -Scope CurrentUser
if ($policy -eq "Restricted") {
    Write-Host "⚠️  Execution policy restricted, o'zgartirish..." -ForegroundColor Yellow
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
}

& $activateScript
Write-Host "✅ Virtual environment faol" -ForegroundColor Green
Write-Host ""

# 4. Pip yangilaymiz
Write-Host "📍 Pip yangilanmoqda..." -ForegroundColor Yellow
& python -m pip install --upgrade pip setuptools wheel | Out-Null
Write-Host "✅ Pip yangilandi" -ForegroundColor Green
Write-Host ""

# 5. Zависимостиlarni o'rnatamiz
Write-Host "📍 Zависимостиlar o'rnatilmoqda..." -ForegroundColor Yellow
if (Test-Path "requirements.txt") {
    & pip install -r requirements.txt
    Write-Host "✅ Zависимостilar o'rnatildi" -ForegroundColor Green
} else {
    Write-Host "⚠️  requirements.txt topilmadi" -ForegroundColor Yellow
}
Write-Host ""

# 6. Proyektni o'rnatamiz
Write-Host "📍 Proyekt o'rnatilmoqda..." -ForegroundColor Yellow
& pip install -e .
Write-Host "✅ Proyekt o'rnatildi" -ForegroundColor Green
Write-Host ""

Write-Host "╔════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║  ✅ O'rnatish muvaffaqiyatli!                          ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""
Write-Host "🚀 Dasturni ishga tushirish uchun:" -ForegroundColor Cyan
Write-Host "   aziz" -ForegroundColor Yellow
Write-Host ""
