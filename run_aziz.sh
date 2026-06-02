#!/bin/bash
# Quick setup script - faqat birinchi marta chalamasdan keyin qayta chalaydigan shortcut

# Agar virtual environment faol bo'lmasa, faollashtir
if [ -z "$VIRTUAL_ENV" ]; then
    source "$(dirname "$0")/venv/bin/activate"
fi

# Robo dasturini ishga tush
python3 -m robo "$@"
