from PIL import Image, ImageDraw, ImageFont

# Arkaplan boyutları
width, height = 1584, 396  # LinkedIn arka plan önerilen boyutları

# Arkaplan oluşturma
background = Image.new("RGB", (width, height), color="white")
draw = ImageDraw.Draw(background)

# Yazı fontu ve boyutu ayarlama
try:
    font = ImageFont.truetype("arial.ttf", 40)  # Arial font
except:
    font = ImageFont.load_default()

# Yazılacak metin
text = """
    ███╗   ██╗██╗ ██████╗██╗  ██╗███████╗███╗   ██╗
    ████╗  ██║██║██╔════╝██║ ██╔╝██╔════╝████╗  ██║
    ██╔██╗ ██║██║██║     █████╔╝ █████╗  ██╔██╗ ██║
    ██║╚██╗██║██║██║     ██╔═██╗ ██╔══╝  ██║╚██╗██║
    ██║ ╚████║██║╚██████╗██║  ██╗███████╗██║ ╚████║
    ╚═╝  ╚═══╝╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝

       Artificial Intelligence | Python | Java
"""

# Metni çizim yüzeyine ekle
text_width, text_height = draw.textsize(text, font=font)
text_x = (width - text_width) // 2
text_y = (height - text_height) // 2
draw.text((text_x, text_y), text, font=font, fill="black")

# Dosyayı kaydetme
background.save("linkedin_background.png")
print("LinkedIn arkaplanı oluşturuldu: linkedin_background.png")
