#!/usr/bin/env python3
"""
Merge the 6 digest JSON files from C:\\tmp\\d1..d6.json into one strategies.json,
plus build scene-prompts.json (full AI prompts wrapped around each scene_hook).
Also auto-fixes minor schema drift (why arrays padded to 5 words).
"""
import json, pathlib, collections, re, sys

ROOT = pathlib.Path(__file__).parent
SRC = [rf"C:\tmp\d{i}.json" for i in range(1, 7)]
OUT_STRATS = ROOT / "strategies.json"
OUT_SCENES = ROOT / "scene-prompts.json"

PAD_WHY = ["MECHANICAL", "SYSTEMATIC", "RESEARCHED", "DIVERSIFIED", "DISCIPLINED"]

SCENE_SCAFFOLD = (
    "Premium photoreal cinematic 3D render, vertical poster BACKDROP only. {hook} "
    "Dark navy-to-black room, dramatic teal and warm-gold rim lighting, volumetric haze, glossy floor reflections, cinematic depth. "
    "CRITICAL COMPOSITION: the ENTIRE LEFT HALF and the TOP THIRD of the image must be dark, calm, EMPTY negative space "
    "(deep navy-to-black gradient) reserved for text — no objects there. "
    "Absolutely NO text, NO numbers, NO letters, NO logos, NO UI labels anywhere. Clean, uncluttered, high-end."
)

def load(path):
    return json.load(open(path, encoding="utf-8-sig"))

def fix(entry):
    # pad why to 5 if short
    why = list(entry.get("why", []))
    if len(why) < 5:
        for w in PAD_WHY:
            if w not in why: why.append(w)
            if len(why) >= 5: break
    entry["why"] = why[:5]
    # truncate if 6+
    return entry

def main():
    all_entries = []
    seen_sids = {}
    seen_kw = {}
    for p in SRC:
        try:
            entries = load(p)
        except FileNotFoundError:
            print(f"[!] missing: {p}")
            continue
        print(f"[+] {p}: {len(entries)} entries")
        for e in entries:
            e = fix(e)
            sid = e["sid"]
            if sid in seen_sids:
                print(f"  [!] duplicate sid: {sid} (also in {seen_sids[sid]})")
                continue
            seen_sids[sid] = p
            kw = e["dm_keyword"].upper()
            if kw in seen_kw:
                # disambiguate by appending sid number suffix
                new = kw + sid.split("-")[0]
                print(f"  [!] dup dm_keyword '{kw}' (also in {seen_kw[kw]}); renaming to '{new}'")
                e["dm_keyword"] = new
                kw = new
            seen_kw[kw] = sid
            all_entries.append(e)

    # also include already-done 034, 035 as digest entries so the JSON is the complete tier-1 set
    DONE = {
        "034-tsmom": {"sid":"034-tsmom","name":"Time-Series Momentum","dm_keyword":"TREND","folder":"034-time-series-momentum","_already_built":True},
        "035-xsmom": {"sid":"035-xsmom","name":"Cross-Sectional Momentum","dm_keyword":"WINNERS","folder":"035-cross-sectional-momentum","_already_built":True},
    }
    for sid, stub in DONE.items():
        all_entries.insert(0 if sid=="034-tsmom" else 1, stub)

    OUT_STRATS.write_text(json.dumps(all_entries, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n[+] wrote {OUT_STRATS} ({len(all_entries)} entries)")

    # scene prompts
    scenes = {}
    for e in all_entries:
        if e.get("_already_built"): continue
        hook = e.get("scene_hook", "").strip()
        if not hook: continue
        scenes[e["sid"]] = {"size": "1024x1536", "prompt": SCENE_SCAFFOLD.format(hook=hook)}
    OUT_SCENES.write_text(json.dumps(scenes, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[+] wrote {OUT_SCENES} ({len(scenes)} scene prompts)")

    # report
    kws = collections.Counter(e["dm_keyword"] for e in all_entries)
    dups = [k for k,v in kws.items() if v>1]
    print(f"\n=== {len(all_entries)} total · dm_keyword dups: {dups or 'none'} ===")

if __name__ == "__main__":
    main()
