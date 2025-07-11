import flet as ft
from gui_theme import (
    get_theme_colors, get_language_color, get_language_icon,
    FONT_SIZES, SPACING, STYLE_CONSTANTS
)

def create_app_card(name, language, description="", version="1.0.0", theme_mode="dark"):
    """
    Uygulama bilgilerini gösteren bir kart oluşturur.
    
    Args:
        name (str): Uygulama adı
        language (str): Programlama dili
        description (str): Uygulama açıklaması
        version (str): Uygulama sürümü
        theme_mode (str): Tema modu
        
    Returns:
        ft.Card: Uygulama kartı
    """
    colors = get_theme_colors(theme_mode)
    lang_color = get_language_color(language)
    lang_icon = get_language_icon(language)
    
    # Kart içeriği
    card_content = ft.Container(
        content=ft.Column([
            # Başlık satırı
            ft.Row([
                ft.Icon(
                    lang_icon,
                    color=lang_color,
                    size=STYLE_CONSTANTS["icon_size"]
                ),
                ft.Text(
                    name,
                    size=FONT_SIZES["large"],
                    weight=ft.FontWeight.BOLD,
                    color=colors["text"]
                ),
                ft.Container(expand=True),  # Spacer
                ft.Text(
                    f"v{version}",
                    size=FONT_SIZES["small"],
                    color=colors["on_surface"]
                )
            ], alignment=ft.MainAxisAlignment.START),
            
            # Dil bilgisi
            ft.Container(
                content=ft.Text(
                    language.capitalize(),
                    size=FONT_SIZES["small"],
                    color=lang_color,
                    weight=ft.FontWeight.W_500
                ),
                margin=ft.margin.only(left=SPACING["gutter"])
            ),
            
            # Açıklama
            ft.Text(
                description if description else "Açıklama yok",
                size=FONT_SIZES["normal"],
                color=colors["on_surface"],
                max_lines=2,
                overflow=ft.TextOverflow.ELLIPSIS
            ) if description else ft.Container(),
            
        ], spacing=SPACING["gutter"]),
        padding=ft.padding.all(SPACING["card_padding"]),
        border_radius=ft.border_radius.all(STYLE_CONSTANTS["border_radius"])
    )
    
    return ft.Card(
        content=card_content,
        elevation=STYLE_CONSTANTS["card_elevation"],
        color=colors["surface"],
        margin=ft.margin.all(SPACING["margin"]),
    )

def create_section_title(title, theme_mode="dark"):
    """
    Bölüm başlığı oluşturur.
    
    Args:
        title (str): Başlık metni
        theme_mode (str): Tema modu
        
    Returns:
        ft.Text: Başlık komponenti
    """
    colors = get_theme_colors(theme_mode)
    
    return ft.Text(
        title,
        size=FONT_SIZES["title"],
        weight=ft.FontWeight.BOLD,
        color=colors["text"]
    )

def create_info_row(label, value, theme_mode="dark"):
    """
    Bilgi satırı oluşturur (etiket: değer formatında).
    
    Args:
        label (str): Etiket
        value (str): Değer
        theme_mode (str): Tema modu
        
    Returns:
        ft.Row: Bilgi satırı
    """
    colors = get_theme_colors(theme_mode)
    
    return ft.Row([
        ft.Text(
            f"{label}:",
            size=FONT_SIZES["normal"],
            weight=ft.FontWeight.W_500,
            color=colors["text"]
        ),
        ft.Text(
            value,
            size=FONT_SIZES["normal"],
            color=colors["on_surface"]
        )
    ])

def create_search_bar(on_change=None, hint_text="Ara...", theme_mode="dark"):
    """
    Arama çubuğu oluşturur.
    
    Args:
        on_change: Değişiklik fonksiyonu
        hint_text (str): İpucu metni
        theme_mode (str): Tema modu
        
    Returns:
        ft.TextField: Arama çubuğu
    """
    colors = get_theme_colors(theme_mode)
    
    return ft.TextField(
        hint_text=hint_text,
        prefix_icon=ft.Icons.SEARCH,
        on_change=on_change,
        border_radius=ft.border_radius.all(STYLE_CONSTANTS["border_radius"]),
        bgcolor=colors["surface"],
        color=colors["text"],
        cursor_color=colors["primary"],
        hint_style=ft.TextStyle(color=colors["on_surface"]),
        border_color=colors["on_surface"],
        focused_border_color=colors["primary"],
    )

def create_empty_state(message, icon=ft.Icons.INBOX, theme_mode="dark"):
    """
    Boş durum göstergesi oluşturur.
    
    Args:
        message (str): Gösterilecek mesaj
        icon: Gösterilecek ikon
        theme_mode (str): Tema modu
        
    Returns:
        ft.Column: Boş durum komponenti
    """
    colors = get_theme_colors(theme_mode)
    
    return ft.Column([
        ft.Icon(
            icon,
            size=64,
            color=colors["on_surface"]
        ),
        ft.Text(
            message,
            size=FONT_SIZES["large"],
            color=colors["on_surface"],
            text_align=ft.TextAlign.CENTER
        )
    ], 
    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    spacing=SPACING["padding"]
    )

def create_loading_indicator(theme_mode="dark"):
    """
    Yükleme göstergesi oluşturur.
    
    Args:
        theme_mode (str): Tema modu
        
    Returns:
        ft.ProgressRing: Yükleme göstergesi
    """
    colors = get_theme_colors(theme_mode)
    
    return ft.ProgressRing(
        color=colors["primary"],
        bgcolor=colors["surface"],
        stroke_width=4
    )

def create_empty_state(icon, title, description, action_text=None, action_callback=None, theme_mode="dark"):
    """
    Boş durum göstergesi oluşturur (yeni API).
    
    Args:
        icon: Gösterilecek ikon
        title (str): Başlık
        description (str): Açıklama
        action_text (str): Aksiyon butonu metni
        action_callback: Aksiyon butonu callback'i
        theme_mode (str): Tema modu
        
    Returns:
        ft.Column: Boş durum komponenti
    """
    colors = get_theme_colors(theme_mode)
    
    components = [
        ft.Icon(
            icon,
            size=64,
            color=colors["on_surface"]
        ),
        ft.Text(
            title,
            size=FONT_SIZES["large"],
            weight=ft.FontWeight.BOLD,
            color=colors["text"],
            text_align=ft.TextAlign.CENTER
        ),
        ft.Text(
            description,
            size=FONT_SIZES["normal"],
            color=colors["on_surface"],
            text_align=ft.TextAlign.CENTER
        )
    ]
    
    if action_text and action_callback:
        components.append(
            ft.ElevatedButton(
                action_text,
                on_click=action_callback,
                bgcolor=colors["primary"],
                color=colors["on_primary"]
            )
        )
    
    return ft.Column(
        components,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=SPACING["padding"]
    )

def create_loading_state(message="Yükleniyor...", theme_mode="dark"):
    """
    Yükleme durumu göstergesi oluşturur.
    
    Args:
        message (str): Yükleme mesajı
        theme_mode (str): Tema modu
        
    Returns:
        ft.Column: Yükleme durumu komponenti
    """
    colors = get_theme_colors(theme_mode)
    
    return ft.Column([
        ft.ProgressRing(
            color=colors["primary"],
            bgcolor=colors["surface"],
            stroke_width=4
        ),
        ft.Text(
            message,
            size=FONT_SIZES["normal"],
            color=colors["on_surface"],
            text_align=ft.TextAlign.CENTER
        )
    ], 
    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    spacing=SPACING["padding"]
    )

def show_snackbar(page, message, is_error=False, duration=3000):
    """
    Snackbar gösterir.
    
    Args:
        page: Flet page
        message (str): Mesaj
        is_error (bool): Hata mesajı mı
        duration (int): Gösterim süresi (ms)
    """
    colors = get_theme_colors()
    
    page.snack_bar = ft.SnackBar(
        content=ft.Text(
            message,
            color=ft.Colors.WHITE if is_error else colors["on_primary"]
        ),
        bgcolor=ft.Colors.RED_400 if is_error else colors["primary"],
        duration=duration
    )
    page.snack_bar.open = True
    page.update() 