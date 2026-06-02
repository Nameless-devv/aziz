# Qishloq Xo'jaligi Roboti - Interaktiv Dala Planner

## Loyiha haqida

Bu tizim qishloq xo'jaligi robotlari uchun **interaktiv dala va to'siq rejalashtirish** dasturi. Siz grafikli interfeys orqali:

1. 🎨 **Ixtiyoriy shakldagi dala** chizishingiz mumkin
2. 📍 **Turli xil to'siqlarni** (daraxt, tosh, bino, suv) qo'shishingiz mumkin
3. 📏 **To'siq hajmini** slider bilan o'zgartirishingiz mumkin
4. 🤖 **Robot uchun optimal yo'l** rejalashtirish mumkin
5. 📊 **Simulyatsiya** va **vizualizatsiya** ko'rishingiz mumkin

## Tizim Arxitekturasi

```
┌─────────────────────────────────────────────────────────┐
│     QISHLOQ XO'JALIGI ROBOTI - INTERAKTIV PLANNER       │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────────────────────────────────────┐       │
│  │   Interactive Field Planner (GUI)            │       │
│  │   - Maydon chizish                           │       │
│  │   - To'siqlarni qo'shish                     │       │
│  │   - Robot yo'lini rejalashtirish             │       │
│  └──────────────────┬───────────────────────────┘       │
│                     │                                   │
│     ┌───────────────┴───────────────┐                   │
│     ▼                               ▼                   │
│  ┌──────────────────┐    ┌──────────────────────┐       │
│  │  Environment     │    │  Coverage Path      │       │
│  │  Modeling        │◄──►│  Planner            │       │
│  │  - Maydon        │    │  - Boustrophedon    │       │
│  │  - To'siqlar     │    │  - Spiral           │       │
│  └──────────────────┘    └──────────────────────┘       │
│                                                         │
│              Matplotlibda Vizualizatsiya                │
└─────────────────────────────────────────────────────────┘
```

## Modullar

### 1. Environment Modeling Module (`environment_modeling.py`)
- Dala muhitini modellashtiradi
- To'siqlarni turli tiplari: daraxt, tosh, bino, suv, boshqa
- Maydon shakli ixtiyoriy ko'pburchak

### 2. Coverage Planning Module (`coverage_planning.py`)
- **Boustrophedon** algorithm (to'g'ri qatorlar)
- **Spiral** algorithm (spiral yo'l)
- Dala qoplamaning 100% ta'minlashi
- Overlap parametri bilan ajustable

## 🚀 Tezkor O'rnatish

### macOS / Linux:
```bash
git clone https://github.com/Nameless-devv/aziz.git
cd aziz
bash install.sh
aziz
```

### Windows:

**Option 1: Git Bash (Tavsiya etiladi)**
```bash
git clone https://github.com/Nameless-devv/aziz.git
cd aziz
bash install.bat
aziz
```

**Option 2: PowerShell (Administrator sifatida)**
```powershell
git clone https://github.com/Nameless-devv/aziz.git
cd aziz
.\install.ps1
aziz
```

**Option 3: CMD (Administrator sifatida)**
```cmd
git clone https://github.com/Nameless-devv/aziz.git
cd aziz
install.bat
aziz
```

⚠️ **MUHIM:** Python va Git o'rnatilganligi tekshirig: https://www.python.org va https://git-scm.com

## Manual O'rnatish

```bash
# Virtual environment yaratish
python3 -m venv venv

# Faollashtirish (macOS/Linux):
source venv/bin/activate
# Yoki Windows:
# venv\Scripts\activate

# Kutubxonalarni o'rnatish
pip install -e .

# Dasturni ishga tushirish
aziz
```

## Boshqa Kompyuterga O'tkazish

```bash
git clone https://github.com/Nameless-devv/aziz.git
cd aziz
bash install.sh    # macOS/Linux
# Yoki Windows-da: install.bat yoki install.ps1
aziz
```

## Foydalanish

### 1️⃣ **Maydon Yaratish (Maydon rejimi)**
   - Chap klik orqali nuqtalarni birma-bir kiritish
   - **Enter** tugmasini bosish maydonni yakunlash uchun
   - Kamida 3 ta nuqta kerak

### 2️⃣ **To'siqlarni Qo'shish (To'siq rejimi)**
   - **To'siq turi** tanlang: Daraxt, Tosh, Bino, Suv, Boshqa
   - **Slider** bilan to'siq **hajmini** o'zgartiring (1-10 metr)
   - **Chap klik**: Doira shaklida to'siq qo'shish
   - **O'ng klik**: Polygon shaklida to'siq uchun nuqtalar kiritish
   - **Enter**: Polygon to'siqni yakunlash

### 3️⃣ **Boshlang'ich Nuqtani Belgilash (Boshlash rejimi)**
   - Chap klik: Robot uchun boshlang'ich nuqtasini tanlash

### 4️⃣ **Yo'l Rejalashtirish**
   - **Yo'l** tugmasi: Boustrophedon algorithm bilan
   - **Spiral** tugmasi: Spiral yo'l bilan

### 5️⃣ **Simulyatsiya**
   - **SIMULYATSIYA** tugmasini bosing

### 6️⃣ **Saqlash**
   - **Saqlash** tugmasi bilan ma'lumotlarni JSON formatida saqlash

## Talablar

- Python 3.8+
- Barcha kutubxonalar avtomatik o'rnatiladi

## 🚀 Tezkor O'rnatish

### Option 1: Avtomatik O'rnatish (Tavsiya etiladi)

#### macOS / Linux:
```bash
cd /path/to/aziz
bash install.sh
aziz
```

#### Windows (CMD yoki PowerShell):
```cmd
cd C:\path\to\aziz
install.bat
aziz
```

### Option 2: Manual O'rnatish

```bash
# 1. Proyektga kiramiz
cd aziz

# 2. Virtual environment yaratamiz
python3 -m venv venv

# 3. Virtual environment faollashtirish
# macOS/Linux:
source venv/bin/activate
# yoki Windows:
# venv\Scripts\activate

# 4. Paketlarni o'rnatamiz
pip install -e .

# 5. Dasturni boshlash
aziz
```

### Option 3: Git orqali (boshqa kompyuterga)

```bash
git clone <repository-url>
cd aziz
bash install.sh  # yoki Windows uchun: install.bat
aziz
```

## 📋 O'rnatishdan Keyin

Birinchi marta o'rnatgandan keyin:

```bash
# Terminal qayta ochamiz yoki:
source ~/.zshrc  # yoki ~/.bashrc

# Keyin istalgan joydan:
aziz
```

## ❓ Muammolar

### 1. "aziz: command not found"
```bash
source ~/.zshrc  # yoki source ~/.bashrc
aziz
```

### 2. ModuleNotFoundError
```bash
pip install -r requirements.txt
```

### 3. Python topilmasi
Python 3.8+ o'rnating: [python.org](https://www.python.org/downloads/)

## 📦 Kutubxonalar

- NumPy
- Matplotlib
- SciPy
- Shapely
- PyYAML

## Litsenziya

MIT License
