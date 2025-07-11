#!/usr/bin/env python3
"""
clapp GUI Ana Giriş Dosyası
5 ana bölüm ile navigasyon: Dashboard, App Store, Developer Tools, System Tools, Settings
"""

import flet as ft
import sys
import os

# GUI modüllerini import et
from gui_dashboard import build_dashboard
from gui_store import build_store
from gui_developer import build_developer
from gui_tools import build_tools
from gui_settings import build_settings
from gui_theme import get_theme_colors

class ClappGUI:
    def __init__(self):
        self.current_tab = 0
        self.page = None
        self.theme_colors = get_theme_colors()
        
    def main(self, page: ft.Page):
        """Ana GUI fonksiyonu"""
        self.page = page
        
        # Sayfa ayarları
        page.title = "clapp GUI"
        page.window_width = 1000
        page.window_height = 680
        page.window_min_width = 800
        page.window_min_height = 600
        page.theme_mode = ft.ThemeMode.DARK
        page.padding = 0
        
        # Navigasyon sekmelerini oluştur
        self.create_navigation()
        
        # İlk sekmeyi yükle
        self.load_tab_content(0)
        
        page.update()
    
    def create_navigation(self):
        """Navigasyon yapısını oluştur"""
        # Sekme tanımları
        tabs = [
            {"text": "Dashboard", "icon": ft.Icons.HOME, "route": "/"},
            {"text": "App Store", "icon": ft.Icons.STOREFRONT, "route": "/store"},
            {"text": "Developer", "icon": ft.Icons.CODE, "route": "/developer"},
            {"text": "System Tools", "icon": ft.Icons.BUILD, "route": "/tools"},
            {"text": "Settings", "icon": ft.Icons.SETTINGS, "route": "/settings"},
        ]
        
        # NavigationRail oluştur
        self.nav_rail = ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=100,
            min_extended_width=200,
            destinations=[
                ft.NavigationRailDestination(
                    icon=tab["icon"],
                    selected_icon=tab["icon"],
                    label=tab["text"]
                ) for tab in tabs
            ],
            on_change=self.on_nav_change,
            bgcolor=self.theme_colors["surface"]
        )
        
        # Ana içerik alanı
        self.content_area = ft.Container(
            content=ft.Text("Loading...", size=16),
            expand=True,
            padding=20,
            bgcolor=self.theme_colors["background"]
        )
        
        # Ana layout
        main_layout = ft.Row(
            controls=[
                self.nav_rail,
                ft.VerticalDivider(width=1, color=self.theme_colors["outline"]),
                self.content_area
            ],
            expand=True,
            spacing=0
        )
        
        self.page.add(main_layout)
    
    def on_nav_change(self, e):
        """Navigasyon değişikliği"""
        self.current_tab = e.control.selected_index
        self.load_tab_content(self.current_tab)
        self.page.update()
    
    def load_tab_content(self, tab_index):
        """Sekme içeriğini yükle"""
        try:
            if tab_index == 0:  # Dashboard
                content = build_dashboard(self.page)
            elif tab_index == 1:  # App Store
                content = build_store(self.page)
            elif tab_index == 2:  # Developer Tools
                content = build_developer(self.page)
            elif tab_index == 3:  # System Tools
                content = build_tools(self.page)
            elif tab_index == 4:  # Settings
                content = build_settings(self.page)
            else:
                content = ft.Text("Bilinmeyen sekme", size=16)
            
            self.content_area.content = content
            
        except Exception as e:
            # Hata durumunda basit bir mesaj göster
            error_content = ft.Column([
                ft.Text("Sekme yüklenirken hata oluştu:", size=16, weight=ft.FontWeight.BOLD),
                ft.Text(str(e), size=14, color=ft.Colors.RED),
                ft.ElevatedButton(
                    "Yeniden Dene",
                    on_click=lambda _: self.load_tab_content(tab_index)
                )
            ])
            self.content_area.content = error_content

def main(page: ft.Page):
    """Ana GUI entry point"""
    app = ClappGUI()
    app.main(page)

if __name__ == "__main__":
    # GUI'yi başlat
    ft.app(target=main) 