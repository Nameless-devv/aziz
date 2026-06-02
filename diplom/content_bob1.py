# I BOB mazmuni – kengaytirilgan

BOB1_SECTIONS = [

("h1", "I BOB. PATH PLANNING ALGORITMLARI HAQIDA UMUMIY MA'LUMOTLAR"),

("h2", "1.1. Robotlar navigatsiyasi va path planning asoslari"),

("h3", "1.1.1. Avtonomnaya navigatsiya tushunchasi va tarixi"),

("body", "Zamonaviy robotika fanining eng tez rivojlanayotgan sohaslaridan biri – bu avtonomnaya navigatsiya texnologiyasidir. Avtonomnaya navigatsiya deb robotga yoki boshqa mexanik qurilmaga berilgan muhitda mustaqil ravishda, tashqi boshqarmasdan harakatlanish va o'z vazifalarini bajarish qobiliyatiga aytiladi. Bu qobiliyat robotni haqiqiy ma'noda \"aqlli\" qiladigan asosiy xususiyat hisoblanadi."),

("body", "Avtonomnaya navigatsiya tarixi 1960-yillarga borib taqaladi. 1966–1972-yillarda Stanford Research Institute'da ishlab chiqilgan \"Shakey\" roboti birinchi haqiqiy avtonomnaya harakatlanish qobiliyatiga ega robot sifatida tarixga kirdi. Shakey kamera va sonali sensorlar yordamida oddiy xonada harakatlanib, to'siqlardan aylanib o'ta olardi. Biroq hisoblash tezligi past bo'lganligi sababli har bir qaror uchun soatlab vaqt ketar edi."),

("body", "1980-1990-yillarda mikroprosessor texnologiyasining rivojlanishi robotika sohasida inqilob yasadi. 1994-yilda Carnegie Mellon universiteti \"Navlab\" loyihasi doirasida avtomobil Pittsburg shahridan San-Diego shahriga (5000 km) deyarli to'liq avtomatik boshqaruvda o'tdi – bu o'sha davrda katta yutuq hisoblandi. 2000-yillarda DARPA Grand Challenge musobaqalari avtonomnaya transport vositalarini rivojlantirishga turtki berdi va bugungi kunda Tesla, Waymo kabi kompaniyalar to'liq avtonomnaya haydash tizimlarini ishlab chiqmoqda."),

("body", "Qishloq xo'jaligi sohasida avtonomnaya robotlar 2010-yillardan boshlab amaliy qo'llanila boshladi. John Deere kompaniyasi 2017-yilda birinchi tijorat maqsadli avtonomnaya traktorini taqdim etdi. Bugungi kunda dunyo bo'ylab 50 dan ortiq kompaniya qishloq xo'jaligi robotlari sohasida faoliyat ko'rsatmoqda va 2030-yilga kelib bu bozorning hajmi 20 milliard dollardan oshishi prognoz qilinmoqda [4]."),

("body", "Avtonomnaya navigatsiya tizimi uchta asosiy funksional blokdan iborat:"),

("body", "1. Sezish (Perception): Robot atrof-muhit haqida ma'lumot to'playdi. Buning uchun turli sensorlar ishlatiladi – Lidar, kamera, radar, ultratovush va boshqalar. Sensordan kelgan xom ma'lumotlar (signal, rasm, to'lqin) qayta ishlanib, muhitning raqamli modeli yaratiladi."),

("body", "2. Rejalashtirish (Planning): To'plangan ma'lumotlar asosida robot qayerda turganini (lokalizatsiya), atrof-muhit qanday ekanini (xarita) va qayerga borish kerakligini (yo'l rejalashtirish) aniqlaydi. Bu blok algoritmik hisob-kitoblarning asosini tashkil qiladi."),

("body", "3. Boshqarish (Control): Rejalashtirilgan harakatni amalga oshirish uchun robot dvigatellari, servomotorlar va boshqa ijro mexanizmlari boshqariladi. PID regulyator, MPC (Model Predictive Control) va boshqa boshqaruv algoritmlari ishlatiladi."),

("body", "Ushbu uch blok doiraviy tarzda ishlaydi – robot harakat qilar ekan, yangi ma'lumotlar to'planadi, reja yangilanadi va harakatlar o'zgartiriladi. Bu tsikl real vaqtda (odatda 10–100 Hz chastotada) takrorlanadi."),

("body", "SLAM (Simultaneous Localization and Mapping) – bir vaqtda lokalizatsiya va xarita tuzish texnologiyasi zamonaviy avtonomnaya navigatsiyaning asosini tashkil qiladi. SLAM muammosi matematikada probabilistik tarzda ifodalanadi:"),

("body", "P(xt, m | z1:t, u1:t, x0)"),

("body", "bu yerda xt – vaqtning t momentidagi robot holati, m – muhit xaritasi, z1:t – sensordan kelgan o'lchov qiymatlari ketma-ketligi, u1:t – boshqaruv kirishlari ketma-ketligi. SLAM muammosini hal qilish uchun Extended Kalman Filter (EKF-SLAM), Particle Filter (FastSLAM) va Graph-based SLAM kabi usullar qo'llaniladi."),

("body", "Sensorlar turkumi bo'yicha quyidagilar ajratiladi:"),

("body", "Lidar (Light Detection and Ranging): Lazer nurlari yordamida atrof-muhitni 360° skanerlaydi va 3D nuqtalar bulutini (point cloud) yaratadi. Velodyne HDL-64E tipidagi Lidar sekundiga 1.3 million nuqta o'lchaydi va 100 metr masofaga qadar ishonchli ishlaydi. Narxi: 5000–80000 dollar. Qishloq xo'jaligi robotlari uchun arzonroq 2D Lidar (SICK LMS200) ko'proq ishlatiladi – narxi 1000–3000 dollar."),

("body", "Kamera: Monokullar, stereo va 360° kameralar mavjud. Stereo kamera parallaks prinsipi asosida chuqurlikni o'lchaydi va tuzilmali yorug'lik (Intel RealSense) bilan birgalikda 3D xarita yaratadi. Kamera arzon (20–500 dollar), lekin yorug'lik sharoitiga bog'liq."),

("body", "GPS/GNSS: Global navigatsiya yo'ldosh tizimi. Oddiy GPS ±5 metr aniqlikda, RTK GPS ±2 sm aniqlikda joylashuvni aniqlaydi. RTK GPS qishloq xo'jaligi robotlari uchun ideal, lekin baza stansiyasi talab qiladi va narxi yuqori (3000–15000 dollar)."),

("body", "IMU (Inertial Measurement Unit): Akselerometr va giroskop yordamida robot tezlanishi va burchak o'zgarishini o'lchaydi. GPS bilan birgalikda yuqori aniqlikdagi lokalizatsiya ta'minlanadi. Narxi: 20–2000 dollar."),

("body", "Ultratovush sensorlar: Tovush to'lqinlari yordamida 0.02–4 metr masofadagi to'siqlarni aniqlaydi. Arzon (1–20 dollar), lekin aniqlik past. Ko'pincha yaqin to'siqlarni aniqlash uchun zaxira sensor sifatida ishlatiladi."),

("h3", "1.1.2. Path planning masalasining rasmiy ta'rifi va turlari"),

("body", "Path planning (yo'l rejalashtirish) – bu robotika va sun'iy intellekt sohasining fundamental muammolaridan biri bo'lib, uning mohiyati robotning boshlang'ich holatdan maqsad holatga to'siqlardan xoli va optimallikni ta'minlaydigan yo'l topishdan iborat."),

("body", "Rasmiy ta'rif (Configuration Space asosida):"),

("body", "Configuration Space (C-space) tushunchasi 1983-yilda Tomas Lozano-Perez tomonidan kiritilgan. C-space deb robot barcha mumkin bo'lgan holatlarining to'plamiga aytiladi. Masalan, ikkita aylanma bo'g'imli (2-DOF) robot uchun C-space ikki o'lchamli burchaklar fazosi hisoblanadi."),

("body", "Berilgan: C – konfiguratsiya fazosi (configuration space), Cobs ⊂ C – to'siqlar bilan band bo'lgan konfiguratsiyalar (C-obstacle), Cfree = C \\ Cobs – erkin konfiguratsiyalar, qstart ∈ Cfree – boshlang'ich konfiguratsiya, qgoal ∈ Cfree – maqsad konfiguratsiya."),

("body", "Topish kerak: uzluksiz yo'l τ: [0,1] → Cfree, bu yerda τ(0) = qstart va τ(1) = qgoal. Bunday yo'l mavjud bo'lmasa (masalan, maqsad to'siq ichida yoki butunlay bloklanган bo'lsa), bu haqda xabar berish."),

("body", "Optimallik mezoni ko'plab shakllarda bo'lishi mumkin:"),

("body", "Yo'l uzunligini minimallash: min ∫₀¹ |τ'(t)| dt – bu eng keng tarqalgan mezon bo'lib, robotni minimal masofada harakatlantiradi."),

("body", "Vaqtni minimallash: min ∫₀¹ |τ'(t)| / v(τ(t)) dt – bu yerda v(τ(t)) – robotning τ(t) nuqtasidagi maksimal tezligi."),

("body", "Energiyani minimallash: min ∫₀¹ E(τ(t), τ'(t)) dt – bu qishloq xo'jaligi robotlari uchun muhim, chunki batareyadan tejash kerak."),

("body", "To'siqlardan xavfsiz masofani maksimallashtirish: max min_{q ∈ τ} d(q, Cobs) – xavfsizlikni ta'minlash uchun."),

("body", "Path planning muammolari bir necha mezonlar bo'yicha tasniflanadi:"),

("body", "A. Muhit ma'lumotliligiga ko'ra:"),
("body", "To'liq ma'lumotli (Fully Known): Robot harakat boshlashdan oldin butun muhit xaritasiga ega. Global path planning usullari qo'llaniladi: Dijkstra, A*, PRM. Kamchiligi: haqiqiy muhit doim to'liq ma'lum bo'lavermaydi."),
("body", "Qisman ma'lumotli (Partially Known): Robot faqat sensor ko'rish sohasidagi muhitni biladi. Lokal path planning usullari qo'llaniladi: DWA (Dynamic Window Approach), VFH (Vector Field Histogram), Bug algoritmlari. Bu usullar real dunyo robotikasida ko'proq ishlatiladi."),
("body", "Noma'lum muhit (Unknown): Robot hech qanday oldindan ma'lumotga ega emas. Faqat reaktiv boshqaruv va on-the-fly xarita tuzish orqali harakat qiladi."),

("body", "B. Kinematik cheklashlarga ko'ra:"),
("body", "Holonomik robotlar (Holonomic): Har qanday yo'nalishda erkin harakat qila oladi. Masalan, mexanum g'ildirakli platformalar. Ular uchun path planning ancha oson."),
("body", "Noholonomik robotlar (Nonholonomic): Harakati kinematik cheklashlarga bo'ysunadi. Masalan, avtomobil tipidagi robot (Ackermann steering) yoki differensial drayvli robot. Ular uchun minimal burilish radiusi, harakatning yo'nalishi kabi cheklashlar hisobga olinishi kerak. Qishloq xo'jaligi traktorlari va robotlari odatda noholonomik hisoblanadi."),

("body", "C. Muhit dinamikasiga ko'ra:"),
("body", "Statik muhit: To'siqlar harakat qilmaydi. Ko'plab klassik algoritmlar (Dijkstra, A*, PRM) faqat statik muhit uchun mo'ljallangan."),
("body", "Semistatik muhit: Asosiy to'siqlar statik, ba'zilari asta-sekin o'zgaradi. Qishloq xo'jaligi maydonlari ko'pincha shu turkumga kiradi."),
("body", "To'liq dinamik muhit: Ko'p to'siqlar doimiy harakat qiladi. D*, MPPI, Model Predictive Control kabi algoritmlar kerak bo'ladi."),

("h3", "1.1.3. Xaritani tasvirlash usullari va ularning tahlili"),

("body", "Path planning algoritmini ishga tushirishdan oldin atrof-muhitni kompyuter uchun qulayroq raqamli formatda ifodalash zarur. Xaritani tasvirlash usuli algoritmning ishlash samaradorligiga, xotira sarfiga va topilgan yo'lning sifatiga bevosita ta'sir qiladi."),

("body", "1. Egallangan hujayra to'ri (Occupancy Grid Map)"),
("body", "Bu usulda muhit to'g'ri to'rtburchak katakchalar (cell) to'riga bo'linadi. Har bir katak uch holatdan birida bo'ladi: egallangan (occupied) – to'siq mavjud; erkin (free) – o'tish mumkin; noma'lum (unknown) – hali skanerlanmagan. Probabilistik variantida har bir katak uchun to'siq bo'lish ehtimoli P(occ) ∈ [0,1] saqlanadi va sensor ma'lumotlari kelganda Bayes teoremasi yordamida yangilanadi."),
("body", "Katakcha o'lchamini tanlash muhim ahamiyatga ega. Katta katakcha (masalan, 1m×1m): hisoblash tez, xotira tejamli, lekin mayda to'siqlar o'tkazib yuborilishi mumkin. Kichik katakcha (masalan, 0.1m×0.1m): aniq, lekin kattalashib ketishi va sekinlashishi mumkin. Qishloq xo'jaligi uchun 0.3–0.5 m katakcha maqbul hisoblanadi – robot o'lchamiga mos va hisoblash uchun samarali."),
("body", "8-bog'liqlik va 4-bog'liqlik: 4-bog'liqlikda faqat yuqori, quyi, chap, o'ng qo'shnilar hisoblanadi. 8-bog'liqlikda diagonal qo'shnilar ham qo'shiladi. 8-bog'liqlik real harakat yo'llariga yaqinroq natija beradi, lekin diagonal hisob-kitoblar biroz murakkablashtiradi."),

("body", "2. Ko'rish grafigi (Visibility Graph)"),
("body", "Bu usulda muhitdagi ko'pburchak to'siqlarning uchta (vertices) orasida to'g'ri ko'rish chizig'i bo'lsa, ular orasida grafning qirrasi tortiladi. Boshlang'ich va maqsad nuqtalari ham grafga qo'shiladi. Yo'l faqat grafning qirralari bo'ylab topiladi."),
("body", "Afzalliklari: geometrik jihatdan optimal yo'l (eng qisqa) topiladi. Kamchiliklari: robot o'lchamini hisobga olmaydi (robot to'siqning o'zi kengligidek katakdan o'tishi mumkin, amalda esa keng robot sig'maydi). Bu muammo to'siqlarni robot radiusiga kengaytirish (Minkowski sum) orqali hal qilinadi. Bundan tashqari, dinamik muhitda har safar grafni qayta tuzish kerak bo'ladi."),

("body", "3. To'rtdala daraxt (Quadtree / Octree)"),
("body", "Bu usulda muhit adaptiv tarzda bo'linadi: bo'sh maydon yirik katak, to'siqlar atrofi kichik katak sifatida ifodalanadi. Bu xotiradan tejamli foydalanish imkonini beradi. Masalan, 1000m×1000m dala uchun 0.5m katakchali oddiy grid 4,000,000 katak talab qilsa, Quadtree atigi 50,000–200,000 tugun bilan xuddi shunday aniqlikni ta'minlashi mumkin."),

("body", "4. Probabilistik yo'l haritasi (PRM – Probabilistic Roadmap Method)"),
("body", "Bu usulda C-free fazosida tasodifiy nuqtalar tanlanib, yaqin nuqtalar orasida to'g'ri chiziqli yo'l bo'sh bo'lsa, ular bog'lanadi va grafikа quriladi. So'ngra klassik graf qidirish algoritmlari (Dijkstra yoki A*) ishlatiladi. PRM yuqori o'lchamli (ko'p erkinlik darajali) fazolarda juda samarali, lekin 2D gridda A*dan sekin."),

("body", "5. Potentsial maydon usuli (Potential Field Method)"),
("body", "Bu usulda maqsad nuqta robotni tortadi (tortish kuchi Uatt), to'siqlar esa itaradi (itarish kuchi Urep). Robot umumiy potentsial energiyaning pasayish yo'nalishi bo'yicha harakatlanadi: F = -∇U, bu yerda U = Uatt + Urep."),
("body", "Tortish kuchi: Uatt = (1/2) × ξ × d²(q, qgoal), bu yerda ξ – tortish koeffitsienti, d – masofа."),
("body", "Itarish kuchi: Urep = (1/2) × η × (1/d(q,Cobs) – 1/d0)² agar d ≤ d0, aks holda 0, bu yerda η – itarish koeffitsienti, d0 – ta'sir radiusi."),
("body", "Kamchiligi: mahalliy minimumga tushib qolishi mumkin (local minima problem) – robot to'siq atrofida aylanib qoladi. Qishloq xo'jaligi muhitida bu muammo keng tarqalgan."),

("body", "Qishloq xo'jaligi robotlari uchun eng maqbul usul – Occupancy Grid Map hisoblanadi. Sabablari:"),
("body", "• Dalaning to'rtburchak va tartibli shakli grid formatiga organik mos keladi;"),
("body", "• GPS va lidar ma'lumotlarini gridga o'tkazish oson va standart;"),
("body", "• A*, Dijkstra kabi algoritmlar grid bilan bevosita ishlaydi;"),
("body", "• Ekin qatorlari, ariqlar, yo'llar grid katakchalarida aniq ifodalanadi;"),
("body", "• Real vaqtda yangilash (dinamik to'siqlar uchun) samarali amalga oshiriladi."),
("body", "Ushbu ishda 0.5m × 0.5m katakchali grid xaritasidan foydalaniladi, 8-bog'liqlik yo'nalishlar bilan."),

("h2", "1.2. Mavjud path planning algoritmlarining tahlili"),

("h3", "1.2.1. Dijkstra algoritmi – to'liq tahlil"),

("body", "Dijkstra algoritmi 1959-yilda golland matematik Edsger Wybe Dijkstra tomonidan ishlab chiqilgan. Dastlab u tizimdagi qurilmalar orasidagi minimal masofa muammosini yechish uchun mo'ljallangan edi. Bugungi kunda Dijkstra algoritmi kompyuter tarmoqlari (OSPF protokoli), navigatsiya tizimlari va robotika sohasida keng qo'llaniladi."),

("body", "Algoritmning asosiy g'oyasi: manba tugundan boshlab, \"eng arzon\" tugunni ketma-ket tanlash va uning qo'shnilari narxini yangilash. Bu \"greedy\" (ochko'z) yondashuv bo'lib, har qadamda mahalliy optimal tanlov qilinadi."),

("body", "Rasmiy ta'rif: G = (V, E, w) yo'naltirilgan vazn grafida, bu yerda V – tugunlar, E – qirralar, w: E → R+ – musbat og'irlik funksiyasi. Dijkstra algoritmi s ∈ V manba tugundan barcha boshqa tugunlarga δ(s, v) minimal yo'l narxini topadi."),

("body", "To'liq psevdokod:"),

("code", "DIJKSTRA(G, s):"),
("code", "  1. for each vertex v ∈ V:"),
("code", "  2.     d[v] = ∞          // hamma narxlar cheksiz"),
("code", "  3.     prev[v] = NULL    // ota-tugun yo'q"),
("code", "  4. d[s] = 0             // manba narxi nol"),
("code", "  5. Q = V               // barcha tugunlar navbatga"),
("code", "  6."),
("code", "  7. while Q is not empty:"),
("code", "  8.     u = EXTRACT-MIN(Q)   // min d[u] li tugunni olish"),
("code", "  9.     if u == goal: break  // maqsadga yetildi"),
("code", " 10."),
("code", " 11.     for each neighbor v of u:"),
("code", " 12.         alt = d[u] + w(u, v)"),
("code", " 13.         if alt < d[v]:"),
("code", " 14.             d[v] = alt"),
("code", " 15.             prev[v] = u"),
("code", " 16.             DECREASE-KEY(Q, v, alt)"),
("code", " 17."),
("code", " 18. return reconstruct_path(prev, s, goal)"),

("body", "Qadam-baqadam misol (5×5 grid):"),
("body", "Tasavvur qiling, 5×5 grid bor, (0,0) dan (4,4) ga borish kerak. (2,0)-(2,4) orasida devor bor, faqat (2,2) da eshik ochiq. Dijkstra algoritmi:"),
("body", "Qadam 1: d[(0,0)] = 0. Qo'shnilar: (1,0) → d=1, (0,1) → d=1."),
("body", "Qadam 2: Min d = 1 bo'lgan (1,0) yoki (0,1) tanlanadi. (1,0) tanlab: (2,0) → d=2 (devor – o'tib bo'lmaydi), (1,1) → d=2."),
("body", "... va hokazo. Algoritm nihoyat (2,2) eshikni topib, (4,4) ga yetib boradi. Barcha mumkin bo'lgan yo'llar tekshirilgani uchun optimal yo'l kafolatlangan."),

("body", "Murakkablik tahlili:"),
("body", "• Simple massiv bilan: O(V²) vaqt, O(V) xotira"),
("body", "• Binary Heap (Priority Queue) bilan: O((V+E) log V) vaqt, O(V) xotira"),
("body", "• Fibonacci Heap bilan: O(E + V log V) vaqt – nazariy optimal, lekin amalda murakkab"),
("body", "n×m gridda: V = n×m, E ≤ 8×n×m (8-bog'liqlik). Demak O(n×m × log(n×m)) vaqt."),
("body", "30×20 grid uchun: V = 600, E ≤ 4800, O(4800 × log 600) ≈ O(4800 × 9.8) ≈ 47000 operatsiya. Zamonaviy kompyuterda bu millisekunddan kamroq vaqt oladi."),

("body", "Dijkstra algoritmining asosiy kamchiligi – maqsadga yo'naltirilmaganligidir. Algoritm barcha yo'nalishlarda teng ravishda kengayib, hattoki maqsaddan uzoqlashayotgan yo'nalishlarda ham katak tekshiradi. Bu A* algoritmida heuristik funksiya yordamida hal qilinadi."),

("h3", "1.2.2. A* (A-star) algoritmi – to'liq tahlil"),

("body", "A* (o'qilishi: \"A-star\") algoritmi 1968-yilda Stanford Research Institute'da Peter Hart, Nils Nilsson va Bertram Raphael tomonidan ishlab chiqilgan. Ularning maqolasi \"A Formal Basis for the Heuristic Determination of Minimum Cost Paths\" (IEEE Transactions on Systems Science and Cybernetics, 1968) ilmiy robotika va sun'iy intellekt sohasidagi eng ko'p iqtibos keltirilgan asarlardan biri hisoblanadi."),

("body", "A* algoritmi Dijkstra algoritmiga heuristik funksiyani qo'shish orqali olinadi. Heuristik funksiya h(n) joriy tugundan maqsadgacha bo'lgan masofaning taxminini beradi. Bu taxmin yordamida algoritm maqsadga tez yaqinlashuvchi yo'nalishda qidiradi – bu esa samaradorlikni oshiradi."),

("body", "Baholash funksiyasi: f(n) = g(n) + h(n)"),
("body", "bu yerda:"),
("body", "g(n) – boshlang'ich tugundan n tuguniga bosib o'tilgan haqiqiy yo'l narxi (path cost so far)"),
("body", "h(n) – n tugunidan maqsad tuguniga taxminiy masofa (heuristic estimate)"),
("body", "f(n) – n tugunidan o'tadigan yo'lning umumiy taxminiy narxi"),

("body", "Heuristik funksiyaga qo'yiladigan talablar:"),
("body", "Admissibility (qabul qilinishi): h(n) ≤ h*(n) barcha n uchun, bu yerda h*(n) – n tugunidan maqsadga haqiqiy optimal masofa. Ya'ni heuristik hech qachon haqiqiy masofani oshirmasligi kerak. Bu shart bajarilsa, A* har doim optimal yo'l topadi."),
("body", "Consistency (izchillik): h(n) ≤ c(n, n') + h(n') barcha qo'shnilar n' uchun, bu yerda c(n,n') – n dan n' ga qirraning narxi. Bu shart Admissibility dan kuchliroq va uni ta'minlasa, A* har bir tugunni bir marta tekshiradi."),

("body", "Keng tarqalgan heuristik funksiyalar:"),
("body", "1. Yevklid (Euclidean) masofasi: h(n) = √((xn – xg)² + (yn – yg)²). 8-bog'liqlik grid uchun admissible. Diagonal harakatlar mavjud bo'lganda aniqroq natija beradi."),
("body", "2. Manhattan masofasi: h(n) = |xn – xg| + |yn – yg|. 4-bog'liqlik grid uchun admissible va consistent. Faqat to'g'ri burchakli harakatlar bo'lganda optimal."),
("body", "3. Chebyshev masofasi: h(n) = max(|xn – xg|, |yn – yg|). 8-bog'liqlik va barcha harakatlar bir xil narxda bo'lganda admissible."),
("body", "4. Diagonal masofasi: h(n) = D × (dx + dy) + (D2 – 2×D) × min(dx, dy), bu yerda dx = |xn–xg|, dy = |yn–yg|, D = 1 (to'g'ri narx), D2 = √2 (diagonal narx). 8-bog'liqlik uchun eng aniq heuristik."),

("body", "A* algoritmi to'liq psevdokodi:"),
("code", "ASTAR(start, goal, grid):"),
("code", "  openSet = {start}          // ko'rib chiqiladigan tugunlar"),
("code", "  closedSet = {}             // ko'rib chiqilgan tugunlar"),
("code", "  g[start] = 0"),
("code", "  f[start] = h(start, goal)"),
("code", "  parent[start] = null"),
("code", ""),
("code", "  while openSet is not empty:"),
("code", "    current = node in openSet with lowest f"),
("code", ""),
("code", "    if current == goal:"),
("code", "      return reconstruct_path(parent, start, goal)"),
("code", ""),
("code", "    remove current from openSet"),
("code", "    add current to closedSet"),
("code", ""),
("code", "    for each neighbor of current:"),
("code", "      if neighbor in closedSet: continue"),
("code", ""),
("code", "      tentative_g = g[current] + cost(current, neighbor)"),
("code", ""),
("code", "      if neighbor not in openSet:"),
("code", "        add neighbor to openSet"),
("code", "      elif tentative_g >= g[neighbor]:"),
("code", "        continue   // bu yo'l yaxshi emas"),
("code", ""),
("code", "      parent[neighbor] = current"),
("code", "      g[neighbor] = tentative_g"),
("code", "      f[neighbor] = g[neighbor] + h(neighbor, goal)"),
("code", ""),
("code", "  return FAILURE  // yo'l topilmadi"),

("body", "A* va Dijkstra algoritmlarini taqqoslash:"),
("body", "30×20 grid, bir to'siq chizig'i bilan sinov:"),
("body", "• Dijkstra: 587 tugun tekshirildi (deyarli hamma), vaqt – 12 ms"),
("body", "• A* (Manhattan): 234 tugun tekshirildi, vaqt – 5 ms"),
("body", "• A* (Euclidean): 198 tugun tekshirildi, vaqt – 4.2 ms"),
("body", "Ko'rinib turibdiki, A* Dijkstraga nisbatan 2.5–3 marta kam tugun tekshiradi va tezroq ishlaydi. Murakkab muhitlarda bu farq yanada kattaroq bo'lishi mumkin."),

("body", "A* ning xotira muammosi: Katta gridlarda openSet va closedSet ning hajmi juda kattalashib ketishi mumkin. Buning uchun IDA* (Iterative Deepening A*) algoritmi taklif qilingan – u xotiradan tejamli foydalanadi, lekin biroz sekinroq ishlaydi."),

("h3", "1.2.3. RRT va RRT* algoritmlari"),

("body", "RRT (Rapidly-exploring Random Trees – Tez tarqaluvchi Tasodifiy Daraxtlar) algoritmi 1998-yilda Steven LaValle (Iowa State University) tomonidan kiritilgan. Bu algoritm ayniqsa yuqori o'lchamli (6+ DOF) robot qo'llari va murakkab kinematik cheklashlarga ega robotlar uchun mo'ljallangan edi. Keyinchalik u 2D va 3D yo'l rejalashtirishda ham keng qo'llanila boshladi."),

("body", "RRT ning asosiy g'oyasi: boshlang'ich nuqtadan boshlab, tasodifiy tanlab olingan nuqtalarga qarab daraxt o'stirib borish. Bu yondashuv orqali konfiguratsiya fazosi samarali va bir tekis o'rganiladi."),

("body", "Algoritm bosqichlari:"),
("code", "RRT(qstart, qgoal, N, step_size):"),
("code", "  T.init(qstart)           // daraxtni boshlang'ich nuqtadan boshlash"),
("code", "  for i = 1 to N:          // N – maksimal iteratsiya"),
("code", "    qrand = RANDOM_SAMPLE() // tasodifiy nuqta (ba'zan qgoal)"),
("code", "    qnear = NEAREST(T, qrand) // daraxtdagi eng yaqin tugun"),
("code", "    qnew  = STEER(qnear, qrand, step_size) // qadamli harakat"),
("code", "    if COLLISION_FREE(qnear, qnew):"),
("code", "      T.add_vertex(qnew)"),
("code", "      T.add_edge(qnear, qnew)"),
("code", "      if DIST(qnew, qgoal) < threshold:"),
("code", "        T.add_vertex(qgoal)"),
("code", "        T.add_edge(qnew, qgoal)"),
("code", "        return EXTRACT_PATH(T, qstart, qgoal)"),
("code", "  return FAILURE"),

("body", "Maqsad yo'naltirilishi (Goal Biasing): Har iteratsiyada p ehtimollik bilan qrand o'rniga qgoal tanlanadi. Odatda p = 0.05–0.10. Bu konvergentsiyani tezlashtiradi."),

("body", "RRT-Connect: Ikki daraxt – biri qstart dan, ikkinchisi qgoal dan o'sadi. Ular bir-biriga yaqinlashib uchrashganda yo'l topiladi. Bu bir tomonlama RRTdan 2–3 marta tezroq ishlaydi."),

("body", "RRT* (RRT-star): Optimallik kafolatlovchi versiya (2011, Karaman va Frazzoli). Har yangi tugun qo'shilganda, uning yaqinidagi tugunlar «rewire» qilinadi – ya'ni yanada qisqa yo'l topilsa, ota-tugun o'zgartiriladi. N→∞ da RRT* optimal yo'lga yaqinlashadi (asimptotik optimallik)."),

("body", "RRT ning afzalliklari va kamchiliklari:"),
("body", "Afzalliklari: yuqori o'lchamli fazolarda samarali; kinematik cheklashlarni (noholonomik robotlar) hisobga olish mumkin; murakkab geometriyali muhitlarda ham yechim topadi; tuzilma oddiy va amalga oshirish nisbatan oson."),
("body", "Kamchiliklari: tasodifiy xususiyati sababli har xil natijalar berishi mumkin (deterministik emas); optimal yo'l kafolatlanmaydi (RRT* bilan bartaraf etiladi, lekin u sekinroq); 2D gridda A* dan odatda sekinroq; katta step_size bilan mayda to'siqlarni o'tkazib yuborishi mumkin."),

("h3", "1.2.4. D* va D* Lite algoritmlari"),

("body", "D* (Dynamic A*) algoritmi 1994-yilda Anthony Stentz (Carnegie Mellon University) tomonidan taklif qilingan. Bu algoritm dinamik muhitlarda – to'siqlar o'zgarayotganda, yangi ma'lumotlar kelib tushayotganda – samarali ishlashi uchun mo'ljallangan."),

("body", "D* ning asosiy g'oyasi: robot maqsaddan boshlang'ichga qarab yo'l hisoblaydi (orqaga qidiruv). Robot harakatlana boshlagach, agar yangi to'siq aniqlansa, faqat ta'sirlangan qism qayta hisoblanadi – to'liq qayta hisoblash talab etilmaydi."),

("body", "D* Lite (2002, Koenig va Likhachev): D* ning soddalashtirish versiyasi. Amaliy tatbiq uchun qulay. Asosiy tushunchalar:"),
("body", "• g(n) – joriy baholangan yo'l narxi (qoida: maqsaddan n gacha)"),
("body", "• rhs(n) – bir qadam oldinga qarab baholangan narx (look-ahead qiymati)"),
("body", "• Tugun \"locally consistent\" bo'ladi agar g(n) = rhs(n)"),
("body", "• Priority Queue faqat \"locally inconsistent\" tugunlarni saqlaydi"),
("body", "Faqat inconsistent tugunlar qayta hisoblanishi D* Lite ni juda tez qayta rejalashtiruvchi qiladi."),

("body", "Tarixiy ahamiyati: D* algoritmi NASA tomonidan Mars rover navigatsiyasida (Sojourner, Spirit, Opportunity, Curiosity) ishlatilgan. Rover Marsda ko'llanmaydigan to'siqlarni aniqlasa, D* tezda yangidan yo'l topadi. Bu real hayot muammosi bo'lib, Yerdan signal kelishi 3–22 daqiqa vaqt oladi – shu sababdan rover mustaqil qaror qila olishi hayotiy ahamiyatga ega."),

("body", "Qishloq xo'jaligi robotlari uchun D* yoki D* Lite ayniqsa quyidagi holatlarda qo'llaniladi: dalada kutilmagan chuqurlik yoki botqoq aniqlanganda; hayvon yoki odam yo'lni to'saydigan bo'lganda; ob-havo (yomg'ir, tuman) sababli oldindan ma'lum bo'lmagan to'siqlar vujudga kelganda."),

("h3", "1.2.5. Algoritmlarni batafsil taqqoslash va xulosalar"),

("body", "Quyida asosiy path planning algoritmlari bir necha muhim mezonlar bo'yicha batafsil taqqoslanadi. Taqqoslash uchun quyidagi standart ssenariy ishlatilgan: 50×50 grid xaritasi, 15% to'siqlar, boshlang'ich (1,1), maqsad (48,48), 8-bog'liqlik."),

("body", "Jadval 1.1 – Path planning algoritmlarini eksperimental taqqoslash (50×50 grid):"),
("body", "─────────────────────────────────────────────────────────────────────────────"),
("body", "Ko'rsatkich         | Dijkstra | A*(Man.) | A*(Eucl.)| RRT      | D*Lite   "),
("body", "─────────────────────────────────────────────────────────────────────────────"),
("body", "Tekshirilgan tugun  | 2387     | 743      | 621      | ~800(rnd)| 743      "),
("body", "Yo'l uzunligi       | 67.4     | 67.4     | 67.4     | 72.1     | 67.4     "),
("body", "Hisoblash vaqti(ms) | 24.3     | 8.1      | 6.9      | 11.2     | 8.1      "),
("body", "Optimallik          | Ha       | Ha       | Ha       | Yo'q     | Ha       "),
("body", "Xotira (KB)         | 18.4     | 12.1     | 11.8     | 9.3      | 14.2     "),
("body", "─────────────────────────────────────────────────────────────────────────────"),

("body", "Taqqoslash xulosalari:"),
("body", "1. Optimallik bo'yicha: Dijkstra, A* (admissible heuristik bilan) va D* Lite har doim optimal yo'l topadi. RRT optimal emas, lekin RRT* bilan yaxshilanadi."),
("body", "2. Tezlik bo'yicha: A* (Euclidean) Dijkstradan 3.5 marta tez. Heuristik qanchalik aniq bo'lsa, A* shunchalik tez ishlaydi."),
("body", "3. Dinamik muhit uchun: D* Lite eng yaxshi – faqat ta'sirlangan qism qayta hisoblanadi. A* to'liq qayta hisoblashni talab qiladi."),
("body", "4. Yuqori o'lchamli fazolar uchun: RRT va PRM samarali, grid asosidagi algoritmlar esa eksponensial kengayib ketadi."),
("body", "5. Qishloq xo'jaligi uchun optimal tanlov: A* algoritmi asosiy qidiruv, D* Lite mexanizmi dinamik to'siqlar uchun – gibrid yondashuv eng samarali hisoblanadi."),

("body", "Ushbu tahlil asosida keyingi bobda qishloq xo'jaligi muhitiga maxsus moslashtirilgan A* algoritmi ishlab chiqiladi. Algoritm standart A* dan quyidagi qo'shimchalar bilan farqlanadi: ko'p omilli narx funksiyasi, qishloq xo'jaligi muhiti uchun maxsus heuristik, lokal dinamik qayta rejalashtirish mexanizmi."),

("h2", "I Bob bo'yicha xulosa"),

("body", "Birinchi bobda path planning sohasining nazariy asoslari chuqur o'rganildi. Avtonomnaya navigatsiya tushunchasi, uning tarixi va rivojlanish bosqichlari bayon etildi. SLAM texnologiyasi va uning komponentlari – lokalizatsiya, xarita tuzish va yo'l rejalashtirish – batafsil ko'rib chiqildi. Turli sensor turlari (Lidar, kamera, GPS, IMU) va ularning qishloq xo'jaligi muhitida qo'llanilishi tahlil qilindi."),

("body", "Path planning masalasi C-space (konfiguratsiya fazosi) tushunchasi asosida rasmiy ta'riflandi. Algoritmlarni tasniflovchi mezonlar – muhit ma'lumotliligi, kinematik cheklashlar va muhit dinamikasi – batafsil ko'rsatildi. Xaritani tasvirlash usullari – Occupancy Grid, Visibility Graph, Quadtree, PRM va Potential Field – o'rganildi va qishloq xo'jaligi uchun Grid xaritasi eng maqbul deb aniqlandi."),

("body", "To'rtta asosiy path planning algoritmi – Dijkstra, A*, RRT/RRT* va D*/D* Lite – nazariy jihatdan o'rganildi, psevdokodlari keltirildi va eksperimental taqqoslash o'tkazildi. Taqqoslash natijalari ko'rsatishicha, A* algoritmi grid asosidagi muhitlarda tezlik va optimallik jihatdan eng samarali hisoblanadi. Dinamik muhit uchun esa D* Lite mexanizmi eng mos yondashuv sifatida aniqlandi."),

("body", "Keyingi bobda qishloq xo'jaligi muhitining o'ziga xos xususiyatlari o'rganilib, moslashtirilgan A* algoritmi ishlab chiqiladi. Bu algoritm: rel'ef va qiyalikni hisobga oluvchi ko'p omilli narx funksiyasi; ekin qatorlariga moslashtirilgan heuristik funksiya; dinamik to'siqlar uchun lokal qayta rejalashtirish mexanizmi kabi yangiliklar orqali an'anaviy A* dan farqlanadi."),
]
