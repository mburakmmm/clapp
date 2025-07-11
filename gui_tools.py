#!/usr/bin/env python3
"""
clapp GUI System Tools Modülü
Sistem araçları: doctor, clean, check-env gibi bakım ve tanı araçları
"""

import flet as ft
import os
import subprocess
import threading
from gui_theme import get_theme_colors
from gui_utils import show_snackbar, create_empty_state, create_loading_state

def build_tools(page: ft.Page):
    """System Tools UI'sini oluştur"""
    theme_colors = get_theme_colors()
    
    # Header
    header = ft.Container(
        content=ft.Row([
            ft.Text(
                "System Tools",
                size=24,
                weight=ft.FontWeight.BOLD,
                color=theme_colors["on_background"]
            ),
            ft.Container(expand=True),  # Spacer
            ft.Icon(ft.Icons.BUILD, size=28, color=theme_colors["primary"])
        ]),
        padding=ft.padding.only(bottom=20)
    )
    
    # Tool sections
    sections = [
        create_diagnostics_section(page),
        create_maintenance_section(page),
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

def create_diagnostics_section(page):
    """Tanı araçları bölümü"""
    theme_colors = get_theme_colors()
    
    # Doctor Check
    doctor_card = ft.Card(
        content=ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.HEALTH_AND_SAFETY, size=24, color=theme_colors["primary"]),
                    ft.Text("Sistem Tanısı", size=16, weight=ft.FontWeight.BOLD)
                ]),
                ft.Text("Sistem sağlığını ve konfigürasyonu kontrol edin", size=14, color=theme_colors["outline"]),
                ft.ElevatedButton(
                    "Doctor Check",
                    icon=ft.Icons.MEDICAL_SERVICES,
                    on_click=lambda _: run_doctor_check(page),
                    bgcolor=theme_colors["primary"],
                    color=theme_colors["on_primary"]
                )
            ], spacing=10),
            padding=20
        )
    )
    
    # Check Environment
    check_env_card = ft.Card(
        content=ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.ENVIRONMENT, size=24, color=theme_colors["secondary"]),
                    ft.Text("Ortam Kontrolü", size=16, weight=ft.FontWeight.BOLD)
                ]),
                ft.Text("Python, PATH ve bağımlılıkları kontrol edin", size=14, color=theme_colors["outline"]),
                ft.ElevatedButton(
                    "Check Environment",
                    icon=ft.Icons.CHECKLIST,
                    on_click=lambda _: run_check_env(page),
                    bgcolor=theme_colors["secondary"],
                    color=theme_colors["on_secondary"]
                )
            ], spacing=10),
            padding=20
        )
    )
    
    return ft.Container(
        content=ft.Column([
            ft.Text("🔍 Sistem Tanısı", size=18, weight=ft.FontWeight.BOLD),
            ft.Row([doctor_card, check_env_card], spacing=15)
        ], spacing=10),
        padding=ft.padding.only(bottom=20)
    )

def create_maintenance_section(page):
    """Bakım araçları bölümü"""
    theme_colors = get_theme_colors()
    
    # Clean System
    clean_card = ft.Card(
        content=ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.CLEANING_SERVICES, size=24, color=theme_colors["tertiary"]),
                    ft.Text("Sistem Temizliği", size=16, weight=ft.FontWeight.BOLD)
                ]),
                ft.Text("Geçici dosyaları ve önbellekleri temizleyin", size=14, color=theme_colors["outline"]),
                ft.Row([
                    ft.ElevatedButton(
                        "Clean (Dry Run)",
                        icon=ft.Icons.PREVIEW,
                        on_click=lambda _: run_clean_system(page, dry_run=True),
                        bgcolor=theme_colors["outline"],
                        color=theme_colors["on_outline"]
                    ),
                    ft.ElevatedButton(
                        "Clean Now",
                        icon=ft.Icons.DELETE_SWEEP,
                        on_click=lambda _: show_clean_confirm_dialog(page),
                        bgcolor=theme_colors["tertiary"],
                        color=theme_colors["on_tertiary"]
                    )
                ], spacing=10)
            ], spacing=10),
            padding=20
        )
    )
    
    return ft.Container(
        content=ft.Column([
            ft.Text("🧹 Sistem Bakımı", size=18, weight=ft.FontWeight.BOLD),
            ft.Row([clean_card], spacing=15)
        ], spacing=10),
        padding=ft.padding.only(bottom=20)
    )

def create_system_info_section(page):
    """Sistem bilgileri bölümü"""
    theme_colors = get_theme_colors()
    
    # System Status
    status_card = ft.Card(
        content=ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.INFO, size=24, color=theme_colors["primary"]),
                    ft.Text("Sistem Durumu", size=16, weight=ft.FontWeight.BOLD)
                ]),
                ft.Text("Detaylı sistem bilgilerini görüntüleyin", size=14, color=theme_colors["outline"]),
                ft.ElevatedButton(
                    "System Status",
                    icon=ft.Icons.MONITOR,
                    on_click=lambda _: show_system_status(page)
                )
            ], spacing=10),
            padding=20
        )
    )
    
    # Export Logs
    export_card = ft.Card(
        content=ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.DOWNLOAD, size=24, color=theme_colors["secondary"]),
                    ft.Text("Rapor Dışa Aktar", size=16, weight=ft.FontWeight.BOLD)
                ]),
                ft.Text("Sistem raporunu dosyaya kaydedin", size=14, color=theme_colors["outline"]),
                ft.ElevatedButton(
                    "Export Report",
                    icon=ft.Icons.SAVE_ALT,
                    on_click=lambda _: export_system_report(page),
                    bgcolor=theme_colors["secondary"],
                    color=theme_colors["on_secondary"]
                )
            ], spacing=10),
            padding=20
        )
    )
    
    return ft.Container(
        content=ft.Column([
            ft.Text("📊 Sistem Bilgileri", size=18, weight=ft.FontWeight.BOLD),
            ft.Row([status_card, export_card], spacing=15)
        ], spacing=10)
    )

def run_doctor_check(page):
    """Doctor check çalıştır"""
    def run_in_thread():
        try:
            result = subprocess.run(
                ["python", "main.py", "doctor"],
                capture_output=True,
                text=True,
                cwd=os.getcwd()
            )
            
            # Sonucu göster
            show_command_result(page, "Doctor Check", result.stdout + result.stderr, result.returncode == 0)
            
        except Exception as e:
            show_snackbar(page, f"❌ Doctor check hatası: {str(e)}", is_error=True)
    
    threading.Thread(target=run_in_thread, daemon=True).start()
    show_snackbar(page, "🔍 Sistem tanısı çalıştırılıyor...")

def run_check_env(page):
    """Environment check çalıştır"""
    def run_in_thread():
        try:
            result = subprocess.run(
                ["python", "main.py", "check-env"],
                capture_output=True,
                text=True,
                cwd=os.getcwd()
            )
            
            # Sonucu göster
            show_command_result(page, "Environment Check", result.stdout + result.stderr, result.returncode == 0)
            
        except Exception as e:
            show_snackbar(page, f"❌ Environment check hatası: {str(e)}", is_error=True)
    
    threading.Thread(target=run_in_thread, daemon=True).start()
    show_snackbar(page, "🔍 Ortam kontrolü çalıştırılıyor...")

def show_clean_confirm_dialog(page):
    """Temizlik onay dialog'u göster"""
    def close_dialog(_):
        dialog.open = False
        page.update()
    
    def confirm_clean(_):
        close_dialog(_)
        run_clean_system(page, dry_run=False)
    
    dialog = ft.AlertDialog(
        title=ft.Text("Sistem Temizliği"),
        content=ft.Text("Geçici dosyalar ve önbellekler silinecek. Devam etmek istediğinizden emin misiniz?"),
        actions=[
            ft.TextButton("İptal", on_click=close_dialog),
            ft.ElevatedButton(
                "Temizle",
                on_click=confirm_clean,
                bgcolor=ft.Colors.RED_400,
                color=ft.Colors.WHITE
            )
        ]
    )
    
    page.dialog = dialog
    dialog.open = True
    page.update()

def run_clean_system(page, dry_run=False):
    """Sistem temizliği çalıştır"""
    def run_in_thread():
        try:
            cmd = ["python", "main.py", "clean"]
            if dry_run:
                cmd.append("--dry-run")
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=os.getcwd()
            )
            
            # Sonucu göster
            title = "Clean System (Dry Run)" if dry_run else "Clean System"
            show_command_result(page, title, result.stdout + result.stderr, result.returncode == 0)
            
        except Exception as e:
            show_snackbar(page, f"❌ Temizlik hatası: {str(e)}", is_error=True)
    
    threading.Thread(target=run_in_thread, daemon=True).start()
    action = "Temizlik simülasyonu" if dry_run else "Sistem temizliği"
    show_snackbar(page, f"🧹 {action} çalıştırılıyor...")

def show_system_status(page):
    """Sistem durumunu göster"""
    def get_status_in_thread():
        try:
            # Birden fazla komut çalıştır
            commands = [
                ("Version", ["python", "main.py", "version", "--detailed"]),
                ("Health", ["python", "main.py", "health"]),
                ("Environment", ["python", "main.py", "check-env"])
            ]
            
            status_text = "=== SISTEM DURUMU ===\n\n"
            
            for cmd_name, cmd in commands:
                try:
                    result = subprocess.run(
                        cmd,
                        capture_output=True,
                        text=True,
                        cwd=os.getcwd(),
                        timeout=30
                    )
                    
                    status_text += f"--- {cmd_name} ---\n"
                    status_text += result.stdout + result.stderr
                    status_text += "\n\n"
                    
                except subprocess.TimeoutExpired:
                    status_text += f"--- {cmd_name} ---\n"
                    status_text += "Komut zaman aşımına uğradı\n\n"
                except Exception as e:
                    status_text += f"--- {cmd_name} ---\n"
                    status_text += f"Hata: {str(e)}\n\n"
            
            show_command_result(page, "System Status", status_text, True)
            
        except Exception as e:
            show_snackbar(page, f"❌ Sistem durumu hatası: {str(e)}", is_error=True)
    
    threading.Thread(target=get_status_in_thread, daemon=True).start()
    show_snackbar(page, "📊 Sistem durumu alınıyor...")

def export_system_report(page):
    """Sistem raporunu dışa aktar"""
    def export_in_thread():
        try:
            # Sistem raporunu oluştur
            commands = [
                ("Version", ["python", "main.py", "version", "--detailed"]),
                ("Doctor", ["python", "main.py", "doctor"]),
                ("Environment", ["python", "main.py", "check-env"]),
                ("Apps", ["python", "main.py", "list"])
            ]
            
            report_text = f"=== CLAPP SISTEM RAPORU ===\n"
            report_text += f"Tarih: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            
            for cmd_name, cmd in commands:
                try:
                    result = subprocess.run(
                        cmd,
                        capture_output=True,
                        text=True,
                        cwd=os.getcwd(),
                        timeout=30
                    )
                    
                    report_text += f"--- {cmd_name} ---\n"
                    report_text += result.stdout + result.stderr
                    report_text += "\n\n"
                    
                except subprocess.TimeoutExpired:
                    report_text += f"--- {cmd_name} ---\n"
                    report_text += "Komut zaman aşımına uğradı\n\n"
                except Exception as e:
                    report_text += f"--- {cmd_name} ---\n"
                    report_text += f"Hata: {str(e)}\n\n"
            
            # Dosyaya kaydet
            import datetime
            filename = f"clapp_system_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            
            with open(filename, "w", encoding="utf-8") as f:
                f.write(report_text)
            
            show_snackbar(page, f"✅ Rapor kaydedildi: {filename}")
            
        except Exception as e:
            show_snackbar(page, f"❌ Rapor dışa aktarma hatası: {str(e)}", is_error=True)
    
    threading.Thread(target=export_in_thread, daemon=True).start()
    show_snackbar(page, "📄 Sistem raporu oluşturuluyor...")

def show_command_result(page, title, result_text, is_success):
    """Komut sonucunu göster"""
    def close_dialog(_):
        dialog.open = False
        page.update()
    
    def copy_to_clipboard(_):
        page.set_clipboard(result_text)
        show_snackbar(page, "📋 Panoya kopyalandı")
    
    # Sonuç rengini belirle
    title_color = ft.Colors.GREEN if is_success else ft.Colors.RED
    icon = ft.Icons.CHECK_CIRCLE if is_success else ft.Icons.ERROR
    
    dialog = ft.AlertDialog(
        title=ft.Row([
            ft.Icon(icon, color=title_color),
            ft.Text(title, color=title_color)
        ]),
        content=ft.Container(
            content=ft.Column([
                ft.Text(
                    result_text,
                    selectable=True,
                    size=12,
                    expand=True
                )
            ]),
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