import flet as ft
import json
import os
from gui_utils import create_section_title, create_info_row
from gui_theme import get_theme_colors, SPACING, FONT_SIZES

# Sürüm bilgisi dosyası
VERSION_FILE = "version.json"

# Varsayılan uygulama bilgileri
DEFAULT_APP_INFO = {
    "app_name": "clapp",
    "version": "1.0.0",
    "author": "Melih Burak Memiş",
    "description": "Basit ve güçlü paket yöneticisi",
    "source": "https://github.com/melihburak/clapp",
    "license": "MIT",
    "build_date": "2024-01-01"
}

def load_version_info():
    """
    Sürüm bilgilerini yükler.
    
    Returns:
        dict: Uygulama bilgileri
    """
    try:
        if os.path.exists(VERSION_FILE):
            with open(VERSION_FILE, 'r', encoding='utf-8') as f:
                info = json.load(f)
            
            # Eksik bilgileri varsayılanlarla tamamla
            for key, value in DEFAULT_APP_INFO.items():
                if key not in info:
                    info[key] = value
            
            return info
        else:
            return DEFAULT_APP_INFO.copy()
    
    except (json.JSONDecodeError, FileNotFoundError):
        return DEFAULT_APP_INFO.copy()

def render_about_screen(page, theme_mode="dark"):
    """
    Hakkında ekranını oluşturur ve sayfaya ekler.
    
    Args:
        page (ft.Page): Flet sayfası
        theme_mode (str): Tema modu
    """
    colors = get_theme_colors(theme_mode)
    
    # Uygulama bilgilerini yükle
    app_info = load_version_info()
    
    # Ana container
    main_container = ft.Container(
        bgcolor=colors["background"],
        padding=ft.padding.all(SPACING["padding"]),
        expand=True
    )
    
    # Logo/İkon
    app_icon = ft.Icon(
        ft.Icons.APPS,
        size=80,
        color=colors["primary"]
    )
    
    # Uygulama adı ve sürüm
    app_title = ft.Text(
        f"{app_info['app_name']} v{app_info['version']}",
        size=FONT_SIZES["header"],
        weight=ft.FontWeight.BOLD,
        color=colors["text"],
        text_align=ft.TextAlign.CENTER
    )
    
    # Açıklama
    app_description = ft.Text(
        app_info['description'],
        size=FONT_SIZES["normal"],
        color=colors["on_surface"],
        text_align=ft.TextAlign.CENTER
    )
    
    # Yazar bilgisi
    author_info = ft.Text(
        f"Geliştiren: {app_info['author']}",
        size=FONT_SIZES["normal"],
        color=colors["text"],
        text_align=ft.TextAlign.CENTER
    )
    
    # Kaynak kod linki
    def on_source_click(e):
        page.launch_url(app_info['source'])
    
    source_link = ft.TextButton(
        text="Kaynak Kodu",
        on_click=on_source_click,
                    icon=ft.Icons.CODE,
        style=ft.ButtonStyle(
            color=colors["primary"],
        )
    )
    
    # GitHub linki (eğer GitHub URL'si ise)
    github_button = None
    if "github.com" in app_info['source']:
        def on_github_click(e):
            page.launch_url(app_info['source'])
        
        github_button = ft.ElevatedButton(
            text="GitHub'da Görüntüle",
            on_click=on_github_click,
            icon=ft.Icons.OPEN_IN_NEW,
            bgcolor=colors["primary"],
            color=colors["text"]
        )
    
    # Lisans bilgisi
    license_info = ft.Text(
        f"Lisans: {app_info['license']}",
        size=FONT_SIZES["small"],
        color=colors["on_surface"],
        text_align=ft.TextAlign.CENTER
    )
    
    # Yapım tarihi
    build_date = ft.Text(
        f"Yapım Tarihi: {app_info['build_date']}",
        size=FONT_SIZES["small"],
        color=colors["on_surface"],
        text_align=ft.TextAlign.CENTER
    )
    
    # Özellikler listesi
    features_title = ft.Text(
        "Özellikler",
        size=FONT_SIZES["large"],
        weight=ft.FontWeight.BOLD,
        color=colors["text"]
    )
    
    features_list = ft.Column([
        ft.Row([
            ft.Icon(ft.Icons.CHECK_CIRCLE, color=colors["primary"], size=20),
            ft.Text("Python ve Lua uygulamalarını çalıştırma", color=colors["text"])
        ]),
        ft.Row([
            ft.Icon(ft.Icons.CHECK_CIRCLE, color=colors["primary"], size=20),
            ft.Text("Görsel uygulama mağazası", color=colors["text"])
        ]),
        ft.Row([
            ft.Icon(ft.Icons.CHECK_CIRCLE, color=colors["primary"], size=20),
            ft.Text("Koyu/Açık tema desteği", color=colors["text"])
        ]),
        ft.Row([
            ft.Icon(ft.Icons.CHECK_CIRCLE, color=colors["primary"], size=20),
            ft.Text("Basit manifest yapısı", color=colors["text"])
        ]),
        ft.Row([
            ft.Icon(ft.Icons.CHECK_CIRCLE, color=colors["primary"], size=20),
            ft.Text("Komut satırı ve GUI arayüzü", color=colors["text"])
        ]),
    ], spacing=SPACING["gutter"])
    
    # Teşekkürler bölümü
    thanks_title = ft.Text(
        "Teşekkürler",
        size=FONT_SIZES["large"],
        weight=ft.FontWeight.BOLD,
        color=colors["text"]
    )
    
    thanks_text = ft.Text(
        "Bu proje Flet framework'ü kullanılarak geliştirilmiştir.\n"
        "Katkıda bulunan herkese teşekkürler!",
        size=FONT_SIZES["normal"],
        color=colors["on_surface"],
        text_align=ft.TextAlign.CENTER
    )
    
    # İletişim bilgileri
    contact_title = ft.Text(
        "İletişim",
        size=FONT_SIZES["large"],
        weight=ft.FontWeight.BOLD,
        color=colors["text"]
    )
    
    # E-posta butonu (eğer varsa)
    contact_buttons = ft.Row([
        ft.TextButton(
            text="Geri Bildirim",
            on_click=lambda e: page.launch_url(f"{app_info['source']}/issues"),
            icon=ft.Icons.BUG_REPORT,
            style=ft.ButtonStyle(color=colors["primary"])
        ),
        ft.TextButton(
            text="Özellik İsteği",
            on_click=lambda e: page.launch_url(f"{app_info['source']}/issues/new"),
            icon=ft.Icons.LIGHTBULB,
            style=ft.ButtonStyle(color=colors["primary"])
        ),
    ], alignment=ft.MainAxisAlignment.CENTER)
    
    # Ana düzen
    content = ft.Column([
        # Logo ve başlık
        ft.Container(
            content=ft.Column([
                app_icon,
                app_title,
                app_description,
                author_info,
            ], 
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=SPACING["gutter"]
            ),
            padding=ft.padding.all(SPACING["padding"])
        ),
        
        ft.Divider(height=20, color=colors["on_surface"]),
        
        # Bağlantılar
        ft.Row([
            source_link,
            github_button if github_button else ft.Container(),
        ], alignment=ft.MainAxisAlignment.CENTER),
        
        ft.Container(height=20),
        
        # Özellikler
        features_title,
        features_list,
        
        ft.Container(height=20),
        
        # Teşekkürler
        thanks_title,
        thanks_text,
        
        ft.Container(height=20),
        
        # İletişim
        contact_title,
        contact_buttons,
        
        ft.Container(height=30),
        
        # Alt bilgi
        ft.Column([
            license_info,
            build_date,
        ], 
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=SPACING["gutter"]
        ),
        
    ], 
    spacing=SPACING["gutter"],
    scroll=ft.ScrollMode.AUTO,
    expand=True,
    horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
    
    main_container.content = content
    
    # Sayfayı temizle ve yeni içeriği ekle
    page.controls.clear()
    page.add(main_container)
    page.update()

def create_version_file():
    """
    Varsayılan sürüm dosyasını oluşturur.
    """
    try:
        with open(VERSION_FILE, 'w', encoding='utf-8') as f:
            json.dump(DEFAULT_APP_INFO, f, ensure_ascii=False, indent=2)
        print(f"Sürüm dosyası oluşturuldu: {VERSION_FILE}")
    except Exception as e:
        print(f"Sürüm dosyası oluşturulurken hata: {e}")

if __name__ == "__main__":
    # Test için sürüm dosyasını oluştur
    create_version_file() 