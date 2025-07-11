import flet as ft
from gui_appstore import render_appstore
from gui_settings import render_settings_screen, get_current_theme
from gui_about import render_about_screen
from gui_theme import get_theme_colors

def main(page: ft.Page):
    """
    Ana GUI fonksiyonu. Flet uygulamasının giriş noktası.
    
    Args:
        page (ft.Page): Flet sayfası
    """
    # Mevcut tema ayarını yükle
    current_theme = get_current_theme()
    
    # Sayfa ayarları
    page.title = "clapp App Store"
    page.theme_mode = ft.ThemeMode.DARK if current_theme == "dark" else ft.ThemeMode.LIGHT
    page.window_width = 800
    page.window_height = 600
    page.window_min_width = 600
    page.window_min_height = 400
    page.padding = 0
    page.spacing = 0
    
    # Mevcut sekme durumu
    current_tab = "appstore"
    
    # Ana container
    main_container = ft.Container(
        expand=True,
        padding=0
    )
    
    # Sekme değiştirme fonksiyonu
    def switch_tab(tab_name):
        nonlocal current_tab
        current_theme = get_current_theme()
        
        if tab_name == "appstore":
            render_appstore(page, current_theme)
        elif tab_name == "settings":
            render_settings_screen(page, current_theme)
        elif tab_name == "about":
            render_about_screen(page, current_theme)
        
        current_tab = tab_name
        update_navigation()
    
    # Navigasyon çubuğu
    def update_navigation():
        colors = get_theme_colors(get_current_theme())
        
        # Navigasyon butonları
        nav_buttons = [
            ft.NavigationRailDestination(
                icon=ft.Icons.APPS,
                selected_icon=ft.Icons.APPS,
                label="App Store",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.SETTINGS,
                selected_icon=ft.Icons.SETTINGS,
                label="Ayarlar",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.INFO,
                selected_icon=ft.Icons.INFO,
                label="Hakkında",
            ),
        ]
        
        # Mevcut sekme indeksi
        selected_index = 0
        if current_tab == "appstore":
            selected_index = 0
        elif current_tab == "settings":
            selected_index = 1
        elif current_tab == "about":
            selected_index = 2
        
        # Navigasyon rail'i güncelle
        if hasattr(page, 'navigation_rail'):
            page.navigation_rail.selected_index = selected_index
            page.update()
    
    # Navigasyon değişiklik handler'ı
    def on_nav_change(e):
        tab_names = ["appstore", "settings", "about"]
        if e.control.selected_index < len(tab_names):
            switch_tab(tab_names[e.control.selected_index])
    
    # Navigasyon rail oluştur
    colors = get_theme_colors(current_theme)
    navigation_rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        min_extended_width=200,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.Icons.APPS,
                selected_icon=ft.Icons.APPS,
                label="App Store",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.SETTINGS,
                selected_icon=ft.Icons.SETTINGS,
                label="Ayarlar",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.INFO,
                selected_icon=ft.Icons.INFO,
                label="Hakkında",
            ),
        ],
        on_change=on_nav_change,
        bgcolor=colors["surface"],
        indicator_color=colors["primary"],
    )
    
    # Sayfaya navigasyon rail'i ekle
    page.navigation_rail = navigation_rail
    
    # İçerik container'ı
    content_container = ft.Container(
        expand=True,
        padding=0
    )
    
    # Ana layout
    main_row = ft.Row([
        navigation_rail,
        ft.VerticalDivider(width=1, color=colors["on_surface"]),
        content_container,
    ], expand=True, spacing=0)
    
    # Sayfaya ana layout'u ekle
    page.add(main_row)
    
    # İlk sekmeyi yükle
    switch_tab("appstore")

def main_with_tabs(page: ft.Page):
    """
    Alternatif tab-based ana GUI fonksiyonu.
    
    Args:
        page (ft.Page): Flet sayfası
    """
    # Mevcut tema ayarını yükle
    current_theme = get_current_theme()
    
    # Sayfa ayarları
    page.title = "clapp App Store"
    page.theme_mode = ft.ThemeMode.DARK if current_theme == "dark" else ft.ThemeMode.LIGHT
    page.window_width = 800
    page.window_height = 600
    page.window_min_width = 600
    page.window_min_height = 400
    
    colors = get_theme_colors(current_theme)
    
    # Tab değiştirme fonksiyonu
    def on_tab_change(e):
        current_theme = get_current_theme()
        
        if e.control.selected_index == 0:
            # App Store sekmesi
            tab_content.content = create_appstore_content(current_theme)
        elif e.control.selected_index == 1:
            # Ayarlar sekmesi
            tab_content.content = create_settings_content(current_theme)
        elif e.control.selected_index == 2:
            # Hakkında sekmesi
            tab_content.content = create_about_content(current_theme)
        
        page.update()
    
    def create_appstore_content(theme_mode):
        """App Store içeriği oluştur"""
        from package_registry import list_packages
        from gui_utils import create_app_card, create_empty_state
        
        packages = list_packages()
        
        if not packages:
            return create_empty_state(
                "Henüz yüklü uygulama yok\nUygulamaları 'apps/' dizinine yerleştirin",
                ft.Icons.APPS,
                theme_mode
            )
        
        cards = []
        for package in packages:
            card = create_app_card(
                name=package['name'],
                language=package['language'],
                description=package['description'],
                version=package['version'],
                theme_mode=theme_mode
            )
            cards.append(card)
        
        return ft.Column(
            cards,
            scroll=ft.ScrollMode.AUTO,
            spacing=10
        )
    
    def create_settings_content(theme_mode):
        """Ayarlar içeriği oluştur"""
        from gui_settings import load_settings, save_settings
        
        colors = get_theme_colors(theme_mode)
        current_settings = load_settings()
        
        def on_theme_change(e):
            theme_value = "dark" if e.control.value == "Koyu" else "light"
            current_settings["theme"] = theme_value
            save_settings(current_settings)
            page.theme_mode = ft.ThemeMode.DARK if theme_value == "dark" else ft.ThemeMode.LIGHT
            page.update()
        
        return ft.Column([
            ft.Text("Ayarlar", size=24, weight=ft.FontWeight.BOLD),
            ft.Dropdown(
                label="Tema",
                value="Koyu" if current_settings["theme"] == "dark" else "Açık",
                options=[
                    ft.dropdown.Option("Koyu"),
                    ft.dropdown.Option("Açık"),
                ],
                on_change=on_theme_change,
            ),
            ft.TextField(
                label="Geliştirici Adı",
                value=current_settings["developer_name"],
            ),
        ], spacing=20)
    
    def create_about_content(theme_mode):
        """Hakkında içeriği oluştur"""
        from gui_about import load_version_info
        
        app_info = load_version_info()
        
        return ft.Column([
            ft.Icon(ft.Icons.APPS, size=80, color=colors["primary"]),
            ft.Text(
                f"{app_info['app_name']} v{app_info['version']}",
                size=28,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER
            ),
            ft.Text(
                app_info['description'],
                text_align=ft.TextAlign.CENTER
            ),
            ft.Text(
                f"Geliştiren: {app_info['author']}",
                text_align=ft.TextAlign.CENTER
            ),
        ], 
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20)
    
    # Tabs
    tabs = ft.Tabs(
        selected_index=0,
        on_change=on_tab_change,
        tabs=[
            ft.Tab(
                text="App Store",
                icon=ft.Icons.APPS,
            ),
            ft.Tab(
                text="Ayarlar",
                icon=ft.Icons.SETTINGS,
            ),
            ft.Tab(
                text="Hakkında",
                icon=ft.Icons.INFO,
            ),
        ],
    )
    
    # Tab içeriği
    tab_content = ft.Container(
        content=create_appstore_content(current_theme),
        expand=True,
        padding=20
    )
    
    # Ana layout
    page.add(
        ft.Column([
            tabs,
            tab_content,
        ], expand=True)
    )

# Flet uygulamasını başlat
if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.FLET_APP) 