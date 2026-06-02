# 🌾 Aziz Robo - Portativ O'rnatish Ko'rsatmasi

## ✅ Boshlandi!

Sizning proyektiniz endi **istalgan terminaldagi `aziz` buyrug'i** bilan ishga tushadigan qilib o'rnatildi!

## 🚀 Birinchi Foydalanish

### 1️⃣ Hozirgi Kompyuterda

```bash
# Virtual environment faollashtiring (birinchi marta)
source ~/.zshrc

# Keyin istalgan joydan:
aziz
```

### 2️⃣ Boshqa Kompyuterga O'tkazish

#### Variant A: Git orqali (tavsiya etiladi)
```bash
# Source kodni clone qiling
git clone <repository-url>
cd aziz

# Avtomatik o'rnatamiz
bash install.sh  # macOS/Linux
install.bat      # Windows

# Dasturni ishga tushiramiz
aziz
```

#### Variant B: Zip orqali
```bash
# Loyihani zip qilamiz va o'tkazamiz
zip -r aziz.zip aziz -x "aziz/venv/*" "aziz/.venv/*" "aziz/__pycache__/*"

# Boshqa kompyuterda
unzip aziz.zip
cd aziz
bash install.sh  # yoki install.bat Windows uchun
aziz
```

## 📦 O'rnatilgan Narsalar

✅ **Virtual Environment** - Python zDependencies izolyatsiyalangan  
✅ **Setup.py** - Paket boshqaruvi  
✅ **Entry Point** - `aziz` bumarag'i  
✅ **install.sh** - macOS/Linux avtomatik o'rnatish  
✅ **install.bat** - Windows avtomatik o'rnatish  
✅ **Shell Alias** - `.zshrc`/`.bashrc`ga alias qo'shildi  

## 🔧 O'rnatilgan Kutubxonalar

```
numpy >= 1.21.0
scipy >= 1.7.0
matplotlib >= 3.4.0
pygame >= 2.1.0
pillow >= 8.0.0
pandas >= 1.3.0
shapely >= 1.8.0
pyyaml >= 5.4.0
pytest >= 6.0.0
```

## ❓ Muammolar va Yechimlari

### 🔴 "aziz: command not found"

**Yechim:**
```bash
# Terminal qayta ochamiz (eslatib xabar)
source ~/.zshrc    # macOS/Linux Zsh uchun
# yoki
source ~/.bashrc   # Linux Bash uchun
```

### 🔴 "ModuleNotFoundError: No module named 'numpy'"

**Yechim:**
```bash
cd /path/to/aziz
source venv/bin/activate
pip install -r requirements.txt
```

### 🔴 "Python3 topilmadi"

**Yechim:**  
Python 3.8+ o'rnating: https://www.python.org/downloads/

### 🔴 Virtual environment faolashmadi

**Yechim:**
```bash
cd /path/to/aziz
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

## 📁 Proyekt Strukturasi

```
aziz/
├── venv/                      # Virtual environment (git-da yo'q)
├── setup.py                   # Paket o'rnatish fayli
├── requirements.txt           # Python dependencies
├── robo.py                    # Asosiy dastur
├── install.sh                 # macOS/Linux o'rnatish
├── install.bat                # Windows o'rnatish
├── SETUP_INSTRUCTIONS.md      # Sizning bu ko'rsatma
├── README.md                  # Proyekt haqida
├── config/                    # Konfiguratsiya
├── src/                       # Source kodlar
├── tests/                     # Testlar
└── diplom/                    # Diplom materiallari
```

## 🔄 Git'da Ishlarni Sохранить

```bash
# Virtual environment va cache fayllarni ignore qilish
git add .gitignore
git add .

# Faqat source kodni commit qilish
git commit -m "Portativ o'rnatish qo'shildi"
git push
```

## 💡 Ba'zi Maslahatlar

1. **Virtual environment bilan ishlang** - Bu zamanasidan o'ta yo'q
2. **Zависимостиlarni yangilanturmaydi** - requirements.txt dan o'zgartirib qayta chiqaring
3. **Boshqa kompyuterga berish** - `venv/` papkasi kerak emas
4. **Source kodni backup qiling** - Git yoki Zip sifatida

## 📞 Yana Savollar?

Agar loyihada muammolar bo'lsa:

```bash
# Tekshiring:
cd /path/to/aziz
source venv/bin/activate
python3 -c "import robo; print('OK')"

# Logni ko'ring:
pip list
which aziz
```

---

✨ **Tayyor!** Endi sizning loyihangiz istalgan terminalda `aziz` bilan ishga tushadigan qilib o'rnatildi!

🎉 Muvaffaqiyotlar!
