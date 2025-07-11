import flet as ft
from package_registry import list_packages
from gui_utils import create_app_card, create_section_title, create_empty_state, create_search_bar
from gui_theme import get_theme_colors, SPACING

def render_appstore(page, theme_mode="dark"):
    """
    App Store görünümünü oluşturur ve sayfaya ekler.
    
    Args:
        page (ft.Page): Flet sayfası
        theme_mode (str): Tema modu
    """
    colors = get_theme_colors(theme_mode)
    
    # Yüklü paketleri al
    packages = list_packages()
    
    # Arama fonksiyonu için state
    search_query = ""
    filtered_packages = packages.copy()
    
    # Ana container
    main_container = ft.Container(
        bgcolor=colors["background"],
        padding=ft.padding.all(SPACING["padding"]),
        expand=True
    )
    
    # Arama çubuğu
    def on_search_change(e):
        nonlocal search_query, filtered_packages
        search_query = e.control.value.lower()
        
        # Paketleri filtrele
        if search_query:
            filtered_packages = [
                pkg for pkg in packages 
                if (search_query in pkg['name'].lower() or 
                    search_query in pkg['description'].lower() or
                    search_query in pkg['language'].lower())
            ]
        else:
            filtered_packages = packages.copy()
        
        # Görünümü güncelle
        update_package_list()
    
    search_bar = create_search_bar(
        on_change=on_search_change,
        hint_text="Uygulama ara...",
        theme_mode=theme_mode
    )
    
    # Paket listesi container'ı
    package_list_container = ft.Column(
        spacing=SPACING["gutter"],
        scroll=ft.ScrollMode.AUTO,
        expand=True
    )
    
    def update_package_list():
        """Paket listesini günceller."""
        package_list_container.controls.clear()
        
        if not filtered_packages:
            if search_query:
                # Arama sonucu bulunamadı
                empty_state = create_empty_state(
                    f"'{search_query}' için sonuç bulunamadı",
                    ft.Icons.SEARCH_OFF,
                    theme_mode
                )
            else:
                # Hiç paket yok
                empty_state = create_empty_state(
                    "Henüz yüklü uygulama yok\nUygulamaları 'apps/' dizinine yerleştirin",
                    ft.Icons.APPS,
                    theme_mode
                )
            package_list_container.controls.append(empty_state)
        else:
            # Paketleri listele
            for package in filtered_packages:
                card = create_app_card(
                    name=package['name'],
                    language=package['language'],
                    description=package['description'],
                    version=package['version'],
                    theme_mode=theme_mode
                )
                package_list_container.controls.append(card)
        
        page.update()
    
    # İlk yükleme
    update_package_list()
    
    # Ana düzen
    content = ft.Column([
        # Başlık
        create_section_title("clapp App Store", theme_mode),
        
        # İstatistik
        ft.Text(
            f"{len(packages)} yüklü uygulama",
            size=14,
            color=colors["on_surface"]
        ),
        
        ft.Divider(height=20, color=colors["on_surface"]),
        
        # Arama çubuğu
        search_bar,
        
        ft.Container(height=10),  # Spacer
        
        # Paket listesi
        ft.Container(
            content=package_list_container,
            expand=True
        )
    ], 
    spacing=SPACING["gutter"],
    expand=True
    )
    
    main_container.content = content
    
    # Sayfayı temizle ve yeni içeriği ekle
    page.controls.clear()
    page.add(main_container)
    page.update()

def render_filtered_appstore(page, theme_mode="dark"):
    """
    Filtrelenebilir App Store görünümünü oluşturur.
    
    Args:
        page (ft.Page): Flet sayfası
        theme_mode (str): Tema modu
    """
    colors = get_theme_colors(theme_mode)
    packages = list_packages()
    
    # Filtre durumu
    current_filter = "all"  # "all", "python", "lua"
    search_query = ""
    
    def get_filtered_packages():
        """Mevcut filtrelere göre paketleri döndürür."""
        result = packages.copy()
        
        # Dil filtresi
        if current_filter != "all":
            result = [pkg for pkg in result if pkg['language'].lower() == current_filter]
        
        # Arama filtresi
        if search_query:
            result = [
                pkg for pkg in result 
                if (search_query in pkg['name'].lower() or 
                    search_query in pkg['description'].lower())
            ]
        
        return result
    
    # Ana container
    main_container = ft.Container(
        bgcolor=colors["background"],
        padding=ft.padding.all(SPACING["padding"]),
        expand=True
    )
    
    # Filtre butonları
    def on_filter_change(filter_type):
        def handler(e):
            nonlocal current_filter
            current_filter = filter_type
            update_display()
        return handler
    
    filter_buttons = ft.Row([
        ft.ElevatedButton(
            "Tümü",
            on_click=on_filter_change("all"),
            bgcolor=colors["primary"] if current_filter == "all" else colors["surface"]
        ),
        ft.ElevatedButton(
            "Python",
            on_click=on_filter_change("python"),
            bgcolor=colors["primary"] if current_filter == "python" else colors["surface"]
        ),
        ft.ElevatedButton(
            "Lua",
            on_click=on_filter_change("lua"),
            bgcolor=colors["primary"] if current_filter == "lua" else colors["surface"]
        ),
    ], spacing=SPACING["gutter"])
    
    # Arama çubuğu
    def on_search_change(e):
        nonlocal search_query
        search_query = e.control.value.lower()
        update_display()
    
    search_bar = create_search_bar(
        on_change=on_search_change,
        hint_text="Uygulama ara...",
        theme_mode=theme_mode
    )
    
    # Paket listesi
    package_list = ft.Column(
        spacing=SPACING["gutter"],
        scroll=ft.ScrollMode.AUTO,
        expand=True
    )
    
    def update_display():
        """Görünümü günceller."""
        # Filtre butonlarını güncelle
        for i, btn in enumerate(filter_buttons.controls):
            filter_types = ["all", "python", "lua"]
            btn.bgcolor = colors["primary"] if current_filter == filter_types[i] else colors["surface"]
        
        # Paket listesini güncelle
        filtered_packages = get_filtered_packages()
        package_list.controls.clear()
        
        if not filtered_packages:
            empty_state = create_empty_state(
                "Filtre kriterlerine uygun uygulama bulunamadı",
                ft.Icons.FILTER_LIST_OFF,
                theme_mode
            )
            package_list.controls.append(empty_state)
        else:
            for package in filtered_packages:
                card = create_app_card(
                    name=package['name'],
                    language=package['language'],
                    description=package['description'],
                    version=package['version'],
                    theme_mode=theme_mode
                )
                package_list.controls.append(card)
        
        page.update()
    
    # İlk yükleme
    update_display()
    
    # Ana düzen
    content = ft.Column([
        create_section_title("clapp App Store", theme_mode),
        ft.Text(f"{len(packages)} yüklü uygulama", size=14, color=colors["on_surface"]),
        ft.Divider(height=20, color=colors["on_surface"]),
        
        # Filtreler
        ft.Text("Filtreler:", size=16, color=colors["text"]),
        filter_buttons,
        
        # Arama
        search_bar,
        
        ft.Container(height=10),
        
        # Paket listesi
        ft.Container(content=package_list, expand=True)
    ], 
    spacing=SPACING["gutter"],
    expand=True
    )
    
    main_container.content = content
    page.controls.clear()
    page.add(main_container)
    page.update() 