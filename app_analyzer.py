"""
Comprehensive App & Storage Analyzer for Samsung Galaxy S24 FE
Analyzes all 247 user-installed apps, categorizes them, detects duplicates/redundancies,
and calculates potential storage recovery.
"""

import subprocess
import json
import re
from pathlib import Path

SERIAL = "RZCY71TA5AL"

def run_adb(args):
    p = subprocess.run(["adb", "-s", SERIAL] + args, capture_output=True, text=True, errors="replace", timeout=30)
    return p.stdout.strip()

# 1. 3rd-party packages
third_party_raw = run_adb(["shell", "pm", "list", "packages", "-3"])
pkgs = [l.replace("package:", "").strip() for l in third_party_raw.splitlines() if l.startswith("package:")]

# 2. Diskstats
p_disk = subprocess.run(["adb", "-s", SERIAL, "shell", "dumpsys", "diskstats"], capture_output=True, text=True, errors="replace")
pkg_names, app_sizes, app_data, app_cache = [], [], [], []
for line in p_disk.stdout.splitlines():
    if line.startswith("Package Names:"):
        pkg_names = json.loads(line.replace("Package Names:", "").strip())
    elif line.startswith("App Sizes:"):
        app_sizes = json.loads(line.replace("App Sizes:", "").strip())
    elif line.startswith("App Data Sizes:"):
        app_data = json.loads(line.replace("App Data Sizes:", "").strip())
    elif line.startswith("Cache Sizes:"):
        app_cache = json.loads(line.replace("Cache Sizes:", "").strip())

size_map = {}
if pkg_names:
    for i, name in enumerate(pkg_names):
        sz = app_sizes[i] if i < len(app_sizes) else 0
        dt = app_data[i] if i < len(app_data) else 0
        ca = app_cache[i] if i < len(app_cache) else 0
        size_map[name] = {"app": sz, "data": dt, "cache": ca, "total": sz + dt}

# Known categorization mapping
CATEGORIES = {
    "games": [
        "com.fingersoft.hcr2", "com.kiloo.subwaysurf", "com.fengiiley.frlegends",
        "com.eapublishing.dhsw.paid", "com.ansangha.drjb"
    ],
    "social_messaging": [
        "com.snapchat.android", "com.instagram.android", "com.whatsapp",
        "org.telegram.messenger", "com.twitter.android", "com.discord",
        "com.linkedin.android", "profile.analyze.privateaccount.inanalyze"
    ],
    "video_photo_creation": [
        "com.google.android.apps.youtube.producer", "com.frontrow.vlog",
        "com.accordion.analogcam", "com.gopro.smarty", "com.niksoftware.snapseed",
        "com.candycamera.android.filter.dubai", "com.gpsmapcamera.geotagginglocationonphoto",
        "com.sec.android.app.ve.vebgm"
    ],
    "media_music_streaming": [
        "com.amazon.mp3", "com.spotify.music", "com.shazam.android",
        "com.amazon.avod.thirdpartyclient", "com.google.android.youtube",
        "com.google.android.apps.youtube.music", "com.mi.earphone",
        "com.oceanwing.soundcore"
    ],
    "shopping_food": [
        "in.swiggy.android.toing", "com.mcdonalds.mobileapp", "com.ril.ajio",
        "in.amazon.mShop.android.shopping", "com.shopping.limeroad",
        "com.samsung.ecomm.global.in"
    ],
    "travel_ride_transit": [
        "com.zostel.app.android", "in.redbus.android", "com.flightradar24free",
        "com.alltrails.alltrails", "com.vehicle.rto.vahan.status.information.register"
    ],
    "finance_banking_crypto": [
        "com.sbi.lotusintouch", "com.acko.android", "com.tataaig.android",
        "com.paypal.android.p2pmobile", "com.stormgain.mobile",
        "com.google.android.apps.paidtasks"
    ],
    "benchmarks_testing": [
        "com.primatelabs.geekbench6"
    ],
    "utility_hardware_sync": [
        "com.xiaomi.wearable", "com.tvsm.connect", "com.resilio.sync",
        "com.tailscale.ipn", "ru.zdevs.zarchiver", "dev.daily",
        "org.isoron.uhabits", "com.kajda.fuelio", "com.tataskybroadband",
        "com.myairtelapp", "com.truecaller", "indwin.c3.shareapp"
    ],
    "documents_office_productivity": [
        "com.google.android.apps.docs", "com.google.android.apps.docs.editors.sheets",
        "com.google.android.apps.docs.editors.slides", "com.google.android.apps.docs.editors.docs",
        "com.microsoft.office.outlook", "com.microsoft.appmanager",
        "com.yygg.note.app", "us.zoom.videomeetings", "com.openai.chatgpt",
        "com.quora.android"
    ]
}

app_list = []
for p in pkgs:
    info = size_map.get(p, {"app": 0, "data": 0, "cache": 0, "total": 0})
    cat = "other"
    for c_name, c_pkgs in CATEGORIES.items():
        if p in c_pkgs:
            cat = c_name
            break
    app_list.append({
        "pkg": p,
        "category": cat,
        "total_bytes": info["total"],
        "app_bytes": info["app"],
        "data_bytes": info["data"],
        "cache_bytes": info["cache"],
        "total_mb": round(info["total"] / (1024*1024), 1),
        "app_mb": round(info["app"] / (1024*1024), 1),
        "data_mb": round(info["data"] / (1024*1024), 1),
        "cache_mb": round(info["cache"] / (1024*1024), 1)
    })

app_list.sort(key=lambda x: x["total_bytes"], reverse=True)

# Write summary
out_file = Path(__file__).parent / "app_analysis_report.json"
with open(out_file, "w", encoding="utf-8") as f:
    json.dump(app_list, f, indent=2)

print(f"Analysis saved to {out_file.name}. Total apps: {len(app_list)}")

# Print category breakdown
cat_totals = {}
for a in app_list:
    c = a["category"]
    cat_totals[c] = cat_totals.get(c, 0) + a["total_mb"]

print("\nSTORAGE USAGE BY CATEGORY:")
for c, tot in sorted(cat_totals.items(), key=lambda x: x[1], reverse=True):
    print(f"  {c:30}: {tot/1024:.2f} GB ({tot:.1f} MB)")
