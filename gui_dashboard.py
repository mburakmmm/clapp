#!/usr/bin/env python3
"""
clapp GUI Dashboard Modülü
Yüklü uygulamaları listeler ve her uygulama için action butonları sağlar
"""

import flet as ft
import os
import subprocess
import threading
from package_registry import list_packages, list_app_names, get_manifest
from gui_theme import get_theme_colors
from gui_utils import create_app_card, show_snackbar, create_empty_state

def build_dashboard(page: ft.Page):
    """Dashboard UI'sini oluştur"""
    theme_colors = get_theme_colors()
    
    # Header
    header = ft.Container(
        content=ft.Row([
            ft.Text(
                "Yüklü Uygulamalar",
                size=24,
                weight=ft.FontWeight.BOLD,
                color=theme_colors["on_background"]
            ),
            ft.Container(expand=True),  # Spacer
            ft.IconButton(
                icon=ft.Icons.REFRESH,
                tooltip="Listeyi Yenile",
                on_click=lambda _: refresh_dashboard(page)
            )
        ]),
        padding=ft.padding.only(bottom=20)
    )
    
    # Yüklü uygulamaları listele
    apps = list_app_names()
    
    if not apps:
        # Hiç uygulama yoksa boş durum göster
        content = create_empty_state(
            icon=ft.Icons.APPS,
            title="Hiç Uygulama Yüklü Değil",
            description="Başlamak için yeni bir uygulama yükleyin",
            action_text="App Store'a Git",
            action_callback=lambda _: navigate_to_store(page)
        )
    else:
        # Uygulama kartlarını oluştur
        app_cards = []
        for app in apps:
            card = create_dashboard_app_card(app, page)
            app_cards.append(card)
        
        # Scrollable liste
        content = ft.Column(
            controls=app_cards,
            spacing=10,
            scroll=ft.ScrollMode.AUTO,
            expand=True
        )
    
    # FloatingActionButton
    fab = ft.FloatingActionButton(
        icon=ft.Icons.ADD,
        text="Yeni Uygulama",
        tooltip="Yeni uygulama yükle",
        on_click=lambda _: show_install_dialog(page),
        bgcolor=theme_colors["primary"],
        foreground_color=theme_colors["on_primary"]
    )
    
    # Ana layout
    main_layout = ft.Column([
        header,
        content
    ], expand=True)
    
    # Page'e FAB ekle
    page.floating_action_button = fab
    page.update()
    
    return main_layout

def create_dashboard_app_card(app, page):
    """Dashboard için uygulama kartı oluştur"""
    theme_colors = get_theme_colors()
    
    # Manifest bilgilerini al
    manifest = get_manifest(app)
    if not manifest:
        return ft.Card(
            content=ft.Container(
                content=ft.Text(f"Hata: {app} manifest'i okunamadı"),
                padding=15
            )
        )
    
    name = manifest.get("name", app)
    version = manifest.get("version", "1.0.0")
    language = manifest.get("language", "unknown")
    description = manifest.get("description", "Açıklama yok")
    
    # Language badge
    language_badge = ft.Container(
        content=ft.Text(
            language.upper(),
            size=10,
            weight=ft.FontWeight.BOLD,
            color=theme_colors["on_primary"]
        ),
        padding=ft.padding.symmetric(horizontal=8, vertical=4),
        bgcolor=theme_colors["primary"],
        border_radius=12
    )
    
    # Action buttons
    action_buttons = ft.Row([
        ft.ElevatedButton(
            "Çalıştır",
            icon=ft.Icons.PLAY_ARROW,
            on_click=lambda _: run_app(app, page),
            bgcolor=theme_colors["primary"],
            color=theme_colors["on_primary"]
        ),
        ft.OutlinedButton(
            "Bilgi",
            icon=ft.Icons.INFO,
            on_click=lambda _: show_app_info(app, page)
        ),
        ft.OutlinedButton(
            "Konum",
            icon=ft.Icons.FOLDER,
            on_click=lambda _: show_app_location(app, page)
        ),
        ft.OutlinedButton(
            "Kaldır",
            icon=ft.Icons.DELETE,
            on_click=lambda _: show_remove_dialog(app, page),
            style=ft.ButtonStyle(
                color=ft.Colors.RED_400
            )
        )
    ], spacing=10)
    
    # Kart içeriği
    card_content = ft.Container(
        content=ft.Column([
            # Header row
            ft.Row([
                ft.Text(name, size=18, weight=ft.FontWeight.BOLD),
                ft.Container(expand=True),
                language_badge
            ]),
            # Version
            ft.Text(f"v{version}", size=12, color=theme_colors["outline"]),
            # Description
            ft.Text(
                description,
                size=14,
                max_lines=2,
                overflow=ft.TextOverflow.ELLIPSIS
            ),
            ft.Divider(height=20),
            # Action buttons
            action_buttons
        ], spacing=8),
        padding=20
    )
    
    return ft.Card(
        content=card_content,
        margin=ft.margin.only(bottom=10)
    )

def run_app(app_name, page):
    """Uygulamayı çalıştır"""
    def run_in_thread():
        try:
            # CLI komutu çalıştır
            result = subprocess.run(
                ["python", "main.py", "run", app_name],
                capture_output=True,
                text=True,
                cwd=os.getcwd()
            )
            
            if result.returncode == 0:
                show_snackbar(page, f"✅ {app_name} başarıyla çalıştırıldı")
            else:
                show_snackbar(page, f"❌ Hata: {result.stderr}", is_error=True)
                
        except Exception as e:
            show_snackbar(page, f"❌ Çalıştırma hatası: {str(e)}", is_error=True)
    
    # Background thread'de çalıştır
    threading.Thread(target=run_in_thread, daemon=True).start()
    show_snackbar(page, f"🚀 {app_name} çalıştırılıyor...")

def show_app_info(app_name, page):
    """Uygulama bilgilerini göster"""
    def get_info_in_thread():
        try:
            result = subprocess.run(
                ["python", "main.py", "info", app_name],
                capture_output=True,
                text=True,
                cwd=os.getcwd()
            )
            
            if result.returncode == 0:
                # Info dialog'u göster
                show_info_dialog(page, app_name, result.stdout)
            else:
                show_snackbar(page, f"❌ Bilgi alınamadı: {result.stderr}", is_error=True)
                
        except Exception as e:
            show_snackbar(page, f"❌ Bilgi alma hatası: {str(e)}", is_error=True)
    
    threading.Thread(target=get_info_in_thread, daemon=True).start()

def show_app_location(app_name, page):
    """Uygulama konumunu göster"""
    def get_location_in_thread():
        try:
            result = subprocess.run(
                ["python", "main.py", "where", app_name],
                capture_output=True,
                text=True,
                cwd=os.getcwd()
            )
            
            if result.returncode == 0:
                location = result.stdout.strip()
                show_snackbar(page, f"📁 Konum: {location}")
            else:
                show_snackbar(page, f"❌ Konum bulunamadı: {result.stderr}", is_error=True)
                
        except Exception as e:
            show_snackbar(page, f"❌ Konum alma hatası: {str(e)}", is_error=True)
    
    threading.Thread(target=get_location_in_thread, daemon=True).start()

def show_info_dialog(page, app_name, info_text):
    """Bilgi dialog'u göster"""
    def close_dialog(_):
        dialog.open = False
        page.update()
    
    dialog = ft.AlertDialog(
        title=ft.Text(f"{app_name} - Bilgiler"),
        content=ft.Container(
            content=ft.Text(
                info_text,
                selectable=True,
                size=12
            ),
            width=500,
            height=300,
            padding=10
        ),
        actions=[
            ft.TextButton("Kapat", on_click=close_dialog)
        ]
    )
    
    page.dialog = dialog
    dialog.open = True
    page.update()

def show_remove_dialog(app_name, page):
    """Kaldırma onay dialog'u göster"""
    def close_dialog(_):
        dialog.open = False
        page.update()
    
    def confirm_remove(_):
        close_dialog(_)
        remove_app(app_name, page)
    
    dialog = ft.AlertDialog(
        title=ft.Text("Uygulamayı Kaldır"),
        content=ft.Text(f"{app_name} uygulamasını kaldırmak istediğinizden emin misiniz?"),
        actions=[
            ft.TextButton("İptal", on_click=close_dialog),
            ft.ElevatedButton(
                "Kaldır",
                on_click=confirm_remove,
                bgcolor=ft.Colors.RED_400,
                color=ft.Colors.WHITE
            )
        ]
    )
    
    page.dialog = dialog
    dialog.open = True
    page.update()

def remove_app(app_name, page):
    """Uygulamayı kaldır"""
    def remove_in_thread():
        try:
            result = subprocess.run(
                ["python", "main.py", "uninstall", app_name],
                capture_output=True,
                text=True,
                cwd=os.getcwd()
            )
            
            if result.returncode == 0:
                show_snackbar(page, f"✅ {app_name} başarıyla kaldırıldı")
                refresh_dashboard(page)
            else:
                show_snackbar(page, f"❌ Kaldırma hatası: {result.stderr}", is_error=True)
                
        except Exception as e:
            show_snackbar(page, f"❌ Kaldırma hatası: {str(e)}", is_error=True)
    
    threading.Thread(target=remove_in_thread, daemon=True).start()

def show_install_dialog(page):
    """Yükleme dialog'u göster"""
    def close_dialog(_):
        dialog.open = False
        page.update()
    
    def install_from_file(_):
        # Dosya seçici açılacak (gelecek sürümde)
        show_snackbar(page, "📁 Dosya seçici henüz desteklenmiyor. CLI kullanın: clapp install <dosya>")
        close_dialog(_)
    
    def go_to_store(_):
        close_dialog(_)
        navigate_to_store(page)
    
    dialog = ft.AlertDialog(
        title=ft.Text("Yeni Uygulama Yükle"),
        content=ft.Text("Nasıl yüklemek istiyorsunuz?"),
        actions=[
            ft.TextButton("İptal", on_click=close_dialog),
            ft.ElevatedButton("Dosyadan Yükle", on_click=install_from_file),
            ft.ElevatedButton("App Store'dan Seç", on_click=go_to_store)
        ]
    )
    
    page.dialog = dialog
    dialog.open = True
    page.update()

def navigate_to_store(page):
    """App Store sekmesine git"""
    # Ana GUI'deki navigation'ı güncelle
    if hasattr(page, 'navigation_rail'):
        page.navigation_rail.selected_index = 1
    show_snackbar(page, "🏪 App Store sekmesine geçin")

def refresh_dashboard(page):
    """Dashboard'u yenile"""
    # Sayfayı yeniden yükle
    new_content = build_dashboard(page)
    # Bu fonksiyon main_gui.py'den çağrılacak
    show_snackbar(page, "🔄 Dashboard yenilendi") 