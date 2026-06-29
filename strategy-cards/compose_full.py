#!/usr/bin/env python3
"""
TRUE HYBRID compositor — AI text-free backdrop + 100% code-drawn text/panels/logo.
Guarantees: no text cuts, no duplicates, perfect spelling, real Viprasol logo.
Rich styling: metallic title, glassmorphic glowing panels, drawn icons, scrims.
Usage: python compose_full.py 034-tsmom
"""
import sys, pathlib, math, json
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = pathlib.Path(__file__).parent
# Each strategy lives in its OWN folder: strategy-cards/<sid>/{scene.png, card.png, card-45.png, captions.json}
# No shared output/ — keeps every strategy self-contained, zero confusion.
LOGO = r"C:\Users\viprasol\Desktop\viprasol-website\assets\images\logo.png"
F    = r"C:\Windows\Fonts"
W, H = 1024, 1536

# palette
WHITE = (236, 241, 245)
TEAL  = (64, 214, 206)
TEALD = (28, 150, 150)
GOLD  = (232, 184, 92)
GREY  = (150, 163, 173)
LGREY = (206, 214, 221)
RED   = (235, 96, 96)
GREEN = (76, 210, 132)

def bz(name, size):
    f = ImageFont.truetype(f"{F}\\bahnschrift.ttf", size)
    try: f.set_variation_by_name(name)
    except Exception: pass
    return f
def arial(size, bold=False):
    return ImageFont.truetype(f"{F}\\{'arialbd' if bold else 'arial'}.ttf", size)

COND_B  = lambda s: bz("Bold Condensed", s)
COND_SB = lambda s: bz("SemiBold Condensed", s)
COND    = lambda s: bz("Condensed", s)

# ---------- helpers ----------
def vgrad_scrim(size, c, a_top, a_bot):
    w, h = size
    g = Image.new("L", (1, h))
    for y in range(h):
        g.putpixel((0, y), int(a_top + (a_bot - a_top) * y / max(1, h - 1)))
    a = g.resize((w, h))
    img = Image.new("RGBA", (w, h), c + (0,))
    img.putalpha(a)
    return img

def hgrad_scrim(size, c, a_left, a_right):
    w, h = size
    g = Image.new("L", (w, 1))
    for x in range(w):
        g.putpixel((x, 0), int(a_left + (a_right - a_left) * x / max(1, w - 1)))
    a = g.resize((w, h))
    img = Image.new("RGBA", (w, h), c + (0,))
    img.putalpha(a)
    return img

def tracked(draw, xy, text, fnt, fill, tracking=0, anchor="la", shadow=None):
    widths = [draw.textlength(c, font=fnt) for c in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x, y = xy
    if anchor in ("ma", "mm"): x -= total / 2
    if anchor in ("ra",): x -= total
    for c, w in zip(text, widths):
        if shadow:
            draw.text((x + shadow[0], y + shadow[1]), c, font=fnt, fill=shadow[2], anchor="la")
        draw.text((x, y), c, font=fnt, fill=fill + (255,) if len(fill)==3 else fill, anchor="la")
        x += w + tracking
    return total

def metallic_text(base, xy, text, fnt, anchor="mm", tracking=2):
    """Render chrome/metallic gradient text via a mask."""
    d0 = ImageDraw.Draw(base)
    widths = [d0.textlength(c, font=fnt) for c in text]
    total = sum(widths) + tracking * (len(text) - 1)
    asc, desc = fnt.getmetrics()
    th = asc + desc
    mask = Image.new("L", (int(total) + 8, th + 8), 0)
    md = ImageDraw.Draw(mask)
    x = 4
    for c, w in zip(text, widths):
        md.text((x, 4), c, font=fnt, fill=255)
        x += w + tracking
    # silver vertical gradient
    grad = Image.new("RGB", (1, th + 8))
    stops = [(0,(245,248,252)),(0.30,(150,160,170)),(0.50,(232,238,244)),(0.62,(120,130,140)),(1.0,(205,212,220))]
    for y in range(th + 8):
        t = y / (th + 7)
        for i in range(len(stops)-1):
            a,ca = stops[i]; b,cb = stops[i+1]
            if a <= t <= b:
                f = (t-a)/(b-a)
                col = tuple(int(ca[k]+(cb[k]-ca[k])*f) for k in range(3)); break
        else: col = stops[-1][1]
        grad.putpixel((0,y), col)
    grad = grad.resize((int(total)+8, th+8))
    gx = int(xy[0] - total/2) if anchor in ("mm","ma") else int(xy[0])
    gy = int(xy[1] - (th+8)/2) if anchor in ("mm",) else int(xy[1])
    # soft dark shadow for depth
    sh = Image.new("RGBA", base.size, (0,0,0,0))
    sh.paste((0,0,0,180), (gx+2, gy+3), mask)
    sh = sh.filter(ImageFilter.GaussianBlur(2))
    base.alpha_composite(sh)
    base.paste(grad, (gx, gy), mask)

def glass_panel(base, box, radius=18, fill=(12,22,30,165), border=TEAL, glow=TEAL, bw=2, glow_a=70):
    x0,y0,x1,y1 = box
    # outer glow
    g = Image.new("RGBA", base.size, (0,0,0,0))
    gd = ImageDraw.Draw(g)
    gd.rounded_rectangle([x0-3,y0-3,x1+3,y1+3], radius=radius+3, fill=glow+(glow_a,))
    g = g.filter(ImageFilter.GaussianBlur(9))
    base.alpha_composite(g)
    # panel
    p = Image.new("RGBA", base.size, (0,0,0,0))
    pd = ImageDraw.Draw(p)
    pd.rounded_rectangle(box, radius=radius, fill=fill, outline=border+(180,), width=bw)
    base.alpha_composite(p)

def icon_box(base, x, y, s, drawer):
    glass_panel(base, [x, y, x+s, y+s], radius=12, fill=(14,30,36,180), glow=TEAL, glow_a=55, bw=2)
    d = ImageDraw.Draw(base)
    drawer(d, x, y, s)

# --- simple line icons (teal) ---
def i_trend(d,x,y,s):
    p=[(x+9,y+s-12),(x+s*0.4,y+s*0.55),(x+s*0.6,y+s*0.66),(x+s-9,y+11)]
    d.line(p, fill=TEAL, width=3, joint="curve")
    d.polygon([(x+s-16,y+11),(x+s-9,y+11),(x+s-9,y+18)], fill=TEAL)
def i_scale(d,x,y,s):
    cx=x+s/2; d.line([(cx,y+10),(cx,y+s-10)],fill=TEAL,width=3)
    d.line([(x+12,y+18),(x+s-12,y+18)],fill=TEAL,width=3)
    for bx in (x+12,x+s-12):
        d.arc([bx-9,y+18,bx+9,y+34],0,180,fill=TEAL,width=3)
    d.ellipse([cx-4,y+8,cx+4,y+16],fill=TEAL)
def i_globe(d,x,y,s):
    b=[x+11,y+11,x+s-11,y+s-11]; d.ellipse(b,outline=TEAL,width=3)
    cx=(b[0]+b[2])/2
    d.line([(cx,b[1]),(cx,b[3])],fill=TEAL,width=2)
    d.ellipse([cx-((b[2]-b[0])/2),b[1]+6,cx+((b[2]-b[0])/2),b[3]-6],outline=TEAL,width=2)
    d.line([(b[0],(b[1]+b[3])/2),(b[2],(b[1]+b[3])/2)],fill=TEAL,width=2)
def i_refresh(d,x,y,s):
    b=[x+12,y+12,x+s-12,y+s-12]
    d.arc(b,40,330,fill=TEAL,width=3)
    d.polygon([(x+s-14,y+10),(x+s-6,y+18),(x+s-16,y+22)],fill=TEAL)
def i_shield(d,x,y,s):
    cx=x+s/2; top=y+10; w=s*0.32
    d.polygon([(cx,top),(cx+w,top+8),(cx+w,y+s*0.55),(cx,y+s-10),(cx-w,y+s*0.55),(cx-w,top+8)],outline=TEAL,width=3)
    d.line([(cx-7,y+s*0.5),(cx-2,y+s*0.58),(cx+9,y+s*0.4)],fill=TEAL,width=3,joint="curve")
def i_clock(d,x,y,s):
    b=[x+11,y+11,x+s-11,y+s-11]; d.ellipse(b,outline=TEAL,width=3)
    cx=(b[0]+b[2])/2; cy=(b[1]+b[3])/2
    d.line([(cx,cy),(cx,cy-9)],fill=TEAL,width=3); d.line([(cx,cy),(cx+7,cy+3)],fill=TEAL,width=3)

def check(d, x, y, r=11):
    d.ellipse([x,y,x+2*r,y+2*r], outline=GREEN, width=3)
    d.line([(x+r*0.55,y+r),(x+r*0.9,y+r*1.4),(x+r*1.5,y+r*0.6)], fill=GREEN, width=3, joint="curve")

# ---------- data ----------
STRATS = {
    "034-tsmom": {
        "tier": "TIER 1 · ELITE",
        "h1": "STOP CHASING NOISE.",
        "h2": [("FOLLOW THE ", WHITE), ("TREND.", TEAL)],
        "tag": "LET THE DATA DECIDE — LONG, SHORT, OR FLAT.",
        "kicker": "THE PEER-REVIEWED BACKBONE OF TREND-FOLLOWING",
        "title": "TIME-SERIES MOMENTUM",
        "sub": "ANALYZE   ·   RANK   ·   SIZE   ·   REBALANCE",
        "features": [
            (i_trend,  "12-MONTH SIGNAL", "Trade the sign of the past year's return"),
            (i_scale,  "INVERSE-VOL SIZING", "Every position scaled to equal risk"),
            (i_globe,  "GLOBAL DIVERSIFICATION", "Commodities, equities, bonds & FX"),
            (i_refresh,"MONTHLY REBALANCE", "Fully mechanical, zero discretion"),
            (i_shield, "PEER-REVIEWED", "Journal of Financial Economics, 2012"),
            (i_clock,  "A CENTURY STUDIED", "Researched across 140+ years of data"),
        ],
        "stats": [
            ("12 / 1", "MONTH LOOKBACK  ·  HOLD", TEAL),
            ("58",     "GLOBAL FUTURES MARKETS", TEAL),
            ("4",      "ASSET CLASSES", GOLD),
        ],
        "decision": ("100% SYSTEMATIC", "NO FORECASTING  ·  NO EMOTION"),
        "why": ["SYSTEMATIC", "DIVERSIFIED", "RISK-SCALED", "MECHANICAL", "RESEARCHED"],
        "evidence_h": "BUILT ON EVIDENCE, NOT OPINION.",
        "evidence": ["Peer-reviewed — JFE, 2012", "58 markets, 4 asset classes",
                     "Studied across 140+ years of data", "One mechanical rulebook"],
        "cta1": "WANT THE COMPLETE ALGO + RESEARCH FILE?",
        "cta2": "DM VIPRASOL  \"TREND\"  —  let's build it",
        "disclaimer": ("Strategy logic documented in Moskowitz, Ooi & Pedersen (2012), Journal of Financial Economics. "
                       "Shared for education and research reference only — not investment advice. 1 of 440 in our research library."),
    },
    "035-xsmom": {
        "tier": "TIER 1 · ELITE",
        "h1": "BUY THE WINNERS.",
        "h2": [("SHORT THE ", WHITE), ("LOSERS.", GOLD)],
        "tag": "RELATIVE STRENGTH — RANKED, NOT GUESSED.",
        "kicker": "THE FACTOR THAT BROKE THE EFFICIENT MARKET HYPOTHESIS",
        "title": "CROSS-SECTIONAL MOMENTUM",
        "sub": "RANK   ·   SORT   ·   LONG-SHORT   ·   REBALANCE",
        "features": [
            (i_trend,  "6-MONTH FORMATION", "Rank each stock by trailing 6-month return"),
            (i_scale,  "DECILE LONG-SHORT", "Long top 10% winners, short bottom 10% losers"),
            (i_refresh,"SKIP THE LAST MONTH", "Avoid short-term reversal & bid-ask noise"),
            (i_globe,  "OVERLAPPING COHORTS", "Six rolling baskets — only 1/6 turns each month"),
            (i_shield, "PEER-REVIEWED", "Journal of Finance, 1993 · JFE, 2016"),
            (i_clock,  "REPLICATED GLOBALLY", "Equities, currencies, commodities & bonds"),
        ],
        "stats": [
            ("6 / 6", "MONTH FORMATION  ·  HOLD", TEAL),
            ("10",    "DECILE LONG-SHORT CUT", TEAL),
            ("4×4",   "PARAMETER GRID TESTED", GOLD),
        ],
        "decision": ("DOLLAR-NEUTRAL", "LONG-SHORT  ·  MONTHLY REBALANCE"),
        "why": ["RANKED", "RELATIVE", "DOLLAR-NEUTRAL", "MECHANICAL", "REPLICATED"],
        "evidence_h": "BUILT ON EVIDENCE, NOT OPINION.",
        "evidence": ["Jegadeesh & Titman — JF, 1993", "Out-of-sample confirmed — JF, 2001",
                     "Standardized as Carhart UMD factor", "Crash-managed variants doubled risk-adjusted profile"],
        "cta1": "WANT THE COMPLETE ALGO + RESEARCH FILE?",
        "cta2": "DM VIPRASOL  \"WINNERS\"  —  let's build it",
        "disclaimer": ("Strategy logic documented in Jegadeesh & Titman (1993), Journal of Finance, with crash-management refinements in Daniel & Moskowitz (2016), JFE. "
                       "Shared for education and research reference only — not investment advice. 1 of 440 in our research library."),
    },
}

ICONS = {"trend": i_trend, "scale": i_scale, "globe": i_globe, "refresh": i_refresh, "shield": i_shield, "clock": i_clock}
COLORS = {"TEAL": TEAL, "GOLD": GOLD, "GREEN": GREEN, "WHITE": WHITE}

def _from_json(entry):
    """Convert a digest JSON entry into the STRATS dict shape."""
    return {
        "tier": "TIER 1 · ELITE",
        "h1": entry["h1"],
        "h2": [(entry["h2_white"], WHITE), (entry["h2_accent"], COLORS[entry.get("h2_color","TEAL")])],
        "tag": entry["tag"],
        "kicker": entry["kicker"],
        "title": entry["title"],
        "sub": entry["sub"],
        "features": [(ICONS[f["icon"]], f["title"], f["desc"]) for f in entry["features"]],
        "stats": [(s["num"], s["label"], COLORS[s.get("color","TEAL")]) for s in entry["stats"]],
        "decision": (entry["decision_top"], entry["decision_sub"]),
        "why": entry["why"],
        "evidence_h": entry.get("evidence_h", "BUILT ON EVIDENCE, NOT OPINION."),
        "evidence": entry["evidence"],
        "cta1": entry.get("cta1", "WANT THE COMPLETE ALGO + RESEARCH FILE?"),
        "cta2": entry.get("cta2", f'DM VIPRASOL  "{entry["dm_keyword"]}"  —  let\'s build it'),
        "disclaimer": entry["disclaimer"],
    }

def _load_strategy(sid):
    if sid in STRATS: return STRATS[sid]
    js = ROOT / "strategies.json"
    if js.exists():
        for e in json.loads(js.read_text(encoding="utf-8")):
            if e["sid"] == sid: return _from_json(e)
    raise KeyError(f"strategy '{sid}' not in STRATS dict or strategies.json")

def compose(sid):
    s = _load_strategy(sid)
    strat_dir = ROOT / sid
    strat_dir.mkdir(exist_ok=True)
    base = Image.open(strat_dir / "scene.png").convert("RGBA").resize((W, H))

    # scrims for legibility
    base.alpha_composite(vgrad_scrim((W, 470), (3,8,13), 232, 40), (0, 0))            # top
    base.alpha_composite(hgrad_scrim((520, 650), (3,8,13), 224, 0), (0, 455))         # left col
    base.alpha_composite(vgrad_scrim((W, 120), (3,8,13), 0, 235), (0, 1070))          # bottom fade
    bottom = Image.new("RGBA", (W, 360), (3,8,13,240)); base.alpha_composite(bottom, (0, 1185))

    d = ImageDraw.Draw(base)
    cx = W // 2

    # ---- header ----
    logo = Image.open(LOGO).convert("RGBA").resize((74, 74), Image.LANCZOS)
    base.alpha_composite(logo, (40, 34)); d = ImageDraw.Draw(base)
    tracked(d, (126, 52), "VIPRASOL  TECH", COND_B(26), WHITE, tracking=1)
    tracked(d, (128, 84), "VERIFIED STRATEGY SERIES", COND_SB(16), TEAL, tracking=3)
    # tier pill (top-right)
    tf = COND_SB(18); tw = d.textlength(s["tier"], font=tf) + 36
    glass_panel(base, [W-44-tw, 44, W-44, 86], radius=21, fill=(36,28,8,180), border=GOLD, glow=GOLD, glow_a=55)
    d = ImageDraw.Draw(base); d.text((W-44-tw/2, 65), s["tier"], font=tf, fill=GOLD, anchor="mm")

    # headline
    tracked(d, (cx, 120), s["h1"], COND_B(58), WHITE, tracking=1, anchor="ma", shadow=(2,2,(0,0,0,200)))
    # h2 colored segments centered
    h2f = COND_B(58)
    seg_w = [d.textlength(t, font=h2f) for t,_ in s["h2"]]
    x = cx - sum(seg_w)/2
    for (t,c),wd in zip(s["h2"], seg_w):
        d.text((x+2,186), t, font=h2f, fill=(0,0,0,200), anchor="la")
        d.text((x,184), t, font=h2f, fill=c, anchor="la"); x += wd
    # tagline + kicker
    tracked(d, (cx, 256), s["tag"], COND_SB(20), GREY, tracking=2, anchor="ma")
    tracked(d, (cx, 286), s["kicker"], COND_SB(17), TEAL, tracking=2, anchor="ma")
    # metallic title (auto-fit width)
    tsize = 76
    while True:
        tf2 = COND_B(tsize)
        if ImageDraw.Draw(base).textlength(s["title"], font=tf2) + 2*1 <= W-80 or tsize<=48: break
        tsize -= 2
    metallic_text(base, (cx, 350), s["title"], COND_B(tsize), anchor="mm", tracking=1)
    d = ImageDraw.Draw(base)
    tracked(d, (cx, 404), s["sub"], COND_SB(21), LGREY, tracking=3, anchor="ma")

    # ---- feature column ----
    fy = 470
    for drawer, title, desc in s["features"]:
        icon_box(base, 44, fy, 50, drawer); d = ImageDraw.Draw(base)
        tracked(d, (110, fy-2), title, COND_B(25), WHITE, tracking=1)
        d.text((110, fy+30), desc, font=arial(16), fill=GREY, anchor="la")
        fy += 100

    # ---- stat panels (right) ----
    sx0, sx1 = 596, 1000
    sy = 482
    for num, lab, col in s["stats"]:
        glass_panel(base, [sx0, sy, sx1, sy+104], radius=16, fill=(10,20,28,180), glow=col, glow_a=60)
        d = ImageDraw.Draw(base)
        d.text((sx0+22, sy+18), num, font=COND_B(50), fill=col, anchor="la")
        tracked(d, (sx0+24, sy+76), lab, COND_SB(16), GREY, tracking=2)
        sy += 122
    # decision pill
    glass_panel(base, [sx0, sy, sx1, sy+92], radius=16, fill=(8,28,18,190), border=GREEN, glow=GREEN, glow_a=70)
    d = ImageDraw.Draw(base)
    d.ellipse([sx0+20, sy+34, sx0+34, sy+48], fill=GREEN)
    tracked(d, (sx0+48, sy+22), s["decision"][0], COND_B(28), GREEN, tracking=1)
    tracked(d, (sx0+48, sy+58), s["decision"][1], COND_SB(16), LGREY, tracking=2)

    # ---- why row ----
    wy = 1098
    tracked(d, (cx, wy), "WHY THIS EDGE IS DIFFERENT", COND_B(24), TEAL, tracking=4, anchor="ma")
    n = len(s["why"]); x0, x1 = 60, W-60; slot = (x1-x0)/n
    for i, lab in enumerate(s["why"]):
        c = x0 + slot*(i+0.5)
        # small diamond marker
        d.regular_polygon((c, wy+50, 9), 4, rotation=0, outline=GOLD, width=2)
        tracked(d, (c, wy+70), lab, COND_SB(18), LGREY, tracking=1, anchor="ma")

    # ---- evidence (left) ----
    ey = 1235
    tracked(d, (50, ey), s["evidence_h"], COND_B(33), WHITE, tracking=1)
    ly = ey + 56
    for item in s["evidence"]:
        check(d, 54, ly, r=11)
        d.text((92, ly-2), item, font=arial(19), fill=LGREY, anchor="la")
        ly += 42

    # ---- CTA box (right) ----
    glass_panel(base, [556, ey+44, 996, ey+196], radius=18, fill=(10,26,30,200), glow=TEAL, glow_a=70)
    d = ImageDraw.Draw(base)
    lg2 = Image.open(LOGO).convert("RGBA").resize((52,52), Image.LANCZOS)
    base.alpha_composite(lg2, (574, ey+58)); d = ImageDraw.Draw(base)
    tracked(d, (640, ey+62), s["cta1"], COND_B(21), WHITE, tracking=1)
    d.text((640, ey+92), "Limited build slots for serious traders.", font=arial(15), fill=GREY, anchor="la")
    glass_panel(base, [574, ey+128, 978, ey+176], radius=14, fill=(20,120,118,235), border=TEAL, glow=TEAL, glow_a=80)
    d = ImageDraw.Draw(base)
    d.text((776, ey+152), s["cta2"], font=COND_B(22), fill=(7,18,20), anchor="mm")

    # ---- disclaimer ----
    df = arial(14); words = s["disclaimer"].split(" "); line=""; lines=[]
    for w in words:
        if d.textlength(line+" "+w, font=df) > W-90: lines.append(line.strip()); line=w
        else: line += " "+w
    lines.append(line.strip())
    fy2 = H - 16 - len(lines)*19
    for ln in lines:
        d.text((cx, fy2), ln, font=df, fill=(120,132,142), anchor="ma"); fy2 += 19

    out = strat_dir / "card.png"
    base.convert("RGB").save(out, quality=95)
    print("saved ->", out)

if __name__ == "__main__":
    compose(sys.argv[1] if len(sys.argv) > 1 else "034-tsmom")
