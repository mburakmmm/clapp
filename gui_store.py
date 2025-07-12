#!/usr/bin/env python3
"""
clapp GUI App Store Modülü
GitHub'dan uzak paketleri getirir ve yükleme için gösterir
"""

import flet as ft
import json
import urllib.request
import threading
import subprocess
import os
from gui_theme import get_theme_colors
from gui_utils import create_app_card, show_snackbar, create_empty_state, create_loading_state

# GitHub repository bilgileri
GITHUB_REPO = "mburakmmm/clapp-packages"
PACKAGES_JSON_URL = f"https://raw.githubusercontent.com/{GITHUB_REPO}/main/packages.json"

def build_store(page: ft.Page):
    """App Store UI'sini oluştur"""
    theme_colors = get_theme_colors()
    
    # Header
    header = ft.Container(
        content=ft.Row([
            ft.Text(
                "App Store",
                size=24,
                weight=ft.FontWeight.BOLD,
                color=theme_colors["on_background"]
            ),
            ft.Container(expand=True),  # Spacer
            ft.IconButton(
                icon=ft.Icons.REFRESH,
                tooltip="Paket listesini yenile",
                on_click=lambda _: refresh_store(page)
            )
        ]),
        padding=ft.padding.only(bottom=20)
    )
    
    # Loading state
    loading_content = create_loading_state("Paketler yükleniyor...")
    
    # Ana layout
    main_layout = ft.Column([
        header,
        loading_content
    ], expand=True)
    
    # Paketleri background'da yükle
    load_packages_async(page, main_layout)
    
    return main_layout

def load_packages_async(page, main_layout):
    """Paketleri asenkron olarak yükle"""
    def load_in_thread():
        try:
            # GitHub'dan paket listesini al
            packages = fetch_packages_from_github()
            
            if packages:
                # Paket kartlarını oluştur
                content = create_packages_content(packages, page)
            else:
                # Boş durum
                content = create_empty_state(
                    icon=ft.Icons.CLOUD_OFF,
                    title="Paketler Yüklenemedi",
                    description="İnternet bağlantınızı kontrol edin ve yeniden deneyin",
                    action_text="Yeniden Dene",
                    action_callback=lambda _: refresh_store(page)
                )
            
            # UI'yi güncelle
            main_layout.controls[1] = content
            page.update()
            
        except Exception as e:
            # Hata durumu
            error_content = create_empty_state(
                icon=ft.Icons.ERROR,
                title="Hata Oluştu",
                description=f"Paketler yüklenirken hata: {str(e)}",
                action_text="Yeniden Dene",
                action_callback=lambda _: refresh_store(page)
            )
            main_layout.controls[1] = error_content
            page.update()
    
    threading.Thread(target=load_in_thread, daemon=True).start()

def fetch_packages_from_github():
    """GitHub'dan paket listesini getir"""
    try:
        with urllib.request.urlopen(PACKAGES_JSON_URL, timeout=10) as response:
            data = json.loads(response.read().decode())
            return data.get("packages", [])
    except Exception as e:
        print(f"GitHub'dan paket listesi alınamadı: {e}")
        # Hata durumunda boş liste döndür
        return []

def create_packages_content(packages, page):
    """Paket kartlarını içeren içerik oluştur"""
    theme_colors = get_theme_colors()
    
    if not packages:
        return create_empty_state(
            icon=ft.Icons.INVENTORY_2,
            title="Hiç Paket Yok",
            description="Henüz yüklenebilir paket bulunmuyor",
            action_text="Yenile",
            action_callback=lambda _: refresh_store(page)
        )
    
    # Paket kartlarını oluştur
    package_cards = []
    for package in packages:
        card = create_store_package_card(package, page)
        package_cards.append(card)
    
    # Scrollable liste
    content = ft.Column(
        controls=[
            ft.Text(
                f"{len(packages)} paket bulundu",
                size=14,
                color=theme_colors["outline"]
            ),
            ft.Divider(height=10),
            *package_cards
        ],
        spacing=10,
        scroll=ft.ScrollMode.AUTO,
        expand=True
    )
    
    return content

def create_store_package_card(package, page):
    """Store için paket kartı oluştur"""
    theme_colors = get_theme_colors()
    
    name = package.get("name", "Unknown")
    version = package.get("version", "1.0.0")
    language = package.get("language", "unknown")
    description = package.get("description", "Açıklama yok")
    author = package.get("author", "Unknown")
    dependencies = package.get("dependencies", [])
    category = package.get("category", "other")
    
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
    
    # Category badge
    category_badge = ft.Container(
        content=ft.Text(
            category.upper(),
            size=10,
            weight=ft.FontWeight.BOLD,
            color=theme_colors["on_secondary"]
        ),
        padding=ft.padding.symmetric(horizontal=8, vertical=4),
        bgcolor=theme_colors["secondary"],
        border_radius=12
    )
    
    # Dependencies info
    deps_text = ""
    if dependencies:
        deps_text = f"Bağımlılıklar: {', '.join(dependencies)}"
    else:
        deps_text = "Bağımlılık yok"
    
    # Install button
    install_button = ft.ElevatedButton(
        "Yükle",
        icon=ft.Icons.DOWNLOAD,
        on_click=lambda _: install_package(package, page),
        bgcolor=theme_colors["primary"],
        color=theme_colors["on_primary"]
    )
    
    # Info button
    info_button = ft.OutlinedButton(
        "Detaylar",
        icon=ft.Icons.INFO,
        on_click=lambda _: show_package_details(package, page)
    )
    
    # Kart içeriği
    card_content = ft.Container(
        content=ft.Column([
            # Header row
            ft.Row([
                ft.Text(name, size=18, weight=ft.FontWeight.BOLD),
                ft.Container(expand=True),
                language_badge,
                category_badge
            ]),
            # Version and author
            ft.Row([
                ft.Text(f"v{version}", size=12, color=theme_colors["outline"]),
                ft.Text(" • ", size=12, color=theme_colors["outline"]),
                ft.Text(f"by {author}", size=12, color=theme_colors["outline"])
            ]),
            # Description
            ft.Text(
                description,
                size=14,
                max_lines=2,
                overflow=ft.TextOverflow.ELLIPSIS
            ),
            # Dependencies
            ft.Text(
                deps_text,
                size=12,
                color=theme_colors["outline"],
                italic=True
            ),
            ft.Divider(height=15),
            # Action buttons
            ft.Row([
                install_button,
                info_button
            ], spacing=10)
        ], spacing=8),
        padding=20
    )
    
    return ft.Card(
        content=card_content,
        margin=ft.margin.only(bottom=10)
    )

def install_package(package, page):
    """Paketi yükle"""
    name = package.get("name", "Unknown")
    download_url = package.get("download_url")
    
    if not download_url:
        show_snackbar(page, f"❌ {name} için indirme linki bulunamadı", is_error=True)
        return
    
    def install_in_thread():
        try:
            # CLI komutu ile yükle
            result = subprocess.run(
                ["python", "main.py", "install", download_url],
                capture_output=True,
                text=True,
                cwd=os.getcwd()
            )
            
            if result.returncode == 0:
                show_snackbar(page, f"✅ {name} başarıyla yüklendi")
            else:
                show_snackbar(page, f"❌ Yükleme hatası: {result.stderr}", is_error=True)
                
        except Exception as e:
            show_snackbar(page, f"❌ Yükleme hatası: {str(e)}", is_error=True)
    
    # Background thread'de yükle
    threading.Thread(target=install_in_thread, daemon=True).start()
    show_snackbar(page, f"📦 {name} yükleniyor...")

def show_package_details(package, page):
    """Paket detaylarını göster"""
    def close_dialog(_):
        dialog.open = False
        page.update()
    
    name = package.get("name", "Unknown")
    version = package.get("version", "1.0.0")
    language = package.get("language", "unknown")
    description = package.get("description", "Açıklama yok")
    author = package.get("author", "Unknown")
    dependencies = package.get("dependencies", [])
    category = package.get("category", "other")
    download_url = package.get("download_url", "")
    
    # Detay metni oluştur
    details_text = f"""
Paket Adı: {name}
Sürüm: {version}
Dil: {language}
Kategori: {category}
Yazar: {author}

Açıklama:
{description}

Bağımlılıklar:
{', '.join(dependencies) if dependencies else 'Yok'}

İndirme Linki:
{download_url}
    """.strip()
    
    dialog = ft.AlertDialog(
        title=ft.Text(f"{name} - Detaylar"),
        content=ft.Container(
            content=ft.Text(
                details_text,
                selectable=True,
                size=12
            ),
            width=500,
            height=300,
            padding=10
        ),
        actions=[
            ft.TextButton("Kapat", on_click=close_dialog),
            ft.ElevatedButton(
                "Yükle",
                on_click=lambda _: [close_dialog(_), install_package(package, page)]
            )
        ]
    )
    
    page.dialog = dialog
    dialog.open = True
    page.update()

def refresh_store(page):
    """Store'u yenile"""
    # Yeni içerik oluştur
    new_content = build_store(page)
    show_snackbar(page, "🔄 App Store yenilendi") 