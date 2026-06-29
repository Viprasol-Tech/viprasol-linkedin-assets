#!/usr/bin/env python3
"""
Blotato multi-platform poster for Viprasol strategy cards.
Reads keys from .env, captions from a <id>-captions.json, posts the hosted image
+ per-platform caption to all configured networks.

SAFE BY DEFAULT: dry-run prints the exact payloads and sends NOTHING.
Add --live to actually publish.

Usage:
  python poster.py 034-tsmom            # dry-run (default) — shows payloads
  python poster.py 034-tsmom --live     # actually publish
  python poster.py 034-tsmom --live --only linkedin,twitter
"""
import sys, json, pathlib, urllib.request, urllib.error
try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass

ROOT = pathlib.Path(__file__).parent
RAW_BASE = "https://raw.githubusercontent.com/Viprasol-Tech/viprasol-linkedin-assets/main/"
POSTS_URL = "https://backend.blotato.com/v2/posts"

def load_env():
    env = {}
    for line in (ROOT / ".env").read_text().splitlines():
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip()
    return env

ENV = load_env()
KEY = ENV["BLOTATO_API_KEY"]

# platform -> (accountId, extra target fields). YouTube excluded (video-only).
# Pinterest excluded until a boardId is supplied.
PLATFORMS = {
    "linkedin":  {"accountId": "15028", "target": {"targetType": "linkedin"}},
    "twitter":   {"accountId": "14115", "target": {"targetType": "twitter"}},
    "threads":   {"accountId": "5162",  "target": {"targetType": "threads"}},
    "facebook":  {"accountId": "22912", "target": {"targetType": "facebook", "pageId": "749059211623894"}},
    "instagram": {"accountId": "35256", "target": {"targetType": "instagram"}},
    "bluesky":   {"accountId": "49393", "target": {"targetType": "bluesky"}},
    # youtube (30192) excluded — video-only. pinterest no longer connected.
}

def build_payload(platform, text, media_url):
    cfg = PLATFORMS[platform]
    return {
        "post": {
            "accountId": cfg["accountId"],
            "content": {
                "text": text,
                "mediaUrls": [media_url],
                "platform": platform,
            },
            "target": cfg["target"],
        }
    }

def send(payload):
    body = json.dumps(payload).encode()
    req = urllib.request.Request(
        POSTS_URL, data=body,
        headers={"blotato-api-key": KEY, "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return r.status, r.read().decode()
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()

def main():
    if len(sys.argv) < 2:
        raise SystemExit("usage: python poster.py <strategy-id> [--live] [--only a,b]")
    sid = sys.argv[1]
    live = "--live" in sys.argv
    only = None
    if "--only" in sys.argv:
        only = sys.argv[sys.argv.index("--only") + 1].split(",")

    data = json.loads((ROOT / sid / "captions.json").read_text(encoding="utf-8"))
    default_img = data["image_file"]
    overrides = data.get("image_overrides", {})
    caps = data["captions"]

    targets = [p for p in PLATFORMS if (only is None or p in only) and p in caps]
    mode = "🔴 LIVE" if live else "🟡 DRY-RUN (nothing sent)"
    print(f"\n=== Blotato poster · {sid} · {mode} ===\n")

    for p in targets:
        text = caps[p]
        media_url = RAW_BASE + overrides.get(p, default_img)
        img_tag = "  [4:5 IG fill]" if p in overrides else ""
        warn = ""
        limit = {"twitter": 280, "threads": 500, "bluesky": 300}.get(p)
        if limit and len(text) > limit:
            warn = f"  ⚠️ {len(text)} chars > {limit}!"
        if p == "instagram" and text.count("#") > 5:
            warn += f"  ⚠️ {text.count('#')} hashtags > 5 (IG max via Blotato)!"
        payload = build_payload(p, text, media_url)
        print(f"--- {p.upper()} (account {PLATFORMS[p]['accountId']}, {len(text)} chars){img_tag}{warn} ---")
        if live:
            status, resp = send(payload)
            ok = "✅" if status in (200, 201) else "❌"
            print(f"{ok} HTTP {status}: {resp[:300]}\n")
        else:
            print(json.dumps(payload, ensure_ascii=False)[:600] + "\n")

    if not live:
        print("Dry-run only. Re-run with --live to publish.")

if __name__ == "__main__":
    main()
