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

# ---------- CONTENT ----------
now = datetime.datetime.now()
last_login = now.strftime("Last login: %a %b %d %H:%M:%S on console")

# You can edit these lines to match your exact vibe.
lines = [
    ("$ mythmatch --discover", FG),
    ("", FG),

    ("MYTHMATCH", FG),
    ("", FG),

    ("\"What archetype are you actually acting out?\"", FG),
    ("", FG),

    ("MythMatch uses AI to match you with myths and archetypal characters", ACCENT),
    ("from world mythology based on your personality and psychology.", ACCENT),
    ("", FG),

    ("Answer questions about yourself, and discover the myths", ACCENT),
    ("that mirror your journey.", ACCENT),
    ("", FG),

    ("$ mythmatch --about", FG),
    ("", FG),

    ("What is MythMatch?", FG),
    ("", FG),

    ("A personality-based mythology matching system that connects you", ACCENT),
    ("with stories from across cultures:", ACCENT),
    ("Greek, Norse, Egyptian, Hindu, Celtic, and more.", ACCENT),
    ("", FG),

    ("$ mythmatch --status", FG),
    ("", FG),

    ("Project Status", FG),
    ("", FG),

    ("[Phase 1] Data Extraction     — In Progress", DIM),
    ("Digitizing and extracting content from mythology encyclopedia.", DIM),
    ("", FG),

    ("[Phase 2] Myth Profiling      — Planned", DIM),
    ("Creating psychological profiles for mythological characters and stories.", DIM),
    ("", FG),

    ("[Phase 3] Matching System    — Planned", DIM),
    ("Building the personality-to-myth matching algorithm.", DIM),
    ("", FG),

    ("$ mythmatch --tech", FG),
    ("", FG),

    ("Tech Stack", FG),
    ("Python 3.8+", DIM),
    ("Claude / GPT", DIM),
    ("LangChain", DIM),
    ("ChromaDB", DIM),
    ("RAG", DIM),
    ("", FG),

    ("$ mythmatch --install", FG),
    ("", FG),

    ("Installation", FG),
    ("git clone https://github.com/yourusername/mythmatch.git", DIM),
    ("cd mythmatch", DIM),
    ("python3 -m venv M_venv", DIM),
    ("source M_venv/bin/activate", DIM),
    ("pip install -r requirements.txt", DIM),
    ("", FG),

    ("$ mythmatch --license", FG),
    ("", FG),

    ("License", FG),
    ("MIT", DIM),
    ("", FG),

    ("$ ", FG),
]


# ---------- RENDER ----------
img = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img)

line_gap = int(FONT_SIZE * 0.60)
y = PADDING_Y
max_text_width = W - 2 * PADDING_X

def draw_wrapped(text, color, y):
    # wrap by pixel width using a rough character estimate
    # (monospace makes this stable)
    avg_char_w = draw.textbbox((0, 0), "M" * 10, font=FONT)[2] / 10
    max_chars = max(10, int(max_text_width / avg_char_w))
    for wrapped in textwrap.wrap(text, width=max_chars, replace_whitespace=False, drop_whitespace=False):
        draw.text((PADDING_X, y), wrapped, fill=color, font=FONT)
        y += FONT_SIZE + line_gap
    return y

for text, color in lines:
    y = draw_wrapped(text, color, y)

# ---------- SUBTLE TERMINAL "SCREEN" EFFECT ----------
# Light noise for realism
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

# Very slight blur to mimic a screenshot (optional)
img = img.filter(ImageFilter.GaussianBlur(radius=0.35))

img.save(OUT_PATH)
print(f"✅ Created {OUT_PATH}")
