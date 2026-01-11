from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os, random, datetime, textwrap

# ---------- OUTPUT ----------
OUT_PATH = "docs/terminal_readme.png"
os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)

# ---------- CANVAS ----------
W, H = 1600, 2200                 # "full page" feel
PADDING_X, PADDING_Y = 70, 70
BG = (8, 8, 8)                    # near-black terminal
FG = (245, 245, 245)              # terminal white
DIM = (200, 200, 200)             # slightly dimmer system text
ACCENT = (180, 180, 180)          # subtle accent (still gray/white)

# ---------- FONT (macOS terminal look) ----------
def load_font(size: int):
    candidates = [
        "/System/Library/Fonts/Menlo.ttc",          # macOS Terminal default
        "/System/Library/Fonts/Monaco.ttf",         # classic Mac terminal
        "/System/Library/Fonts/Supplemental/Courier New.ttf",
    ]
    for p in candidates:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

FONT_SIZE = 34
FONT = load_font(FONT_SIZE)

def load_bold_font(size: int):
    candidates = [
        "/System/Library/Fonts/Menlo-Bold.ttc",
        "/System/Library/Fonts/Monaco.ttf",  # Monaco is heavier by default
    ]
    for p in candidates:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return FONT

BOLD_FONT = load_bold_font(FONT_SIZE)

# ---------- CONTENT ----------
now = datetime.datetime.now()
last_login = now.strftime("Last login: %a %b %d %H:%M:%S on console")

# Use (text, color, style). style: "normal" or "command"
lines = [
    ("$ mythmatch --discover", FG, "command"),
    ("", FG, "normal"),

    ("What archetype are you actually acting out?", FG, "normal"),
    ("", FG, "normal"),

    ("MythMatch uses AI to match you with myths and archetypal characters", ACCENT, "normal"),
    ("from world mythology based on your personality and psychology.", ACCENT, "normal"),
    ("", FG, "normal"),

    ("Answer questions about yourself, and discover the myths", ACCENT, "normal"),
    ("that mirror your journey.", ACCENT, "normal"),
    ("", FG, "normal"),

    ("$ mythmatch --about", FG, "command"),
    ("", FG, "normal"),

    ("What is MythMatch?", FG, "normal"),
    ("", FG, "normal"),

    ("A personality-based mythology matching system that connects you", ACCENT, "normal"),
    ("with stories from across cultures:", ACCENT, "normal"),
    ("Greek, Norse, Egyptian, Hindu, Celtic, and more.", ACCENT, "normal"),
    ("", FG, "normal"),

    ("$ mythmatch --status", FG, "command"),
    ("", FG, "normal"),

    ("Project Status", FG, "normal"),
    ("", FG, "normal"),

    ("[Phase 1] Data Extraction     — In Progress", DIM, "normal"),
    ("Digitizing and extracting content from mythology encyclopedia.", DIM, "normal"),
    ("", FG, "normal"),

    ("[Phase 2] Myth Profiling      — Planned", DIM, "normal"),
    ("Creating psychological profiles for mythological characters and stories.", DIM, "normal"),
    ("", FG, "normal"),

    ("[Phase 3] Matching System     — Planned", DIM, "normal"),
    ("Building the personality-to-myth matching algorithm.", DIM, "normal"),
    ("", FG, "normal"),

    ("$ mythmatch --tech", FG, "command"),
    ("", FG, "normal"),

    ("Tech Stack", FG, "normal"),
    ("Python 3.8+", DIM, "normal"),
    ("Claude / GPT", DIM, "normal"),
    ("LangChain", DIM, "normal"),
    ("ChromaDB", DIM, "normal"),
    ("RAG", DIM, "normal"),
    ("", FG, "normal"),

    ("$ mythmatch --install", FG, "command"),
    ("", FG, "normal"),

    ("Installation", FG, "normal"),
    ("git clone https://github.com/yourusername/mythmatch.git", DIM, "normal"),
    ("cd mythmatch", DIM, "normal"),
    ("python3 -m venv M_venv", DIM, "normal"),
    ("source M_venv/bin/activate", DIM, "normal"),
    ("pip install -r requirements.txt", DIM, "normal"),
    ("", FG, "normal"),

    ("$ mythmatch --license", FG, "command"),
    ("", FG, "normal"),

    ("License", FG, "normal"),
    ("MIT", DIM, "normal"),
    ("", FG, "normal"),

    ("$ ", FG, "normal"),
]

# ---------- RENDER ----------
img = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img)

line_gap = int(FONT_SIZE * 0.60)
y = PADDING_Y
max_text_width = W - 2 * PADDING_X

def draw_wrapped(text, color, y, style="normal"):
    """
    Draw wrapped text at (PADDING_X, y). If style == "command",
    draw in bold and add extra spacing after the line.
    """
    font = FONT
    extra_spacing = 0

    if style == "command":
        font = BOLD_FONT
        extra_spacing = int(FONT_SIZE * 0.9)  # extra gap after command lines

    # Empty line => just advance one line
    if text.strip() == "":
        return y + FONT_SIZE + line_gap + extra_spacing

    avg_char_w = draw.textbbox((0, 0), "M" * 10, font=font)[2] / 10
    max_chars = max(10, int(max_text_width / avg_char_w))

    for wrapped in textwrap.wrap(
        text,
        width=max_chars,
        replace_whitespace=False,
        drop_whitespace=False
    ):
        # If bold font isn't available, fake bold by drawing twice with 1px offset
        if style == "command" and font == FONT:
            draw.text((PADDING_X, y), wrapped, fill=color, font=font)
            draw.text((PADDING_X + 1, y), wrapped, fill=color, font=font)
        else:
            draw.text((PADDING_X, y), wrapped, fill=color, font=font)
        y += FONT_SIZE + line_gap

    return y + extra_spacing

for text, color, style in lines:
    y = draw_wrapped(text, color, y, style)

# ---------- SUBTLE TERMINAL "SCREEN" EFFECT ----------
px = img.load()
noise_points = int(W * H * 0.0025)  # adjust up/down
for _ in range(noise_points):
    rx = random.randint(0, W - 1)
    ry = random.randint(0, H - 1)
    r, g, b = px[rx, ry]
    jitter = random.randint(-10, 10)
    px[rx, ry] = (
        max(0, min(255, r + jitter)),
        max(0, min(255, g + jitter)),
        max(0, min(255, b + jitter)),
    )

img = img.filter(ImageFilter.GaussianBlur(radius=0.35))

img.save(OUT_PATH)
print(f"✅ Created {OUT_PATH}")
