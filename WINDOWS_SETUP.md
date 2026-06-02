# 🪟 Windows-da O'rnatish - Qadamlar

## ❌ Muammo
Windows-da git va bash topilmayapti

## ✅ Yechim

### Option 1: Git Bash Orqali (TAVSIYA ETILADI)

**1. Git o'rnatish:**
- Brauzerdan: https://git-scm.com/download/win
- Download qilamiz va o'rnatamiz (DEFAULT sozlamalar)

**2. Git Bash ochamiz:**
- Start Menu-dan "Git Bash" izlash va ochish
- Yoki: File Explorer-da folder ochamiz, o'ngdan click → "Open Git Bash here"

**3. Terminal-da quyidagi buyruqlarni yozamiz:**

```bash
git clone https://github.com/Nameless-devv/aziz.git
cd aziz
bash install.bat
aziz
```

**Bu shunday ishlaydi:**
- ✅ Git clone ishlaydi
- ✅ install.bat bash orqali chalaydigan bo'ladi
- ✅ Virtual environment yaratiladi
- ✅ Barcha kutubxonalar o'rnatiladi
- ✅ aziz buyrug'i tayyor bo'ladi

---

### Option 2: CMD (Command Prompt) Orqali

**1. Agar git o'rnatilgan bo'lsa:**

```cmd
git clone https://github.com/Nameless-devv/aziz.git
cd aziz
install.bat
aziz
```

**2. Agar git topilmasa:**
- Python o'rnatish kerak: https://www.python.org
- Git o'rnatish kerak: https://git-scm.com

---

### Option 3: PowerShell Orqali

```powershell
git clone https://github.com/Nameless-devv/aziz.git
cd aziz
.\install.bat
aziz
```

---

## 📋 Windows Setup Checklist

- [ ] Python 3.8+ o'rnatilgan (https://www.python.org)
- [ ] Git o'rnatilgan (https://git-scm.com)
- [ ] Git Bash orqali `bash install.bat` yoki `install.bat` CMD-da chalaydim
- [ ] Terminal qayta ochdim
- [ ] `aziz` buyrug'i tayyor

---

## 🚀 Windows-da FINAL BUYRUQLAR:

**Git Bash-da:**
```bash
git clone https://github.com/Nameless-devv/aziz.git
cd aziz
bash install.bat
aziz
```

**CMD-da:**
```cmd
git clone https://github.com/Nameless-devv/aziz.git
cd aziz
install.bat
aziz
```

---

## ❓ Agar hali xatoliklar bo'lsa:

### "git topilmadi"
→ Git o'rnating: https://git-scm.com/download/win

### "python topilmadi"
→ Python o'rnating: https://www.python.org (PATH-ga qo'shish flag-ini yo'qlamang)

### "install.bat topilmadi"
→ `cd aziz` ichida ekanligingizni tekshiring

---

## 💡 Tavsiya

**Windows uchun BEST approach:**
1. Git o'rnating
2. **Git Bash ochasiz** (terminal sifatida)
3. `bash install.bat` chalamasiz
4. `aziz` chalamasiz

Bu eng oson va ishonchli usul!
