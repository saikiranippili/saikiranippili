"""
Build a neofetch-style info card SVG (Andrew6rant style) to sit to the RIGHT of
the ASCII portrait: colored key/value rows for work experience, tech stack, and
highlights -- NOT GitHub stats (the contribution graph covers those).

Static content, hand-authored below. Lines fade/slide in on a short stagger so
it feels like the panel is printing alongside the portrait. STATIC=1 emits the
frozen state for Quick Look previews.

Long "kv" values and "bul" lines are wrapped automatically to fit the card
width, and the card height (H) is computed automatically from the content --
no more manual guessing / bumping H when you add rows.
"""
import html
import os
import textwrap

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "info-card.svg")
STATIC = bool(os.environ.get("STATIC"))

W = 480
PAD = 20
TITLEBAR_H = 30
KEY_X = PAD
VAL_X = PAD + 92
LINE_H = 20.5
WRAP_LINE_H = 17.5   # tighter spacing for wrapped continuation lines

BG = "#0d1117"
BG2 = "#111722"
FRAME = "#30363d"
MUTED = "#7d8590"
INK = "#c9d1d9"
KEY = "#ffa657"      # orange keys (matches Andrew)
SECTION = "#58a6ff"  # blue section headers
GREEN = "#3fb950"
ACCENT = "#22d3ee"

# ~0.6em per monospace character is a safe estimate at this font stack/size.
CHAR_W = 7.3
BUL_WRAP_CHARS = int((W - PAD - 14 - PAD) / CHAR_W)   # bullets start at KEY_X+14
KV_WRAP_CHARS = int((W - VAL_X - PAD) / CHAR_W)        # values start at VAL_X

# ===========================================================================
#  EDIT THIS  -- your info panel. Long values/bullets wrap automatically and
#  the card auto-sizes to fit; only bump the README's width= if you change W.
#
#  row types:
#    ("host",)              -> "you@github" header + rule
#    ("kv", key, value)     -> orange key + light value
#    ("sec", title)         -> blue "— title —" section rule
#    ("bul", text)          -> green dot + light bullet
#    ("gap",)               -> a little vertical space
# ===========================================================================
HOST = "saikiran"   # shown as  saikiran@github  in the header

ROWS = [
    ("host",),
    ("kv", "Now", "Software Engineer (Fresher)"),
    ("kv", "Status", "Seeking full-time SDE roles"),
    ("kv", "Edu", "B.Tech CSE, VSSUT Odisha '24"),
    ("gap",),
    ("sec", "Stack"),
    ("kv", "Languages", "C, C++, Python, JavaScript"),
    ("kv", "Frontend", "React.js, HTML, CSS"),
    ("kv", "Backend", "Node.js, Express.js"),
    ("kv", "Databases", "MySQL, MongoDB"),
    ("kv", "Cloud", "AWS, GCP, Git, GitHub"),
    ("gap",),
    ("sec", "Highlights"),
    ("bul", "B.Tech in Computer Science & Engineering, 2024"),
    ("bul", "Open to full-time Software Development roles"),
    ("bul", "Knowledge of Data Structures & Algorithms, OOP, DBMS, and Computer Networks"),
    ("bul", "AWS Cloud Foundations and Cisco CCNAv7 Certified"),
    ("bul", "Fluent in English, Hindi, Telugu, and Odia"),
]


def esc(s):
    return html.escape(s)


def rise(inner, i, static):
    """fade + slight upward slide, staggered by row index; freezes visible."""
    if static:
        return f"<g>{inner}</g>"
    delay = 0.15 + i * 0.06
    return (f'<g opacity="0" transform="translate(0,5)">{inner}'
            f'<animate attributeName="opacity" from="0" to="1" begin="{delay:.2f}s" dur="0.4s" fill="freeze"/>'
            f'<animateTransform attributeName="transform" type="translate" from="0 5" to="0 0" '
            f'begin="{delay:.2f}s" dur="0.4s" fill="freeze" calcMode="spline" keySplines="0.2 0.8 0.2 1"/></g>')


def layout(static):
    """Builds all row groups and returns (parts, content_bottom_y)."""
    parts = []
    y = TITLEBAR_H + 30
    for i, row in enumerate(ROWS):
        kind = row[0]
        if kind == "gap":
            y += LINE_H * 0.5
            continue
        if kind == "host":
            host = esc(HOST)
            rule_x = KEY_X + (len(HOST) + 7) * 8 + 8
            inner = (f'<text x="{KEY_X}" y="{y:.1f}" font-size="14" font-weight="700">'
                     f'<tspan fill="{GREEN}">{host}</tspan><tspan fill="{MUTED}">@</tspan>'
                     f'<tspan fill="{ACCENT}">github</tspan></text>'
                     f'<line x1="{rule_x}" y1="{y-4:.1f}" x2="{W-PAD}" y2="{y-4:.1f}" '
                     f'stroke="{FRAME}" stroke-opacity="0.8"/>')
            parts.append(rise(inner, i, static))
            y += LINE_H
        elif kind == "sec":
            title = esc(row[1])
            inner = (f'<text x="{KEY_X}" y="{y:.1f}" fill="{SECTION}" font-size="12.5" font-weight="700">'
                     f'&#8212; {title}</text>'
                     f'<line x1="{KEY_X + 12 + len(row[1])*8}" y1="{y-4:.1f}" x2="{W-PAD}" y2="{y-4:.1f}" '
                     f'stroke="{FRAME}" stroke-opacity="0.8"/>')
            parts.append(rise(inner, i, static))
            y += LINE_H
        elif kind == "kv":
            key, val_raw = row[1], row[2]
            lines = textwrap.wrap(val_raw, KV_WRAP_CHARS) or [""]
            key_text = f'<text x="{KEY_X}" y="{y:.1f}" fill="{KEY}" font-size="12.5" font-weight="700">{esc(key)}</text>'
            val_text = f'<text x="{VAL_X}" y="{y:.1f}" fill="{INK}" font-size="12.5">{esc(lines[0])}</text>'
            inner = key_text + val_text
            parts.append(rise(inner, i, static))
            y += LINE_H
            for cont in lines[1:]:
                inner = f'<text x="{VAL_X}" y="{y:.1f}" fill="{INK}" font-size="12.5">{esc(cont)}</text>'
                parts.append(rise(inner, i, static))
                y += WRAP_LINE_H
        elif kind == "bul":
            lines = textwrap.wrap(row[1], BUL_WRAP_CHARS) or [""]
            inner = (f'<circle cx="{KEY_X+3}" cy="{y-4:.1f}" r="2.5" fill="{GREEN}"/>'
                     f'<text x="{KEY_X+14}" y="{y:.1f}" fill="{INK}" font-size="12.5">{esc(lines[0])}</text>')
            parts.append(rise(inner, i, static))
            y += LINE_H
            for cont in lines[1:]:
                inner = f'<text x="{KEY_X+14}" y="{y:.1f}" fill="{INK}" font-size="12.5">{esc(cont)}</text>'
                parts.append(rise(inner, i, static))
                y += WRAP_LINE_H
    return parts, y


def build_svg():
    # pass 1: compute required content height so the card always fits
    _, content_bottom = layout(static=True)
    H = int(content_bottom + PAD)

    row_parts, content_bottom = layout(static=STATIC)

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
        f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">',
        '<defs>'
        f'<linearGradient id="ibg" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/></linearGradient></defs>',
        f'<rect width="{W}" height="{H}" rx="12" fill="url(#ibg)"/>',
        f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="none" stroke="{FRAME}"/>',
        f'<line x1="0" y1="{TITLEBAR_H}" x2="{W}" y2="{TITLEBAR_H}" stroke="{FRAME}"/>',
    ]
    for i, dotcol in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
        parts.append(f'<circle cx="{PAD + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{dotcol}"/>')
    parts.append(f'<text x="{W/2}" y="{TITLEBAR_H/2 + 4}" fill="{MUTED}" font-size="12" '
                 f'text-anchor="middle">{esc(HOST)}@github: ~$ neofetch</text>')

    parts.extend(row_parts)
    parts.append("</svg>")
    return "\n".join(parts), H, content_bottom


if __name__ == "__main__":
    svg, H, content_bottom = build_svg()
    with open(OUT, "w") as f:
        f.write(svg)
    print("wrote", OUT, len(svg), "bytes;", W, "x", H, "content_bottom", round(content_bottom))
