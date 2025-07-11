#!/usr/bin/env python3
"""
clapp GUI Developer Tools Modülü
Geliştirici araçları: scaffold, publish, validate, info, where, version
"""

import flet as ft
import os
import subprocess
import threading
import json
from gui_theme import get_theme_colors
from gui_utils import show_snackbar, create_empty_state

def build_developer(page: ft.Page):
    """Developer Tools UI'sini oluştur"""
    theme_colors = get_theme_colors()
    
    # Header
    header = ft.Container(
        content=ft.Row([
            ft.Text(
                "Developer Tools",
                size=24,
                weight=ft.FontWeight.BOLD,
                color=theme_colors["on_background"]
            ),
            ft.Container(expand=True),  # Spacer
            ft.Icon(ft.Icons.CODE, size=28, color=theme_colors["primary"])
        ]),
        padding=ft.padding.only(bottom=20)
    )
    
    # Tool sections
    sections = [
        create_app_development_section(page),
        create_app_management_section(page),
        create_system_info_section(page)
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

def create_app_development_section(page):
    """Uygulama geliştirme bölümü"""
    theme_colors = get_theme_colors()
    
    # Scaffold New App
    scaffold_card = ft.Card(
        content=ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.CREATE_NEW_FOLDER, size=24, color=theme_colors["primary"]),
                    ft.Text("Yeni Uygulama Oluştur", size=16, weight=ft.FontWeight.BOLD)
                ]),
                ft.Text("Boş bir uygulama şablonu oluşturun", size=14, color=theme_colors["outline"]),
                ft.ElevatedButton(
                    "Scaffold",
                    icon=ft.Icons.ADD,
                    on_click=lambda _: show_scaffold_dialog(page),
                    bgcolor=theme_colors["primary"],
                    color=theme_colors["on_primary"]
                )
            ], spacing=10),
            padding=20
        )
    )
    
    # Publish App
    publish_card = ft.Card(
        content=ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.PUBLISH, size=24, color=theme_colors["secondary"]),
                    ft.Text("Uygulama Yayınla", size=16, weight=ft.FontWeight.BOLD)
                ]),
                ft.Text("Uygulamanızı .clapp.zip formatında paketleyin", size=14, color=theme_colors["outline"]),
                ft.ElevatedButton(
                    "Publish",
                    icon=ft.Icons.UPLOAD,
                    on_click=lambda _: show_publish_dialog(page),
                    bgcolor=theme_colors["secondary"],
                    color=theme_colors["on_secondary"]
                )
            ], spacing=10),
            padding=20
        )
    )
    
    return ft.Container(
        content=ft.Column([
            ft.Text("🚀 Uygulama Geliştirme", size=18, weight=ft.FontWeight.BOLD),
            ft.Row([scaffold_card, publish_card], spacing=15)
        ], spacing=10),
        padding=ft.padding.only(bottom=20)
    )

def create_app_management_section(page):
    """Uygulama yönetimi bölümü"""
    theme_colors = get_theme_colors()
    
    # Validate App
    validate_card = ft.Card(
        content=ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.VERIFIED, size=24, color=theme_colors["tertiary"]),
                    ft.Text("Uygulama Doğrula", size=16, weight=ft.FontWeight.BOLD)
                ]),
                ft.Text("Uygulama yapısını ve manifest'ini kontrol edin", size=14, color=theme_colors["outline"]),
                ft.ElevatedButton(
                    "Validate",
                    icon=ft.Icons.CHECK_CIRCLE,
                    on_click=lambda _: show_validate_dialog(page),
                    bgcolor=theme_colors["tertiary"],
                    color=theme_colors["on_tertiary"]
                )
            ], spacing=10),
            padding=20
        )
    )
    
    # App Info
    info_card = ft.Card(
        content=ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.INFO, size=24, color=theme_colors["primary"]),
                    ft.Text("Uygulama Bilgileri", size=16, weight=ft.FontWeight.BOLD)
                ]),
                ft.Text("Yüklü uygulamaların detaylı bilgilerini görün", size=14, color=theme_colors["outline"]),
                ft.ElevatedButton(
                    "App Info",
                    icon=ft.Icons.INFO_OUTLINE,
                    on_click=lambda _: show_app_info_dialog(page)
                )
            ], spacing=10),
            padding=20
        )
    )
    
    # App Location
    location_card = ft.Card(
        content=ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.FOLDER, size=24, color=theme_colors["secondary"]),
                    ft.Text("Uygulama Konumu", size=16, weight=ft.FontWeight.BOLD)
                ]),
                ft.Text("Uygulamaların dosya sistemindeki konumunu bulun", size=14, color=theme_colors["outline"]),
                ft.ElevatedButton(
                    "Where",
                    icon=ft.Icons.FOLDER_OPEN,
                    on_click=lambda _: show_where_dialog(page)
                )
            ], spacing=10),
            padding=20
        )
    )
    
    return ft.Container(
        content=ft.Column([
            ft.Text("🔧 Uygulama Yönetimi", size=18, weight=ft.FontWeight.BOLD),
            ft.Row([validate_card, info_card], spacing=15),
            ft.Row([location_card], spacing=15)
        ], spacing=10),
        padding=ft.padding.only(bottom=20)
    )

def create_system_info_section(page):
    """Sistem bilgileri bölümü"""
    theme_colors = get_theme_colors()
    
    # Version Info
    version_card = ft.Card(
        content=ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.INFO, size=24, color=theme_colors["primary"]),
                    ft.Text("Sistem Bilgileri", size=16, weight=ft.FontWeight.BOLD)
                ]),
                ft.Text("clapp sürümü ve sistem bilgilerini görün", size=14, color=theme_colors["outline"]),
                ft.ElevatedButton(
                    "Version Info",
                    icon=ft.Icons.INFO,
                    on_click=lambda _: show_version_info(page)
                )
            ], spacing=10),
            padding=20
        )
    )
    
    return ft.Container(
        content=ft.Column([
            ft.Text("ℹ️ Sistem Bilgileri", size=18, weight=ft.FontWeight.BOLD),
            ft.Row([version_card], spacing=15)
        ], spacing=10)
    )

def show_scaffold_dialog(page):
    """Scaffold dialog'u göster"""
    app_name_field = ft.TextField(
        label="Uygulama Adı",
        hint_text="my-awesome-app",
        autofocus=True
    )
    
    language_dropdown = ft.Dropdown(
        label="Dil",
        value="python",
        options=[
            ft.dropdown.Option("python", "Python"),
            ft.dropdown.Option("lua", "Lua")
        ]
    )
    
    def close_dialog(_):
        dialog.open = False
        page.update()
    
    def create_app(_):
        app_name = app_name_field.value.strip()
        language = language_dropdown.value
        
        if not app_name:
            show_snackbar(page, "❌ Uygulama adı boş olamaz", is_error=True)
            return
        
        close_dialog(_)
        scaffold_app(app_name, language, page)
    
    dialog = ft.AlertDialog(
        title=ft.Text("Yeni Uygulama Oluştur"),
        content=ft.Container(
            content=ft.Column([
                app_name_field,
                language_dropdown,
                ft.Text("Not: Uygulama apps/ klasörüne oluşturulacak", size=12, italic=True)
            ], spacing=15),
            width=400,
            height=200
        ),
        actions=[
            ft.TextButton("İptal", on_click=close_dialog),
            ft.ElevatedButton("Oluştur", on_click=create_app)
        ]
    )
    
    page.dialog = dialog
    dialog.open = True
    page.update()

def scaffold_app(app_name, language, page):
    """Yeni uygulama scaffold et"""
    def scaffold_in_thread():
        try:
            # Apps klasörünü oluştur
            apps_dir = "apps"
            if not os.path.exists(apps_dir):
                os.makedirs(apps_dir)
            
            app_dir = os.path.join(apps_dir, app_name)
            if os.path.exists(app_dir):
                show_snackbar(page, f"❌ {app_name} zaten mevcut", is_error=True)
                return
            
            # Uygulama klasörünü oluştur
            os.makedirs(app_dir)
            
            # Manifest dosyası oluştur
            manifest = {
                "name": app_name,
                "version": "1.0.0",
                "language": language,
                "entry": f"main.{language}",
                "description": f"A new {language} application"
            }
            
            with open(os.path.join(app_dir, "manifest.json"), "w") as f:
                json.dump(manifest, f, indent=2)
            
            # Entry dosyası oluştur
            if language == "python":
                entry_content = '''#!/usr/bin/env python3
"""
{app_name} - A clapp application
"""

def main():
    print("Hello from {app_name}!")
    print("This is a new Python clapp application.")

if __name__ == "__main__":
    main()
'''.format(app_name=app_name)
            else:  # lua
                entry_content = '''-- {app_name} - A clapp application

function main()
    print("Hello from {app_name}!")
    print("This is a new Lua clapp application.")
end

main()
'''.format(app_name=app_name)
            
            with open(os.path.join(app_dir, f"main.{language}"), "w") as f:
                f.write(entry_content)
            
            show_snackbar(page, f"✅ {app_name} başarıyla oluşturuldu")
            
        except Exception as e:
            show_snackbar(page, f"❌ Scaffold hatası: {str(e)}", is_error=True)
    
    threading.Thread(target=scaffold_in_thread, daemon=True).start()
    show_snackbar(page, f"🚀 {app_name} oluşturuluyor...")

def show_publish_dialog(page):
    """Publish dialog'u göster"""
    folder_field = ft.TextField(
        label="Uygulama Klasörü",
        hint_text="apps/my-app",
        autofocus=True
    )
    
    def close_dialog(_):
        dialog.open = False
        page.update()
    
    def publish_app(_):
        folder_path = folder_field.value.strip()
        
        if not folder_path:
            show_snackbar(page, "❌ Klasör yolu boş olamaz", is_error=True)
            return
        
        close_dialog(_)
        publish_app_folder(folder_path, page)
    
    dialog = ft.AlertDialog(
        title=ft.Text("Uygulama Yayınla"),
        content=ft.Container(
            content=ft.Column([
                folder_field,
                ft.Text("Not: .clapp.zip dosyası oluşturulacak", size=12, italic=True)
            ], spacing=15),
            width=400,
            height=150
        ),
        actions=[
            ft.TextButton("İptal", on_click=close_dialog),
            ft.ElevatedButton("Yayınla", on_click=publish_app)
        ]
    )
    
    page.dialog = dialog
    dialog.open = True
    page.update()

def publish_app_folder(folder_path, page):
    """Uygulama klasörünü yayınla"""
    def publish_in_thread():
        try:
            result = subprocess.run(
                ["python", "main.py", "publish", folder_path],
                capture_output=True,
                text=True,
                cwd=os.getcwd()
            )
            
            if result.returncode == 0:
                show_snackbar(page, f"✅ {folder_path} başarıyla yayınlandı")
            else:
                show_snackbar(page, f"❌ Yayınlama hatası: {result.stderr}", is_error=True)
                
        except Exception as e:
            show_snackbar(page, f"❌ Yayınlama hatası: {str(e)}", is_error=True)
    
    threading.Thread(target=publish_in_thread, daemon=True).start()
    show_snackbar(page, f"📦 {folder_path} yayınlanıyor...")

def show_validate_dialog(page):
    """Validate dialog'u göster"""
    from package_registry import list_app_names
    
    apps = list_app_names()
    if not apps:
        show_snackbar(page, "❌ Doğrulanacak uygulama bulunamadı", is_error=True)
        return
    
    app_dropdown = ft.Dropdown(
        label="Uygulama Seç",
        options=[ft.dropdown.Option(app, app) for app in apps]
    )
    
    def close_dialog(_):
        dialog.open = False
        page.update()
    
    def validate_app(_):
        app_name = app_dropdown.value
        
        if not app_name:
            show_snackbar(page, "❌ Uygulama seçin", is_error=True)
            return
        
        close_dialog(_)
        validate_app_folder(f"apps/{app_name}", page)
    
    dialog = ft.AlertDialog(
        title=ft.Text("Uygulama Doğrula"),
        content=ft.Container(
            content=ft.Column([
                app_dropdown,
                ft.Text("Not: Manifest ve dosya yapısı kontrol edilecek", size=12, italic=True)
            ], spacing=15),
            width=400,
            height=150
        ),
        actions=[
            ft.TextButton("İptal", on_click=close_dialog),
            ft.ElevatedButton("Doğrula", on_click=validate_app)
        ]
    )
    
    page.dialog = dialog
    dialog.open = True
    page.update()

def validate_app_folder(folder_path, page):
    """Uygulama klasörünü doğrula"""
    def validate_in_thread():
        try:
            result = subprocess.run(
                ["python", "main.py", "validate", folder_path],
                capture_output=True,
                text=True,
                cwd=os.getcwd()
            )
            
            if result.returncode == 0:
                show_validation_result(page, folder_path, result.stdout, True)
            else:
                show_validation_result(page, folder_path, result.stderr, False)
                
        except Exception as e:
            show_snackbar(page, f"❌ Doğrulama hatası: {str(e)}", is_error=True)
    
    threading.Thread(target=validate_in_thread, daemon=True).start()
    show_snackbar(page, f"🔍 {folder_path} doğrulanıyor...")

def show_validation_result(page, folder_path, result_text, is_success):
    """Doğrulama sonucunu göster"""
    def close_dialog(_):
        dialog.open = False
        page.update()
    
    title = f"✅ {folder_path} - Doğrulama Başarılı" if is_success else f"❌ {folder_path} - Doğrulama Hatası"
    
    dialog = ft.AlertDialog(
        title=ft.Text(title),
        content=ft.Container(
            content=ft.Text(
                result_text,
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

def show_app_info_dialog(page):
    """App info dialog'u göster"""
    from package_registry import list_app_names
    
    apps = list_app_names()
    if not apps:
        show_snackbar(page, "❌ Bilgi alınacak uygulama bulunamadı", is_error=True)
        return
    
    app_dropdown = ft.Dropdown(
        label="Uygulama Seç",
        options=[ft.dropdown.Option(app, app) for app in apps]
    )
    
    def close_dialog(_):
        dialog.open = False
        page.update()
    
    def show_info(_):
        app_name = app_dropdown.value
        
        if not app_name:
            show_snackbar(page, "❌ Uygulama seçin", is_error=True)
            return
        
        close_dialog(_)
        get_app_info(app_name, page)
    
    dialog = ft.AlertDialog(
        title=ft.Text("Uygulama Bilgileri"),
        content=ft.Container(
            content=app_dropdown,
            width=400,
            height=100
        ),
        actions=[
            ft.TextButton("İptal", on_click=close_dialog),
            ft.ElevatedButton("Bilgi Al", on_click=show_info)
        ]
    )
    
    page.dialog = dialog
    dialog.open = True
    page.update()

def get_app_info(app_name, page):
    """Uygulama bilgilerini al"""
    def get_info_in_thread():
        try:
            result = subprocess.run(
                ["python", "main.py", "info", app_name],
                capture_output=True,
                text=True,
                cwd=os.getcwd()
            )
            
            if result.returncode == 0:
                show_info_result(page, app_name, result.stdout)
            else:
                show_snackbar(page, f"❌ Bilgi alınamadı: {result.stderr}", is_error=True)
                
        except Exception as e:
            show_snackbar(page, f"❌ Bilgi alma hatası: {str(e)}", is_error=True)
    
    threading.Thread(target=get_info_in_thread, daemon=True).start()

def show_info_result(page, app_name, info_text):
    """Bilgi sonucunu göster"""
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

def show_where_dialog(page):
    """Where dialog'u göster"""
    from package_registry import list_app_names
    
    apps = list_app_names()
    if not apps:
        show_snackbar(page, "❌ Konumu bulunacak uygulama yok", is_error=True)
        return
    
    app_dropdown = ft.Dropdown(
        label="Uygulama Seç",
        options=[ft.dropdown.Option(app, app) for app in apps]
    )
    
    def close_dialog(_):
        dialog.open = False
        page.update()
    
    def show_location(_):
        app_name = app_dropdown.value
        
        if not app_name:
            show_snackbar(page, "❌ Uygulama seçin", is_error=True)
            return
        
        close_dialog(_)
        get_app_location(app_name, page)
    
    dialog = ft.AlertDialog(
        title=ft.Text("Uygulama Konumu"),
        content=ft.Container(
            content=app_dropdown,
            width=400,
            height=100
        ),
        actions=[
            ft.TextButton("İptal", on_click=close_dialog),
            ft.ElevatedButton("Konum Bul", on_click=show_location)
        ]
    )
    
    page.dialog = dialog
    dialog.open = True
    page.update()

def get_app_location(app_name, page):
    """Uygulama konumunu al"""
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
                show_snackbar(page, f"📁 {app_name} konumu: {location}")
            else:
                show_snackbar(page, f"❌ Konum bulunamadı: {result.stderr}", is_error=True)
                
        except Exception as e:
            show_snackbar(page, f"❌ Konum alma hatası: {str(e)}", is_error=True)
    
    threading.Thread(target=get_location_in_thread, daemon=True).start()

def show_version_info(page):
    """Sistem bilgilerini göster"""
    def get_version_in_thread():
        try:
            result = subprocess.run(
                ["python", "main.py", "version", "--detailed"],
                capture_output=True,
                text=True,
                cwd=os.getcwd()
            )
            
            if result.returncode == 0:
                show_version_result(page, result.stdout)
            else:
                show_snackbar(page, f"❌ Sürüm bilgisi alınamadı: {result.stderr}", is_error=True)
                
        except Exception as e:
            show_snackbar(page, f"❌ Sürüm bilgisi hatası: {str(e)}", is_error=True)
    
    threading.Thread(target=get_version_in_thread, daemon=True).start()

def show_version_result(page, version_text):
    """Sürüm bilgisi sonucunu göster"""
    def close_dialog(_):
        dialog.open = False
        page.update()
    
    dialog = ft.AlertDialog(
        title=ft.Text("Sistem Bilgileri"),
        content=ft.Container(
            content=ft.Text(
                version_text,
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