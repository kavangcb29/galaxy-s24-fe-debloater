# 🚀 Samsung Galaxy S24 FE Debloater & Optimizer Toolkit

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Changelog](https://img.shields.io/badge/Changelog-v1.0.0-blue.svg)](CHANGELOG.md)
[![Python: 3.9+](https://img.shields.io/badge/Python-3.9%2B-brightgreen.svg)](https://www.python.org/)
[![Platform: Android / One UI](https://img.shields.io/badge/Platform-One%20UI%206.1.1%20%7C%207%20%7C%208%20%7C%208.5%20%7C%209-orange.svg)](https://www.samsung.com)
[![Device: Galaxy S24 FE](https://img.shields.io/badge/Device-Galaxy%20S24%20FE%20(SM--S721B%2FU%2FW%2FN)-blueviolet.svg)](#supported-devices)
[![Knox Safe](https://img.shields.io/badge/Knox-Untouched%20(0x0)-success.svg)](#-safety--security-model)
[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-Donate-yellow.svg?logo=buy-me-a-coffee)](https://buymeacoffee.com/kavangcb29)
[![Ko-fi](https://img.shields.io/badge/Ko--fi-Support-red.svg?logo=ko-fi)](https://ko-fi.com/kavangcb29)
[![PayPal](https://img.shields.io/badge/PayPal-Donate-00457C.svg?logo=paypal&logoColor=white)](https://paypal.me/KavanSudev)
[![UPI Support](https://img.shields.io/badge/UPI-GPay%20%7C%20PhonePe%20%7C%20Paytm-blueviolet.svg)](#-support-the-project)

An intelligent, rootless debloater, storage reclaimer, and performance accelerator designed specifically for the **Samsung Galaxy S24 FE (SM-S721B, SM-S721U, SM-S721W, SM-S721N)** running **One UI 6.1.1, 7.0, 8.0, 8.5, and One UI 9+**.

Reclaims **15 GB+ of storage**, eliminates Exynos 2400e micro-stutters, halts standby battery drain, and **100% safeguards Circle to Search, Generative Photo Edit, Live Call Translation, Camera, and Phone Telephony**.

---

## 📸 Preview

```
  ╔══════════════════════════════════════════════════════════════╗
  ║       SAMSUNG GALAXY S24 FE DEBLOATER & OPTIMIZER TOOLKIT    ║
  ║       Tailored for One UI 6.1.1 / 7 / 8 / 9 & Exynos 2400e   ║
  ║       Safeguards Galaxy AI, Camera, Biometrics & Phone Core  ║
  ╚══════════════════════════════════════════════════════════════╝

┌─[ CONNECTED DEVICE ]─────────────────────────────────────────
│  Model: SM-S721B [★ Galaxy S24 FE (Global/India 5G) DETECTED]
│  Chipset: Exynos 2400e (4nm Deca-core)
│  Android: 15 | One UI: 7.0 | Region: India (INS/INU) | Battery: 88%
└──────────────────────────────────────────────────────────────
```

---

## 🌟 Key Features

* **🤖 100% Galaxy AI Protection**: **Circle to Search**, **Generative Photo Edit** (Object Eraser / Fill), **Live Call Translation**, **Note Assist**, and **Samsung Core Services** are hard-locked and protected against accidental removal.
* **⚡ 1-Click S24 FE Flagship Turbo**: Removes Meta/Facebook, Samsung telemetry/analytics, AR Zone, Deco Pic, Glance lock screen ads, Samsung Kids, and Bixby voice daemons in a single click.
* **🧠 RAM Plus Stutter Elimination**: Samsung enables RAM Plus by default, creating virtual swap memory on internal flash storage. When storage is low, swap thrashing causes severe frame drops and keyboard lag. The toolkit provides a 1-click toggle to disable RAM Plus (0 GB) and let the Exynos 2400e run purely on physical 8 GB LPDDR5X RAM.
* **🧹 Instant Storage Cache Trimmer**: Reclaims multiple gigabytes of internal storage by executing `pm trim-caches` across stale system and application caches without touching personal photos or chat logs.
* **🎮 Exynos 2400e / GOS Unthrottling**: Disables Game Optimizing Service (GOS) to remove artificial thermal throttling and restore raw CPU/GPU frequencies.
* **🚀 0.5x UI Speed Accelerator**: Halves One UI animation durations to make the 120Hz Dynamic AMOLED display feel instantaneous.
* **🔒 Phone Core & Biometrics Safeguarded**: Cellular calling, emergency SOS (911/112), VoLTE, optical under-display fingerprint sensor, and triple camera engine are protected.
* **🔄 100% Reversible & Rootless**: Operates via `pm disable-user --user 0` and `pm uninstall -k --user 0`. Zero root needed, zero Knox trip (0x0).
* **💾 Automatic Backup Snapshots**: Automatically records a full JSON snapshot of all installed packages before any action.
* **📦 Auto-Provisioning ADB**: If ADB is not found in your system PATH, the tool auto-downloads Google's official platform-tools.
* **🖥️ Dual Interface**: Features both a sleek dark-themed Desktop GUI and an interactive Terminal CLI.

---

## 🎯 Curated Presets

| Preset | Description | Target Profile |
|---|---|---|
| **S24 FE Ultimate Flagship Turbo** *(Recommended)* | Safe debloat (Meta, Telemetry, AR Zone, Deco Pic, Glance lock screen ads, Samsung Kids) + full De-Bixby removal + Exynos 2400e GOS unthrottling + 0.5x UI speed boost. 100% PRESERVES Galaxy AI, Camera, Biometrics & Phone calling. | **Best for most users.** Eliminates stutter, frees RAM & storage, and keeps Galaxy AI completely active. |
| **Safe & Clean Baseline** | Removes Meta, telemetry, AR Zone, Deco Pic, Glance ads, and kids mode while preserving Bixby and Galaxy AI. | Users who still use Bixby voice routines. |
| **De-Bixby Only** | Removes Bixby Voice assistant, 24/7 background hotword listening, Bixby Vision, and Samsung Free feed. | Stops background microphone listening without touching Galaxy AI. |
| **Storage Saver Edition** | Aggressive space recovery (everything above + Microsoft OneDrive/365 + partner stubs + cache trim). | Space-constrained Galaxy S24 FE models (128 GB) running low on storage. |

---

## 🛡️ Critical Features Protected (Never Removed)

The following packages are explicitly marked **DANGER / CRITICAL** and protected:

* **Circle to Search** (`com.google.android.googlequicksearchbox`): Google app gesture engine.
* **Generative Photo Edit** (`com.sec.android.mimage.photoretouching` & `gallery3d`): Gallery AI object eraser and generative fill.
* **Samsung Core Services** (`com.samsung.android.scs`): On-device neural processing engine for Galaxy AI.
* **Live Call Translation & Interpreter** (`com.samsung.android.intellivoiceservice` & `offline.langpack`): Real-time multilingual voice translation.
* **Cellular Phone & Emergency SOS** (`com.android.phone`, `incallui`, `dialer`, `emergencymode.service`): Core phone dialer, cellular radio, and emergency calling.
* **VoLTE & Dual SIM** (`com.samsung.android.app.telephonyui`): Carrier HD voice and SIM management.
* **Optical Fingerprint Sensor** (`com.samsung.android.biometrics`): Under-display optical biometric driver.
* **Triple Camera Engine** (`com.sec.android.app.camera`): 50MP main, 8MP 3x OIS telephoto, and 12MP ultrawide camera pipeline.
* **Samsung Keyboard** (`com.samsung.android.honeyboard`): Main keyboard with AI writing assistant.

---

## 🚀 Quick Start Guide

### 1. Enable Developer Options on Your Galaxy S24 FE
1. Open **Settings** on your phone.
2. Go to **About phone** ➔ **Software information**.
3. Tap **Build number** **7 times** rapidly until you see *"Developer mode has been turned on"*.

### 2. Configure Samsung Auto Blocker (Crucial for One UI 6.1.1 / 7 / 8 / 9!)
> [!IMPORTANT]
> Samsung introduced **Auto Blocker** in One UI 6.0 and enforces it strictly in **One UI 6.1.1, 7.0, and 8.0+**. Auto Blocker blocks USB cable software commands and ADB by default.
>
> If your phone shows "No Device Connected" or ADB commands fail:
> 1. Open **Settings** on your phone.
> 2. Tap **Security and privacy** ➔ **Auto Blocker**.
> 3. Toggle Auto Blocker **OFF** (or turn off **"Maximum restrictions"** / **"Block software updates by USB cable"**).
> 4. *(You can safely turn Auto Blocker back ON after you finish debloating.)*

### 3. Enable USB Debugging
1. Return to **Settings** ➔ scroll to the very bottom and tap **Developer options**.
2. Locate **USB debugging** and toggle it to **ON**.
3. Tap **OK** on the confirmation prompt.

### 4. Connect to PC & Authorize Phone
1. Connect your phone to your PC via a USB-C data cable.
2. Unlock your phone screen. A prompt will appear: *"Allow USB debugging?"*.
3. Check **"Always allow from this computer"** and tap **Allow**.

### 5. Launch the Toolkit
* **Desktop Graphical Interface (GUI)**: Double-click `run.bat`.
* **Terminal CLI**: Double-click `run_cli.bat`.

---

## 💻 CLI Commands & Options

You can also run the toolkit directly from the command line:

```bash
# Launch Desktop GUI
python debloater.py --gui

# Launch Interactive Terminal CLI
python debloater.py --cli

# Apply Recommended Flagship Turbo Preset directly
python debloater.py --preset s24fe_turbo_ai_safe --mode disable -y

# Apply 0.5x UI Speed Boost
python debloater.py --tweaks

# Turn OFF RAM Plus to eliminate stutter (0 GB)
python debloater.py --ram-plus 0

# Trim storage caches to reclaim gigabytes of disk space
python debloater.py --trim-cache

# Restore all debloated packages
python debloater.py --restore-all
```

---

## 📱 Supported Devices

* **Samsung Galaxy S24 FE (Global / India / Dual SIM)**: `SM-S721B`, `SM-S721B/DS`
* **Samsung Galaxy S24 FE (USA Carrier)**: `SM-S721U`
* **Samsung Galaxy S24 FE (USA Factory Unlocked)**: `SM-S721U1`
* **Samsung Galaxy S24 FE (Canada)**: `SM-S721W`
* **Samsung Galaxy S24 FE (Korea)**: `SM-S721N`
* Compatible with **One UI 6.1.1, 7.0, 8.0, 8.5, and 9.0+**

---

## ☕ Support the Project

If this toolkit helped make your Galaxy S24 FE snappier, freed up storage space, and stopped stutter, consider supporting future development:

* **☕ Buy Me a Coffee**: [buymeacoffee.com/kavangcb29](https://buymeacoffee.com/kavangcb29)
* **❤️ Ko-fi**: [ko-fi.com/kavangcb29](https://ko-fi.com/kavangcb29)
* **💳 PayPal Direct**: [paypal.me/KavanSudev](https://paypal.me/KavanSudev)
* **🇮🇳 UPI Support (India)**: `kavangcb@gmail.com` *(GPay / PhonePe / Paytm)*

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.
