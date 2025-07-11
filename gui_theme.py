import flet as ft

# Koyu tema renkleri
DARK_MODE_COLORS = {
    "background": "#121212",
    "surface": "#1E1E1E",
    "primary": "#BB86FC",
    "secondary": "#03DAC6",
    "tertiary": "#FFB74D",
    "text": "#FFFFFF",
    "error": "#CF6679",
    "on_surface": "#E1E1E1",
    "on_background": "#FFFFFF",
    "on_primary": "#000000",
    "on_secondary": "#000000",
    "on_tertiary": "#000000",
    "on_outline": "#FFFFFF",
    "outline": "#444444"
}

# Açık tema renkleri
LIGHT_MODE_COLORS = {
    "background": "#FFFFFF",
    "surface": "#F5F5F5",
    "primary": "#6200EE",
    "secondary": "#03DAC6",
    "tertiary": "#FF6F00",
    "text": "#000000",
    "error": "#B00020",
    "on_surface": "#1E1E1E",
    "on_background": "#000000",
    "on_primary": "#FFFFFF",
    "on_secondary": "#000000",
    "on_tertiary": "#FFFFFF",
    "on_outline": "#000000",
    "outline": "#CCCCCC"
}

# Font boyutları
FONT_SIZES = {
    "small": 12,
    "normal": 14,
    "large": 18,
    "title": 22,
    "header": 28
}

# Boşluk değerleri
SPACING = {
    "padding": 12,
    "margin": 10,
    "gutter": 8,
    "card_padding": 16
}

# Diğer stil sabitleri
STYLE_CONSTANTS = {
    "border_radius": 12,
    "card_elevation": 2,
    "button_height": 40,
    "icon_size": 24
}

def get_theme_colors(mode="dark"):
    """
    Tema moduna göre renk setini döndürür.
    
    Args:
        mode (str): "dark" veya "light"
        
    Returns:
        dict: Renk seti
    """
    if mode == "light":
        return LIGHT_MODE_COLORS
    return DARK_MODE_COLORS

def get_language_color(language):
    """
    Programlama diline göre renk döndürür.
    
    Args:
        language (str): Programlama dili
        
    Returns:
        str: Hex renk kodu
    """
    language_colors = {
        "python": "#3776AB",
        "lua": "#000080",
        "javascript": "#F7DF1E",
        "typescript": "#3178C6",
        "unknown": "#808080"
    }
    
    return language_colors.get(language.lower(), language_colors["unknown"])

def get_language_icon(language):
    """
    Programlama diline göre ikon döndürür.
    
    Args:
        language (str): Programlama dili
        
    Returns:
        str: Flet ikon adı
    """
    language_icons = {
            "python": ft.Icons.CODE,
    "lua": ft.Icons.INTEGRATION_INSTRUCTIONS,
    "javascript": ft.Icons.JAVASCRIPT,
    "typescript": ft.Icons.CODE,
    "unknown": ft.Icons.HELP_OUTLINE
    }
    
    return language_icons.get(language.lower(), language_icons["unknown"])

def create_themed_card(content, theme_mode="dark"):
    """
    Tema renklerine uygun kart oluşturur.
    
    Args:
        content: Kart içeriği
        theme_mode (str): Tema modu
        
    Returns:
        ft.Card: Tema renklerine uygun kart
    """
    colors = get_theme_colors(theme_mode)
    
    return ft.Card(
        content=content,
        elevation=STYLE_CONSTANTS["card_elevation"],
        color=colors["surface"],
        margin=ft.margin.all(SPACING["margin"]),
    )

def create_themed_button(text, on_click=None, theme_mode="dark", primary=True):
    """
    Tema renklerine uygun buton oluşturur.
    
    Args:
        text (str): Buton metni
        on_click: Tıklama fonksiyonu
        theme_mode (str): Tema modu
        primary (bool): Birincil buton mu
        
    Returns:
        ft.ElevatedButton: Tema renklerine uygun buton
    """
    colors = get_theme_colors(theme_mode)
    
    return ft.ElevatedButton(
        text=text,
        on_click=on_click,
        height=STYLE_CONSTANTS["button_height"],
        bgcolor=colors["primary"] if primary else colors["surface"],
        color=colors["text"],
    ) 