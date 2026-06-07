from pptx import Presentation
from pptx.util import Inches, Pt

slides_content = [
    ("Aziz Robo", ["Qishloq xo'jaligi uchun Coverage Path Planning", "Interaktiv dala va to'siq rejalashtirish"]),
    ("Muammo", ["Maydon va to'siqlarni vizual tarzda chizish qiyin", "Robot uchun to'liq qoplama yo'llarini avtomatik yaratish kerak"]),
    ("Yechim", ["Interaktiv matplotlib GUI (maydon + to'siq)", "Boustrophedon va spiral coverage algoritmlari", "Portativ o'rnatish - `aziz` buyruqi"]),
    ("Arxitektura", ["`robo.py` - GUI entrypoint", "`src/environment_modeling.py` - maydon va to'siq modellari", "`src/coverage_planning.py` - coverage algoritmlari"]),
    ("Modullar va Funksiyalar", ["Field yaratish va to'siq qo'shish", "Planner: CoveragePathPlanner", "Vizualizatsiya: matplotlib"]),
    ("O'rnatish va Ishga tushirish", ["git clone https://github.com/Nameless-devv/aziz.git", "bash install.sh  (macOS/Linux)", "install.bat yoki .\\install.ps1 (Windows)", "aziz  — dastur ishga tushadi"]),
    ("Demo va Ekranlar", ["Interaktiv maydon chizish", "To'siqlarni qo'shish", "Yo'lni rejalashtirish va vizualizatsiya"]),
    ("Natija va Foyda", ["Portativ va qayta o'rnatiluvchi loyiha", "Oson integratsiya boshqa tizimlarga", "Ta'lim va ilmiy ishlar uchun mos"]),
    ("Keyingi Qadamlar", ["Qo'shimcha algoritmlar", "ROS integratsiyasi", "Sensorlarni simulyatsiya qilish va testlar"]),
    ("Kontakt", ["Repository: https://github.com/Nameless-devv/aziz", "Muallif: Sanjarbek / Nameless-devv"]),
]

prs = Presentation()

for title, bullets in slides_content:
    slide_layout = prs.slide_layouts[1]  # Title and Content
    slide = prs.slides.add_slide(slide_layout)
    title_placeholder = slide.shapes.title
    body = slide.shapes.placeholders[1]

    title_placeholder.text = title

    tf = body.text_frame
    tf.clear()
    for i, b in enumerate(bullets):
        if i == 0:
            p = tf.paragraphs[0]
            p.text = b
            p.level = 0
            p.font.size = Pt(18)
        else:
            p = tf.add_paragraph()
            p.text = b
            p.level = 1
            p.font.size = Pt(16)

# Save presentation
out_path = "Aziz_Presentation.pptx"
prs.save(out_path)
print(f"Presentation saved to {out_path}")
