#!/usr/bin/env python3
"""
Template-generate per-platform captions.json for every strategy in strategies.json.
Captions vary by category (momentum/value/carry/options-vrp/etc.) so they're not robotic.
All within platform limits: TW<=280, TH<=500, BS<=300, IG<=5 hashtags + image required.
"""
import json, pathlib, re, sys

ROOT = pathlib.Path(__file__).parent
STRATS = ROOT / "strategies.json"

PLATFORM_LIMITS = {"twitter": 280, "threads": 500, "bluesky": 300}

# Category-specific hashtag clusters (always <=5, IG-safe)
HASHTAGS_IG = {
    "momentum":    "#AlgorithmicTrading #QuantTrading #MomentumInvesting #SystematicTrading #Fintech",
    "value":       "#AlgorithmicTrading #QuantTrading #ValueInvesting #FactorInvesting #Fintech",
    "carry":       "#AlgorithmicTrading #QuantTrading #CarryTrade #SystematicTrading #Fintech",
    "quality":     "#AlgorithmicTrading #QuantTrading #FactorInvesting #QualityInvesting #Fintech",
    "options-vrp": "#AlgorithmicTrading #QuantTrading #OptionsTrading #VolatilityRiskPremium #Fintech",
    "defensive":   "#AlgorithmicTrading #QuantTrading #LowVolatility #FactorInvesting #Fintech",
    "seasonality": "#AlgorithmicTrading #QuantTrading #SystematicTrading #MarketAnomalies #Fintech",
    "technical":   "#AlgorithmicTrading #QuantTrading #TechnicalAnalysis #SystematicTrading #Fintech",
    "distress":    "#AlgorithmicTrading #QuantTrading #FactorInvesting #FinancialResearch #Fintech",
    "other":       "#AlgorithmicTrading #QuantTrading #SystematicTrading #FactorInvesting #Fintech",
}

# LinkedIn full hashtag set (richer)
HASHTAGS_LI = {
    "momentum":    "#AlgorithmicTrading #QuantitativeFinance #MomentumInvesting #FactorInvesting #SystematicTrading #Fintech",
    "value":       "#AlgorithmicTrading #QuantitativeFinance #ValueInvesting #FactorInvesting #SystematicTrading #Fintech",
    "carry":       "#AlgorithmicTrading #QuantitativeFinance #CarryTrade #FactorInvesting #SystematicTrading #Fintech",
    "quality":     "#AlgorithmicTrading #QuantitativeFinance #QualityInvesting #FactorInvesting #SystematicTrading #Fintech",
    "options-vrp": "#AlgorithmicTrading #QuantitativeFinance #OptionsTrading #VolatilityRiskPremium #SystematicTrading #Fintech",
    "defensive":   "#AlgorithmicTrading #QuantitativeFinance #LowVolatility #FactorInvesting #SystematicTrading #Fintech",
    "seasonality": "#AlgorithmicTrading #QuantitativeFinance #SystematicTrading #MarketAnomalies #Fintech",
    "technical":   "#AlgorithmicTrading #QuantitativeFinance #TechnicalAnalysis #SystematicTrading #Fintech",
    "distress":    "#AlgorithmicTrading #QuantitativeFinance #FactorInvesting #FinancialResearch #Fintech",
    "other":       "#AlgorithmicTrading #QuantitativeFinance #SystematicTrading #FactorInvesting #Fintech",
}

def bullets(items):
    return "\n".join(f"🔹 {x.rstrip('.')}." for x in items)

def short_paper(p):
    """Compress 'Asness, Moskowitz & Pedersen (2013), Journal of Finance' → 'JF 2013'."""
    yr = re.search(r"\b(19|20)\d{2}\b", p)
    year = yr.group(0) if yr else ""
    jl = ""
    if "Journal of Finance" in p and "Economics" not in p: jl = "JF"
    elif "Journal of Financial Economics" in p: jl = "JFE"
    elif "Journal of Portfolio Management" in p: jl = "JPM"
    elif "Review of Financial Studies" in p: jl = "RFS"
    elif "Financial Analysts Journal" in p: jl = "FAJ"
    elif "CBOE" in p: jl = "CBOE"
    else:
        m = re.search(r"\(([^)]+)\)\s*$", p)
        jl = m.group(1)[:8] if m else ""
    return f"{jl} {year}".strip() or p[:30]

def linkedin(e):
    feats = e.get("mechanism_bullets") or [f["title"] + " — " + f["desc"].lower() for f in e["features"][:4]]
    return (
        f"{e['h1'].capitalize()} {e['h2_white'].lower()}{e['h2_accent'].lower()} 📊\n\n"
        f"{e['title'].title()} — {e['kicker'].lower()}.\n\n"
        f"Here's the complete logic. No black box:\n\n"
        + bullets(feats) + "\n\n"
        f"{e['disclaimer'].split('.')[0]}.\n\n"
        f"We're not here to sell signals or promise returns. We share the strategy — the real logic — for free. 🎯\n\n"
        f"This is just 1 of 440 strategies in our research library.\n\n"
        f"👉 Want this as a complete, ready-to-run algorithm — with the full research file behind it? DM us \"{e['dm_keyword']}\".\n"
        f"👉 Or build something custom — your edge or one of ours, engineered into live, risk-gated execution.\n\n"
        f"Viprasol Tech — we turn proven research into systems that actually run. 🚀\n\n"
        + HASHTAGS_LI.get(e["category"], HASHTAGS_LI["other"])
    )

def twitter(e):
    paper = short_paper(e["paper"])
    feats = [f["title"] for f in e["features"][:3]]
    text = (
        f"{e['title'].title()} 📊\n\n"
        f"🔹 {feats[0].lower()}\n🔹 {feats[1].lower()}\n🔹 {feats[2].lower()}\n"
        f"🔹 Peer-reviewed ({paper})\n\n"
        f"Strategy shared free. Want the algo + research file? DM \"{e['dm_keyword']}\" 👇"
    )
    return _fit(text, 280, e["dm_keyword"], feats, paper)

def _fit(text, limit, kw, feats, paper):
    if len(text) <= limit: return text
    # progressively shorter fallback
    t = (
        f"{', '.join(feats[:2])} + Peer-reviewed ({paper}).\n\n"
        f"Strategy shared free. DM \"{kw}\" for the algo + research file 👇"
    )
    if len(t) <= limit: return t
    return f"Verified quant strategy. DM \"{kw}\" for the algo + research file. 1 of 440 in our research library."

def threads(e):
    paper = short_paper(e["paper"])
    feats = [f["title"] + " — " + f["desc"].lower() for f in e["features"][:4]]
    text = (
        f"{e['h1'].capitalize()} {e['h2_white'].lower()}{e['h2_accent'].lower()} 📊\n\n"
        f"{e['title'].title()} — the complete logic:\n\n"
        + bullets(feats) + "\n\n"
        f"Peer-reviewed ({paper}). 1 of 440 in our research library. 🎯\n\n"
        f"Want the algo + research file? DM \"{e['dm_keyword']}\"."
    )
    if len(text) > 500:
        feats = [f["title"] for f in e["features"][:4]]
        text = (
            f"{e['title'].title()} — the complete logic:\n\n"
            + bullets(feats) + "\n\n"
            f"Peer-reviewed ({paper}). 1 of 440 in our research library. 🎯\n\n"
            f"Want the algo + research file? DM \"{e['dm_keyword']}\"."
        )
    return text[:500]

def facebook(e):
    return linkedin(e).split("\n\n#")[0]  # same body, no hashtag block

def instagram(e):
    paper = short_paper(e["paper"])
    feats = [f["title"] for f in e["features"][:5]]
    text = (
        f"{e['h1'].capitalize()} {e['h2_white'].lower()}{e['h2_accent'].lower()} 📊\n\n"
        f"{e['title'].title()} — the complete logic:\n"
        + "\n".join(f"🔹 {x.lower()}" for x in feats) + "\n\n"
        f"Peer-reviewed ({paper}). 1 of 440 in our research library. 🎯\n\n"
        f"Want the complete algo + research file? DM \"{e['dm_keyword']}\" 👇\n.\n.\n"
        + HASHTAGS_IG.get(e["category"], HASHTAGS_IG["other"])
    )
    return text

def bluesky(e):
    paper = short_paper(e["paper"])
    feats = [f["title"] for f in e["features"][:3]]
    text = (
        f"{e['title'].title()} 📊\n\n"
        f"🔹 {feats[0].lower()}\n🔹 {feats[1].lower()}\n🔹 {feats[2].lower()}\n"
        f"🔹 Peer-reviewed ({paper})\n\n"
        f"Strategy shared free. Want the algo + research file? DM \"{e['dm_keyword']}\" 👇"
    )
    if len(text) > 300:
        text = f"{e['title'].title()} — peer-reviewed.\n\nStrategy shared free. DM \"{e['dm_keyword']}\" for the algo + research file 👇"
    return text

def build_one(e):
    sid = e["sid"]
    return {
        "strategy": e["folder"],
        "image_file": f"images/strategy-{sid}.png",
        "image_overrides": {"instagram": f"images/strategy-{sid}-45.png"},
        "positioning": f"Educate (give the strategy logic free). NO return claims. Soft close: DM {e['dm_keyword']} for the complete algo + research file, or a custom build.",
        "captions": {
            "linkedin": linkedin(e),
            "twitter": twitter(e),
            "threads": threads(e),
            "facebook": facebook(e),
            "instagram": instagram(e),
            "bluesky": bluesky(e),
        }
    }

def main():
    only = None
    if "--only" in sys.argv:
        only = set(sys.argv[sys.argv.index("--only")+1].split(","))
    data = json.loads(STRATS.read_text(encoding="utf-8"))
    written = 0; warned = 0
    for e in data:
        if e.get("_already_built"): continue
        if only and e["sid"] not in only: continue
        out_dir = ROOT / e["sid"]
        out_dir.mkdir(exist_ok=True)
        cap = build_one(e)
        # validate platform limits
        for p, limit in PLATFORM_LIMITS.items():
            if len(cap["captions"][p]) > limit:
                print(f"  [!] {e['sid']} {p}: {len(cap['captions'][p])} > {limit}")
                warned += 1
        if cap["captions"]["instagram"].count("#") > 5:
            print(f"  [!] {e['sid']} instagram: {cap['captions']['instagram'].count('#')} hashtags > 5")
            warned += 1
        (out_dir / "captions.json").write_text(json.dumps(cap, indent=2, ensure_ascii=False), encoding="utf-8")
        written += 1
    print(f"\n[+] wrote {written} captions.json files · {warned} warnings")

if __name__ == "__main__":
    main()
