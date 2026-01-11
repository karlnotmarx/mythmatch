from PIL import Image, ImageDraw, ImageFont

width, height = 1200, 400
img = Image.new('RGB', (width, height), color='#000000')
draw = ImageDraw.Draw(img)

try:
    sanskrit_font = ImageFont.truetype('/System/Library/Fonts/Supplemental/DevanagariSangamMN.ttf', 70)
    title_font = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf', 50)
    subtitle_font = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf', 28)
except:
    sanskrit_font = ImageFont.load_default()
    title_font = ImageFont.load_default()
    subtitle_font = ImageFont.load_default()

sanskrit_text = "मिथकम् ज्ञानम् आत्मज्ञानम्"
bbox = draw.textbbox((0, 0), sanskrit_text, font=sanskrit_font)
text_width = bbox[2] - bbox[0]
x = (width - text_width) // 2
draw.text((x, 120), sanskrit_text, fill='#FFFFFF', font=sanskrit_font)

title = "MYTHMATCH"
bbox = draw.tex = bbox[2] - bbox[0]
x = (width - text_width) // 2
draw.text((x, 50), title, fill='#FFFFFF', font=title_font)

subtitle = '"Myth is Knowledge, Knowledge is Self"'
bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
text_width = bbox[2] - bbox[0]
x = (width - text_width) // 2
draw.text((x, 230), subtitle, fill='#CCCCCC', font=subtitle_font)

desc = "AI-Powered Personality Matching with World Mythology"
bbox = draw.textbbox((0, 0), desc, font=subtitle_font)
text_width = bbox[2] - bbox[0]
x = (width - text_width) // 2
draw.text((x, 280), desc, fill='#888888', font=subtitle_font)

img.save('docs/banner.png')
print("Banner created: docs/banner.png")
