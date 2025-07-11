#!/usr/bin/env python3
"""
clapp GUI Settings Modülü
Ayarlar sayfası - tema, dil, konfigürasyon görüntüleme
"""

import flet as ft
import json
import os
import sys
import subprocess
from gui_theme import get_theme_colors
from gui_utils import show_snackbar, create_empty_state

# Ayarlar dosyası yolu
SETTINGS_FILE = os.path.expanduser("~/.clapp/settings.json")

# Varsayılan ayarlar
DEFAULT_SETTINGS = {
    "theme": "dark",
    "language": "tr",
    "developer_name": "Kullanıcı",
    "auto_update": True,
    "show_descriptions": True
}

def build_settings(page: ft.Page):
    """Settings UI'sini oluştur"""
    theme_colors = get_theme_colors()
    
    # Header
    header = ft.Container(
        content=ft.Row([
            ft.Text(
                "Settings",
                size=24,
                weight=ft.FontWeight.BOLD,
                color=theme_colors["on_background"]
            ),
            ft.Container(expand=True),  # Spacer
            ft.Icon(ft.Icons.SETTINGS, size=28, color=theme_colors["primary"])
        ]),
        padding=ft.padding.only(bottom=20)
    )
    
    # Settings sections
    sections = [
        create_appearance_section(page),
        create_system_info_section(page),
        create_config_section(page)
    ]
    
    # Ana layout
    main_layout = ft.Column([
        header,
        ft.Column(
            controls=sections,
            spacing=20,
            scroll=ft.ScrollMode.AUTO,
            expand=True
        )
    ], expand=True)
    
    return main_layout

def create_appearance_section(page):
    """Görünüm ayarları bölümü"""
    theme_colors = get_theme_colors()
    current_settings = load_settings()
    
    # Theme toggle
    def on_theme_change(e):
        new_theme = "dark" if e.control.value else "light"
        current_settings["theme"] = new_theme
        save_settings(current_settings)
        
        # Tema değişikliği
        page.theme_mode = ft.ThemeMode.DARK if new_theme == "dark" else ft.ThemeMode.LIGHT
        page.update()
        show_snackbar(page, f"🎨 Tema değiştirildi: {new_theme}")
    
    theme_switch = ft.Switch(
        label="Koyu Tema",
        value=current_settings["theme"] == "dark",
        on_change=on_theme_change,
        active_color=theme_colors["primary"]
    )
    
    # Language dropdown
    def on_language_change(e):
        new_lang = e.control.value
        current_settings["language"] = new_lang
        save_settings(current_settings)
        show_snackbar(page, f"🌍 Dil değiştirildi: {new_lang}")
    
    language_dropdown = ft.Dropdown(
        label="Dil",
        value=current_settings["language"],
        options=[
            ft.dropdown.Option("tr", "Türkçe"),
            ft.dropdown.Option("en", "English")
        ],
        on_change=on_language_change
    )
    
    # Developer name
    def on_developer_name_change(e):
        current_settings["developer_name"] = e.control.value
        save_settings(current_settings)
    
    developer_name_field = ft.TextField(
        label="Geliştirici Adı",
        value=current_settings["developer_name"],
        on_change=on_developer_name_change
    )
    
    appearance_card = ft.Card(
        content=ft.Container(
            content=ft.Column([
                ft.Text("🎨 Görünüm", size=18, weight=ft.FontWeight.BOLD),
                theme_switch,
                language_dropdown,
                developer_name_field,
                ft.ElevatedButton(
                    "Ayarları Sıfırla",
                    icon=ft.Icons.RESTORE,
                    on_click=lambda _: reset_settings(page),
                    bgcolor=ft.Colors.RED_400,
                    color=ft.Colors.WHITE
                )
            ], spacing=15),
            padding=20
        )
    )
    
    return appearance_card

def create_system_info_section(page):
    """Sistem bilgileri bölümü"""
    theme_colors = get_theme_colors()
    
    # Sistem bilgilerini al
    def get_system_info():
        try:
            # clapp yolu
            clapp_path = os.path.abspath(".")
            
            # Python yolu
            python_path = sys.executable
            
            # Apps klasörü
            apps_dir = os.path.join(clapp_path, "apps")
            apps_count = len([d for d in os.listdir(apps_dir) if os.path.isdir(os.path.join(apps_dir, d))]) if os.path.exists(apps_dir) else 0
            
            return {
                "clapp_path": clapp_path,
                "python_path": python_path,
                "apps_count": apps_count,
                "platform": sys.platform,
                "python_version": sys.version.split()[0]
            }
        except Exception as e:
            return {"error": str(e)}
    
    system_info = get_system_info()
    
    info_items = []
    if "error" not in system_info:
        info_items = [
            ft.Text(f"📁 clapp Yolu: {system_info['clapp_path']}", size=12, selectable=True),
            ft.Text(f"🐍 Python: {system_info['python_path']}", size=12, selectable=True),
            ft.Text(f"📦 Yüklü Uygulamalar: {system_info['apps_count']}", size=12),
            ft.Text(f"💻 Platform: {system_info['platform']}", size=12),
            ft.Text(f"🔢 Python Sürümü: {system_info['python_version']}", size=12)
        ]
    else:
        info_items = [ft.Text(f"❌ Hata: {system_info['error']}", size=12, color=ft.Colors.RED)]
    
    system_info_card = ft.Card(
        content=ft.Container(
            content=ft.Column([
                ft.Text("ℹ️ Sistem Bilgileri", size=18, weight=ft.FontWeight.BOLD),
                *info_items
            ], spacing=10),
            padding=20
        )
    )
    
    return system_info_card

def create_config_section(page):
    """Konfigürasyon bölümü"""
    theme_colors = get_theme_colors()
    
    # Config dosyasını göster
    def show_config_file(_):
        try:
            config_text = ""
            
            # Ayarlar dosyası
            if os.path.exists(SETTINGS_FILE):
                with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
                    config_text += "=== Settings (settings.json) ===\n"
                    config_text += f.read()
                    config_text += "\n\n"
            
            # Version dosyası
            version_file = "version.json"
            if os.path.exists(version_file):
                with open(version_file, 'r', encoding='utf-8') as f:
                    config_text += "=== Version (version.json) ===\n"
                    config_text += f.read()
                    config_text += "\n\n"
            
            if not config_text:
                config_text = "Konfigürasyon dosyası bulunamadı."
            
            show_config_dialog(page, config_text)
            
        except Exception as e:
            show_snackbar(page, f"❌ Config okuma hatası: {str(e)}", is_error=True)
    
    # Config dosyasını düzenle
    def edit_config_file(_):
        show_snackbar(page, "⚠️ Config düzenleme henüz desteklenmiyor")
    
    config_card = ft.Card(
        content=ft.Container(
            content=ft.Column([
                ft.Text("⚙️ Konfigürasyon", size=18, weight=ft.FontWeight.BOLD),
                ft.Text("Ayar dosyalarını görüntüleyin ve düzenleyin", size=14, color=theme_colors["outline"]),
                ft.Row([
                    ft.ElevatedButton(
                        "Config Görüntüle",
                        icon=ft.Icons.VISIBILITY,
                        on_click=show_config_file
                    ),
                    ft.OutlinedButton(
                        "Config Düzenle",
                        icon=ft.Icons.EDIT,
                        on_click=edit_config_file
                    )
                ], spacing=10)
            ], spacing=15),
            padding=20
        )
    )
    
    return config_card

def show_config_dialog(page, config_text):
    """Config dialog'u göster"""
    def close_dialog(_):
        dialog.open = False
        page.update()
    
    def copy_to_clipboard(_):
        page.set_clipboard(config_text)
        show_snackbar(page, "📋 Config panoya kopyalandı")
    
    dialog = ft.AlertDialog(
        title=ft.Text("Konfigürasyon Dosyaları"),
        content=ft.Container(
            content=ft.Text(
                config_text,
                selectable=True,
                size=12
            ),
            width=600,
            height=400,
            padding=10
        ),
        actions=[
            ft.TextButton("Panoya Kopyala", on_click=copy_to_clipboard),
            ft.TextButton("Kapat", on_click=close_dialog)
        ]
    )
    
    page.dialog = dialog
    dialog.open = True
    page.update()

def reset_settings(page):
    """Ayarları sıfırla"""
    try:
        save_settings(DEFAULT_SETTINGS.copy())
        show_snackbar(page, "✅ Ayarlar sıfırlandı")
        # Sayfayı yenile
        page.theme_mode = ft.ThemeMode.DARK
        page.update()
    except Exception as e:
        show_snackbar(page, f"❌ Ayar sıfırlama hatası: {str(e)}", is_error=True)

def load_settings():
    """
    Ayarları yükler. Dosya yoksa varsayılan ayarları döndürür.
    
    Returns:
        dict: Ayarlar dictionary'si
    """
    try:
        # Ayarlar dizini yoksa oluştur
        settings_dir = os.path.dirname(SETTINGS_FILE)
        if not os.path.exists(settings_dir):
            os.makedirs(settings_dir)
        
        # Ayarlar dosyasını yükle
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
                settings = json.load(f)
            
            # Eksik ayarları varsayılanlarla tamamla
            for key, value in DEFAULT_SETTINGS.items():
                if key not in settings:
                    settings[key] = value
            
            return settings
        else:
            return DEFAULT_SETTINGS.copy()
    
    except (json.JSONDecodeError, FileNotFoundError):
        return DEFAULT_SETTINGS.copy()

def save_settings(settings):
    """
    Ayarları dosyaya kaydeder.
    
    Args:
        settings (dict): Kaydedilecek ayarlar
    """
    try:
        # Ayarlar dizini yoksa oluştur
        settings_dir = os.path.dirname(SETTINGS_FILE)
        if not os.path.exists(settings_dir):
            os.makedirs(settings_dir)
        
        # Ayarları kaydet
        with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
            json.dump(settings, f, ensure_ascii=False, indent=2)
    
    except Exception as e:
        print(f"Ayarlar kaydedilirken hata oluştu: {e}")

# Yardımcı fonksiyonlar (geriye uyumluluk için)
def get_current_theme():
    """
    Mevcut tema ayarını döndürür.
    
    Returns:
        str: "dark" veya "light"
    """
    settings = load_settings()
    return settings.get("theme", "dark")

def get_current_language():
    """
    Mevcut dil ayarını döndürür.
    
    Returns:
        str: "tr" veya "en"
    """
    settings = load_settings()
    return settings.get("language", "tr")

def render_settings_screen(page, theme_mode="dark"):
    """
    Eski API - geriye uyumluluk için
    """
    return build_settings(page) 