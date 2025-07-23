-- LWM Tema Dosyası
-- Modern ve profesyonel görünüm

local theme = {}

-- Font ayarları
theme.font          = "JetBrains Mono 10"

-- Renk paleti (Modern Dark Theme)
theme.bg_normal     = "#1a1a1a"
theme.bg_focus      = "#2d2d2d"
theme.bg_urgent     = "#ff0000"
theme.bg_minimize   = "#1a1a1a"
theme.bg_systray    = theme.bg_normal

theme.fg_normal     = "#ffffff"
theme.fg_focus      = "#00ff88"
theme.fg_urgent     = "#ffffff"
theme.fg_minimize   = "#888888"

-- Kenarlık renkleri
theme.border_normal = "#333333"
theme.border_focus  = "#00ff88"
theme.border_marked = "#91231c"
theme.border_width  = 2

-- Widget renkleri
theme.widget_bg     = "#2d2d2d"
theme.widget_fg     = "#ffffff"
theme.widget_border = "#444444"

-- Menü renkleri
theme.menu_height   = 25
theme.menu_width    = 180
theme.menu_bg_normal = "#2d2d2d"
theme.menu_bg_focus  = "#00ff88"
theme.menu_fg_normal = "#ffffff"
theme.menu_fg_focus  = "#000000"
theme.menu_border_color = "#444444"
theme.menu_border_width = 1

-- Tag list renkleri
theme.taglist_bg_focus = "#00ff88"
theme.taglist_fg_focus = "#000000"
theme.taglist_bg_occupied = "#444444"
theme.taglist_fg_occupied = "#ffffff"
theme.taglist_bg_empty = "#2d2d2d"
theme.taglist_fg_empty = "#888888"
theme.taglist_bg_urgent = "#ff0000"
theme.taglist_fg_urgent = "#ffffff"

-- Task list renkleri
theme.tasklist_bg_normal = "#2d2d2d"
theme.tasklist_fg_normal = "#ffffff"
theme.tasklist_bg_focus = "#00ff88"
theme.tasklist_fg_focus = "#000000"
theme.tasklist_bg_urgent = "#ff0000"
theme.tasklist_fg_urgent = "#ffffff"

-- Titlebar renkleri
theme.titlebar_bg_normal = "#2d2d2d"
theme.titlebar_fg_normal = "#ffffff"
theme.titlebar_bg_focus = "#00ff88"
theme.titlebar_fg_focus = "#000000"

-- Tooltip renkleri
theme.tooltip_bg_color = "#2d2d2d"
theme.tooltip_fg_color = "#ffffff"
theme.tooltip_border_color = "#444444"
theme.tooltip_border_width = 1

-- Prompt renkleri
theme.prompt_bg = "#2d2d2d"
theme.prompt_fg = "#ffffff"
theme.prompt_border_color = "#444444"
theme.prompt_border_width = 1

-- Hotkeys popup renkleri
theme.hotkeys_bg = "#1a1a1a"
theme.hotkeys_fg = "#ffffff"
theme.hotkeys_border_color = "#00ff88"
theme.hotkeys_border_width = 2
theme.hotkeys_modifiers_fg = "#00ff88"
theme.hotkeys_label_bg = "#2d2d2d"
theme.hotkeys_label_fg = "#ffffff"
theme.hotkeys_group_margin = 20

-- Notification renkleri
theme.notification_bg = "#2d2d2d"
theme.notification_fg = "#ffffff"
theme.notification_border_color = "#444444"
theme.notification_border_width = 1
theme.notification_shape = function(cr, width, height)
    gears.shape.rounded_rect(cr, width, height, 8)
end

-- Wallpaper
theme.wallpaper = nil

-- Icon yolu
theme.awesome_icon = "/usr/share/awesome/themes/default/awesome-icon.png"

-- Layout icon'ları
theme.layout_tile = "/usr/share/awesome/themes/default/layouts/tile.png"
theme.layout_tileleft = "/usr/share/awesome/themes/default/layouts/tileleft.png"
theme.layout_tilebottom = "/usr/share/awesome/themes/default/layouts/tilebottom.png"
theme.layout_tiletop = "/usr/share/awesome/themes/default/layouts/tiletop.png"
theme.layout_fair = "/usr/share/awesome/themes/default/layouts/fair.png"
theme.layout_fairh = "/usr/share/awesome/themes/default/layouts/fairh.png"
theme.layout_spiral = "/usr/share/awesome/themes/default/layouts/spiral.png"
theme.layout_dwindle = "/usr/share/awesome/themes/default/layouts/dwindle.png"
theme.layout_max = "/usr/share/awesome/themes/default/layouts/max.png"
theme.layout_fullscreen = "/usr/share/awesome/themes/default/layouts/fullscreen.png"
theme.layout_magnifier = "/usr/share/awesome/themes/default/layouts/magnifier.png"
theme.layout_floating = "/usr/share/awesome/themes/default/layouts/floating.png"
theme.layout_cornernw = "/usr/share/awesome/themes/default/layouts/cornernw.png"
theme.layout_cornerne = "/usr/share/awesome/themes/default/layouts/cornerne.png"
theme.layout_cornersw = "/usr/share/awesome/themes/default/layouts/cornersw.png"
theme.layout_cornerse = "/usr/share/awesome/themes/default/layouts/cornerse.png"

-- Widget spacing
theme.useless_gap = 8
theme.gap_single_client = true

-- Wibar ayarları
theme.wibar_height = 32
theme.wibar_bg = "#1a1a1a"
theme.wibar_fg = "#ffffff"
theme.wibar_border_color = "#333333"
theme.wibar_border_width = 1

-- Systray ayarları
theme.systray_icon_spacing = 4
theme.systray_max_rows = 1

-- Clock format
theme.clock_format = "%H:%M"

-- Mouse cursor
theme.mouse_focus_cursor = "left_ptr"
theme.mouse_move_cursor = "fleur"

-- Window snap
theme.snap_bg = "#00ff88"
theme.snap_border_width = 2

-- Master fill factor
theme.master_fill_policy = "expand"

-- Client opacity
theme.opacity_normal = 1.0
theme.opacity_focus = 1.0
theme.opacity_urgent = 1.0

-- Compositor ayarları
theme.enable_compositor = true
theme.compositor_backend = "xrender"

-- Animasyon ayarları
theme.enable_animations = true
theme.animation_duration = 0.3
theme.animation_easing = "easeInOutCubic"

-- Özel widget renkleri
theme.widget_cpu_bg = "#00ff88"
theme.widget_cpu_fg = "#000000"
theme.widget_mem_bg = "#ff8800"
theme.widget_mem_fg = "#000000"
theme.widget_temp_bg = "#ff0088"
theme.widget_temp_fg = "#ffffff"
theme.widget_net_bg = "#0088ff"
theme.widget_net_fg = "#ffffff"
theme.widget_vol_bg = "#8800ff"
theme.widget_vol_fg = "#ffffff"

-- Battery widget renkleri
theme.widget_battery_bg = "#00ff88"
theme.widget_battery_fg = "#000000"
theme.widget_battery_bg_critical = "#ff0000"
theme.widget_battery_fg_critical = "#ffffff"
theme.widget_battery_bg_low = "#ff8800"
theme.widget_battery_fg_low = "#000000"

-- Weather widget renkleri
theme.widget_weather_bg = "#0088ff"
theme.widget_weather_fg = "#ffffff"

-- Calendar widget renkleri
theme.widget_calendar_bg = "#2d2d2d"
theme.widget_calendar_fg = "#ffffff"
theme.widget_calendar_bg_focus = "#00ff88"
theme.widget_calendar_fg_focus = "#000000"
theme.widget_calendar_bg_weekend = "#ff8800"
theme.widget_calendar_fg_weekend = "#000000"

-- Music widget renkleri
theme.widget_music_bg = "#8800ff"
theme.widget_music_fg = "#ffffff"
theme.widget_music_bg_playing = "#00ff88"
theme.widget_music_fg_playing = "#000000"

-- Email widget renkleri
theme.widget_email_bg = "#ff0088"
theme.widget_email_fg = "#ffffff"
theme.widget_email_bg_new = "#00ff88"
theme.widget_email_fg_new = "#000000"

-- Özel efektler
theme.enable_blur = true
theme.blur_strength = 10
theme.enable_shadows = true
theme.shadow_color = "#000000"
theme.shadow_opacity = 0.3
theme.shadow_offset_x = 2
theme.shadow_offset_y = 2
theme.shadow_blur_radius = 8

-- Özel şekiller
theme.client_shape_rounded = function(cr, width, height)
    gears.shape.rounded_rect(cr, width, height, 8)
end

theme.client_shape_rounded_small = function(cr, width, height)
    gears.shape.rounded_rect(cr, width, height, 4)
end

theme.client_shape_rounded_large = function(cr, width, height)
    gears.shape.rounded_rect(cr, width, height, 16)
end

-- Özel gradient'ler
theme.gradient_bg_normal = gears.color.create_linear_pattern(
    {0, 0, 0, height},
    {0, height, 0, 0},
    {"#1a1a1a", "#2d2d2d"}
)

theme.gradient_bg_focus = gears.color.create_linear_pattern(
    {0, 0, 0, height},
    {0, height, 0, 0},
    {"#00ff88", "#00cc66"}
)

-- Özel font ağırlıkları
theme.font_bold = "JetBrains Mono Bold 10"
theme.font_italic = "JetBrains Mono Italic 10"
theme.font_bold_italic = "JetBrains Mono Bold Italic 10"

-- Özel boyutlar
theme.icon_size = 16
theme.widget_height = 20
theme.widget_margin = 4
theme.widget_spacing = 8

-- Özel zamanlayıcılar
theme.auto_focus_timeout = 0.5
theme.auto_raise_timeout = 0.1
theme.urgent_timeout = 5

return theme 