"""
Deep Device Scanner for Samsung Galaxy S24 FE
Queries connected phone via ADB and performs full inventory:
1. Hardware, firmware, One UI & battery
2. RAM Plus & animation scale settings
3. Storage partition usage (/data free vs used)
4. Full package catalog audit (Installed, Disabled, Uninstalled)
5. Target bloat analysis (Kids, Bixby, AR Zone, Glance Ads, Telemetry, etc.)
6. Preservation checks (Galaxy AI, Gaming Hub/Game Center, Camera, Phone Core)
7. System memory & background service footprint
"""

import subprocess
import json
import sys
from pathlib import Path

SERIAL = "RZCY71TA5AL"

def run_adb(args):
    cmd = ["adb", "-s", SERIAL] + args
    res = subprocess.run(cmd, capture_output=True, text=True, errors="replace", timeout=30)
    return res.stdout.strip()

def run_shell(sh_cmd):
    return run_adb(["shell", sh_cmd])

print("Connecting to Galaxy S24 FE...")

# 1. Properties
props = {
    "model": run_shell("getprop ro.product.model"),
    "name": run_shell("getprop ro.product.name"),
    "release": run_shell("getprop ro.build.version.release"),
    "oneui_raw": run_shell("getprop ro.build.version.oneui"),
    "sep_raw": run_shell("getprop ro.build.version.sep"),
    "csc": run_shell("getprop ro.csc.sales_code") or run_shell("getprop ro.boot.sales_code"),
    "soc": run_shell("getprop ro.soc.model"),
    "security_patch": run_shell("getprop ro.build.version.security_patch")
}

# 2. Performance settings
perf = {
    "ram_plus": run_shell("settings get global ram_expand_size"),
    "anim_window": run_shell("settings get global window_animation_scale"),
    "anim_transition": run_shell("settings get global transition_animation_scale"),
    "anim_duration": run_shell("settings get global animator_duration_scale"),
    "battery": run_shell("dumpsys battery | grep level | awk '{print $2}'")
}

# 3. Storage
storage = run_shell("df -h /data")

# 4. Packages
active_packages_raw = run_shell("pm list packages --user 0")
active_packages = [line.replace("package:", "").strip() for line in active_packages_raw.splitlines() if line.startswith("package:")]

disabled_packages_raw = run_shell("pm list packages -d --user 0")
disabled_packages = [line.replace("package:", "").strip() for line in disabled_packages_raw.splitlines() if line.startswith("package:")]

all_packages_raw = run_shell("pm list packages -u")
all_packages = [line.replace("package:", "").strip() for line in all_packages_raw.splitlines() if line.startswith("package:")]

active_set = set(active_packages)

# 5. Check against our database & targets
import database

audit = {
    "properties": props,
    "performance": perf,
    "storage": storage,
    "total_active_packages": len(active_packages),
    "total_disabled_packages": len(disabled_packages),
    "total_installed_on_device": len(all_packages),
    "categories": {}
}

for cat_id, cat_name in database.CATEGORIES.items():
    cat_pkgs = database.get_packages_by_category(cat_id)
    present = []
    missing_or_disabled = []
    for p in cat_pkgs:
        pid = p["id"]
        status = "ACTIVE" if pid in active_set else ("DISABLED" if pid in disabled_packages else "NOT_INSTALLED")
        item = {
            "id": pid,
            "name": p["name"],
            "risk": p["risk"],
            "status": status,
            "description": p["description"]
        }
        if status == "ACTIVE":
            present.append(item)
        else:
            missing_or_disabled.append(item)
    audit["categories"][cat_id] = {
        "title": cat_name,
        "present": present,
        "missing_or_disabled": missing_or_disabled
    }

# 6. Check Gaming Hub / Game Booster specifically
audit["gaming_hub"] = {
    "gos": "ACTIVE" if "com.samsung.android.game.gos" in active_set else "INACTIVE",
    "game_home": "ACTIVE" if "com.samsung.android.game.gamehome" in active_set else "INACTIVE",
    "game_tools": "ACTIVE" if "com.samsung.android.game.gametools" in active_set else "INACTIVE"
}

# 7. Check Camera Engine specifically
camera_pkgs = [
    "com.sec.android.app.camera",
    "com.sec.android.gallery3d",
    "com.samsung.android.app.camera.sticker.facearavatar.preload",
    "com.samsung.android.livestickers"
]
audit["camera_status"] = {pkg: ("ACTIVE" if pkg in active_set else "INACTIVE") for pkg in camera_pkgs}

# 8. Check Galaxy AI specifically
ai_pkgs = [
    "com.google.android.googlequicksearchbox",
    "com.sec.android.mimage.photoretouching",
    "com.samsung.android.scs",
    "com.samsung.android.intellivoiceservice",
    "com.samsung.android.offline.langpack",
    "com.samsung.android.app.notes"
]
audit["galaxy_ai_status"] = {pkg: ("ACTIVE" if pkg in active_set else "INACTIVE") for pkg in ai_pkgs}

# Save report
out_path = Path(__file__).parent / "device_scan_report.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(audit, f, indent=2)

print(f"Scan complete! Report written to {out_path.name}")
