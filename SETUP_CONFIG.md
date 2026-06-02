# Portativ O'rnatish Konfiguratsiyasi

## Loyihaning Nomi
**Aziz Robo** - Qishloq xo'jaligi roboti - Coverage Path Planning

## Versiya
**1.0.0**

## O'rnatish Statusi
✅ **Tugallandi**

### Vaqt va Sana
- O'rnatish sanasi: 2 June 2026
- Python versiyasi: 3.14.3
- Operatsion tizimi: macOS

### O'rnatilgan Komponentlar

#### 1. Paket Boshqaruvi
- ✅ setup.py - Python paket o'rnatish fayli
- ✅ requirements.txt - ZDependencies ro'yxati

#### 2. Virtual Environment
- ✅ venv/ - Izolyalangan Python muhiti
- ✅ 9 asosiy kutubxona o'rnatilgan

#### 3. Entry Points
- ✅ aziz - Asosiy buyruq (robo.py->main())
- ✅ .zshrc - Alias qo'shildi

#### 4. O'rnatish Skriptlari
- ✅ install.sh - macOS/Linux avtomatik o'rnatish
- ✅ install.bat - Windows avtomatik o'rnatish
- ✅ run_aziz.sh - Tez ishga tushirish

#### 5. Dokumentatsiya
- ✅ README.md - Asosiy dokumentatsiya
- ✅ INSTALLATION_COMPLETE.md - O'rnatish tushunutgi
- ✅ SETUP_INSTRUCTIONS.md - Setup talimati
- ✅ SETUP_CONFIG.md - Bu fayl

### O'rnatilgan Kutubxonalar

| Paket | Versiya | Maqsad |
|-------|---------|--------|
| numpy | 2.4.6 | Sonli hisob-kitoblar |
| scipy | 1.17.1 | Ilmiy hisob-kitoblar |
| matplotlib | 3.10.9 | Grafik chizish |
| pandas | 3.0.3 | Ma'lumot bilan ishlash |
| pygame | 2.6.1 | Grafiklar va interaksiya |
| pillow | 12.2.0 | Rastrli tasvirlar |
| shapely | 2.1.2 | Geometrik operatsiyalar |
| pyyaml | 6.0.3 | YAML konfiguratsiya |
| pytest | 9.0.3 | Testlarni ishga tushirish |

### Boshqa Kompyuterga O'tkazish

**Git orqali (afzalroq):**
```bash
git clone <repo-url>
cd aziz
bash install.sh  # yoki install.bat
aziz
```

**Zip orqali:**
```bash
zip -r aziz.zip aziz -x "aziz/venv/*"
# (Boshqa kompyuterda)
unzip aziz.zip
cd aziz
bash install.sh
aziz
```

### Tekshirish Buyrughlari

```bash
# O'rnatish to'g'riligini tekshirish
which aziz
aziz --version  # agar mavjud bo'lsa

# Virtual environment
source venv/bin/activate
python3 -c "import robo; print('OK')"

# Kutubxonalar
pip list

# Testlar
pytest tests/
```

### Muammolarni Tekshirish

```bash
# Agar "aziz: command not found" bo'lsa
source ~/.zshrc

# Agar kutubxonalar topilmasa
cd aziz
source venv/bin/activate
pip install -r requirements.txt

# Virtual environment qayta yaratish
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

### Git-da Qo'shish

```bash
# venv va kesh fayllarini ignore qilish
git add .gitignore

# Barcha fayllarni qo'shish (venv-dan tashqari)
git add .
git commit -m "Portativ o'rnatish qo'shildi"
git push
```

### Keyingi Qadamlar

1. **Loyiha o'zgartirilsa:**
   - `requirements.txt` ni yangilaymiz
   - `pip install -r requirements.txt` chalaymiz

2. **Boshqa talabalar bo'lsa:**
   - Yangi kutubxonalarni `pip install` qilamiz
   - `pip freeze > requirements.txt` chalaymiz

3. **Versiya yangilanishi:**
   - `setup.py` dagi versiyani o'zgartiramiz
   - Git tagni qo'shamiz

---

**Barcha narsalar tayyor!** 🎉  
Loyiha endi **istalgan terminalda `aziz` bilan** ishga tushadigan qilib o'rnatildi.
