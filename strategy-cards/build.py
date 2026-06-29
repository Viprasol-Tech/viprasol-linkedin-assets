#!/usr/bin/env python3
"""
One-shot builder for a strategy card.

Layout (everything for one strategy lives in ONE folder — no shared output/):
  strategy-cards/<sid>/
    scene.png        AI backdrop (from generate.py)
    card.png         hybrid composite 1024x1536 (from compose_full.py)
    card-45.png      4:5 IG version with blurred side-fill (from frame.py)
    captions.json    per-platform captions + hosted image paths

Usage:
  python build.py <sid>                # compose + frame (assumes scene.png exists)
  python build.py <sid> --scene <prompt_id>   # also generates the AI scene first
  python build.py <sid> --host         # also copies hybrid card + 4:5 to images/ for hosting
"""
import sys, pathlib, shutil, subprocess

ROOT = pathlib.Path(__file__).parent

def run(cmd):
    print(f"\n$ {' '.join(cmd)}")
    r = subprocess.run(cmd, cwd=ROOT)
    if r.returncode != 0:
        raise SystemExit(f"step failed: {' '.join(cmd)}")

def main():
    if len(sys.argv) < 2:
        raise SystemExit("usage: python build.py <sid> [--scene <prompt_id>] [--host]")
    sid = sys.argv[1]
    strat = ROOT / sid
    strat.mkdir(exist_ok=True)

    if "--scene" in sys.argv:
        pid = sys.argv[sys.argv.index("--scene") + 1]
        run([sys.executable, "generate.py", pid, sid])

    if not (strat / "scene.png").exists():
        raise SystemExit(f"[!] {strat/'scene.png'} missing — run with --scene <prompt_id> first")

    run([sys.executable, "compose_full.py", sid])
    run([sys.executable, "frame.py", str(strat / "card.png"), str(strat / "card-45.png"), "1080x1350"])

    if "--host" in sys.argv:
        images = ROOT.parent / "images"
        images.mkdir(exist_ok=True)
        for src, dst in [(strat / "card.png", images / f"strategy-{sid}.png"),
                         (strat / "card-45.png", images / f"strategy-{sid}-45.png")]:
            shutil.copy2(src, dst)
            print(f"hosted -> {dst}")
        print("\n[i] now: git add images/ && git commit && git push, then poster.py", sid)

    print(f"\n[+] {sid} built. files in {strat}/")

if __name__ == "__main__":
    main()
