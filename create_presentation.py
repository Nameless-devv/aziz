#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Qishloq Xo'jaligi Roboti - Interaktiv Dala Planner
Prezintatsiyani yaratish
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor

def add_title_slide(prs, title, subtitle):
    """Sarlavha slaydini qo'shish"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank layout
    
    # Fon rangini o'rnatish
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(25, 118, 210)  # Ko'k rang
    
    # Sarlavha
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(2), Inches(9), Inches(1.5))
    title_frame = title_box.text_frame
    title_frame.word_wrap = True
    p = title_frame.paragraphs[0]
    p.text = title
    p.font.size = Pt(54)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)
    p.alignment = PP_ALIGN.CENTER
    
    # Kichik sarlavha
    subtitle_box = slide.shapes.add_textbox(Inches(0.5), Inches(3.8), Inches(9), Inches(1))
    subtitle_frame = subtitle_box.text_frame
    subtitle_frame.word_wrap = True
    p = subtitle_frame.paragraphs[0]
    p.text = subtitle
    p.font.size = Pt(28)
    p.font.color.rgb = RGBColor(255, 255, 255)
    p.alignment = PP_ALIGN.CENTER
    
    # Sana
    date_box = slide.shapes.add_textbox(Inches(0.5), Inches(6), Inches(9), Inches(0.5))
    date_frame = date_box.text_frame
    p = date_frame.paragraphs[0]
    p.text = "2026-yil May"
    p.font.size = Pt(16)
    p.font.color.rgb = RGBColor(255, 255, 255)
    p.alignment = PP_ALIGN.CENTER


def add_content_slide(prs, title, content_points):
    """Kontent slaydini qo'shish"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    # Oq fon
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(245, 245, 245)
    
    # Sarlavha
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(9), Inches(0.6))
    title_frame = title_box.text_frame
    p = title_frame.paragraphs[0]
    p.text = title
    p.font.size = Pt(40)
    p.font.bold = True
    p.font.color.rgb = RGBColor(25, 118, 210)
    
    # Chiziq
    line = slide.shapes.add_shape(1, Inches(0.5), Inches(1.0), Inches(9), Inches(0))
    line.line.color.rgb = RGBColor(25, 118, 210)
    line.line.width = Pt(2)
    
    # Kontent
    content_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.3), Inches(8.4), Inches(5.2))
    text_frame = content_box.text_frame
    text_frame.word_wrap = True
    
    for i, point in enumerate(content_points):
        if i > 0:
            text_frame.add_paragraph()
        p = text_frame.paragraphs[i]
        p.text = point
        p.font.size = Pt(18)
        p.font.color.rgb = RGBColor(50, 50, 50)
        p.space_before = Pt(6)
        p.space_after = Pt(6)
        p.level = 0
        
        # Bullet
        if not point.startswith("▪"):
            p.text = "▪ " + point


def add_two_column_slide(prs, title, left_content, right_content):
    """Ikki ustunli slayd"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    # Oq fon
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(245, 245, 245)
    
    # Sarlavha
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(9), Inches(0.6))
    title_frame = title_box.text_frame
    p = title_frame.paragraphs[0]
    p.text = title
    p.font.size = Pt(40)
    p.font.bold = True
    p.font.color.rgb = RGBColor(25, 118, 210)
    
    # Chiziq
    line = slide.shapes.add_shape(1, Inches(0.5), Inches(1.0), Inches(9), Inches(0))
    line.line.color.rgb = RGBColor(25, 118, 210)
    line.line.width = Pt(2)
    
    # Chap ustun
    left_box = slide.shapes.add_textbox(Inches(0.5), Inches(1.3), Inches(4.2), Inches(5.2))
    left_frame = left_box.text_frame
    left_frame.word_wrap = True
    
    for i, point in enumerate(left_content):
        if i > 0:
            left_frame.add_paragraph()
        p = left_frame.paragraphs[i]
        p.text = "▪ " + point
        p.font.size = Pt(16)
        p.font.color.rgb = RGBColor(50, 50, 50)
        p.space_before = Pt(4)
        p.space_after = Pt(4)
    
    # O'ng ustun
    right_box = slide.shapes.add_textbox(Inches(5.3), Inches(1.3), Inches(4.2), Inches(5.2))
    right_frame = right_box.text_frame
    right_frame.word_wrap = True
    
    for i, point in enumerate(right_content):
        if i > 0:
            right_frame.add_paragraph()
        p = right_frame.paragraphs[i]
        p.text = "▪ " + point
        p.font.size = Pt(16)
        p.font.color.rgb = RGBColor(50, 50, 50)
        p.space_before = Pt(4)
        p.space_after = Pt(4)


# Prezintatsiyani yaratish
prs = Presentation()
prs.slide_width = Inches(10)
prs.slide_height = Inches(7.5)

# 1-slayd: Sarlavha
add_title_slide(
    prs,
    "🚜 QISHLOQ XO'JALIGI ROBOTI",
    "Interaktiv Dala Planner Tizimi"
)

# 2-slayd: Loyihaning Maqsadi
add_content_slide(
    prs,
    "Loyihaning Maqsadi",
    [
        "Qishloq xo'jaligi robotlari uchun oптимал yo'l rejalashtirish tizimi",
        "Interaktiv grafikli interfeys orqali oson foydalanish",
        "Ixtiyoriy shakldagi dala va turli xil to'siqlarni qo'llash",
        "Real vaqt simulyatsiyasi va vizualizatsiyasi",
        "Robotning dala qoplamaning maksimal samaradorligini ta'minlash"
    ]
)

# 3-slayd: Asosiy Xususiyatlar
add_content_slide(
    prs,
    "Asosiy Xususiyatlar",
    [
        "🎨 Ixtiyoriy shakldagi dala chizish",
        "📍 Turli turdagi to'siqlarni qo'shish (daraxt, tosh, bino, suv)",
        "📏 To'siq hajmini slider bilan sozlash (1-10 metr)",
        "🤖 Boustrophedon va Spiral algoritmlar bilan yo'l rejalashtirish",
        "📊 Real vaqt simulyatsiyasi",
        "💾 Ma'lumotlarni JSON formatida saqlash"
    ]
)

# 4-slayd: Tizim Arxitekturasi
add_content_slide(
    prs,
    "Tizim Arxitekturasi",
    [
        "Interactive Planner (GUI) - Foydalanuvchi interfeysi",
        "Environment Modeling - Muhit va to'siqlarni modellashtirish",
        "Coverage Planning - Dala qoplash yo'li rejalashtirish",
        "Matplotlib - Vizualizatsiya va animatsiya",
        "Fayllar: interactive_planner.py, environment_modeling.py, coverage_planning.py"
    ]
)

# 5-slayd: Muhit Modeling
add_content_slide(
    prs,
    "Muhit Modellashtirish (Environment Modeling)",
    [
        "2D maydon ko'pburchak shaklida ifodalanadi",
        "Turli xil to'siq turlari: TREE, ROCK, BUILDING, IRRIGATION, UNKNOWN",
        "Doira va ko'pburchak shaklida to'siqlarni qo'llash",
        "To'siq klassifikatsiyasi va pozitsiya saqlanish",
        "Xavfsiz navigatsiya zonasini hisoblash"
    ]
)

# 6-slayd: Dala Qoplash (Coverage Planning)
add_content_slide(
    prs,
    "Dala Qoplash Algoritmi (Coverage Planning)",
    [
        "Boustrophedon: Parallel qatorlar bo'ylab harakatlanish",
        "Spiral: Markazdan periferiyaga spiral shaklida",
        "100% dala qoplamani ta'minlash",
        "Overlap parametri - takroriy qayta o'tilish",
        "Robot eni: 3 metr (sozlanuvchi)",
        "Yo'l uzunligi va vaqtni hisoblash"
    ]
)

# 7-slayd: Foydalanish (1-qism)
add_content_slide(
    prs,
    "Dasturdan Foydalanish (1/2)",
    [
        "1️⃣ Maydon Yaratish:",
        "   - Chap klik orqali nuqtalarni kiritish",
        "   - Enter tugmasini bosish maydonni yakunlash uchun",
        "   - Kamida 3 ta nuqta kerak",
        "",
        "2️⃣ To'siqlarni Qo'shish:",
        "   - To'siq turi tanlash (Daraxt, Tosh, Bino, Suv, Boshqa)",
        "   - Slider bilan hajmni o'zgartirish (1-10 metr)"
    ]
)

# 8-slayd: Foydalanish (2-qism)
add_content_slide(
    prs,
    "Dasturdan Foydalanish (2/2)",
    [
        "3️⃣ Boshlang'ich Nuqta:",
        "   - Chap klik: Robot uchun boshlang'ich nuqtasini tanlash",
        "",
        "4️⃣ Yo'l Rejalashtirish:",
        "   - 'Yo'l' tugmasi: Boustrophedon algoritmi",
        "   - 'Spiral' tugmasi: Spiral yo'l",
        "",
        "5️⃣ Simulyatsiya va Saqlash:",
        "   - 'SIMULYATSIYA' tugmasi: Roboting harakatini ko'rish",
        "   - 'Saqlash' tugmasi: Ma'lumotlarni saqlash"
    ]
)

# 9-slayd: Texnik Jixozlar (2 ustunli)
add_two_column_slide(
    prs,
    "Texnik Jixozlar va Kutubxonalar",
    [
        "Python 3.9+",
        "NumPy - Raqamli hisob-kitoblar",
        "Matplotlib - Vizualizatsiya",
        "SciPy - Ilmiy hisoblash",
        "Shapely - Geometrik amallar",
        "PyYAML - Konfiguratsiya"
    ],
    [
        "GUI: Matplotlib widgets",
        "Interactive: Slider, Button, RadioButtons",
        "Mouse events: Click va drag",
        "Animation: Real vaqt animatsiya",
        "File I/O: JSON, YAML",
        "Geometry: Polygon, Circle shapes"
    ]
)

# 10-slayd: Loyiha Strukturasi
add_content_slide(
    prs,
    "Loyiha Strukturasi",
    [
        "/aziz/",
        "├── interactive_planner.py  - Asosiy dastur (30 KB)",
        "├── src/",
        "│   ├── environment_modeling.py  - Muhit (21 KB)",
        "│   ├── coverage_planning.py  - Yo'l rejalashtirish (39 KB)",
        "│   └── __init__.py  - Paket initsializatsiyasi",
        "├── config/settings.yaml  - Konfiguratsiya",
        "├── docs/ARCHITECTURE.md  - Dokumentatsiya",
        "└── requirements.txt  - Zависимости"
    ]
)

# 11-slayd: Natijalar va Qo'llanish
add_content_slide(
    prs,
    "Natijalar va Amaliy Qo'llanish",
    [
        "✅ Qishloq xo'jaligi dalalarini samarali rejalashtirish",
        "✅ Robotning harakatini vizualizatsiya qilish",
        "✅ Yo'l uzunligini minimize qilish",
        "✅ Dala qoplamaning mustahkamligini ta'minlash",
        "✅ Real vaqt simulyatsiyasi bilan tekshirish",
        "✅ Turli xil dala shakllari bilan ishlash qobiliyati",
        "✅ Oson va intuitiv foydalanuvchi interfeysi"
    ]
)

# 12-slayd: Xulosa
add_title_slide(
    prs,
    "RAHMAT!",
    "Qishloq Xo'jaligi Roboti Interaktiv Dala Planner"
)

# Prezintatsiyani saqlash
prs.save('Qishloq_Xolaligi_Roboti_Prezintatsiya.pptx')
print("✅ Prezintatsiya yaratildi: Qishloq_Xolaligi_Roboti_Prezintatsiya.pptx")
print("📊 Jami slaydlar: 12")
