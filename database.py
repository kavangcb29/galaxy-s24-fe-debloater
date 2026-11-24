"""
Samsung Galaxy S24 FE Debloater - Package Database & Catalog
Curated specifically for Samsung Galaxy S24 FE (SM-S721B, SM-S721U, SM-S721W, SM-S721N)
and One UI 6.1.1, 7.0, 8.0, 8.5, and 9.0+.

Safeguards:
- 100% Protection for Galaxy AI (Circle to Search, Generative Photo Edit, Note Assist, Live Translate)
- 100% Protection for Core Phone (Cellular dialer, VoLTE, VoWiFi, Emergency SOS)
- 100% Protection for Biometrics (Under-display optical fingerprint, Face unlock, Knox)
- 100% Protection for Triple Camera Hardware & Gallery processing
"""

from typing import Dict, List, Any

# Risk Levels:
# 'safe'    : No impact on device functionality or Galaxy AI; zero crashes; recommended.
# 'optional': User preference (e.g. OneDrive, SmartThings, Samsung Internet).
# 'caution' : May disable an ecosystem link (e.g. Galaxy Store, Samsung Cloud sync).
# 'danger'  : CRITICAL hardware or phone feature! (Galaxy AI, Phone calls, Biometrics, Camera, System UI). DO NOT REMOVE.

CATEGORIES = {
    "telemetry": "Telemetry, Analytics & Background Logging",
    "meta_facebook": "Meta & Facebook Services",
    "ar_emoji": "AR Zone, Deco Pic & Emoji Junk",
    "lockscreen_ads": "Glance & Lock Screen Sponsored Ads",
    "kids_mode": "Samsung Kids Mode Sandbox",
    "bixby": "Bixby Voice & Wakeup (Independent of Galaxy AI)",
    "promotional": "Samsung Promotional & E-Commerce Bloat",
    "microsoft": "Microsoft Pre-installs",
    "carrier_bloat": "Carrier & Partner Pre-installs (AppCloud, Aura)",
    "gos_gaming": "Game Optimizing Service (GOS) & Gaming Hub",
    "google_optional": "Google Optional Apps",
    "samsung_optional": "Samsung Ecosystem Apps (Optional)",
    "galaxy_ai": "Galaxy AI & Intelligent Processing (CRITICAL - DO NOT REMOVE)",
    "phone_critical": "CRITICAL Phone Hardware & Core Telephony (DO NOT REMOVE)"
}

PACKAGES: List[Dict[str, Any]] = [
    # ==========================================
    # 1. Telemetry, Analytics & Background Logging (SAFE)
    # ==========================================
    {
        "id": "com.samsung.android.rubin.app",
        "name": "Samsung Customization Service (Rubin)",
        "category": "telemetry",
        "risk": "safe",
        "description": "Continuously tracks usage patterns, app launches and location to serve targeted Samsung ads and predictive tracking."
    },
    {
        "id": "com.samsung.android.knox.analytics.uploader",
        "name": "Knox Analytics Uploader",
        "category": "telemetry",
        "risk": "safe",
        "description": "Gathers and transmits Knox security and device telemetry logs to Samsung cloud servers in the background."
    },
    {
        "id": "com.sec.android.diagmonagent",
        "name": "Samsung Diagnostic Monitor Agent",
        "category": "telemetry",
        "risk": "safe",
        "description": "Background service sending automated diagnostic metrics, crash telemetry and usage analytics to Samsung."
    },
    {
        "id": "com.samsung.android.da.daagent",
        "name": "Dual App Analytics Agent",
        "category": "telemetry",
        "risk": "safe",
        "description": "Analytics logging agent for dual messenger and dual profile configurations."
    },
    {
        "id": "com.samsung.android.bbc.bbcagent",
        "name": "Samsung B2B Agent",
        "category": "telemetry",
        "risk": "safe",
        "description": "Samsung enterprise and corporate telemetry background agent."
    },
    {
        "id": "com.google.android.feedback",
        "name": "Google Market Feedback Agent",
        "category": "telemetry",
        "risk": "safe",
        "description": "Sends background crash logs and telemetry feedback reports back to Google Play."
    },
    {
        "id": "com.google.android.gms.location.history",
        "name": "Google Location History Tracker",
        "category": "telemetry",
        "risk": "safe",
        "description": "Google location reporting and timeline tracker service."
    },
    {
        "id": "com.samsung.android.ipsgeofence",
        "name": "Samsung Geofence Service",
        "category": "telemetry",
        "risk": "safe",
        "description": "Background geofence service used for location-based Samsung ads and retail beacon tracking."
    },

    # ==========================================
    # 2. Meta & Facebook Services (SAFE)
    # ==========================================
    {
        "id": "com.facebook.katana",
        "name": "Facebook Client App",
        "category": "meta_facebook",
        "risk": "safe",
        "description": "Preloaded Facebook client app stub."
    },
    {
        "id": "com.facebook.system",
        "name": "Meta App Installer",
        "category": "meta_facebook",
        "risk": "safe",
        "description": "Privileged system daemon for silent background Meta app updates and installations."
    },
    {
        "id": "com.facebook.appmanager",
        "name": "Meta App Manager",
        "category": "meta_facebook",
        "risk": "safe",
        "description": "Background daemon managing Facebook apps without Google Play Store intervention."
    },
    {
        "id": "com.facebook.services",
        "name": "Meta Services",
        "category": "meta_facebook",
        "risk": "safe",
        "description": "Background service maintaining persistent Meta network connectivity and advertising IDs."
    },

    # ==========================================
    # 3. AR Zone, Deco Pic & Emoji Junk (SAFE)
    # ==========================================
    {
        "id": "com.samsung.android.aremoji",
        "name": "AR Emoji",
        "category": "ar_emoji",
        "risk": "safe",
        "description": "Samsung 3D avatar generator. Takes up substantial storage and runs background renderers."
    },
    {
        "id": "com.samsung.android.aremojieditor",
        "name": "AR Emoji Editor",
        "category": "ar_emoji",
        "risk": "safe",
        "description": "Avatar clothing, makeup, and hairstyle customization editor."
    },
    {
        "id": "com.samsung.android.arzone",
        "name": "AR Zone Hub",
        "category": "ar_emoji",
        "risk": "safe",
        "description": "Aggregator hub for AR Emoji, Quick Measure, and AR camera filters."
    },
    {
        "id": "com.samsung.android.livestickers",
        "name": "Deco Pic / Live Stickers",
        "category": "ar_emoji",
        "risk": "safe",
        "description": "Decorative live stickers, cartoon masks, and facial filter overlays for the camera."
    },
    {
        "id": "com.sec.android.mimage.avatarstickers",
        "name": "Avatar Stickers",
        "category": "ar_emoji",
        "risk": "safe",
        "description": "Generates animated sticker packs and GIFs from your 3D avatar."
    },
    {
        "id": "com.samsung.android.app.camera.sticker.facearavatar.preload",
        "name": "Face AR Avatar Preload",
        "category": "ar_emoji",
        "risk": "safe",
        "description": "Preloaded avatar facial tracking asset assets."
    },
    {
        "id": "com.samsung.android.stickercenter",
        "name": "Samsung Sticker Center",
        "category": "ar_emoji",
        "risk": "safe",
        "description": "Store for downloading additional keyboard and photo stickers."
    },
    {
        "id": "com.samsung.android.ardrawing",
        "name": "AR Doodle",
        "category": "ar_emoji",
        "risk": "safe",
        "description": "Augmented reality camera drawing engine. Safe to remove."
    },

    # ==========================================
    # 4. Glance & Lock Screen Sponsored Ads (SAFE)
    # ==========================================
    {
        "id": "com.glance.internet",
        "name": "Glance on Samsung",
        "category": "lockscreen_ads",
        "risk": "safe",
        "description": "Sponsored news feed, shopping links, and video ads displayed on your lock screen. Severe battery and storage consumer."
    },
    {
        "id": "com.samsung.android.dynamiclock",
        "name": "Dynamic Lock Screen",
        "category": "lockscreen_ads",
        "risk": "safe",
        "description": "Periodically downloads hundreds of MBs of wallpaper packs and sponsored lock screen content."
    },

    # ==========================================
    # 5. Samsung Kids Mode Sandbox (SAFE)
    # ==========================================
    {
        "id": "com.samsung.android.kidsinstaller",
        "name": "Samsung Kids Installer",
        "category": "kids_mode",
        "risk": "safe",
        "description": "Pre-installed installer for parental sandbox mode. Safe to remove if you do not have children."
    },
    {
        "id": "com.sec.android.app.kidshome",
        "name": "Samsung Kids Mode Home",
        "category": "kids_mode",
        "risk": "safe",
        "description": "Kids sandbox environment interface and game launcher."
    },

    # ==========================================
    # 6. Bixby Voice & Wakeup (SAFE - Independent of Galaxy AI)
    # ==========================================
    {
        "id": "com.samsung.android.bixby.agent",
        "name": "Bixby Voice Assistant",
        "category": "bixby",
        "risk": "safe",
        "description": "Legacy voice assistant. Safe to remove without impacting Circle to Search or Generative Photo Edit."
    },
    {
        "id": "com.samsung.android.bixby.wakeup",
        "name": "Bixby Voice Wakeup",
        "category": "bixby",
        "risk": "safe",
        "description": "Listens 24/7 for 'Hi Bixby' hotword. Disabling stops background audio thread and saves significant battery."
    },
    {
        "id": "com.samsung.android.bixby.service",
        "name": "Bixby Service",
        "category": "bixby",
        "risk": "safe",
        "description": "Core background coordination service for Bixby integration."
    },
    {
        "id": "com.samsung.android.visionintelligence",
        "name": "Bixby Vision",
        "category": "bixby",
        "risk": "safe",
        "description": "Camera visual lookup. Circle to Search and Google Lens are significantly faster and superior."
    },
    {
        "id": "com.samsung.android.bixbyvision.framework",
        "name": "Bixby Vision Framework",
        "category": "bixby",
        "risk": "safe",
        "description": "Background image recognition framework supporting Bixby Vision."
    },
    {
        "id": "com.samsung.android.app.spage",
        "name": "Samsung Free / Bixby Home",
        "category": "bixby",
        "risk": "safe",
        "description": "Leftmost home screen feed displaying sponsored news, games, and podcasts."
    },

    # ==========================================
    # 7. Samsung Promotional & E-Commerce Bloat (SAFE)
    # ==========================================
    {
        "id": "com.samsung.ecomm",
        "name": "Samsung Shop",
        "category": "promotional",
        "risk": "safe",
        "description": "Samsung storefront app for purchasing hardware and accessories."
    },
    {
        "id": "com.samsung.sree",
        "name": "Samsung Global Goals",
        "category": "promotional",
        "risk": "safe",
        "description": "Ad-supported promotional lock screen and charity application."
    },
    {
        "id": "com.samsung.android.rapps",
        "name": "Samsung Regional App Recommendations",
        "category": "promotional",
        "risk": "safe",
        "description": "Regional app suggestions and promotional recommendations stub preloaded on Indian firmware."
    },
    {
        "id": "com.samsung.safetyinformation",
        "name": "Samsung Safety Information",
        "category": "promotional",
        "risk": "safe",
        "description": "Static regulatory and safety manual documentation."
    },
    {
        "id": "com.samsung.android.app.tips",
        "name": "Samsung Tips",
        "category": "promotional",
        "risk": "safe",
        "description": "Sends periodic tutorial notifications and promotional tips."
    },
    {
        "id": "com.samsung.android.app.watchmanagerstub",
        "name": "Galaxy Wearable Stub",
        "category": "promotional",
        "risk": "safe",
        "description": "Stub installer for Galaxy Watch manager (can be reinstalled from Galaxy Store or Play Store)."
    },
    {
        "id": "com.samsung.android.app.sharelive",
        "name": "Quick Share Live / Music Share",
        "category": "promotional",
        "risk": "safe",
        "description": "Background shared playback broadcast service."
    },
    {
        "id": "com.rsupport.rs.activity.rsupport.aas2",
        "name": "Samsung Smart Tutor (Remote Support)",
        "category": "promotional",
        "risk": "safe",
        "description": "Remote customer diagnostics client by RSupport. Safe to remove."
    },
    {
        "id": "com.sec.android.easyMover",
        "name": "Samsung Smart Switch",
        "category": "promotional",
        "risk": "safe",
        "description": "Data migration tool. Safe to remove once initial device setup is completed."
    },
    {
        "id": "com.sec.android.easyMover.Agent",
        "name": "Smart Switch Agent",
        "category": "promotional",
        "risk": "safe",
        "description": "Background receiver daemon for Smart Switch data transfer."
    },
    {
        "id": "com.samsung.android.smartswitchassistant",
        "name": "Smart Switch Setup Assistant",
        "category": "promotional",
        "risk": "safe",
        "description": "Setup wizard helper for device migration."
    },

    # ==========================================
    # 8. Microsoft Pre-installs (SAFE / OPTIONAL)
    # ==========================================
    {
        "id": "com.microsoft.office.officehubrow",
        "name": "Microsoft 365 (Office Hub)",
        "category": "microsoft",
        "risk": "safe",
        "description": "Preloaded Microsoft Office aggregator hub."
    },
    {
        "id": "com.microsoft.skydrive",
        "name": "Microsoft OneDrive",
        "category": "microsoft",
        "risk": "optional",
        "description": "Pre-installed OneDrive client. Note: Samsung Gallery uses this if cloud sync is enabled."
    },
    {
        "id": "com.microsoft.appmanager",
        "name": "Link to Windows Service",
        "category": "microsoft",
        "risk": "optional",
        "description": "Daemon for pairing your Galaxy phone with a Windows PC (Phone Link)."
    },
    {
        "id": "com.linkedin.android",
        "name": "LinkedIn App",
        "category": "microsoft",
        "risk": "optional",
        "description": "LinkedIn professional network application (Preserved and excluded from debloat presets)."
    },

    # ==========================================
    # 9. Carrier & Partner Pre-installs (SAFE)
    # ==========================================
    {
        "id": "com.aura.oobe.samsung",
        "name": "Aura / AppCloud Carrier Installer",
        "category": "carrier_bloat",
        "risk": "safe",
        "description": "Stealth installer pushed by carriers to download unwanted games and apps."
    },
    {
        "id": "com.aura.oobe.samsung.gl",
        "name": "Aura Global Installer",
        "category": "carrier_bloat",
        "risk": "safe",
        "description": "Secondary variant of carrier app downloader."
    },
    {
        "id": "com.ironsource.aura.samsung",
        "name": "IronSource Aura Advertising",
        "category": "carrier_bloat",
        "risk": "safe",
        "description": "Monetization and promotional app engine."
    },
    {
        "id": "com.mygalaxy",
        "name": "Samsung My Galaxy (India)",
        "category": "carrier_bloat",
        "risk": "safe",
        "description": "Regional portal app pre-installed on Indian Galaxy phones. Sends marketing notifications."
    },
    {
        "id": "com.netflix.partner.activation",
        "name": "Netflix Partner Activation Stub",
        "category": "carrier_bloat",
        "risk": "safe",
        "description": "Pre-installed activation stub for Netflix."
    },
    {
        "id": "com.spotify.music",
        "name": "Spotify Stub",
        "category": "carrier_bloat",
        "risk": "optional",
        "description": "Pre-installed Spotify client stub."
    },

    # ==========================================
    # 10. Game Optimizing Service (GOS) & Gaming Hub (OPTIONAL)
    # ==========================================
    {
        "id": "com.samsung.android.game.gos",
        "name": "Game Optimizing Service (GOS)",
        "category": "gos_gaming",
        "risk": "safe",
        "description": "Artificially throttles Exynos 2400e CPU & Xclipse 940 GPU clock speeds. Removing/disabling restores full unthrottled flagship performance!"
    },
    {
        "id": "com.samsung.android.game.gamehome",
        "name": "Gaming Hub / Game Center",
        "category": "gos_gaming",
        "risk": "optional",
        "description": "Samsung Game library and launcher. Safe to remove if you do not use Gaming Hub."
    },
    {
        "id": "com.samsung.android.game.gametools",
        "name": "Game Booster / In-Game Tools",
        "category": "gos_gaming",
        "risk": "optional",
        "description": "Floating in-game dashboard for FPS monitoring and screen recording."
    },

    # ==========================================
    # 11. Google Optional Apps (OPTIONAL)
    # ==========================================
    {
        "id": "com.google.android.videos",
        "name": "Google TV (Play Movies)",
        "category": "google_optional",
        "risk": "safe",
        "description": "Google TV store and streaming service aggregator. Safe to remove."
    },
    {
        "id": "com.google.android.apps.tachyon",
        "name": "Google Meet",
        "category": "google_optional",
        "risk": "safe",
        "description": "Google video conferencing client. Safe to remove if you use WhatsApp, Teams or Zoom."
    },
    {
        "id": "com.google.android.apps.youtube.music",
        "name": "YouTube Music",
        "category": "google_optional",
        "risk": "safe",
        "description": "Pre-installed YouTube Music client."
    },
    {
        "id": "com.google.android.youtube",
        "name": "YouTube",
        "category": "google_optional",
        "risk": "optional",
        "description": "Official YouTube app. Remove if using alternative players like Revanced."
    },
    {
        "id": "com.google.android.apps.docs",
        "name": "Google Drive",
        "category": "google_optional",
        "risk": "optional",
        "description": "Pre-installed Google Drive client."
    },
    {
        "id": "com.google.android.apps.photos",
        "name": "Google Photos",
        "category": "google_optional",
        "risk": "optional",
        "description": "Google cloud photo backup app."
    },
    {
        "id": "com.android.chrome",
        "name": "Google Chrome",
        "category": "google_optional",
        "risk": "optional",
        "description": "Chrome browser. WARNING: Make sure you have another browser installed before removing!"
    },

    # ==========================================
    # 12. Samsung Ecosystem Apps (OPTIONAL / CAUTION)
    # ==========================================
    {
        "id": "com.sec.android.app.sbrowser",
        "name": "Samsung Internet Browser",
        "category": "samsung_optional",
        "risk": "optional",
        "description": "Samsung web browser. Safe to remove if using Brave, Chrome, or Firefox."
    },
    {
        "id": "com.sec.android.app.samsungapps",
        "name": "Galaxy Store",
        "category": "samsung_optional",
        "risk": "caution",
        "description": "Samsung App Store. Required for updating Good Lock modules and Samsung system app components."
    },
    {
        "id": "com.samsung.android.oneconnect",
        "name": "SmartThings",
        "category": "samsung_optional",
        "risk": "optional",
        "description": "Samsung Smart Home automation & device manager."
    },
    {
        "id": "com.sec.android.app.shealth",
        "name": "Samsung Health",
        "category": "samsung_optional",
        "risk": "optional",
        "description": "Health and fitness tracker. Remove if you do not track health metrics."
    },
    {
        "id": "com.samsung.android.scloud",
        "name": "Samsung Cloud Sync",
        "category": "samsung_optional",
        "risk": "caution",
        "description": "Syncs Wi-Fi passwords, Bluetooth pairings, and Samsung Notes across Galaxy devices."
    },
    {
        "id": "com.samsung.android.spay",
        "name": "Samsung Wallet / Pay",
        "category": "samsung_optional",
        "risk": "optional",
        "description": "Samsung credit cards and digital key wallet. Keep if you use Samsung Pay."
    },
    {
        "id": "com.samsung.android.spaymini",
        "name": "Samsung Pay Mini (India Variant)",
        "category": "samsung_optional",
        "risk": "optional",
        "description": "Lightweight UPI payment client preloaded on Indian Galaxy phones."
    },
    {
        "id": "com.samsung.android.themestore",
        "name": "Galaxy Themes",
        "category": "samsung_optional",
        "risk": "optional",
        "description": "Samsung theme and icon pack store."
    },
    {
        "id": "com.samsung.android.forest",
        "name": "Samsung Digital Wellbeing",
        "category": "samsung_optional",
        "risk": "optional",
        "description": "Screen time monitoring and focus mode manager. Preserved in presets."
    },

    # =========================================================================
    # 13. GALAXY AI SUITE (CRITICAL / PRESERVED - DO NOT REMOVE - DANGER)
    # =========================================================================
    {
        "id": "com.google.android.googlequicksearchbox",
        "name": "Google App (POWERS CIRCLE TO SEARCH)",
        "category": "galaxy_ai",
        "risk": "danger",
        "description": "CRITICAL GALAXY AI! Underpins 'Circle to Search' on Galaxy S24 FE. DO NOT REMOVE."
    },
    {
        "id": "com.sec.android.mimage.photoretouching",
        "name": "Generative Photo Edit Engine (GALAXY AI)",
        "category": "galaxy_ai",
        "risk": "danger",
        "description": "CRITICAL GALAXY AI! Powers Generative Fill, Object Eraser, and Reflection Removal in Gallery. DO NOT REMOVE."
    },
    {
        "id": "com.samsung.android.scs",
        "name": "Samsung Core Services (ON-DEVICE AI BRAIN)",
        "category": "galaxy_ai",
        "risk": "danger",
        "description": "CRITICAL GALAXY AI! On-device intelligence engine handling Note Assist, Summaries, and Language AI. DO NOT REMOVE."
    },
    {
        "id": "com.samsung.android.intellivoiceservice",
        "name": "Intelligent Voice Service (GALAXY AI)",
        "category": "galaxy_ai",
        "risk": "danger",
        "description": "CRITICAL GALAXY AI! Powers Live Call Translation and Voice Interpreter. DO NOT REMOVE."
    },
    {
        "id": "com.samsung.android.offline.langpack",
        "name": "Galaxy AI Language Models",
        "category": "galaxy_ai",
        "risk": "danger",
        "description": "Offline language recognition models for Galaxy AI on-device processing. DO NOT REMOVE."
    },
    {
        "id": "com.samsung.android.callassistant",
        "name": "Samsung Call Assistant (AI CALL SCREENING & TEXT CALL)",
        "category": "galaxy_ai",
        "risk": "danger",
        "description": "CRITICAL AI CALLING! Powers Bixby Text Call, Automatic Speech-to-Text & Live AI Call Screening. DO NOT REMOVE."
    },

    # =========================================================================
    # 14. CRITICAL PHONE CORE & HARDWARE (DO NOT REMOVE - DANGER)
    # =========================================================================
    {
        "id": "com.android.phone",
        "name": "Cellular Radio & Telephony Subsystem",
        "category": "phone_critical",
        "risk": "danger",
        "description": "CRITICAL PHONE CORE! Controls SIM cards, cellular radio, and mobile data. DO NOT REMOVE."
    },
    {
        "id": "com.samsung.android.incallui",
        "name": "In-Call Screen User Interface",
        "category": "phone_critical",
        "risk": "danger",
        "description": "CRITICAL PHONE CORE! Renders call answer, mute, speaker, and in-call screen. DO NOT REMOVE."
    },
    {
        "id": "com.samsung.android.dialer",
        "name": "Samsung Phone Dialer",
        "category": "phone_critical",
        "risk": "danger",
        "description": "CRITICAL PHONE CORE! Main phone app for making phone calls. DO NOT REMOVE."
    },
    {
        "id": "com.android.server.telecom",
        "name": "Android Telecom Subsystem",
        "category": "phone_critical",
        "risk": "danger",
        "description": "CRITICAL PHONE CORE! Core OS call routing. DO NOT REMOVE."
    },
    {
        "id": "com.sec.phone",
        "name": "Samsung Telephony Framework",
        "category": "phone_critical",
        "risk": "danger",
        "description": "CRITICAL PHONE CORE! Samsung proprietary RIL and modem bridge. DO NOT REMOVE."
    },
    {
        "id": "com.samsung.android.emergencymode.service",
        "name": "Emergency SOS & Location Service",
        "category": "phone_critical",
        "risk": "danger",
        "description": "CRITICAL PHONE SAFETY! Handles Emergency SOS, 911 / 112 dialing, and location beaconing. DO NOT REMOVE."
    },
    {
        "id": "com.samsung.android.app.telephonyui",
        "name": "Telephony UI & VoLTE/VoWiFi",
        "category": "phone_critical",
        "risk": "danger",
        "description": "CRITICAL PHONE CORE! Wi-Fi Calling and Voice over LTE call engine. DO NOT REMOVE."
    },
    {
        "id": "com.samsung.android.biometrics",
        "name": "Optical Under-Display Fingerprint Sensor",
        "category": "phone_critical",
        "risk": "danger",
        "description": "CRITICAL HARDWARE! Optical fingerprint sensor driver and calibration engine. DO NOT REMOVE."
    },
    {
        "id": "com.samsung.android.biometrics.service",
        "name": "Biometrics Security Service",
        "category": "phone_critical",
        "risk": "danger",
        "description": "CRITICAL HARDWARE! Knox keystore biometric verification. DO NOT REMOVE."
    },
    {
        "id": "com.sec.android.app.camera",
        "name": "Samsung Triple Camera Hardware App",
        "category": "phone_critical",
        "risk": "danger",
        "description": "CRITICAL HARDWARE! 50MP main, 8MP 3x OIS telephoto, and ultrawide camera driver. DO NOT REMOVE."
    },
    {
        "id": "com.sec.android.gallery3d",
        "name": "Samsung Gallery",
        "category": "phone_critical",
        "risk": "danger",
        "description": "CRITICAL CAMERA ECOSYSTEM! Host application for Galaxy AI photo processing. DO NOT REMOVE."
    },
    {
        "id": "com.samsung.android.app.notes",
        "name": "Samsung Notes (Note Assist Host)",
        "category": "phone_critical",
        "risk": "danger",
        "description": "Note-taking application with Galaxy AI Note Assist integration. DO NOT REMOVE."
    },
    {
        "id": "com.samsung.android.honeyboard",
        "name": "Samsung Keyboard (Honeyboard)",
        "category": "phone_critical",
        "risk": "danger",
        "description": "Main keyboard featuring AI Chat Assist and translation. DO NOT REMOVE without another keyboard installed!"
    },
    {
        "id": "com.sec.android.app.launcher",
        "name": "One UI Home (Main Phone Launcher)",
        "category": "phone_critical",
        "risk": "danger",
        "description": "CRITICAL SYSTEM! Main phone home screen. Removing causes bootloop without third-party launcher. DO NOT REMOVE."
    },
    {
        "id": "com.android.systemui",
        "name": "Android System UI",
        "category": "phone_critical",
        "risk": "danger",
        "description": "CRITICAL SYSTEM! Status bar, quick settings, and navigation gestures. DO NOT REMOVE."
    },
    {
        "id": "com.samsung.android.app.cocktailbarservice",
        "name": "Edge Panels & Split Screen",
        "category": "phone_critical",
        "risk": "danger",
        "description": "Edge panels and split-screen app pairing service. DO NOT REMOVE."
    }
]

def get_packages_by_category(category_key: str) -> List[Dict[str, Any]]:
    return [p for p in PACKAGES if p["category"] == category_key]

def get_packages_by_risk(risk_level: str) -> List[Dict[str, Any]]:
    return [p for p in PACKAGES if p["risk"] == risk_level]

def get_package_map() -> Dict[str, Dict[str, Any]]:
    return {p["id"]: p for p in PACKAGES}
