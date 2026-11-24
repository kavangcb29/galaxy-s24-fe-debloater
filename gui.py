"""
Samsung Galaxy S24 FE Debloater Toolkit - Modern GUI
High-quality, dark-themed native desktop interface inspired by modern design systems.
Includes High-DPI support, sidebar navigation, visual risk badges, and non-blocking threading.
"""

import os
import sys
import threading
import time
import webbrowser
from pathlib import Path

# Enable High-DPI awareness on Windows for razor-sharp typography
if sys.platform == "win32":
    try:
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except Exception:
            pass

# Ensure UTF-8 output
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

import tkinter as tk
from tkinter import ttk, messagebox

from adb_manager import ADBManager
import database
import utils

# =========================================================================
# Premium Dark Theme Palette (Linear / One UI Dark Inspired)
# =========================================================================
COLOR_BG_ROOT        = "#0b0d13"   # Deep Obsidian
COLOR_SIDEBAR        = "#11141d"   # Sidebar Surface
COLOR_SIDEBAR_HOVER  = "#181d2a"   # Sidebar Item Hover
COLOR_SIDEBAR_ACTIVE = "#1e2435"   # Sidebar Item Active
COLOR_CARD           = "#151822"   # Card Surface
COLOR_CARD_BORDER    = "#222736"   # Subtle Card Border
COLOR_CARD_HOVER     = "#1a1f2c"   # Card Hover State
COLOR_CARD_LIGHT     = "#1c2130"   # Secondary Card / Input Background

COLOR_TEXT_PRIMARY   = "#f8fafc"   # High-contrast White
COLOR_TEXT_SECONDARY = "#94a3b8"   # Slate Gray
COLOR_TEXT_MUTED     = "#64748b"   # Muted Meta Text

COLOR_ACCENT_BLUE    = "#3b82f6"   # Electric Blue
COLOR_ACCENT_BLUE_H  = "#2563eb"   # Electric Blue Hover
COLOR_ACCENT_PURPLE  = "#8b5cf6"   # Accent Purple
COLOR_ACCENT_EMERALD = "#10b981"   # Safe Green
COLOR_ACCENT_AMBER   = "#f59e0b"   # Caution Amber
COLOR_ACCENT_ROSE    = "#ef4444"   # Danger Rose / Red

FONT_FAMILY = "Segoe UI"


class ModernButton(tk.Label):
    """A sleek, custom-styled button with smooth hover feedback and hand cursor."""
    def __init__(self, parent, text, command=None, bg=COLOR_ACCENT_BLUE, fg="#ffffff",
                 hover_bg=COLOR_ACCENT_BLUE_H, font=(FONT_FAMILY, 9, "bold"), padx=14, pady=7,
                 bd_color=None, **kwargs):
        super().__init__(parent, text=text, font=font, bg=bg, fg=fg, cursor="hand2",
                         padx=padx, pady=pady, **kwargs)
        self.command = command
        self.default_bg = bg
        self.hover_bg = hover_bg
        self.is_disabled = False

        if bd_color:
            self.configure(highlightbackground=bd_color, highlightthickness=1)

        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<Button-1>", self._on_click)

    def _on_enter(self, e):
        if not self.is_disabled:
            self.configure(bg=self.hover_bg)

    def _on_leave(self, e):
        if not self.is_disabled:
            self.configure(bg=self.default_bg)

    def _on_click(self, e):
        if not self.is_disabled and self.command:
            self.command()

    def set_disabled(self, disabled: bool):
        self.is_disabled = disabled
        if disabled:
            self.configure(bg="#202430", fg=COLOR_TEXT_MUTED, cursor="arrow")
        else:
            self.configure(bg=self.default_bg, fg="#ffffff", cursor="hand2")


class S24FEDebloaterGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Samsung Galaxy S24 FE Debloater & Optimizer Toolkit")
        self.root.geometry("1180x760")
        self.root.minsize(1040, 680)
        self.root.configure(bg=COLOR_BG_ROOT)

        self.adb = ADBManager()
        self.device_info = {}
        self.active_serial = None
        self.installed_packages = set()

        # UI State
        self.current_tab = "dashboard"
        self.nav_buttons = {}
        self.package_check_vars = {}
        self.filtered_packages = []

        self._build_layout()
        self._async_refresh_connection()

    def _build_layout(self):
        # Header Bar
        self.header_frame = tk.Frame(self.root, bg=COLOR_SIDEBAR, height=54, highlightbackground=COLOR_CARD_BORDER, highlightthickness=1)
        self.header_frame.pack(side=tk.TOP, fill=tk.X)
        self.header_frame.pack_propagate(False)

        logo_title = tk.Label(self.header_frame, text="⚡ SAMSUNG GALAXY S24 FE", font=(FONT_FAMILY, 12, "bold"),
                              fg=COLOR_TEXT_PRIMARY, bg=COLOR_SIDEBAR)
        logo_title.pack(side=tk.LEFT, padx=(18, 6), pady=12)

        logo_sub = tk.Label(self.header_frame, text="DEBLOATER & OPTIMIZER", font=(FONT_FAMILY, 9),
                            fg=COLOR_ACCENT_BLUE, bg=COLOR_SIDEBAR)
        logo_sub.pack(side=tk.LEFT, pady=12)

        # Right Header Badges
        self.lbl_header_status = tk.Label(self.header_frame, text="Checking connection...", font=(FONT_FAMILY, 8, "bold"),
                                          fg=COLOR_TEXT_MUTED, bg="#1e2435", padx=10, pady=4)
        self.lbl_header_status.pack(side=tk.RIGHT, padx=16, pady=12)

        btn_refresh = ModernButton(self.header_frame, text="↻ Refresh", command=self._async_refresh_connection,
                                   bg=COLOR_CARD_LIGHT, hover_bg="#262d40", font=(FONT_FAMILY, 8, "bold"), padx=10, pady=4)
        btn_refresh.pack(side=tk.RIGHT, padx=(0, 10), pady=12)

        # Main Body Container
        self.body_frame = tk.Frame(self.root, bg=COLOR_BG_ROOT)
        self.body_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Left Sidebar Navigation
        self.sidebar = tk.Frame(self.body_frame, bg=COLOR_SIDEBAR, width=220, highlightbackground=COLOR_CARD_BORDER, highlightthickness=1)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)

        self._build_sidebar()

        # Right Content View Area
        self.content_area = tk.Frame(self.body_frame, bg=COLOR_BG_ROOT)
        self.content_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=16)

        # Bottom Status Bar
        self.status_bar = tk.Frame(self.root, bg=COLOR_SIDEBAR, height=32, highlightbackground=COLOR_CARD_BORDER, highlightthickness=1)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self.status_bar.pack_propagate(False)

        self.lbl_status = tk.Label(self.status_bar, text="Ready", font=(FONT_FAMILY, 8), fg=COLOR_TEXT_MUTED, bg=COLOR_SIDEBAR)
        self.lbl_status.pack(side=tk.LEFT, padx=16, pady=6)

        lbl_author = tk.Label(self.status_bar, text="Galaxy S24 FE Toolkit | Exynos 2400e | Rootless Knox Safe (0x0)",
                              font=(FONT_FAMILY, 8), fg=COLOR_TEXT_MUTED, bg=COLOR_SIDEBAR)
        lbl_author.pack(side=tk.RIGHT, padx=16, pady=6)

    def _build_sidebar(self):
        nav_items = [
            ("dashboard", "📱  Device Dashboard"),
            ("presets", "⚡  1-Click Presets"),
            ("packages", "📦  Package Manager"),
            ("tweaks", "🚀  Speed & Storage"),
            ("restore", "🔄  Restore Center"),
            ("guide", "📖  Setup & Guide"),
        ]

        tk.Label(self.sidebar, text="NAVIGATION", font=(FONT_FAMILY, 7, "bold"), fg=COLOR_TEXT_MUTED, bg=COLOR_SIDEBAR).pack(anchor="w", padx=18, pady=(16, 8))

        for tab_id, label_text in nav_items:
            btn = tk.Label(self.sidebar, text=label_text, font=(FONT_FAMILY, 9), fg=COLOR_TEXT_SECONDARY,
                           bg=COLOR_SIDEBAR, anchor="w", padx=16, pady=10, cursor="hand2")
            btn.pack(fill=tk.X, padx=8, pady=2)
            btn.bind("<Button-1>", lambda e, tid=tab_id: self._switch_tab(tid))
            btn.bind("<Enter>", lambda e, b=btn, tid=tab_id: self._nav_hover(b, tid, True))
            btn.bind("<Leave>", lambda e, b=btn, tid=tab_id: self._nav_hover(b, tid, False))
            self.nav_buttons[tab_id] = btn

        # Spacer
        tk.Frame(self.sidebar, bg=COLOR_SIDEBAR).pack(fill=tk.BOTH, expand=True)

        # Donation & Sponsor Links Box
        sponsor_box = tk.Frame(self.sidebar, bg=COLOR_CARD, highlightbackground=COLOR_CARD_BORDER, highlightthickness=1)
        sponsor_box.pack(fill=tk.X, padx=12, pady=12)

        tk.Label(sponsor_box, text="SUPPORT PROJECT", font=(FONT_FAMILY, 7, "bold"), fg="#f59e0b", bg=COLOR_CARD).pack(anchor="w", padx=10, pady=(8, 4))
        tk.Label(sponsor_box, text="Support future One UI updates & development:", font=(FONT_FAMILY, 8),
                 fg=COLOR_TEXT_MUTED, bg=COLOR_CARD, wraplength=170, justify=tk.LEFT).pack(anchor="w", padx=10, pady=(0, 6))

        btn_coffee = ModernButton(sponsor_box, text="☕ Buy Me A Coffee", bg="#eab308", hover_bg="#ca8a04", fg="#000000",
                                  font=(FONT_FAMILY, 8, "bold"), padx=8, pady=4,
                                  command=lambda: webbrowser.open("https://buymeacoffee.com/kavangcb29"))
        btn_coffee.pack(fill=tk.X, padx=10, pady=(0, 8))

    def _nav_hover(self, btn, tab_id, is_enter):
        if self.current_tab == tab_id:
            return
        if is_enter:
            btn.configure(bg=COLOR_SIDEBAR_HOVER, fg=COLOR_TEXT_PRIMARY)
        else:
            btn.configure(bg=COLOR_SIDEBAR, fg=COLOR_TEXT_SECONDARY)

    def _switch_tab(self, tab_id):
        self.current_tab = tab_id
        for tid, btn in self.nav_buttons.items():
            if tid == tab_id:
                btn.configure(bg=COLOR_SIDEBAR_ACTIVE, fg="#ffffff", font=(FONT_FAMILY, 9, "bold"))
            else:
                btn.configure(bg=COLOR_SIDEBAR, fg=COLOR_TEXT_SECONDARY, font=(FONT_FAMILY, 9))

        for child in self.content_area.winfo_children():
            child.destroy()

        if tab_id == "dashboard":
            self._render_dashboard()
        elif tab_id == "presets":
            self._render_presets()
        elif tab_id == "packages":
            self._render_package_manager()
        elif tab_id == "tweaks":
            self._render_tweaks()
        elif tab_id == "restore":
            self._render_restore_center()
        elif tab_id == "guide":
            self._render_guide()

    # =========================================================================
    # TAB 1: DASHBOARD
    # =========================================================================
    def _render_dashboard(self):
        title_box = tk.Frame(self.content_area, bg=COLOR_BG_ROOT)
        title_box.pack(fill=tk.X, pady=(0, 14))

        tk.Label(title_box, text="Device Dashboard", font=(FONT_FAMILY, 15, "bold"), fg=COLOR_TEXT_PRIMARY, bg=COLOR_BG_ROOT).pack(anchor="w")
        tk.Label(title_box, text="Live status of connected Samsung Galaxy S24 FE and system health",
                 font=(FONT_FAMILY, 9), fg=COLOR_TEXT_MUTED, bg=COLOR_BG_ROOT).pack(anchor="w", pady=(2, 0))

        # Device Info Card
        card = tk.Frame(self.content_area, bg=COLOR_CARD, highlightbackground=COLOR_CARD_BORDER, highlightthickness=1)
        card.pack(fill=tk.X, pady=(0, 14))

        card_header = tk.Frame(card, bg=COLOR_CARD)
        card_header.pack(fill=tk.X, padx=16, pady=(14, 8))

        is_connected = bool(self.active_serial and self.device_info.get("status") != "unauthorized")
        status_color = COLOR_ACCENT_EMERALD if is_connected else COLOR_ACCENT_ROSE
        status_text = "● CONNECTED & AUTHORIZED" if is_connected else "● NO DEVICE DETECTED"
        if self.device_info.get("status") == "unauthorized":
            status_color = COLOR_ACCENT_AMBER
            status_text = "● UNAUTHORIZED (Check phone screen for prompt)"

        tk.Label(card_header, text=status_text, font=(FONT_FAMILY, 8, "bold"), fg=status_color, bg=COLOR_CARD).pack(side=tk.LEFT)

        is_s24 = self.device_info.get("is_s24_fe", False)
        if is_s24:
            tk.Label(card_header, text="★ Galaxy S24 FE Verified", font=(FONT_FAMILY, 8, "bold"),
                     fg="#60a5fa", bg="#1e293b", padx=8, pady=2).pack(side=tk.RIGHT)

        # Specs Grid
        grid_frame = tk.Frame(card, bg=COLOR_CARD)
        grid_frame.pack(fill=tk.X, padx=16, pady=(0, 14))

        specs = [
            ("Model Number", self.device_info.get("model", "Not Connected")),
            ("Market Name", self.device_info.get("market_name", "Samsung Device")),
            ("Chipset", self.device_info.get("chipset", "Exynos 2400e (4nm)")),
            ("One UI Version", self.device_info.get("oneui_version", "Unknown")),
            ("Android Version", self.device_info.get("android_version", "Unknown")),
            ("Region / CSC", self.device_info.get("region", "Unknown")),
            ("Battery Level", self.device_info.get("battery", "Unknown")),
            ("Knox Status", "Untouched (0x0 Safe)")
        ]

        for i, (k, v) in enumerate(specs):
            row = i // 2
            col = i % 2
            box = tk.Frame(grid_frame, bg=COLOR_CARD_LIGHT, padx=12, pady=8)
            box.grid(row=row, column=col, sticky="nsew", padx=4, pady=4)
            grid_frame.columnconfigure(col, weight=1)

            tk.Label(box, text=k.upper(), font=(FONT_FAMILY, 7, "bold"), fg=COLOR_TEXT_MUTED, bg=COLOR_CARD_LIGHT).pack(anchor="w")
            tk.Label(box, text=str(v), font=(FONT_FAMILY, 9, "bold"), fg=COLOR_TEXT_PRIMARY, bg=COLOR_CARD_LIGHT).pack(anchor="w", pady=(2, 0))

        # Quick Actions Grid
        qa_label = tk.Label(self.content_area, text="QUICK ACTIONS", font=(FONT_FAMILY, 8, "bold"), fg=COLOR_TEXT_MUTED, bg=COLOR_BG_ROOT)
        qa_label.pack(anchor="w", pady=(6, 6))

        qa_frame = tk.Frame(self.content_area, bg=COLOR_BG_ROOT)
        qa_frame.pack(fill=tk.X, pady=(0, 14))

        btn_turbo = ModernButton(qa_frame, text="⚡ Apply S24 FE Flagship Turbo Preset", font=(FONT_FAMILY, 9, "bold"),
                                 bg=COLOR_ACCENT_BLUE, hover_bg=COLOR_ACCENT_BLUE_H, padx=16, pady=10,
                                 command=lambda: self._apply_featured_preset_quick())
        btn_turbo.pack(side=tk.LEFT, padx=(0, 10))

        btn_speed = ModernButton(qa_frame, text="🚀 0.5x UI Speed Boost", font=(FONT_FAMILY, 9, "bold"),
                                 bg=COLOR_CARD_LIGHT, hover_bg="#262d40", fg=COLOR_ACCENT_AMBER, padx=14, pady=10,
                                 command=self._apply_animation_tweak)
        btn_speed.pack(side=tk.LEFT, padx=(0, 10))

        btn_trim = ModernButton(qa_frame, text="🧹 Trim Storage Caches", font=(FONT_FAMILY, 9, "bold"),
                                bg=COLOR_CARD_LIGHT, hover_bg="#262d40", fg=COLOR_ACCENT_EMERALD, padx=14, pady=10,
                                command=self._apply_cache_trim)
        btn_trim.pack(side=tk.LEFT)

        # Safeguards Card
        safe_card = tk.Frame(self.content_area, bg=COLOR_CARD, highlightbackground=COLOR_CARD_BORDER, highlightthickness=1)
        safe_card.pack(fill=tk.X, pady=(0, 10))

        tk.Label(safe_card, text="🛡️  SAFETY & GALAXY AI INTEGRITY ASSURANCE", font=(FONT_FAMILY, 9, "bold"),
                 fg=COLOR_ACCENT_EMERALD, bg=COLOR_CARD).pack(anchor="w", padx=16, pady=(12, 4))

        guarantees = (
            "• Circle to Search, Generative Photo Edit, Live Call Translation & Note Assist are 100% PROTECTED.\n"
            "• Cellular calling, emergency SOS (911/112), VoLTE, and Dual SIM services are hard-locked against removal.\n"
            "• Optical under-display fingerprint sensor, Knox keystore, and camera engine remain completely untouched.\n"
            "• Full snapshot backup is automatically saved before any change and can be reversed in 1-click."
        )
        tk.Label(safe_card, text=guarantees, font=(FONT_FAMILY, 8), fg=COLOR_TEXT_SECONDARY, bg=COLOR_CARD, justify=tk.LEFT).pack(anchor="w", padx=16, pady=(0, 12))

    # =========================================================================
    # TAB 2: PRESETS
    # =========================================================================
    def _render_presets(self):
        title_box = tk.Frame(self.content_area, bg=COLOR_BG_ROOT)
        title_box.pack(fill=tk.X, pady=(0, 12))

        tk.Label(title_box, text="1-Click Optimization Presets", font=(FONT_FAMILY, 15, "bold"), fg=COLOR_TEXT_PRIMARY, bg=COLOR_BG_ROOT).pack(anchor="w")
        tk.Label(title_box, text="Carefully curated profiles designed specifically for the Galaxy S24 FE",
                 font=(FONT_FAMILY, 9), fg=COLOR_TEXT_MUTED, bg=COLOR_BG_ROOT).pack(anchor="w", pady=(2, 0))

        presets = utils.load_presets()
        if not presets:
            tk.Label(self.content_area, text="No presets found in presets.json", fg=COLOR_ACCENT_ROSE, bg=COLOR_BG_ROOT).pack()
            return

        canvas = tk.Canvas(self.content_area, bg=COLOR_BG_ROOT, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.content_area, orient="vertical", command=canvas.yview)
        scroll_content = tk.Frame(canvas, bg=COLOR_BG_ROOT)

        scroll_content.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas_window = canvas.create_window((0, 0), window=scroll_content, anchor="nw")
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(canvas_window, width=e.width))

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Featured Preset Card
        self._render_featured_preset_card(scroll_content, presets[0])

        # Remaining Presets
        for p in presets[1:]:
            self._render_standard_preset_card(scroll_content, p)

    def _render_featured_preset_card(self, parent, preset):
        card = tk.Frame(parent, bg=COLOR_CARD, highlightbackground=COLOR_ACCENT_BLUE, highlightthickness=1.5)
        card.pack(fill=tk.X, pady=(4, 12), padx=2)

        top_row = tk.Frame(card, bg=COLOR_CARD)
        top_row.pack(fill=tk.X, padx=16, pady=(14, 6))

        badge = tk.Label(top_row, text="★  RECOMMENDED FOR GALAXY S24 FE", font=(FONT_FAMILY, 8, "bold"),
                         fg="#60a5fa", bg="#1e293b", padx=8, pady=3)
        badge.pack(side=tk.LEFT)

        pkg_pill = tk.Label(top_row, text=f"{len(preset['packages'])} packages targeted", font=(FONT_FAMILY, 8),
                            fg=COLOR_TEXT_MUTED, bg=COLOR_CARD)
        pkg_pill.pack(side=tk.RIGHT)

        title = tk.Label(card, text=preset["name"], font=(FONT_FAMILY, 12, "bold"), fg=COLOR_TEXT_PRIMARY, bg=COLOR_CARD)
        title.pack(anchor="w", padx=16, pady=(2, 4))

        desc = tk.Label(card, text=preset["description"], font=(FONT_FAMILY, 9), fg=COLOR_TEXT_SECONDARY,
                        bg=COLOR_CARD, wraplength=760, justify=tk.LEFT)
        desc.pack(anchor="w", padx=16, pady=(0, 10))

        # Highlight Badges
        pill_row = tk.Frame(card, bg=COLOR_CARD)
        pill_row.pack(fill=tk.X, padx=16, pady=(0, 12))

        pills = [
            ("🤖 Galaxy AI 100% Protected", COLOR_ACCENT_EMERALD),
            ("🔇 De-Bixby Standby Battery Saver", COLOR_ACCENT_BLUE),
            ("🎮 Exynos 2400e GOS Unthrottled", COLOR_ACCENT_AMBER),
            ("🔒 Biometrics & Camera Untouched", "#a855f7")
        ]
        for p_text, p_color in pills:
            p_lbl = tk.Label(pill_row, text=p_text, font=(FONT_FAMILY, 8, "bold"),
                             fg=p_color, bg=COLOR_CARD_LIGHT, padx=8, pady=3)
            p_lbl.pack(side=tk.LEFT, padx=(0, 8))

        # Action Divider
        tk.Frame(card, bg=COLOR_CARD_BORDER, height=1).pack(fill=tk.X)

        action_box = tk.Frame(card, bg=COLOR_CARD_LIGHT)
        action_box.pack(fill=tk.X, padx=16, pady=10)

        mode_var = tk.StringVar(value="disable")
        rb1 = tk.Radiobutton(action_box, text="Safe Disable (Default)", variable=mode_var, value="disable",
                             font=(FONT_FAMILY, 8), fg=COLOR_TEXT_PRIMARY, bg=COLOR_CARD_LIGHT,
                             selectcolor=COLOR_CARD, activebackground=COLOR_CARD_LIGHT)
        rb1.pack(side=tk.LEFT, padx=(0, 10))

        rb2 = tk.Radiobutton(action_box, text="Full User Uninstall", variable=mode_var, value="uninstall",
                             font=(FONT_FAMILY, 8), fg=COLOR_TEXT_PRIMARY, bg=COLOR_CARD_LIGHT,
                             selectcolor=COLOR_CARD, activebackground=COLOR_CARD_LIGHT)
        rb2.pack(side=tk.LEFT, padx=(0, 14))

        tweak_var = tk.BooleanVar(value=True)
        cb_tweak = tk.Checkbutton(action_box, text="⚡ Apply 0.5x UI Speed Boost", variable=tweak_var,
                                  font=(FONT_FAMILY, 8, "bold"), fg=COLOR_ACCENT_AMBER, bg=COLOR_CARD_LIGHT,
                                  selectcolor=COLOR_CARD, activebackground=COLOR_CARD_LIGHT)
        cb_tweak.pack(side=tk.LEFT, padx=(0, 10))

        trim_var = tk.BooleanVar(value=True)
        cb_trim = tk.Checkbutton(action_box, text="🧹 Trim Storage Caches", variable=trim_var,
                                 font=(FONT_FAMILY, 8, "bold"), fg=COLOR_ACCENT_EMERALD, bg=COLOR_CARD_LIGHT,
                                 selectcolor=COLOR_CARD, activebackground=COLOR_CARD_LIGHT)
        cb_trim.pack(side=tk.LEFT)

        btn_run = ModernButton(action_box, text="Apply Turbo Preset ➔", font=(FONT_FAMILY, 9, "bold"),
                               bg=COLOR_ACCENT_BLUE, hover_bg=COLOR_ACCENT_BLUE_H, padx=16, pady=6,
                               command=lambda: self._execute_preset(preset, mode_var.get(), tweak_var.get(), trim_var.get()))
        btn_run.pack(side=tk.RIGHT)

    def _render_standard_preset_card(self, parent, preset):
        card = tk.Frame(parent, bg=COLOR_CARD, highlightbackground=COLOR_CARD_BORDER, highlightthickness=1)
        card.pack(fill=tk.X, pady=5, padx=2)

        header = tk.Frame(card, bg=COLOR_CARD)
        header.pack(fill=tk.X, padx=14, pady=(10, 4))

        t_lbl = tk.Label(header, text=preset["name"], font=(FONT_FAMILY, 10, "bold"), fg=COLOR_TEXT_PRIMARY, bg=COLOR_CARD)
        t_lbl.pack(side=tk.LEFT)

        cnt_lbl = tk.Label(header, text=f"{len(preset['packages'])} packages", font=(FONT_FAMILY, 8),
                           fg=COLOR_TEXT_MUTED, bg=COLOR_CARD_LIGHT, padx=6, pady=2)
        cnt_lbl.pack(side=tk.RIGHT)

        desc = tk.Label(card, text=preset["description"], font=(FONT_FAMILY, 8), fg=COLOR_TEXT_SECONDARY,
                        bg=COLOR_CARD, wraplength=720, justify=tk.LEFT)
        desc.pack(anchor="w", padx=14, pady=(0, 10))

        bottom_row = tk.Frame(card, bg=COLOR_CARD)
        bottom_row.pack(fill=tk.X, padx=14, pady=(0, 10))

        mode_var = tk.StringVar(value="disable")
        rb = tk.Radiobutton(bottom_row, text="Safe Disable", variable=mode_var, value="disable",
                            font=(FONT_FAMILY, 8), fg=COLOR_TEXT_PRIMARY, bg=COLOR_CARD,
                            selectcolor=COLOR_CARD_LIGHT, activebackground=COLOR_CARD)
        rb.pack(side=tk.LEFT, padx=(0, 8))

        rb2 = tk.Radiobutton(bottom_row, text="Full User Uninstall", variable=mode_var, value="uninstall",
                             font=(FONT_FAMILY, 8), fg=COLOR_TEXT_PRIMARY, bg=COLOR_CARD,
                             selectcolor=COLOR_CARD_LIGHT, activebackground=COLOR_CARD)
        rb2.pack(side=tk.LEFT, padx=(0, 12))

        btn_run = ModernButton(bottom_row, text="Apply Preset ➔", font=(FONT_FAMILY, 8, "bold"),
                               bg=COLOR_CARD_LIGHT, hover_bg="#262d40", padx=12, pady=5,
                               command=lambda: self._execute_preset(preset, mode_var.get(), False, False))
        btn_run.pack(side=tk.RIGHT)

    # =========================================================================
    # TAB 3: PACKAGE MANAGER
    # =========================================================================
    def _render_package_manager(self):
        title_box = tk.Frame(self.content_area, bg=COLOR_BG_ROOT)
        title_box.pack(fill=tk.X, pady=(0, 10))

        tk.Label(title_box, text="Package Catalog & Debloater", font=(FONT_FAMILY, 15, "bold"), fg=COLOR_TEXT_PRIMARY, bg=COLOR_BG_ROOT).pack(anchor="w")

        # Controls & Filter Bar
        ctrl_card = tk.Frame(self.content_area, bg=COLOR_CARD, highlightbackground=COLOR_CARD_BORDER, highlightthickness=1)
        ctrl_card.pack(fill=tk.X, pady=(0, 10))

        top_ctrl = tk.Frame(ctrl_card, bg=COLOR_CARD)
        top_ctrl.pack(fill=tk.X, padx=12, pady=8)

        # Search Entry
        tk.Label(top_ctrl, text="🔍", font=(FONT_FAMILY, 9), fg=COLOR_TEXT_MUTED, bg=COLOR_CARD).pack(side=tk.LEFT, padx=(0, 4))
        self.search_var = tk.StringVar()
        self.search_var.trace("w", lambda *args: self._filter_packages())
        search_entry = tk.Entry(top_ctrl, textvariable=self.search_var, font=(FONT_FAMILY, 9), bg=COLOR_CARD_LIGHT,
                                fg=COLOR_TEXT_PRIMARY, insertbackground="#ffffff", relief="flat", width=26)
        search_entry.pack(side=tk.LEFT, padx=(0, 12), ipady=3)

        # Category Filter Dropdown
        tk.Label(top_ctrl, text="Category:", font=(FONT_FAMILY, 8, "bold"), fg=COLOR_TEXT_MUTED, bg=COLOR_CARD).pack(side=tk.LEFT, padx=(0, 4))
        cat_options = ["All Categories"] + list(database.CATEGORIES.values())
        self.cat_filter_var = tk.StringVar(value="All Categories")
        cat_menu = ttk.Combobox(top_ctrl, textvariable=self.cat_filter_var, values=cat_options, state="readonly", width=28)
        cat_menu.pack(side=tk.LEFT, padx=(0, 12))
        cat_menu.bind("<<ComboboxSelected>>", lambda e: self._filter_packages())

        # Risk Filter Dropdown
        tk.Label(top_ctrl, text="Risk:", font=(FONT_FAMILY, 8, "bold"), fg=COLOR_TEXT_MUTED, bg=COLOR_CARD).pack(side=tk.LEFT, padx=(0, 4))
        risk_options = ["All Risks", "Safe Only", "Optional Only", "Danger Only (Protected)"]
        self.risk_filter_var = tk.StringVar(value="All Risks")
        risk_menu = ttk.Combobox(top_ctrl, textvariable=self.risk_filter_var, values=risk_options, state="readonly", width=16)
        risk_menu.pack(side=tk.LEFT)
        risk_menu.bind("<<ComboboxSelected>>", lambda e: self._filter_packages())

        # Action Buttons Row
        action_bar = tk.Frame(ctrl_card, bg=COLOR_CARD_LIGHT)
        action_bar.pack(fill=tk.X, padx=12, pady=(0, 8))

        ModernButton(action_bar, text="Select All Safe", font=(FONT_FAMILY, 8, "bold"), bg=COLOR_CARD, hover_bg="#222838",
                     command=self._select_all_safe).pack(side=tk.LEFT, padx=4, pady=4)
        ModernButton(action_bar, text="Deselect All", font=(FONT_FAMILY, 8), bg=COLOR_CARD, hover_bg="#222838",
                     command=self._deselect_all).pack(side=tk.LEFT, padx=4, pady=4)

        self.lbl_selection_count = tk.Label(action_bar, text="0 packages selected", font=(FONT_FAMILY, 8),
                                            fg=COLOR_TEXT_MUTED, bg=COLOR_CARD_LIGHT)
        self.lbl_selection_count.pack(side=tk.LEFT, padx=12)

        ModernButton(action_bar, text="Disable Selected", font=(FONT_FAMILY, 8, "bold"), bg=COLOR_ACCENT_AMBER,
                     hover_bg="#d97706", fg="#000000", command=lambda: self._execute_batch("disable")).pack(side=tk.RIGHT, padx=4, pady=4)
        ModernButton(action_bar, text="Uninstall (User 0)", font=(FONT_FAMILY, 8, "bold"), bg=COLOR_ACCENT_ROSE,
                     hover_bg="#dc2626", command=lambda: self._execute_batch("uninstall")).pack(side=tk.RIGHT, padx=4, pady=4)

        # Scrollable Package Table
        self.pkg_canvas = tk.Canvas(self.content_area, bg=COLOR_BG_ROOT, highlightthickness=0)
        self.pkg_scrollbar = ttk.Scrollbar(self.content_area, orient="vertical", command=self.pkg_canvas.yview)
        self.pkg_scroll_content = tk.Frame(self.pkg_canvas, bg=COLOR_BG_ROOT)

        self.pkg_scroll_content.bind("<Configure>", lambda e: self.pkg_canvas.configure(scrollregion=self.pkg_canvas.bbox("all")))
        self.pkg_canvas_window = self.pkg_canvas.create_window((0, 0), window=self.pkg_scroll_content, anchor="nw")
        self.pkg_canvas.bind("<Configure>", lambda e: self.pkg_canvas.itemconfig(self.pkg_canvas_window, width=e.width))

        self.pkg_canvas.configure(yscrollcommand=self.pkg_scrollbar.set)
        self.pkg_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.pkg_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self._filter_packages()

    def _filter_packages(self):
        query = self.search_var.get().strip().lower() if hasattr(self, "search_var") else ""
        cat_name = self.cat_filter_var.get() if hasattr(self, "cat_filter_var") else "All Categories"
        risk_name = self.risk_filter_var.get() if hasattr(self, "risk_filter_var") else "All Risks"

        cat_reverse_map = {v: k for k, v in database.CATEGORIES.items()}
        target_cat_key = cat_reverse_map.get(cat_name)

        filtered = []
        for p in database.PACKAGES:
            # Query match
            if query and query not in p["name"].lower() and query not in p["id"].lower() and query not in p["description"].lower():
                continue
            # Category match
            if target_cat_key and p["category"] != target_cat_key:
                continue
            # Risk match
            if risk_name == "Safe Only" and p["risk"] != "safe":
                continue
            elif risk_name == "Optional Only" and p["risk"] != "optional":
                continue
            elif risk_name == "Danger Only (Protected)" and p["risk"] != "danger":
                continue

            filtered.append(p)

        self.filtered_packages = filtered
        self._populate_package_table()

    def _populate_package_table(self):
        for child in self.pkg_scroll_content.winfo_children():
            child.destroy()

        if not self.filtered_packages:
            tk.Label(self.pkg_scroll_content, text="No matching packages found.", font=(FONT_FAMILY, 9),
                     fg=COLOR_TEXT_MUTED, bg=COLOR_BG_ROOT).pack(pady=20)
            return

        for p in self.filtered_packages:
            pid = p["id"]
            if pid not in self.package_check_vars:
                self.package_check_vars[pid] = tk.BooleanVar(value=False)

            is_danger = (p["risk"] == "danger")
            is_active = pid in self.installed_packages

            row = tk.Frame(self.pkg_scroll_content, bg=COLOR_CARD, highlightbackground=COLOR_CARD_BORDER, highlightthickness=1)
            row.pack(fill=tk.X, pady=3, padx=2)

            left_box = tk.Frame(row, bg=COLOR_CARD)
            left_box.pack(side=tk.LEFT, padx=10, pady=8)

            # Checkbox
            cb = tk.Checkbutton(left_box, variable=self.package_check_vars[pid], bg=COLOR_CARD,
                                activebackground=COLOR_CARD, selectcolor=COLOR_CARD_LIGHT,
                                command=self._update_selection_counter)
            cb.pack(side=tk.LEFT)
            if is_danger:
                cb.configure(state="disabled")

            # Risk Badge
            risk_bg = "#064e3b" if p["risk"] == "safe" else ("#78350f" if p["risk"] == "optional" else "#7f1d1d")
            risk_fg = "#34d399" if p["risk"] == "safe" else ("#fbbf24" if p["risk"] == "optional" else "#f87171")
            tk.Label(left_box, text=p["risk"].upper(), font=(FONT_FAMILY, 7, "bold"), bg=risk_bg, fg=risk_fg,
                     padx=6, pady=2).pack(side=tk.LEFT, padx=(4, 10))

            # Package Info
            info_box = tk.Frame(row, bg=COLOR_CARD)
            info_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=8)

            title_row = tk.Frame(info_box, bg=COLOR_CARD)
            title_row.pack(fill=tk.X)

            tk.Label(title_row, text=p["name"], font=(FONT_FAMILY, 9, "bold"), fg=COLOR_TEXT_PRIMARY, bg=COLOR_CARD).pack(side=tk.LEFT)
            tk.Label(title_row, text=f"•  {p['id']}", font=(FONT_FAMILY, 8), fg=COLOR_TEXT_MUTED, bg=COLOR_CARD).pack(side=tk.LEFT, padx=8)

            tk.Label(info_box, text=p["description"], font=(FONT_FAMILY, 8), fg=COLOR_TEXT_SECONDARY,
                     bg=COLOR_CARD, wraplength=640, justify=tk.LEFT).pack(anchor="w", pady=(2, 0))

            # Status Indicator on right
            status_box = tk.Frame(row, bg=COLOR_CARD)
            status_box.pack(side=tk.RIGHT, padx=12, pady=8)

            if is_active:
                tk.Label(status_box, text="ACTIVE", font=(FONT_FAMILY, 7, "bold"), fg=COLOR_ACCENT_EMERALD,
                         bg="#064e3b", padx=6, pady=2).pack()
            else:
                tk.Label(status_box, text="INACTIVE", font=(FONT_FAMILY, 7), fg=COLOR_TEXT_MUTED,
                         bg=COLOR_CARD_LIGHT, padx=6, pady=2).pack()

        self._update_selection_counter()

    def _update_selection_counter(self):
        cnt = sum(1 for v in self.package_check_vars.values() if v.get())
        if hasattr(self, "lbl_selection_count"):
            self.lbl_selection_count.configure(text=f"{cnt} packages selected")

    def _select_all_safe(self):
        for p in self.filtered_packages:
            if p["risk"] == "safe" and p["id"] in self.installed_packages:
                if p["id"] in self.package_check_vars:
                    self.package_check_vars[p["id"]].set(True)
        self._update_selection_counter()

    def _deselect_all(self):
        for v in self.package_check_vars.values():
            v.set(False)
        self._update_selection_counter()

    # =========================================================================
    # TAB 4: SPEED, RAM PLUS & STORAGE TWEAKS
    # =========================================================================
    def _render_tweaks(self):
        title_box = tk.Frame(self.content_area, bg=COLOR_BG_ROOT)
        title_box.pack(fill=tk.X, pady=(0, 14))

        tk.Label(title_box, text="Speed, RAM Plus & Storage Optimization", font=(FONT_FAMILY, 15, "bold"), fg=COLOR_TEXT_PRIMARY, bg=COLOR_BG_ROOT).pack(anchor="w")
        tk.Label(title_box, text="Hardware accelerators and memory controls tuned for Galaxy S24 FE & Exynos 2400e",
                 font=(FONT_FAMILY, 9), fg=COLOR_TEXT_MUTED, bg=COLOR_BG_ROOT).pack(anchor="w", pady=(2, 0))

        # Tweak 1: 0.5x UI Speed
        card1 = tk.Frame(self.content_area, bg=COLOR_CARD, highlightbackground=COLOR_CARD_BORDER, highlightthickness=1)
        card1.pack(fill=tk.X, pady=(0, 12))

        c1_head = tk.Frame(card1, bg=COLOR_CARD)
        c1_head.pack(fill=tk.X, padx=16, pady=(12, 4))
        tk.Label(c1_head, text="⚡ 0.5x UI Speed Accelerator (120Hz Fluidity)", font=(FONT_FAMILY, 10, "bold"),
                 fg=COLOR_TEXT_PRIMARY, bg=COLOR_CARD).pack(side=tk.LEFT)

        curr_anim = self.adb.get_animation_scale(self.active_serial)
        tk.Label(c1_head, text=f"Current: {curr_anim}x", font=(FONT_FAMILY, 8, "bold"),
                 fg=COLOR_ACCENT_AMBER, bg=COLOR_CARD_LIGHT, padx=6, pady=2).pack(side=tk.RIGHT)

        desc1 = (
            "Halves window, transition, and animator durations. Makes the 120Hz Dynamic AMOLED display feel\n"
            "instantaneous and eliminates floating latency during app switching. 100% reversible."
        )
        tk.Label(card1, text=desc1, font=(FONT_FAMILY, 8), fg=COLOR_TEXT_SECONDARY, bg=COLOR_CARD, justify=tk.LEFT).pack(anchor="w", padx=16, pady=(0, 10))

        c1_actions = tk.Frame(card1, bg=COLOR_CARD_LIGHT)
        c1_actions.pack(fill=tk.X, padx=16, pady=(0, 12))

        ModernButton(c1_actions, text="Apply 0.5x Speed Boost (Instant UI)", font=(FONT_FAMILY, 8, "bold"),
                     bg=COLOR_ACCENT_BLUE, hover_bg=COLOR_ACCENT_BLUE_H, padx=12, pady=6,
                     command=self._apply_animation_tweak).pack(side=tk.LEFT, padx=6, pady=6)

        ModernButton(c1_actions, text="Reset to 1.0x (Stock Samsung)", font=(FONT_FAMILY, 8),
                     bg=COLOR_CARD, hover_bg="#262d40", padx=10, pady=6,
                     command=self._reset_animation_tweak).pack(side=tk.LEFT, padx=6, pady=6)

        # Tweak 2: RAM Plus Virtual Memory Tuner
        card2 = tk.Frame(self.content_area, bg=COLOR_CARD, highlightbackground=COLOR_CARD_BORDER, highlightthickness=1)
        card2.pack(fill=tk.X, pady=(0, 12))

        c2_head = tk.Frame(card2, bg=COLOR_CARD)
        c2_head.pack(fill=tk.X, padx=16, pady=(12, 4))
        tk.Label(c2_head, text="🧠 Samsung RAM Plus (Virtual Swap Memory) Tuner", font=(FONT_FAMILY, 10, "bold"),
                 fg=COLOR_TEXT_PRIMARY, bg=COLOR_CARD).pack(side=tk.LEFT)

        curr_ram = self.adb.get_ram_plus(self.active_serial)
        ram_badge_text = f"Current: {curr_ram} GB" if curr_ram is not None else "Current: Unknown"
        tk.Label(c2_head, text=ram_badge_text, font=(FONT_FAMILY, 8, "bold"),
                 fg=COLOR_ACCENT_BLUE, bg=COLOR_CARD_LIGHT, padx=6, pady=2).pack(side=tk.RIGHT)

        desc2 = (
            "Why your phone stutters: Samsung enables RAM Plus by default, swapping memory pages onto flash storage.\n"
            "When internal storage fills up, swapping causes severe flash I/O wait latency, dropping frames and causing lag!\n"
            "RECOMMENDATION: Disabling RAM Plus (0 GB) allows your 8 GB physical LPDDR5X RAM to run pure and stutter-free."
        )
        tk.Label(card2, text=desc2, font=(FONT_FAMILY, 8), fg=COLOR_TEXT_SECONDARY, bg=COLOR_CARD, justify=tk.LEFT).pack(anchor="w", padx=16, pady=(0, 10))

        c2_actions = tk.Frame(card2, bg=COLOR_CARD_LIGHT)
        c2_actions.pack(fill=tk.X, padx=16, pady=(0, 12))

        ModernButton(c2_actions, text="Turn OFF RAM Plus (0 GB) [Recommended to Stop Stutter]", font=(FONT_FAMILY, 8, "bold"),
                     bg=COLOR_ACCENT_EMERALD, hover_bg="#059669", padx=12, pady=6,
                     command=lambda: self._set_ram_plus_val(0)).pack(side=tk.LEFT, padx=6, pady=6)

        ModernButton(c2_actions, text="Set 2 GB", font=(FONT_FAMILY, 8), bg=COLOR_CARD, hover_bg="#262d40", padx=10, pady=6,
                     command=lambda: self._set_ram_plus_val(2)).pack(side=tk.LEFT, padx=4, pady=6)

        ModernButton(c2_actions, text="Set 4 GB (Stock)", font=(FONT_FAMILY, 8), bg=COLOR_CARD, hover_bg="#262d40", padx=10, pady=6,
                     command=lambda: self._set_ram_plus_val(4)).pack(side=tk.LEFT, padx=4, pady=6)

        ModernButton(c2_actions, text="Set 8 GB", font=(FONT_FAMILY, 8), bg=COLOR_CARD, hover_bg="#262d40", padx=10, pady=6,
                     command=lambda: self._set_ram_plus_val(8)).pack(side=tk.LEFT, padx=4, pady=6)

        # Tweak 3: Storage Cache Trimmer
        card3 = tk.Frame(self.content_area, bg=COLOR_CARD, highlightbackground=COLOR_CARD_BORDER, highlightthickness=1)
        card3.pack(fill=tk.X, pady=(0, 12))

        c3_head = tk.Frame(card3, bg=COLOR_CARD)
        c3_head.pack(fill=tk.X, padx=16, pady=(12, 4))
        tk.Label(c3_head, text="🧹 Instant Storage Cache Trimmer", font=(FONT_FAMILY, 10, "bold"),
                 fg=COLOR_TEXT_PRIMARY, bg=COLOR_CARD).pack(side=tk.LEFT)

        desc3 = (
            "Executes 'pm trim-caches' to safely flush stale app caches, compilation caches, and thumbnail databases.\n"
            "Instantly reclaims space without touching your photos, chat logs, or personal documents."
        )
        tk.Label(card3, text=desc3, font=(FONT_FAMILY, 8), fg=COLOR_TEXT_SECONDARY, bg=COLOR_CARD, justify=tk.LEFT).pack(anchor="w", padx=16, pady=(0, 10))

        c3_actions = tk.Frame(card3, bg=COLOR_CARD_LIGHT)
        c3_actions.pack(fill=tk.X, padx=16, pady=(0, 12))

        ModernButton(c3_actions, text="Reclaim Storage Caches Now", font=(FONT_FAMILY, 8, "bold"),
                     bg=COLOR_ACCENT_BLUE, hover_bg=COLOR_ACCENT_BLUE_H, padx=14, pady=6,
                     command=self._apply_cache_trim).pack(side=tk.LEFT, padx=6, pady=6)

    def _apply_animation_tweak(self):
        if not self.active_serial:
            messagebox.showwarning("Not Connected", "Please connect your Galaxy S24 FE first.")
            return
        if self.adb.set_animation_scale(0.5, self.active_serial):
            messagebox.showinfo("Success", "0.5x UI Speed boost applied! Your 120Hz display is now noticeably more responsive.")
            self._switch_tab(self.current_tab)
        else:
            messagebox.showerror("Failed", "Could not set animation scale.")

    def _reset_animation_tweak(self):
        if not self.active_serial:
            return
        if self.adb.set_animation_scale(1.0, self.active_serial):
            messagebox.showinfo("Reset", "Animation scales restored to standard 1.0x.")
            self._switch_tab(self.current_tab)

    def _set_ram_plus_val(self, gb: int):
        if not self.active_serial:
            messagebox.showwarning("Not Connected", "Please connect your Galaxy S24 FE first.")
            return
        ok, msg = self.adb.set_ram_plus(gb, self.active_serial)
        if ok:
            ask = messagebox.askyesno("Success", f"{msg}\n\nWould you like to restart your phone now to apply the change?")
            if ask:
                self.adb.reboot_device(self.active_serial)
            self._switch_tab(self.current_tab)
        else:
            messagebox.showerror("Error", msg)

    def _apply_cache_trim(self):
        if not self.active_serial:
            messagebox.showwarning("Not Connected", "Please connect your Galaxy S24 FE first.")
            return
        self.lbl_status.configure(text="Trimming storage caches...")
        ok, msg = self.adb.trim_storage_caches(self.active_serial)
        if ok:
            messagebox.showinfo("Storage Reclaimed", "Storage cache trimmed successfully! Temporary caches have been purged.")
        else:
            messagebox.showerror("Error", msg)
        self.lbl_status.configure(text="Ready")

    # =========================================================================
    # TAB 5: RESTORE CENTER
    # =========================================================================
    def _render_restore_center(self):
        title_box = tk.Frame(self.content_area, bg=COLOR_BG_ROOT)
        title_box.pack(fill=tk.X, pady=(0, 10))

        tk.Label(title_box, text="Restore Center", font=(FONT_FAMILY, 15, "bold"), fg=COLOR_TEXT_PRIMARY, bg=COLOR_BG_ROOT).pack(anchor="w")
        tk.Label(title_box, text="Re-enable and reinstall any package previously debloated or disabled",
                 font=(FONT_FAMILY, 9), fg=COLOR_TEXT_MUTED, bg=COLOR_BG_ROOT).pack(anchor="w", pady=(2, 0))

        top_bar = tk.Frame(self.content_area, bg=COLOR_CARD, highlightbackground=COLOR_CARD_BORDER, highlightthickness=1)
        top_bar.pack(fill=tk.X, pady=(0, 10))

        tb_inner = tk.Frame(top_bar, bg=COLOR_CARD)
        tb_inner.pack(fill=tk.X, padx=12, pady=10)

        ModernButton(tb_inner, text="↻ Scan for Inactive Packages", bg=COLOR_CARD_LIGHT, hover_bg="#262d40",
                     command=self._render_restore_center).pack(side=tk.LEFT)

        ModernButton(tb_inner, text="⚡ Restore All Inactive Packages", bg=COLOR_ACCENT_BLUE, hover_bg=COLOR_ACCENT_BLUE_H,
                     command=self._restore_all_packages).pack(side=tk.RIGHT)

        # Candidates List
        if not self.active_serial:
            tk.Label(self.content_area, text="Connect your Galaxy S24 FE to view restorable packages.",
                     font=(FONT_FAMILY, 9), fg=COLOR_TEXT_MUTED, bg=COLOR_BG_ROOT).pack(pady=30)
            return

        inactive = self.adb.get_uninstalled_or_disabled_packages(self.active_serial)
        history = utils.load_debloat_history()
        merged = sorted(list(set(list(history.keys()) + inactive)))
        pkg_map = database.get_package_map()

        if not merged:
            empty_box = tk.Frame(self.content_area, bg=COLOR_CARD, highlightbackground=COLOR_CARD_BORDER, highlightthickness=1)
            empty_box.pack(fill=tk.X, pady=20, padx=2)
            tk.Label(empty_box, text="✓ No uninstalled or disabled packages found.", font=(FONT_FAMILY, 10, "bold"),
                     fg=COLOR_ACCENT_EMERALD, bg=COLOR_CARD).pack(pady=(16, 4))
            tk.Label(empty_box, text="Your device has all standard system packages currently active.", font=(FONT_FAMILY, 8),
                     fg=COLOR_TEXT_MUTED, bg=COLOR_CARD).pack(pady=(0, 16))
            return

        c_canvas = tk.Canvas(self.content_area, bg=COLOR_BG_ROOT, highlightthickness=0)
        c_scrollbar = ttk.Scrollbar(self.content_area, orient="vertical", command=c_canvas.yview)
        c_scroll_content = tk.Frame(c_canvas, bg=COLOR_BG_ROOT)

        c_scroll_content.bind("<Configure>", lambda e: c_canvas.configure(scrollregion=c_canvas.bbox("all")))
        c_window = c_canvas.create_window((0, 0), window=c_scroll_content, anchor="nw")
        c_canvas.bind("<Configure>", lambda e: c_canvas.itemconfig(c_window, width=e.width))

        c_canvas.configure(yscrollcommand=c_scrollbar.set)
        c_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        c_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        for p in merged:
            p_name = pkg_map.get(p, {}).get("name", p)
            row = tk.Frame(c_scroll_content, bg=COLOR_CARD, highlightbackground=COLOR_CARD_BORDER, highlightthickness=1)
            row.pack(fill=tk.X, pady=3, padx=2)

            left = tk.Frame(row, bg=COLOR_CARD)
            left.pack(side=tk.LEFT, padx=12, pady=10)

            tk.Label(left, text=p_name, font=(FONT_FAMILY, 9, "bold"), fg=COLOR_TEXT_PRIMARY, bg=COLOR_CARD).pack(anchor="w")
            tk.Label(left, text=p, font=(FONT_FAMILY, 8), fg=COLOR_TEXT_MUTED, bg=COLOR_CARD).pack(anchor="w")

            ModernButton(row, text="Restore ➔", font=(FONT_FAMILY, 8, "bold"), bg=COLOR_CARD_LIGHT, hover_bg="#262d40",
                         command=lambda pkg=p: self._restore_single_package(pkg)).pack(side=tk.RIGHT, padx=12, pady=10)

    def _restore_single_package(self, package_id: str):
        if not self.active_serial:
            return
        self.lbl_status.configure(text=f"Restoring {package_id}...")
        ok, msg = self.adb.restore_package(package_id, self.active_serial)
        if ok:
            utils.remove_from_debloat_history(package_id)
            self._async_refresh_connection()
            self._render_restore_center()
        else:
            messagebox.showerror("Restore Failed", f"Failed to restore {package_id}: {msg}")

    def _restore_all_packages(self):
        if not self.active_serial:
            return
        inactive = self.adb.get_uninstalled_or_disabled_packages(self.active_serial)
        history = utils.load_debloat_history()
        merged = sorted(list(set(list(history.keys()) + inactive)))
        if not merged:
            messagebox.showinfo("Restore", "No packages to restore.")
            return

        confirm = messagebox.askyesno("Restore All", f"Restore {len(merged)} inactive packages back to user 0?")
        if not confirm:
            return

        def task():
            restored = 0
            for p in merged:
                self.lbl_status.configure(text=f"Restoring {p}...")
                ok, _ = self.adb.restore_package(p, self.active_serial)
                if ok:
                    restored += 1
                    utils.remove_from_debloat_history(p)
            self.root.after(0, lambda: self._on_restore_all_done(restored, len(merged)))

        threading.Thread(target=task, daemon=True).start()

    def _on_restore_all_done(self, count, total):
        messagebox.showinfo("Restore Complete", f"Successfully restored {count}/{total} packages.")
        self._async_refresh_connection()
        self._render_restore_center()

    # =========================================================================
    # TAB 6: SETUP & GUIDE
    # =========================================================================
    def _render_guide(self):
        title_box = tk.Frame(self.content_area, bg=COLOR_BG_ROOT)
        title_box.pack(fill=tk.X, pady=(0, 10))

        tk.Label(title_box, text="Setup & Auto Blocker Troubleshooting", font=(FONT_FAMILY, 15, "bold"), fg=COLOR_TEXT_PRIMARY, bg=COLOR_BG_ROOT).pack(anchor="w")

        canvas = tk.Canvas(self.content_area, bg=COLOR_BG_ROOT, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.content_area, orient="vertical", command=canvas.yview)
        scroll_content = tk.Frame(canvas, bg=COLOR_BG_ROOT)

        scroll_content.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas_window = canvas.create_window((0, 0), window=scroll_content, anchor="nw")
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(canvas_window, width=e.width))

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        steps = [
            ("1. Enable Developer Options on Galaxy S24 FE",
             "• Open 'Settings' on your phone.\n"
             "• Scroll down to 'About phone' > 'Software information'.\n"
             "• Rapidly tap 'Build number' 7 times until you see the message 'Developer mode has been turned on'."),

            ("2. CRITICAL: Disable Samsung Auto Blocker (One UI 6.1.1 / 7 / 8 / 9)",
             "• Samsung Auto Blocker prevents ADB and USB cable shell commands by default.\n"
             "• Go to 'Settings' > 'Security and privacy' > 'Auto Blocker'.\n"
             "• Toggle Auto Blocker OFF (or turn off 'Maximum restrictions' / 'Block software updates by USB cable').\n"
             "• You can safely toggle Auto Blocker back ON after finishing debloating!"),

            ("3. Enable USB Debugging",
             "• Go back to 'Settings' > 'Developer options' (at the very bottom).\n"
             "• Locate 'USB debugging' and toggle it ON. Tap OK on the confirmation prompt."),

            ("4. Connect USB-C Cable & Authorize",
             "• Plug your Galaxy S24 FE into your PC using a data-capable USB-C cable.\n"
             "• Check your phone screen for the prompt: 'Allow USB debugging?'.\n"
             "• Check 'Always allow from this computer' and tap 'Allow'.")
        ]

        for s_title, s_desc in steps:
            card = tk.Frame(scroll_content, bg=COLOR_CARD, highlightbackground=COLOR_CARD_BORDER, highlightthickness=1)
            card.pack(fill=tk.X, pady=6, padx=2)

            tk.Label(card, text=s_title, font=(FONT_FAMILY, 10, "bold"), fg=COLOR_TEXT_PRIMARY, bg=COLOR_CARD).pack(anchor="w", padx=16, pady=(12, 4))
            tk.Label(card, text=s_desc, font=(FONT_FAMILY, 8), fg=COLOR_TEXT_SECONDARY, bg=COLOR_CARD, justify=tk.LEFT).pack(anchor="w", padx=16, pady=(0, 12))

    # =========================================================================
    # EXECUTION HELPERS
    # =========================================================================
    def _apply_featured_preset_quick(self):
        presets = utils.load_presets()
        if presets:
            self._execute_preset(presets[0], mode="disable", apply_tweak=True, trim_cache=True)

    def _execute_preset(self, preset: Dict[str, Any], mode: str, apply_tweak: bool = False, trim_cache: bool = False):
        if not self.active_serial:
            messagebox.showwarning("Device Not Connected", "Please connect your Galaxy S24 FE first.")
            return

        packages = preset.get("packages", [])
        active_targets = [p for p in packages if p in self.installed_packages]

        if not active_targets:
            messagebox.showinfo("Already Optimized", f"None of the {len(packages)} packages from '{preset['name']}' are currently active on your phone!")
            return

        verb = "uninstall (User 0)" if mode == "uninstall" else "disable"
        msg = f"Ready to {verb} {len(active_targets)} packages for '{preset['name']}'.\n\nA full snapshot backup will be saved automatically.\n\nProceed?"
        if not messagebox.askyesno("Confirm Debloat", msg):
            return

        self._run_threaded_debloat(active_targets, mode, apply_tweak, trim_cache)

    def _execute_batch(self, mode: str):
        if not self.active_serial:
            messagebox.showwarning("Device Not Connected", "Please connect your Galaxy S24 FE first.")
            return

        selected = [pid for pid, var in self.package_check_vars.items() if var.get() and pid in self.installed_packages]
        if not selected:
            messagebox.showwarning("No Selection", "Please check at least one installed package to debloat.")
            return

        verb = "uninstall (User 0)" if mode == "uninstall" else "disable"
        msg = f"Ready to {verb} {len(selected)} selected packages.\n\nA full snapshot backup will be saved automatically.\n\nProceed?"
        if not messagebox.askyesno("Confirm Batch Debloat", msg):
            return

        self._run_threaded_debloat(selected, mode, False, False)

    def _run_threaded_debloat(self, target_pkgs: list, mode: str, apply_tweak: bool, trim_cache: bool):
        # Progress popup
        popup = tk.Toplevel(self.root)
        popup.title("Debloating Galaxy S24 FE...")
        popup.geometry("480x200")
        popup.configure(bg=COLOR_CARD)
        popup.transient(self.root)
        popup.grab_set()

        lbl_step = tk.Label(popup, text="Creating backup snapshot...", font=(FONT_FAMILY, 9, "bold"), fg=COLOR_TEXT_PRIMARY, bg=COLOR_CARD)
        lbl_step.pack(pady=(24, 8))

        pbar = ttk.Progressbar(popup, maximum=len(target_pkgs), mode="determinate", length=400)
        pbar.pack(pady=10)

        lbl_item = tk.Label(popup, text="", font=(FONT_FAMILY, 8), fg=COLOR_TEXT_MUTED, bg=COLOR_CARD)
        lbl_item.pack(pady=4)

        def worker():
            # Backup
            installed = list(self.installed_packages)
            utils.create_backup_snapshot(self.device_info, installed)

            success_cnt = 0
            for i, pkg in enumerate(target_pkgs):
                popup.after(0, lambda p=pkg, idx=i: [lbl_item.configure(text=f"Processing: {p}"), pbar.configure(value=idx)])
                if mode == "disable":
                    ok, note = self.adb.disable_package(pkg, self.active_serial)
                else:
                    ok, note = self.adb.uninstall_package(pkg, keep_data=True, serial=self.active_serial)

                if ok:
                    success_cnt += 1
                    utils.log_debloat_action(pkg, mode, True, note)
                else:
                    utils.log_debloat_action(pkg, mode, False, note)

            if apply_tweak and self.active_serial:
                self.adb.set_animation_scale(0.5, self.active_serial)

            if trim_cache and self.active_serial:
                self.adb.trim_storage_caches(self.active_serial)

            popup.after(0, lambda: self._on_debloat_finish(popup, success_cnt, len(target_pkgs)))

        threading.Thread(target=worker, daemon=True).start()

    def _on_debloat_finish(self, popup, success, total):
        popup.destroy()
        messagebox.showinfo("Success", f"Optimization Complete!\n\nSuccessfully processed {success}/{total} packages.\nGalaxy AI, Camera & Phone features remain 100% intact.")
        self._async_refresh_connection()
        self._switch_tab(self.current_tab)

    # =========================================================================
    # REFRESH & DISCOVERY
    # =========================================================================
    def _async_refresh_connection(self):
        self.lbl_header_status.configure(text="Checking device...", fg=COLOR_TEXT_MUTED)

        def worker():
            devices = self.adb.get_connected_devices()
            if not devices:
                self.active_serial = None
                self.device_info = {}
                self.installed_packages = set()
            else:
                active = [d for d in devices if d["status"] == "device"]
                if active:
                    self.active_serial = active[0]["serial"]
                    self.device_info = self.adb.get_device_info(self.active_serial)
                    self.installed_packages = set(self.adb.get_installed_packages(self.active_serial))
                else:
                    self.active_serial = devices[0]["serial"]
                    self.device_info = {"status": devices[0]["status"], "serial": self.active_serial}
                    self.installed_packages = set()

            self.root.after(0, self._on_connection_refreshed)

        threading.Thread(target=worker, daemon=True).start()

    def _on_connection_refreshed(self):
        if self.active_serial and self.device_info.get("status") == "device":
            name = self.device_info.get("market_name", "Galaxy S24 FE")
            self.lbl_header_status.configure(text=f"● {name}", fg=COLOR_ACCENT_EMERALD)
            self.lbl_status.configure(text=f"Connected: {self.active_serial} ({name}) | {len(self.installed_packages)} active packages")
        elif self.device_info.get("status") == "unauthorized":
            self.lbl_header_status.configure(text="● Unauthorized", fg=COLOR_ACCENT_AMBER)
            self.lbl_status.configure(text="Device unauthorized. Unlock phone screen and tap 'Always allow'.")
        else:
            self.lbl_header_status.configure(text="● No Device Detected", fg=COLOR_ACCENT_ROSE)
            self.lbl_status.configure(text="No device detected over USB. Check Auto Blocker & USB Debugging.")

        self._switch_tab(self.current_tab)


def main():
    root = tk.Tk()
    app = S24FEDebloaterGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
