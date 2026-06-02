#!/bin/bash
# Qishloq xo'jaligi roboti - Avtomatik O'rnatish Skripti
# Installation script untuk macOS, Linux, dan Windows (Git Bash)

set -e  # Agar xatolik bo'lsa to'xtamiz

echo "================================"
echo "🌾 Aziz Robo - O'rnatish Skripti"
echo "================================"
echo ""

# 1. Python tekshiramiz
echo "📍 Python tekshirilmoqda..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 topilmadi!"
    echo "Iltimos, Python 3.8+ o'rnating: https://www.python.org/downloads/"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "✅ Python topildi: $PYTHON_VERSION"
echo ""

# 2. Virtual environment yaratamiz (agar mavjud bo'lmasa)
echo "📍 Virtual environment o'rnatilmoqda..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Virtual environment yaratildi"
else
    echo "✅ Virtual environment allaqachon mavjud"
fi
echo ""

# 3. Virtual environment faollashtirish
echo "📍 Virtual environment faollashtirilyapti..."
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
else
    echo "❌ Virtual environment faol qila olmadi"
    exit 1
fi
echo "✅ Virtual environment faol"
echo ""

# 4. Pip yangilaymiz
echo "📍 Pip yangilanmoqda..."
python -m pip install --upgrade pip setuptools wheel > /dev/null 2>&1
echo "✅ Pip yangilandi"
echo ""

# 5. Zависимостиlarni o'rnatamiz
echo "📍 Zависимостиlar o'rnatilmoqda..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
fi
echo "✅ Zависимостиlar o'rnatildi"
echo ""

# 6. Proyektni o'rnatamiz
echo "📍 Proyekt o'rnatilmoqda..."
pip install -e .
echo "✅ Proyekt o'rnatildi"
echo ""

# 7. .zshrc yoki .bashrc ga alias qo'shamiz
if [ -n "$ZSH_VERSION" ] || [ -f "$HOME/.zshrc" ]; then
    # Zsh uchun
    SHELL_CONFIG="$HOME/.zshrc"
    ACTIVATION_CMD="source $(pwd)/venv/bin/activate"
    ALIAS_CMD="alias aziz='source $(pwd)/venv/bin/activate && aziz'"
elif [ -f "$HOME/.bashrc" ]; then
    # Bash uchun
    SHELL_CONFIG="$HOME/.bashrc"
    ACTIVATION_CMD="source $(pwd)/venv/bin/activate"
    ALIAS_CMD="alias aziz='source $(pwd)/venv/bin/activate && aziz'"
fi

if [ -n "$SHELL_CONFIG" ]; then
    if ! grep -q "alias aziz" "$SHELL_CONFIG"; then
        echo "📍 Shell config ga alias qo'shilmoqda..."
        echo "" >> "$SHELL_CONFIG"
        echo "# Aziz Robo" >> "$SHELL_CONFIG"
        echo "$ALIAS_CMD" >> "$SHELL_CONFIG"
        echo "✅ Alias qo'shildi. Iltimos, terminalni qayta ochin:"
        echo "   source $SHELL_CONFIG"
    fi
fi
echo ""

echo "================================"
echo "✅ O'rnatish muvaffaqiyatli!"
echo "================================"
echo ""
echo "📌 Foydalanish:"
echo "   Terminal qayta ochin yoki:"
echo "   source venv/bin/activate"
echo "   aziz"
echo ""
echo "🚀 Boshlash uchun:"
echo "   aziz"
echo ""
