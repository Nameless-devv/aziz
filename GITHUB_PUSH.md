# GitHub-ga Yuborish Ko'rsatmasi

## 1️⃣ GitHub-da Repository Yaratish

1. **GitHub-ga kiramiz:** https://github.com/new
2. **Repository nomi:** `aziz` yoki `aziz-robo`
3. **Tavsifi:** "Qishloq xo'jaligi roboti - Coverage Path Planning"
4. **.gitignore:** Python
5. **License:** MIT (ixtiyoriy)
6. **"Create repository" bosib yaratamiz**

## 2️⃣ Local Reponi GitHub-ga Ulaymiz

GitHub-dan repository yaratilgandan keyin, sizda shunday bir yo'l bo'ladi:
```
https://github.com/YOUR_USERNAME/aziz.git
```

**Terminal-da quyidagi buyruqlarni bajaring:**

```bash
cd /Users/sanjarbek/aziz

# GitHub repository URL-ini o'rnating (YOUR_USERNAME o'rniga haqiqiy username)
git remote add origin https://github.com/YOUR_USERNAME/aziz.git

# Branch nomini main qilamiz
git branch -M main

# Push qilamiz
git push -u origin main
```

## 3️⃣ Tasdiqlanish (agar kerak bo'lsa)

Agar GitHub sizdan tasdiqlanish soraasa:
```bash
# GitHub CLI bilan
gh auth login

# Yoki manual token bilan
# GitHub Settings > Developer settings > Personal access tokens
# Token yaratib, terminal-da kiritish
```

## 4️⃣ Tayyor!

Push tugallangandan keyin, GitHub-dan repository linkini kopyalaymiz:
```
https://github.com/YOUR_USERNAME/aziz
```

Boshqa kompyuterda:
```bash
git clone https://github.com/YOUR_USERNAME/aziz.git
cd aziz
bash install.sh
aziz
```

---

**Keying qadamlar:**
1. Yuqoridagi buyruqlarni terminal-da bajaring
2. GitHub-dan final URL-ni nusxalab beraman
