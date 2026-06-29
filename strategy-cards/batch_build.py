#!/usr/bin/env python3
"""
Batch builder for the full Tier-1 wave.
Reads digest.json (or any --digest file), then for each entry:
  1. ensures the strategy folder exists
  2. generates the AI scene (1 OpenAI call per strategy)  [skip if scene.png exists]
  3. composes the hybrid card
  4. frames the 4:5 IG version
  5. optionally copies to images/ for hosting

Usage:
  python batch_build.py <digest.json>                 # build all entries
  python batch_build.py <digest.json> --only 036,037  # filter
  python batch_build.py <digest.json> --skip-scene    # use existing scene.png (re-render only)
  python batch_build.py <digest.json> --host          # also copy to ../images/
  python batch_build.py <digest.json> --dry-run       # show what would happen, no API/file writes
"""
import sys, json, pathlib, subprocess, shutil, time

ROOT = pathlib.Path(__file__).parent
PY = sys.executable

def run(cmd, dry):
    print(f"  $ {' '.join(cmd)}")
    if dry: return
    r = subprocess.run(cmd, cwd=ROOT)
    if r.returncode != 0:
        raise SystemExit(f"  step failed: {' '.join(cmd)}")

def main():
    if len(sys.argv) < 2:
        raise SystemExit("usage: python batch_build.py <digest.json> [--only a,b] [--skip-scene] [--host] [--dry-run]")
    digest_path = pathlib.Path(sys.argv[1])
    only = None
    if "--only" in sys.argv:
        only = set(sys.argv[sys.argv.index("--only") + 1].split(","))
    skip_scene = "--skip-scene" in sys.argv
    host = "--host" in sys.argv
    dry = "--dry-run" in sys.argv

    entries = json.loads(digest_path.read_text(encoding="utf-8"))
    if only:
        entries = [e for e in entries if e["sid"] in only or e["folder"] in only]

    print(f"\n=== batch_build · {len(entries)} strategies · skip_scene={skip_scene} · host={host} · dry={dry} ===\n")
    started = time.time()

    for i, e in enumerate(entries, 1):
        sid = e["sid"]
        strat = ROOT / sid
        scene = strat / "scene.png"
        card = strat / "card.png"
        card45 = strat / "card-45.png"
        print(f"\n[{i}/{len(entries)}] {sid}  ({e.get('name','?')})")

        strat.mkdir(exist_ok=True)

        # 1. AI scene
        if scene.exists() and skip_scene:
            print("  · scene.png exists, skipping generation")
        elif scene.exists():
            print("  · scene.png exists, re-using (delete to regenerate)")
        else:
            run([PY, "generate.py", f"scene-{sid}", sid], dry)

        # 2. hybrid card
        run([PY, "compose_full.py", sid], dry)

        # 3. 4:5 IG version
        run([PY, "frame.py", str(card), str(card45), "1080x1350"], dry)

        # 4. host
        if host:
            images = ROOT.parent / "images"
            images.mkdir(exist_ok=True)
            for src, dst in [(card, images / f"strategy-{sid}.png"),
                             (card45, images / f"strategy-{sid}-45.png")]:
                if not dry:
                    shutil.copy2(src, dst)
                print(f"  + hosted -> {dst.name}")

    elapsed = time.time() - started
    print(f"\n=== done · {len(entries)} built · {elapsed:.0f}s ===")
    if host:
        print("[i] next: git add images/ && git commit -m 'add tier-1 cards' && git push")

if __name__ == "__main__":
    main()
