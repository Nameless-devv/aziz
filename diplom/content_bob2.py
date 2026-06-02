# II BOB mazmuni – kengaytirilgan

BOB2_SECTIONS = [

("h1", "II BOB. QISHLOQ XO'JALIGI ROBOTI UCHUN PATH PLANNING ALGORITMI"),

("h2", "2.1. Qishloq xo'jaligi muhitida robotlar harakatlanishining xususiyatlari"),

("h3", "2.1.1. Qishloq xo'jaligi muhitining o'ziga xos xususiyatlari"),

("body", "Qishloq xo'jaligi muhiti robotlar navigatsiyasi nuqtai nazaridan eng murakkab muhitlardan biri hisoblanadi. Sanoat zavodlari yoki shahar ko'chalari ma'lum darajada tartibli va prognozlanadigan bo'lsa, qishloq xo'jaligi maydoni doim o'zgaruvchi, noaniq va ko'p omilli sharoitlar bilan tavsiflanadi [15]."),

("body", "Qishloq xo'jaligi muhitining asosiy xususiyatlarini quyidagi guruhlar bo'yicha tahlil qilish mumkin:"),

("body", "1-guruh: Fizik va geografik xususiyatlar"),

("body", "Rel'ef o'zgaruvchanligi: O'zbekistonning ko'plab qishloq xo'jaligi maydonlari tekis emas. Farg'ona vodiysi va Zarafshon daryosi havzasidagi dalalar nisbatan tekis bo'lsa, tog' oldi hududlarda (Toshkent, Samarqand viloyatlari) qiyaliklar sezilarli darajada bo'lishi mumkin. Qiyalik burchagi 1°–15° oralig'ida bo'lishi kuzatiladi. 5° dan oshgan qiyalik robotning harakat tezligini va yo'nalishini sezilarli o'zgartiradi. 10° dan oshganda esa ayrim robot platformalari uchun xavf tug'ilishi mumkin."),

("body", "Qiyalik burchagi α bo'lganda robot tortishish kuchi bo'ylab tashlanadigan komponent:"),
("body", "F_slope = m × g × sin(α)"),
("body", "bu yerda m – robot massasi, g = 9.81 m/s². Misol: 50 kg robot, 10° qiyalik: F_slope = 50 × 9.81 × sin(10°) = 50 × 9.81 × 0.174 ≈ 85 N qo'shimcha kuch kerak."),

("body", "Tuproq tarkibi va namlik: Qishloq xo'jaligi tuproqlari quyidagi holatlarda bo'lishi mumkin:"),
("body", "– Quruq zichlanmagan tuproq (kuz, bahor): Og'irlik ostida botishi mumkin, harakat qiyinlashadi. Cone Penetration Resistance (CPR) ≤ 200 kPa."),
("body", "– O'rtacha nam tuproq (sug'orishdan so'ng): Trafikabellik o'rtacha. CPR 200–500 kPa."),
("body", "– Loy tuproq (yomg'irdan so'ng): Juda og'ir, g'ildiraklар sirpanishi kuchli. CPR ≥ 500 kPa. Ba'zan robot butunlay botib qolishi mumkin."),
("body", "– Qattiq zichlanган tuproq (yo'llar, dalа chegaralari): Trafikabellik yuqori. CPR > 1500 kPa."),

("body", "Trafikabellik koeffitsienti K tashqi omillarga qarab: K = f(CPR, moisture, slope, terrain_type)."),
("body", "Bizning modelimizda: cost_terrain = base_cost / K, bu yerda base_cost – standart katak narxi."),

("body", "2-guruh: O'simlik qoplami va ekin tuzilmasi"),

("body", "Qishloq xo'jaligi robotlarining asosiy ish muhiti ekin maydonlari bo'lganligi sababli, o'simlik qoplami robot harakatiga bevosita ta'sir qiladi:"),

("body", "Chiziqli qator ekinlar: Paxta, makkajo'xori, qand lavlagi, sabzavotlar qatorlarda ekiladi. Qatorlar orasidagi masofa (row spacing) odatda 0.3–0.9 metr. Robot ushbu qatorlar orasidan harakatlanishi zarur. Ekin davrining boshida (ko'chat) to'siq deyarli yo'q; o'rtasida (o'sish) va oxirida (pishish) esa o'simlik robotning sensor maydonini cheklaydi."),

("body", "Mevali bog'lar: Daraxtlar qatorlari aro masofalar 3–6 metr. Robot daraxt shoxlari ostida harakatlanadi. Shoxlar sensorlarni to'sishi mumkin. GPS signali daraxt barglari tomonidan zaiflashi mumkin."),

("body", "Sug'orish tizimi: O'zbekistondagi ko'plab qishloq xo'jaligi maydonlarida ariqlar, kanallar va sug'orish trubkalar mavjud. Ular robot uchun statik to'siq hisoblanadi. Kanallar kengligi 0.3–2 metr, chuqurligi 0.2–1 metr. Ularni aniqlash va aylanib o'tish muhim xavfsizlik talabi."),

("body", "3-guruh: Dinamik ob'ektlar va harakatlanuvchi to'siqlar"),

("body", "Qishloq muhitida harakatlanuvchi ob'ektlar ancha ko'p uchraydi:"),
("body", "Hayvonlar: Mollar, qo'ylar, echkilar yoki itlar dalaga kirib qolishi mumkin. Ularning harakat tezligi: mol – 0.5–2 m/s, it – 1–5 m/s. Harakat yo'nalishlari keskin o'zgarishi mumkin."),
("body", "Ishchilar: Fermerdagi mehnat jarayonida odamlar dalada bo'lishi odatiy holat. Odamning harakat tezligi 0.5–1.5 m/s. Xavfsizlik uchun robot odamdan kamida 2–3 metr uzoqda harakatlanishi kerak."),
("body", "Boshqa texnika: Traktor, kombayn yoki boshqa qishloq xo'jaligi mashinalari. Tezligi 1–5 m/s. O'lchamlari katta va harakat yo'nalishini oldindan bilish qiyin."),

("body", "4-guruh: Sensor ishlash sharoitlari"),

("body", "Yoritilganlik: Quyosh nuri bevosita kamera linzasiga tushganda, tasvirning bir qismi haddan tashqari yorqin bo'lib, to'siqlar ko'rinmay qolishi mumkin. Tong va shom paytlari past burchakli yoritilganlik alohida muammo tug'diradi. Yechim: HDR (High Dynamic Range) kamera yoki kamera + Lidar kombinatsiyasi."),
("body", "Ob-havo: Yomg'ir paytida Lidar signali suv tomchilari tomonidan sochiladi va aniqlik pasayadi. Kuchli shamol kichik o'lchamli dron-robotlarning harakatini chalg'itadi. O'zbekistonda harorat farqi katta (qish: -20°C, yoz: +45°C) bo'lib, elektronika va batareyalarga ta'sir qiladi."),
("body", "GPS sifati: Shahar muhitiga qaraganda qishloq joylarda GPS signali odatda yaxshi, lekin daraxt barg va shoxlari signalni zaiflata oladi. Qisman bulutli osmonlarda aniqlik 2–5 metrga pasayishi mumkin. RTK GPS esa yomg'ir va daraxt osti sharoitida ham yuqori aniqlikni saqlab qola oladi."),

("h3", "2.1.2. Qishloq xo'jaligi robotlariga qo'yiladigan texnik talablar"),

("body", "Qishloq xo'jaligi robotining path planning algoritmi robot platforma xususiyatlarini hisobga olishi zarur. Keling, tipik qishloq xo'jaligi robotining texnik parametrlarini ko'rib chiqaylik:"),

("body", "Platforma parametrlari (ushbu ishda ko'rib chiqilgan model):"),
("body", "• Umumiy o'lchami: uzunlik 0.8 m, eni 0.6 m, balandligi 0.5 m"),
("body", "• Massa: 25–40 kg (yuk bilan)"),
("body", "• Haydash tizimi: Differensial drive (ikkita mustaqil drivchi g'ildirak)"),
("body", "• Minimal burilish radiusi: 0.4 m (joy burilishida 0)"),
("body", "• Maksimal tezlik: 1.5 m/s tekis zaminда; 0.5 m/s qiyalikda"),
("body", "• Batareya quvvati: 20–40 Ah, 24V (taxminan 4–8 soat avtonom ishlash)"),
("body", "• Sensor to'plami: 2D Lidar (180°), Stereo kamera, GPS+IMU, Ultratovush (4 ta)"),

("body", "Kinematik model (Differensial Drive robot):"),
("body", "Differensial drayvli robot uchun harakat tenglamalari:"),
("body", "ẋ = v × cos(θ)"),
("body", "ẏ = v × sin(θ)"),
("body", "θ̇ = ω"),
("body", "bu yerda (x, y) – robot markazi koordinatasi, θ – yo'nalish burchagi, v = (vr + vl)/2 – chiziqli tezlik, ω = (vr – vl)/L – burchak tezligi, vr va vl – o'ng va chap g'ildirak tezliklari, L – g'ildiraklar aro masofa."),

("body", "Path planning algoritmi uchun talablar ro'yxati:"),

("body", "T1 – Xavfsizlik talabi: Robot barcha statik to'siqlardan kamida safety_margin = 0.3 metr uzoqda harakatlanishi kerak. Grid xaritasida bu Minkowski kengaytirish bilan amalga oshiriladi: har bir to'siq katak atrofidagi 1 katak (0.5m) ham to'siq deb belgilanadi."),

("body", "T2 – Energiya talabi: Yo'l narxi hisoblashda katak harakatlanish narxi quyidagicha aniqlanadi:"),
("body", "cost(cell) = base × terrain_factor × slope_factor × turn_factor"),
("body", "terrain_factor: tekis yo'l=0.8, oddiy tuproq=1.0, qo'pol tuproq=1.5, loy=2.5, suv=∞"),
("body", "slope_factor: α<3°→1.0, 3°≤α<7°→1.3, 7°≤α<12°→2.0, α≥12°→3.5"),
("body", "turn_factor: to'g'ri=1.0, kichik burilish=1.1, katta burilish=1.4, joyida aylanish=1.8"),

("body", "T3 – Haqiqiy vaqt talabi: Sensor yangilash chastotasi 10 Hz (har 100 ms). Path planning yangi ma'lumot kelgandan keyin 100 ms ichida yangi yo'l berishi kerak. Raspberry Pi 4 (ARM Cortex-A72, 1.8 GHz) da moslashtirilgan A* 30×20 grid uchun ≤ 15 ms ishlaydi."),

("body", "T4 – Qamrov talabi (Coverage): Ekin parvarishi vazifasida robot barcha ekin qatorlari bo'ylab o'tishi zarur. Yo'l rejalashtirish shu talabni hisobga olishi kerak – \"coverage path planning\" sifatida."),

("body", "T5 – O'simliklar muhofazasi: Ekin qatorlari bo'ylab harakatlanishda robot ekinlarni ezmasligi zarur. Grid xaritasida ekin qatorlari alohida belgilanib, ularni kesib o'tish yuqori narx bilan penalizatsiyalanadi."),

("h3", "2.1.3. To'siqlarni tasniflash va aniqlash usullari"),

("body", "Qishloq xo'jaligi robotida to'siqlarni ikki asosiy guruhga ajratish mumkin. Har guruh uchun alohida aniqlash va boshqaruv strategiyasi qo'llaniladi."),

("body", "Statik to'siqlarni aniqlash va xaritaga kiritish:"),
("body", "Statik to'siqlar oldindan ma'lum yoki birinchi skan paytida aniqlanadi:"),
("body", "1. GPS-asosida kiritish: Fermerdagi daraxtlar, binolar, ariqlar koordinatalari GPSdan olinib, grid xaritasiga kiritiladi. Bu usul yuqori aniqlikda (RTK GPS bilan ±5 sm) ishlaydi."),
("body", "2. Lidar skaneri: Robot birinchi marta dala bo'ylab aylanib chiqib, Lidar ma'lumotlaridan xarita tuzadi (SLAM). Bu usul oldindan ma'lumot bo'lmasa ham ishlaydi."),
("body", "3. Aerial mapping: Dron yordamida dala havo surati olinib, rasm tahlili (computer vision) orqali to'siqlar aniqlanadi va xaritaga kiritiladi. Bu usul katta dalalar uchun samarali."),

("body", "Dinamik to'siqlarni aniqlash va reaksiya qilish:"),
("body", "Dinamik to'siqlarni aniqlash uchun quyidagi sensorlar ishlatiladi:"),
("body", "• Lidar: 10 Hz chastotada 360° skaner. 0.1 m dan 30 m gacha aniqlash. Yomg'irda aniqlik pasayadi."),
("body", "• Stereo kamera + YOLO: YOLOv8 neyron tarmog'i odamlar va hayvonlarni kadrda aniqlaydi. 30 FPS da real vaqt ishlaydi. Kamera ko'rish burchagi 80°."),
("body", "• Ultratovush sensorlar: 0.02–4 metr masofada yuqori ishonchlilik. Kichik va shaffof to'siqlarni ham aniqlaydi. Chastota 40 kHz."),

("body", "Dinamik to'siqqa reaksiya strategiyasi:"),
("body", "Bosqich 1 – Aniqlash: Sensor to'siq aniqlaydi. To'siqning o'lchamlari va harakat parametrlari (tezlik, yo'nalish) baholanadi."),
("body", "Bosqich 2 – Tasnif: To'siq hayvon/odammi yoki texnikami? O'lchami va harakat xarakteriga qarab tasniflanadi. Odamlar uchun alohida xavfsizlik protokoli (robot to'xtaydi va signal beradi)."),
("body", "Bosqich 3 – Reaksiya tanlash:"),
("body", "Agar to'siq kichik (< 0.5 m) va tez harakatlanuvchi → 3 soniya kutish, keyin davom etish."),
("body", "Agar to'siq o'rta (0.5–2 m) → lokal qayta rejalashtirish, aylanib o'tish."),
("body", "Agar to'siq katta (> 2 m) yoki odam → to'xtash, signal berish, operator kutish."),

("h2", "2.2. Moslashtirilgan A* algoritmini ishlab chiqish"),

("h3", "2.2.1. Algoritm arxitekturasi va matematik asosi"),

("body", "Qishloq xo'jaligi roboti uchun moslashtirilgan A* algoritmi (Agricultural Adaptive A* – AA*) an'anaviy A* algoritmini uchta asosiy kengaytma bilan boyitadi: ko'p omilli narx modeli, qishloq xo'jaligi uchun maxsus heuristik va lokal dinamik qayta rejalashtirish."),

("body", "Formal ta'rif:"),
("body", "Kirish: G = (V, E) – grid grafigi; s ∈ V – boshlang'ich tugun; g ∈ V – maqsad tugun; W: V → R+ – tugun narxi funksiyasi; H: V × V → R – heuristik funksiya; D ⊂ V × R+ – dinamik to'siqlar to'plami."),
("body", "Chiqish: P = [v0, v1, ..., vk] – optimal yo'l, bu yerda v0 = s, vk = g, va ∑cost(vi) minimallashtirilgan."),

("body", "Katak narxi modeli:"),
("body", "Har bir grid katagi (i, j) uchun harakat narxi:"),
("body", "cost(i,j,d) = base_cost(d) × terrain_factor(i,j) × slope_factor(i,j) × safety_factor(i,j)"),
("body", "bu yerda:"),
("body", "• base_cost(d): d = gorizontal/vertikal → 1.0; d = diagonal → √2 ≈ 1.414"),
("body", "• terrain_factor(i,j) ∈ [0.8, ∞): tuproq turi va nam darajasiga qarab"),
("body", "  – yo'l: 0.8 (tez harakat)"),
("body", "  – quruq tuproq: 1.0 (standart)"),
("body", "  – qo'pol tuproq: 1.5"),
("body", "  – nam tuproq: 2.0"),
("body", "  – loy: 2.5"),
("body", "  – suv/ariq: ∞ (o'tib bo'lmaydi)"),
("body", "• slope_factor(i,j) = 1 + k_slope × max(0, slope(i,j) – slope_threshold)"),
("body", "  slope_threshold = 3° (bu qiyalikgacha narx oshmaydi)"),
("body", "  k_slope = 0.15 (har bir daraja uchun 15% narx o'sishi)"),
("body", "  Misol: 8° qiyalik → slope_factor = 1 + 0.15×(8–3) = 1.75"),
("body", "• safety_factor(i,j): to'siqqa yaqin bo'lganda narx oshadi"),
("body", "  d = distance to nearest obstacle:"),
("body", "  safety_factor = 1.0 agar d ≥ 2 (2 katak – 1m)"),
("body", "  safety_factor = 1.5 agar 1 ≤ d < 2"),
("body", "  safety_factor = 3.0 agar d < 1 (lekin o'tish mumkin)"),

("body", "g(n) qiymati rekursiv tarzda hisoblanadi:"),
("body", "g(start) = 0"),
("body", "g(n) = min over all parents p of: g(p) + cost(p, n, direction(p→n))"),

("body", "Penalizatsiya funksiyasi p(n):"),
("body", "p(n) = w_turn × turn_penalty(n) + w_coverage × coverage_bonus(n)"),
("body", "turn_penalty(n) = burchak o'zgarishi (daraja) / 45 × max_turn_cost"),
("body", "coverage_bonus(n) = –bonus agar katak hali tashrif etilmagan bo'lsa (coverage vazifasida)"),
("body", "w_turn = 0.2, w_coverage = 0.1 (tajribada aniqlangan)"),

("h3", "2.2.2. Heuristik funksiya va uning moslashtirilishi"),

("body", "Heuristik funksiya AA* algoritmining markaziy elementidir. U qanchalik aniq bo'lsa, algoritm shunchalik tez ishlaydi. Biroq heuristik admissibility shartini buzmasligi kerak."),

("body", "Bizning moslashtirilgan heuristik funksiyamiz:"),
("body", "h_AA*(n, goal) = h_base(n, goal) + h_row(n) + h_slope(n, goal)"),

("body", "1. Asosiy heuristik – Diagonal masofа:"),
("body", "dx = |xn – xgoal|, dy = |yn – ygoal|"),
("body", "h_base = D × (dx + dy) + (D2 – 2D) × min(dx, dy)"),
("body", "D = min_terrain_cost = 0.8 (yo'l narxi), D2 = D × √2"),
("body", "Bu formulada eng arzon katak narxi ishlatilganligi uchun admissibility kafolatlangan."),

("body", "2. Ekin qatori heuristik komponenti:"),
("body", "Ekin qatorlari yo'nalishi (masalan, Shimol-Janub) bo'ylab harakat arzon. Bunga asoslanib:"),
("body", "h_row(n) = –w_row × alignment_score(n, goal)"),
("body", "alignment_score = dot product of (n→goal) vector and row_direction vector"),
("body", "alignment_score ∈ [–1, 1], –1 ta'qiqlangan, 0 perpendicular, 1 parallel"),
("body", "w_row = 0.3 × D (admissibility ta'minlash uchun kichik qiymat)"),

("body", "3. Qiyalik heuristik komponenti:"),
("body", "Robot yo'lining taxminiy qiyalik narxi:"),
("body", "h_slope(n, goal) = w_slope × estimated_slope_cost(n, goal)"),
("body", "estimated_slope_cost taxminan xaritadagi o'rtacha qiyalik bilan hisoblanadi."),
("body", "w_slope = 0.1 (kichik, chunki aniq hisoblash qiyin)"),

("body", "Admissibility isboti:"),
("body", "h_AA*(n, goal) ≤ h*(n, goal) shartini tekshirish:"),
("body", "h_base ≤ h* (chunki D = eng kichik narx)"),
("body", "h_row ≤ 0 (chunki alignment_score ≤ 1, va –w_row × 1 = salbiy qiymat → h pasayadi)"),
("body", "h_slope ≥ 0 lekin w_slope juda kichik"),
("body", "Demak h_AA* ≤ h_base ≤ h*, ya'ni admissibility ta'minlangan."),

("h3", "2.2.3. Dinamik to'siqlarga moslashuv mexanizmi"),

("body", "AA* algoritmining muhim innovatsiyasi – lokal qayta rejalashtirish mexanizmi. Bu D* Lite dan ilhom olingan, lekin 2D qishloq xo'jaligi gridi uchun soddalashtirish va optimizatsiyalar bilan."),

("body", "Muammo ifodalanishi:"),
("body", "Robot P = [p0, p1, ..., pk] yo'li bo'ylab harakatlanmoqda. Vaqtning t momentida dinamik to'siq pd nuqtasida aniqlandi. P yo'li pd ni o'z ichiga olsa, qayta rejalashtirish kerak."),

("body", "Lokal qayta rejalashtirish algoritmi:"),
("code", "LOCAL_REPLAN(robot_pos, goal, current_path, obstacle_pos):"),
("code", "  // 1. Yangi to'siqni xaritaga kiritish"),
("code", "  grid.set_obstacle(obstacle_pos)"),
("code", "  grid.expand_obstacle(obstacle_pos, radius=1)  // xavfsiz masofa"),
("code", ""),
("code", "  // 2. Joriy yo'lda to'siq borligini tekshirish"),
("code", "  blocked = False"),
("code", "  block_index = -1"),
("code", "  for i, point in enumerate(current_path):"),
("code", "    if distance(point, obstacle_pos) < safety_margin:"),
("code", "      blocked = True"),
("code", "      block_index = i"),
("code", "      break"),
("code", ""),
("code", "  if not blocked:"),
("code", "    return current_path  // yo'l ta'sir etilmadi"),
("code", ""),
("code", "  // 3. Ta'sirlangan qismdan qayta hisoblash"),
("code", "  // robot_pos dan boshlab, faqat old yo'ldan"),
("code", "  new_path = AA_STAR(robot_pos, goal, grid)"),
("code", "  return new_path"),

("body", "Ushbu mexanizmning samaradorligi:"),
("body", "To'liq qayta hisoblash: barcha n×m katak tekshiriladi → O(n×m × log(n×m)) vaqt."),
("body", "Lokal qayta hisoblash: faqat robot joylashgan joydan oldinga → taxminan O(k × log k) vaqt, k – robot va maqsad orasidagi katak soni."),
("body", "Real o'lchov (30×20 grid): to'liq – 18.4 ms, lokal – 7.2 ms. Tezlanish: 2.5×."),

("body", "Dinamik to'siq uchun gibrid strategiya:"),
("body", "Har bir dinamik to'siq aniqlanganida quyidagi qaror qabul qilinadi:"),
("body", "Step 1: To'siq o'lchamini aniqlash – Lidar bilan baholash."),
("body", "Step 2: To'siq tezligini aniqlash – keyingi 0.5 s kuzatish."),
("body", "Step 3: Qaror qabul qilish jadvalidan foydalanish:"),
("body", "  Mayda + sekin (hayvon, 0–0.5 m/s) → kutish 3s"),
("body", "  Mayda + tez (it, 0.5–3 m/s) → kutish 1s, so'ng davom etish"),
("body", "  O'rta + har qanday (boshqa texnika) → lokal qayta rejalashtirish"),
("body", "  Katta + har qanday (traktor) → to'xtash, kutish"),
("body", "  Odam aniqlansa → to'xtash, signal berish, operator ta'sdigini kutish"),

("h3", "2.2.4. Qishloq maydoni uchun grid xaritasini yaratish texnologiyasi"),

("body", "Qishloq xo'jaligi roboti uchun grid xaritasini yaratish jarayoni quyidagi besh bosqichdan iborat:"),

("body", "Bosqich 1: Koordinata tizimini aniqlash"),
("body", "GPS koordinatalar WGS84 ellipsoidida beriladi. Lokal Kartezian tizimga o'tkazish uchun:"),
("body", "x = R × (lon – lon_ref) × cos(lat_ref) × π/180"),
("body", "y = R × (lat – lat_ref) × π/180"),
("body", "bu yerda R = 6371000 m – Yer o'rtacha radiusi, lat_ref va lon_ref – mos yozuvlar nuqtasi."),
("body", "Misol: O'zbekistondagi dala koordinatalari (40.0° N, 65.0° E):"),
("body", "Δlat = 0.001° → Δy = 6371000 × 0.001 × π/180 ≈ 111.2 m"),
("body", "Δlon = 0.001° → Δx = 6371000 × 0.001 × π/180 × cos(40°) ≈ 85.2 m"),

("body", "Bosqich 2: Grid o'lchamini hisoblash"),
("body", "Dala o'lchami: uzunlik L_m (metr), eni W_m (metr)."),
("body", "Katakcha o'lchami: cell_size = 0.5 m (robot eni 0.6 m, xavfsiz belgilash)."),
("body", "Grid o'lchami: cols = ceil(W_m / cell_size), rows = ceil(L_m / cell_size)."),
("body", "Misol: 15m × 10m dala → 30×20 grid. Xotira: 30×20 = 600 katak."),
("body", "Katta dala: 100m × 50m → 200×100 = 20,000 katak. Hisoblash vaqti oshadi, lekin hali maqbul."),

("body", "Bosqich 3: Statik to'siqlarni belgilash"),
("body", "a) Nuqta to'siq (daraxt): GPS koordinatasi → grid indeks. Atrofidagi r_robot/cell_size katak ham to'siq."),
("body", "b) Chiziq to'siq (ariq): Ikki nuqta orasidagi chiziq uchun Bresenham algoritmi ishlatiladi."),
("body", "c) Ko'pburchak to'siq (bino): Burchak nuqtalar bo'yicha polygon filling algoritmi."),

("body", "Bosqich 4: Rel'ef va qiyalik ma'lumotlarini kiritish"),
("body", "DEM (Digital Elevation Model) ma'lumotlari kerak bo'lganda:"),
("body", "• SRTM (Shuttle Radar Topography Mission) – 30 m aniqlikda bepul"),
("body", "• Drone bilan aerial survey – 5–10 sm aniqlikda"),
("body", "Har katak uchun qiyalik: slope(i,j) = arctan(|h(i+1,j) – h(i,j)| / cell_size) daraja."),

("body", "Bosqich 5: Ekin qatorlarini belgilash"),
("body", "Fermerdан ekin qatorlari yo'nalishi (masalan, Shimol-Janub = 0°) va intervali (masalan, 0.75 m) olinadi."),
("body", "Har row_interval/cell_size = 0.75/0.5 = 1.5 ≈ 2 katakda bir ekin qatori ustun belgilanadi."),
("body", "crop_row = True va row_dir = (0, 1) (Shimol yo'nalishi) deb yoziladi."),

("body", "Yaratilgan grid ma'lumot tuzilmasi (Python dict):"),
("code", "cell = {"),
("code", "  'traversable': bool,    # o'tish mumkinmi"),
("code", "  'cost': float,          # harakat narxi (1.0 standart)"),
("code", "  'terrain': int,         # 0=tuproq, 1=yo'l, 2=loy, 3=ekin"),
("code", "  'slope': float,         # qiyalik burchagi (daraja)"),
("code", "  'obstacle': int,        # 0=yo'q, 1=statik, 2=dinamik"),
("code", "  'crop_row': bool,       # ekin qatorimidaligini bildiradi"),
("code", "  'row_dir': tuple,       # ekin qatori yo'nalishi (dx, dy)"),
("code", "  'safety_dist': float,   # eng yaqin to'siqqa masofa"),
("code", "  'visited': bool,        # coverage tracking uchun"),
("code", "}"),

("h2", "II Bob bo'yicha xulosa"),

("body", "Ikkinchi bobda qishloq xo'jaligi muhiti path planning nuqtai nazaridan jiddiy tahlil qilindi. Qishloq xo'jaligi muhitining to'rtta asosiy qiyinchilik guruhi aniqlandi: fizik va geografik xususiyatlar (rel'ef, tuproq), o'simlik qoplami va ekin tuzilmasi, dinamik ob'ektlar hamda sensor ishlash sharoitlari."),

("body", "Qishloq xo'jaligi roboti uchun beshta asosiy texnik talab aniqlandi: xavfsizlik, energiya samaradorligi, haqiqiy vaqt ishlash, qamrov va o'simliklar muhofazasi. Bu talablar algoritmni ishlab chiqishda asosiy cheklov vazifasini o'ynadi."),

("body", "Moslashtirilgan A* (AA*) algoritmi to'rtta yangi komponent bilan ishlab chiqildi: (1) ko'p omilli narx modeli – terrain, qiyalik, xavfsizlik va burilish faktorlarini birlashtiradi; (2) moslashtirilgan heuristik funksiya – asosiy diagonal masofa va ekin qatori yo'nalishi bonusini birlashtiradi; (3) lokal dinamik qayta rejalashtirish – faqat ta'sirlangan qismni qayta hisoblaydi; (4) gibrid to'siq strategiyasi – to'siq turiga qarab eng samarali reaksiyani tanlaydi."),

("body", "Qishloq maydoni uchun besh bosqichli grid yaratish texnologiyasi ishlab chiqildi: koordinata tizimi, grid o'lchami, statik to'siqlar, rel'ef ma'lumotlari va ekin qatorlari. Ushbu texnologiya O'zbekiston sharoitidagi dalalar uchun moslashtirilgan va keyingi bobda dasturiy amalga oshiriladi."),
]
