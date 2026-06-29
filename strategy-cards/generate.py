#!/usr/bin/env python3
"""
Viprasol — Trading Strategy reference-image generator.
Uses OpenAI gpt-image-1 to render premium dark-fintech infographics
from the verified 440-strategy knowledge base.

Usage:
  python generate.py <prompt_id> <strategy-id>   # saves -> strategy-cards/<strategy-id>/scene.png
  python generate.py <prompt_id>                 # no sid -> saves to _scratch/ (scene not yet assigned)
All numbers in prompts are pulled from the verified dossiers ONLY.
"""
import os, sys, json, base64, urllib.request, urllib.error, pathlib

ROOT = pathlib.Path(__file__).parent

# --- load API key from gitignored .env ---
def load_key():
    env = ROOT / ".env"
    for line in env.read_text().splitlines():
        if line.startswith("OPENAI_API_KEY="):
            return line.split("=", 1)[1].strip()
    raise SystemExit("OPENAI_API_KEY not found in .env")

KEY = load_key()

# --- prompt library (verified-stats only) ---
PROMPTS = {
    "backdrop-ranked": {
        "size": "1024x1536",
        "prompt": (
            "Premium photoreal cinematic 3D render, vertical poster BACKDROP only. In the LOWER-RIGHT quadrant: a sleek "
            "white-and-chrome humanoid AI trading analyst standing in three-quarter view next to a large floating holographic "
            "leaderboard / vertical ranking column of glowing horizontal bars sorted from top (bright green, longest, winners) "
            "down to bottom (deep red, shortest, losers). Faint translucent bar-stacks suggest deciles. Soft glowing teal-and-gold "
            "rim light, dark navy-to-black room, volumetric haze, glossy floor reflections. "
            "CRITICAL COMPOSITION: the ENTIRE LEFT HALF and the TOP THIRD of the image must be dark, calm, EMPTY negative space "
            "(deep navy-to-black gradient) reserved for text — absolutely no objects there. "
            "Absolutely NO text, NO numbers, NO letters, NO logos, NO UI labels anywhere. Clean, uncluttered, high-end."
        ),
    },
    "backdrop-robot": {
        "size": "1024x1536",
        "prompt": (
            "Premium photoreal cinematic 3D render, vertical poster BACKDROP only. A sleek white-and-chrome humanoid AI "
            "trading robot with faint glowing teal eyes sits at a dark futuristic glass desk in the LOWER-RIGHT quadrant of the "
            "frame, seen three-quarter from behind/side, facing toward soft glowing screens. In the RIGHT background a large, "
            "soft-focus rising teal-and-green trend line with candlesticks glows gently. "
            "CRITICAL COMPOSITION: the ENTIRE LEFT HALF and the TOP THIRD of the image must be dark, calm, EMPTY negative space "
            "(deep navy-to-black gradient) reserved for text — no objects there. Dramatic teal and warm-gold rim lighting, "
            "volumetric haze, glossy floor reflections, cinematic depth. "
            "Absolutely NO text, NO numbers, NO letters, NO logos, NO UI labels anywhere. Clean, uncluttered, high-end."
        ),
    },
    "poster-034-tsmom": {
        "size": "1024x1536",
        "prompt": (
            "A premium, dense, high-end financial marketing INFOGRAPHIC POSTER, vertical, in the exact style of a polished "
            "product-launch graphic: dark navy-to-black background, vibrant teal/green/gold accents, glowing glassmorphic panels, "
            "subtle 3D depth, drop shadows, cinematic lighting. Clean bold condensed sans-serif typography, perfectly spelled.\n\n"
            "TOP: a big bold two-line headline — line 1 'STOP CHASING NOISE.' (white, the word NOISE in red), "
            "line 2 'FOLLOW THE TREND.' (the word TREND in bright green). Under it a thin tagline 'LET THE DATA DECIDE — LONG, SHORT, OR FLAT.' "
            "Then a small teal kicker 'INTRODUCING THE PEER-REVIEWED BACKBONE OF TREND-FOLLOWING' and a HUGE metallic-silver chrome title "
            "'TIME-SERIES MOMENTUM', then a sub-line 'ANALYZE.  RANK.  SIZE.  REBALANCE.'\n\n"
            "LEFT COLUMN: a vertical list of 6 feature rows, each a small glowing teal icon in a rounded square + a bold title + one tiny line of description:\n"
            "'12-MONTH SIGNAL — trade the sign of the past year's return', "
            "'INVERSE-VOL SIZING — every position scaled to equal risk', "
            "'58 GLOBAL MARKETS — commodities, equities, bonds & FX', "
            "'MONTHLY REBALANCE — fully mechanical, zero discretion', "
            "'CRISIS ALPHA — strongest in extreme up & down quarters', "
            "'A CENTURY OF PROOF — positive in every decade since 1880'.\n\n"
            "CENTER-RIGHT: a photoreal sleek white humanoid AI trading robot sitting at a futuristic desk facing a large curved monitor "
            "showing a strong rising teal/green trend line and candlesticks. Floating glassmorphic readout panels next to it: "
            "one card 'MONTHLY ALPHA  1.26%', one 'T-STAT  8.55', one 'GROSS SHARPE  ~1.2', and a green decision panel "
            "'SIGNAL: LONG  ·  12-MONTH RETURN POSITIVE'.\n\n"
            "MIDDLE BAND: a heading 'WHY THIS EDGE IS DIFFERENT' with a row of 5 small icon-features: "
            "'SYSTEMATIC', 'DIVERSIFIED', 'RISK-SCALED', 'MECHANICAL', 'DURABLE'.\n\n"
            "LOWER: a section 'BUILT ON EVIDENCE, NOT OPINION.' with a brain icon and 4 green check-mark bullets: "
            "'No emotions', 'No forecasting', 'No curve-fitting', 'Just data, risk & diversification'.\n\n"
            "CTA STRIP near bottom: a chat icon + 'WANT VERIFIED EDGES BUILT INTO YOUR SYSTEM?' and 'DM VIPRASOL — LIMITED BUILD SLOTS' "
            "with a small 'Let's grow together' script and a rising green arrow.\n\n"
            "BOTTOM: a thin grey disclaimer line 'Source: Moskowitz, Ooi & Pedersen (2012), JFE. Gross of costs; attribution debated. "
            "Past performance does not indicate future results. Research reference, not investment advice.'\n\n"
            "Style: institutional, trustworthy, premium, Bloomberg-meets-luxury, rich and detailed but organised, every word spelled exactly, "
            "no gibberish text, no stock-photo humans."
        ),
    },
    "hero-034-tsmom": {
        "size": "1024x1536",
        "prompt": (
            "Premium photoreal cinematic 3D render for a financial poster, vertical format. "
            "A sleek white-and-chrome humanoid AI trading robot with glowing teal eyes sits at a futuristic dark trading desk, "
            "seen from a three-quarter side angle on the RIGHT side of the frame, looking at a large curved monitor that displays "
            "a strong RISING trend line and candlestick chart glowing teal and green. Several translucent holographic UI panels "
            "float around the robot (BLANK panels, no readable text, no numbers). Dark navy-to-black room, dramatic teal and warm "
            "gold rim lighting, volumetric haze, reflections on the glossy desk. "
            "IMPORTANT COMPOSITION: keep the TOP ~30% of the image and the LEFT third darker and mostly empty (negative space) "
            "for later text overlay; concentrate the robot and screens in the center-right and middle band. "
            "Absolutely NO text, NO words, NO numbers, NO letters, no logos anywhere. Ultra-detailed, institutional, high-end."
        ),
    },
    "bg-dark-fintech": {
        "size": "1024x1536",
        "prompt": (
            "Abstract premium financial-research poster BACKGROUND, vertical format, NO text, NO words, NO numbers, "
            "NO letters anywhere. Deep navy-to-near-black vertical gradient. A single elegant glowing rising trend line "
            "sweeping upward from lower-left to upper-right, rendered in luminous teal with a soft gold highlight at its peak. "
            "Faint, subtle candlestick-chart bars receding into the dark background at low opacity. A very subtle fine grid / "
            "data-mesh texture. Soft teal and gold bokeh glow accents. Cinematic, institutional, high-end, lots of clean "
            "negative space, calm and uncluttered, Bloomberg-meets-luxury aesthetic. Absolutely no typography of any kind."
        ),
    },
    "034-tsmom": {
        "size": "1024x1536",
        "prompt": (
            "A premium, dark, high-end financial-research infographic poster, vertical format. "
            "Cinematic deep-navy-to-black gradient background with subtle glowing teal and gold accent lines, "
            "faint candlestick-chart texture and a rising trend curve in the background. Clean modern sans-serif typography, "
            "sharp and perfectly legible. A small elegant 'VIPRASOL' wordmark and a coiled-viper emblem in gold at the top corner.\n\n"
            "HEADLINE (large, white with a gold underline): 'TIME-SERIES MOMENTUM'\n"
            "Sub-headline (teal): 'The academic backbone of trend-following'\n"
            "A badge ribbon reading: 'PEER-REVIEWED  -  Journal of Financial Economics, 2012'\n\n"
            "A clean grid of 4 stat tiles, each a rounded dark glass card with a glowing number:\n"
            "Tile 1 -> '1.26%' label 'MONTHLY ALPHA (t = 8.55)'\n"
            "Tile 2 -> '58' label 'GLOBAL FUTURES MARKETS'\n"
            "Tile 3 -> '~1.2' label 'GROSS SHARPE RATIO'\n"
            "Tile 4 -> '12-mo / 1-mo' label 'LOOK-BACK / HOLD'\n\n"
            "A short bulleted 'HOW IT WORKS' panel with 3 lines: "
            "'Long if trailing 12-month return is positive, short if negative', "
            "'Size each position inversely to its volatility', "
            "'Rebalance monthly across commodities, equities, bonds, FX'.\n\n"
            "A highlight strip in gold reading: 'CRISIS ALPHA - positive in every decade since 1880'.\n\n"
            "A thin muted disclaimer footer at the very bottom in small grey text: "
            "'Source: Moskowitz, Ooi & Pedersen (2012). Returns are gross of costs; alpha attribution is debated. "
            "Past performance does not indicate future results. Research reference, not investment advice.'\n\n"
            "Overall style: institutional, trustworthy, Bloomberg-meets-luxury, lots of negative space, "
            "no clutter, no fake logos, no stock-photo people, no garbled text. Every word above spelled exactly."
        ),
    },
}

def generate(pid):
    cfg = PROMPTS[pid]
    body = json.dumps({
        "model": "gpt-image-1",
        "prompt": cfg["prompt"],
        "size": cfg.get("size", "1024x1536"),
        "quality": "high",
        "n": 1,
    }).encode()
    req = urllib.request.Request(
        "https://api.openai.com/v1/images/generations",
        data=body,
        headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"},
        method="POST",
    )
    print(f"[*] Generating '{pid}' ({cfg.get('size')}) ... this can take 30-90s")
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            data = json.loads(r.read())
    except urllib.error.HTTPError as e:
        print("[!] HTTP", e.code)
        print(e.read().decode()[:2000])
        raise SystemExit(1)
    b64 = data["data"][0]["b64_json"]
    # second arg = strategy id -> save straight into that strategy's own folder as scene.png
    if len(sys.argv) > 2:
        dest = ROOT / sys.argv[2]
        dest.mkdir(exist_ok=True)
        out = dest / "scene.png"
    else:
        scratch = ROOT / "_scratch"
        scratch.mkdir(exist_ok=True)
        out = scratch / f"{pid}.png"
    out.write_bytes(base64.b64decode(b64))
    print(f"[+] Saved -> {out}")
    if "usage" in data:
        print("[i] usage:", data["usage"])

def _load_from_json(pid):
    """If pid not in PROMPTS, try scene-prompts.json (sid keys or 'scene-<sid>' keys)."""
    js = ROOT / "scene-prompts.json"
    if not js.exists(): return None
    data = json.loads(js.read_text(encoding="utf-8"))
    key = pid.removeprefix("scene-")
    return data.get(pid) or data.get(key)

if __name__ == "__main__":
    pid = sys.argv[1] if len(sys.argv) > 1 else "034-tsmom"
    if pid not in PROMPTS:
        ext = _load_from_json(pid)
        if ext:
            PROMPTS[pid] = ext
        else:
            raise SystemExit(f"Unknown prompt '{pid}'. Available: {list(PROMPTS)} + scene-prompts.json")
    generate(pid)
