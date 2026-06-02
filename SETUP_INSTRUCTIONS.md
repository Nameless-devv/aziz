# Loyihani O'rnatish - Setup Instructions

## Birinchi O'rnatish

Proyektni birinchi marta o'rnatish uchun:

```bash
# 1. Proyekt papkasiga kiramiz
cd /path/to/aziz

# 2. O'rnatamiz (dev rejimida)
pip install -e .
```

## Undan Keyin

Keyin terminalda istalgan joydan sodda buyruq yeterli:

```bash
aziz
```

## Boshqa Kompyuterga O'tkazish

1. **Git orqali** (afzalroq):
```bash
git clone <repository-url>
cd aziz
pip install -e .
aziz
```

2. **Zip orqali** (yangi kompyuterda):
```bash
unzip aziz.zip
cd aziz
pip install -e .
aziz
```

## Muammolarni Hal Qilish

### 1. "aziz" buyruq topilmasa
```bash
python -m pip install --upgrade pip
pip install -e .
```

### 2. Kutubxonalar topilmasa
```bash
pip install -r requirements.txt
```

### 3. Python 3 topilmasa
Iltimos, Python 3.8+ o'rnating: https://www.python.org/downloads/

## O'rnatishni Tekshirish

```bash
which aziz          # Yo'li ko'rsatadi
aziz --version      # Versiyani ko'rsatadi
aziz --help         # Yordam beradi
```
