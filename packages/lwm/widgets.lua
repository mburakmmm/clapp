-- LWM Özel Widget'ları
-- Modern ve kullanışlı widget'lar

local awful = require("awful")
local beautiful = require("beautiful")
local gears = require("gears")
local wibox = require("wibox")
local naughty = require("naughty")
local vicious = require("vicious")

local widgets = {}

-- CPU Widget
function widgets.create_cpu_widget()
    local cpu_widget = wibox.widget.textbox()
    vicious.register(cpu_widget, vicious.widgets.cpu, function(widget, args)
        local cpu_usage = args[1]
        local color = beautiful.widget_cpu_fg
        if cpu_usage > 80 then
            color = "#ff0000"
        elseif cpu_usage > 60 then
            color = "#ff8800"
        end
        return string.format('<span color="%s">CPU: %d%%</span>', color, cpu_usage)
    end, 2)
    return cpu_widget
end

-- Memory Widget
function widgets.create_memory_widget()
    local mem_widget = wibox.widget.textbox()
    vicious.register(mem_widget, vicious.widgets.mem, function(widget, args)
        local mem_usage = args[1]
        local color = beautiful.widget_mem_fg
        if mem_usage > 80 then
            color = "#ff0000"
        elseif mem_usage > 60 then
            color = "#ff8800"
        end
        return string.format('<span color="%s">RAM: %d%%</span>', color, mem_usage)
    end, 2)
    return mem_widget
end

-- Temperature Widget
function widgets.create_temp_widget()
    local temp_widget = wibox.widget.textbox()
    vicious.register(temp_widget, vicious.widgets.thermal, function(widget, args)
        local temp = args[1]
        local color = beautiful.widget_temp_fg
        if temp > 80 then
            color = "#ff0000"
        elseif temp > 60 then
            color = "#ff8800"
        end
        return string.format('<span color="%s">%d°C</span>', color, temp)
    end, 5, "thermal_zone0")
    return temp_widget
end

-- Network Widget
function widgets.create_network_widget()
    local net_widget = wibox.widget.textbox()
    vicious.register(net_widget, vicious.widgets.net, function(widget, args)
        local interface = "wlan0" -- veya "eth0"
        if args["{" .. interface .. " down_kb}"] then
            local down = args["{" .. interface .. " down_kb}"]
            local up = args["{" .. interface .. " up_kb}"]
            return string.format('<span color="%s">↓%s ↑%s</span>', 
                beautiful.widget_net_fg, 
                vicious.format(down, 1024), 
                vicious.format(up, 1024))
        else
            return string.format('<span color="%s">Net: --</span>', beautiful.widget_net_fg)
        end
    end, 2)
    return net_widget
end

-- Volume Widget
function widgets.create_volume_widget()
    local vol_widget = wibox.widget.textbox()
    
    local function update_volume()
        awful.spawn.easy_async("amixer get Master", function(stdout)
            local volume = stdout:match("(%d+)%%")
            if volume then
                local color = beautiful.widget_vol_fg
                local icon = "🔊"
                if tonumber(volume) == 0 then
                    icon = "🔇"
                elseif tonumber(volume) < 50 then
                    icon = "🔉"
                end
                vol_widget:set_markup(string.format('<span color="%s">%s %s%%</span>', color, icon, volume))
            end
        end)
    end
    
    vol_widget:buttons(gears.table.join(
        awful.button({}, 1, function() awful.spawn("amixer set Master toggle") end),
        awful.button({}, 4, function() awful.spawn("amixer set Master 5%+") end),
        awful.button({}, 5, function() awful.spawn("amixer set Master 5%-") end)
    ))
    
    update_volume()
    gears.timer.start_new(1, update_volume)
    
    return vol_widget
end

-- Battery Widget
function widgets.create_battery_widget()
    local bat_widget = wibox.widget.textbox()
    
    local function update_battery()
        awful.spawn.easy_async("cat /sys/class/power_supply/BAT0/capacity", function(stdout)
            local capacity = tonumber(stdout)
            if capacity then
                local color = beautiful.widget_battery_fg
                local icon = "🔋"
                
                if capacity <= 10 then
                    color = beautiful.widget_battery_fg_critical
                    icon = "🔴"
                elseif capacity <= 25 then
                    color = beautiful.widget_battery_fg_low
                    icon = "🟠"
                elseif capacity <= 50 then
                    icon = "🟡"
                elseif capacity <= 75 then
                    icon = "🟢"
                else
                    icon = "🔋"
                end
                
                bat_widget:set_markup(string.format('<span color="%s">%s %d%%</span>', color, icon, capacity))
            end
        end)
    end
    
    update_battery()
    gears.timer.start_new(30, update_battery)
    
    return bat_widget
end

-- Weather Widget
function widgets.create_weather_widget()
    local weather_widget = wibox.widget.textbox()
    
    local function update_weather()
        -- Bu örnek için basit bir weather API kullanımı
        -- Gerçek uygulamada OpenWeatherMap gibi bir API kullanabilirsiniz
        awful.spawn.easy_async("curl -s 'http://wttr.in/?format=%C+%t'", function(stdout)
            if stdout and stdout ~= "" then
                weather_widget:set_markup(string.format('<span color="%s">%s</span>', 
                    beautiful.widget_weather_fg, stdout:gsub("\n", "")))
            end
        end)
    end
    
    update_weather()
    gears.timer.start_new(300, update_weather) -- 5 dakikada bir güncelle
    
    return weather_widget
end

-- Calendar Widget
function widgets.create_calendar_widget()
    local calendar_widget = wibox.widget.textbox()
    local calendar_popup = awful.popup({
        widget = {
            {
                awful.widget.calendar_popup.month(),
                margins = 10,
                widget = wibox.container.margin,
            },
            bg = beautiful.widget_calendar_bg,
            fg = beautiful.widget_calendar_fg,
            border_width = 1,
            border_color = beautiful.widget_calendar_bg,
            widget = wibox.container.background,
        },
        placement = awful.placement.under,
        hide_on_right_click = true,
    })
    
    calendar_widget:set_markup(string.format('<span color="%s">📅</span>', beautiful.widget_calendar_fg))
    calendar_widget:buttons(gears.table.join(
        awful.button({}, 1, function()
            if calendar_popup.visible then
                calendar_popup.visible = false
            else
                calendar_popup.visible = true
            end
        end)
    ))
    
    return calendar_widget
end

-- Music Widget
function widgets.create_music_widget()
    local music_widget = wibox.widget.textbox()
    
    local function update_music()
        awful.spawn.easy_async("playerctl metadata title", function(stdout)
            if stdout and stdout ~= "" then
                local title = stdout:gsub("\n", "")
                if #title > 30 then
                    title = title:sub(1, 27) .. "..."
                end
                music_widget:set_markup(string.format('<span color="%s">🎵 %s</span>', 
                    beautiful.widget_music_fg, title))
            else
                music_widget:set_markup(string.format('<span color="%s">🎵 --</span>', 
                    beautiful.widget_music_fg))
            end
        end)
    end
    
    music_widget:buttons(gears.table.join(
        awful.button({}, 1, function() awful.spawn("playerctl play-pause") end),
        awful.button({}, 4, function() awful.spawn("playerctl next") end),
        awful.button({}, 5, function() awful.spawn("playerctl previous") end)
    ))
    
    update_music()
    gears.timer.start_new(2, update_music)
    
    return music_widget
end

-- Email Widget
function widgets.create_email_widget()
    local email_widget = wibox.widget.textbox()
    
    local function update_email()
        -- Bu örnek için basit bir email kontrolü
        -- Gerçek uygulamada IMAP veya API kullanabilirsiniz
        awful.spawn.easy_async("find ~/.local/share/mail/*/INBOX/new -type f 2>/dev/null | wc -l", function(stdout)
            local count = tonumber(stdout) or 0
            local color = beautiful.widget_email_fg
            if count > 0 then
                color = beautiful.widget_email_fg_new
            end
            email_widget:set_markup(string.format('<span color="%s">📧 %d</span>', color, count))
        end)
    end
    
    update_email()
    gears.timer.start_new(60, update_email) -- 1 dakikada bir güncelle
    
    return email_widget
end

-- System Info Widget
function widgets.create_system_info_widget()
    local sys_widget = wibox.widget.textbox()
    
    local function update_system_info()
        awful.spawn.easy_async("uptime -p", function(stdout)
            if stdout then
                local uptime = stdout:gsub("\n", ""):gsub("up ", "")
                sys_widget:set_markup(string.format('<span color="%s">⏱ %s</span>', 
                    beautiful.widget_fg, uptime))
            end
        end)
    end
    
    update_system_info()
    gears.timer.start_new(60, update_system_info) -- 1 dakikada bir güncelle
    
    return sys_widget
end

-- Workspace Indicator Widget
function widgets.create_workspace_indicator()
    local workspace_widget = wibox.widget.textbox()
    
    local function update_workspace()
        local s = awful.screen.focused()
        if s then
            local current_tag = s.selected_tag
            if current_tag then
                workspace_widget:set_markup(string.format('<span color="%s">🏠 %s</span>', 
                    beautiful.widget_fg, current_tag.name))
            end
        end
    end
    
    -- Tag değişikliklerini dinle
    tag.connect_signal("property::selected", update_workspace)
    screen.connect_signal("property::selected_tag", update_workspace)
    
    update_workspace()
    return workspace_widget
end

-- Quick Launch Widget
function widgets.create_quick_launch_widget()
    local quick_launch = wibox.widget.textbox()
    
    local apps = {
        {icon = "🌐", cmd = "firefox", name = "Firefox"},
        {icon = "📝", cmd = "code", name = "VS Code"},
        {icon = "📁", cmd = "nautilus", name = "Dosya Yöneticisi"},
        {icon = "🎵", cmd = "spotify", name = "Spotify"},
        {icon = "📧", cmd = "thunderbird", name = "Thunderbird"}
    }
    
    local current_app = 1
    
    quick_launch:set_markup(string.format('<span color="%s">%s</span>', 
        beautiful.widget_fg, apps[current_app].icon))
    
    quick_launch:buttons(gears.table.join(
        awful.button({}, 1, function()
            awful.spawn(apps[current_app].cmd)
        end),
        awful.button({}, 4, function()
            current_app = current_app - 1
            if current_app < 1 then current_app = #apps end
            quick_launch:set_markup(string.format('<span color="%s">%s</span>', 
                beautiful.widget_fg, apps[current_app].icon))
        end),
        awful.button({}, 5, function()
            current_app = current_app + 1
            if current_app > #apps then current_app = 1 end
            quick_launch:set_markup(string.format('<span color="%s">%s</span>', 
                beautiful.widget_fg, apps[current_app].icon))
        end)
    ))
    
    return quick_launch
end

-- Notification Center Widget
function widgets.create_notification_center_widget()
    local notif_widget = wibox.widget.textbox()
    local notif_count = 0
    
    notif_widget:set_markup(string.format('<span color="%s">🔔</span>', beautiful.widget_fg))
    
    notif_widget:buttons(gears.table.join(
        awful.button({}, 1, function()
            -- Bildirim merkezini aç
            awful.spawn("notify-send 'Bildirim Merkezi' 'Henüz implement edilmedi'")
        end)
    ))
    
    -- Bildirim sayısını güncelle
    naughty.connect_signal("request::display", function(notification)
        notif_count = notif_count + 1
        notif_widget:set_markup(string.format('<span color="%s">🔔 %d</span>', 
            beautiful.widget_fg, notif_count))
    end)
    
    return notif_widget
end

-- Tüm widget'ları oluşturan fonksiyon
function widgets.create_all_widgets()
    return {
        cpu = widgets.create_cpu_widget(),
        memory = widgets.create_memory_widget(),
        temp = widgets.create_temp_widget(),
        network = widgets.create_network_widget(),
        volume = widgets.create_volume_widget(),
        battery = widgets.create_battery_widget(),
        weather = widgets.create_weather_widget(),
        calendar = widgets.create_calendar_widget(),
        music = widgets.create_music_widget(),
        email = widgets.create_email_widget(),
        system_info = widgets.create_system_info_widget(),
        workspace = widgets.create_workspace_indicator(),
        quick_launch = widgets.create_quick_launch_widget(),
        notification_center = widgets.create_notification_center_widget()
    }
end

return widgets 