from PIL import Image, ImageDraw, ImageFont
import os

# ---------- CONFIG ----------
WIDTH = 1600
HEIGHT = 420
BG_COLOR = "#000000"
TITLE_COLOR = "#FFFFFF"
SUBTITLE_COLOR = "#BBBBBB"

TITLE_TEXT = "मिथमैच"
SUBTITLE_TEXT = "Every person has a myth waiting to be discovered"

OUTPUT_PATH = "docs/banner.png"

# ---------- FONT LOADING ----------
def load_font(size, preferred_paths):
    for path in preferred_paths:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    print("⚠️  No preferred font found, using default font")
    return ImageFont.load_default()

# macOS Devanagari-capable fonts (in priority order)
TITLE_FONT_PATHS = [
    "/System/Library/Fonts/Supplemental/NotoSansDevanagari-Regular.ttf",
    "/System/Library/Fonts/DevanagariSangamMN.ttf",
    "/Library/Fonts/NotoSansDevanagari-Regular.ttf",
]

SUBTITLE_FONT_PATHS = [
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/System/Library/Fonts/SFNS.ttf",
]

title_font = load_font(96, TITLE_FONT_PATHS)
subtitle_font = load_font(36, SUBTITLE_FONT_PATHS)

# ---------- IMAGE ----------
os.makedirs("docs", exist_ok=True)

img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
draw = ImageDraw.Draw(img)

# ---------- CENTERED TITLE ----------
title_bbox = draw.textbbox((0, 0), TITLE_TEXT, font=title_font)
title_width = title_bbox[2] - title_bbox[0]
title_x = (WIDTH - title_width) // 2
title_y = 120

draw.text((title_x, title_y), TITLE_TEXT, fill=TITLE_COLOR, font=title_font)

# ---------- CENTERED SUBTITLE ----------
subtitle_bbox = draw.textbbox((0, 0), SUBTITLE_TEXT, font=subtitle_font)
subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
subtitle_x = (WIDTH - subtitle_width) // 2
subtitle_y = title_y + 120

draw.text((subtitle_x, subtitle_y), SUBTITLE_TEXT, fill=SUBTITLE_COLOR, font=subtitle_font)

# ---------- SAVE ----------
img.save(OUTPUT_PATH)
print(f"✅ Banner created: {OUTPUT_PATH}")
