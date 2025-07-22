-- Menü sistemi
local Menu = {}
Menu.__index = Menu

local Characters = require('characters')

function Menu:new()
    local menu = {
        state = "main", -- main, characterSelect, help
        selectedCharacter = 1,
        selectedTeam = 1, -- 1: mavi, 2: kırmızı
        buttons = {},
        characterButtons = {},
        teamButtons = {}
    }
    
    setmetatable(menu, self)
    menu:setupButtons()
    return menu
end

function Menu:setupButtons()
    -- Ana menü butonları
    self.buttons = {
        {text = "Oyunu Başlat", x = 540, y = 250, width = 200, height = 50, action = "start"},
        {text = "Karakter Seç", x = 540, y = 320, width = 200, height = 50, action = "characterSelect"},
        {text = "Yardım", x = 540, y = 390, width = 200, height = 50, action = "help"},
        {text = "Çıkış", x = 540, y = 460, width = 200, height = 50, action = "exit"}
    }
    
    -- Karakter seçim butonları
    self.characterButtons = {}
    local startX = 50
    local startY = 100
    local buttonWidth = 200
    local buttonHeight = 80
    local buttonsPerRow = 5
    
    for i, charData in ipairs(Characters.DATA) do
        local row = math.floor((i-1) / buttonsPerRow)
        local col = (i-1) % buttonsPerRow
        
        local button = {
            text = charData.name,
            x = startX + col * (buttonWidth + 20),
            y = startY + row * (buttonHeight + 20),
            width = buttonWidth,
            height = buttonHeight,
            charIndex = i,
            category = charData.category,
            color = charData.color
        }
        table.insert(self.characterButtons, button)
    end
    
    -- Takım seçim butonları
    self.teamButtons = {
        {text = "Mavi Takım", x = 400, y = 500, width = 150, height = 50, team = 1, color = {0, 0, 1}},
        {text = "Kırmızı Takım", x = 600, y = 500, width = 150, height = 50, team = 2, color = {1, 0, 0}}
    }
end

function Menu:update(dt)
    -- Menü animasyonları burada olabilir
end

function Menu:draw()
    if self.state == "main" then
        self:drawMainMenu()
    elseif self.state == "characterSelect" then
        self:drawCharacterSelect()
    elseif self.state == "help" then
        self:drawHelp()
    end
end

function Menu:drawMainMenu()
    -- Arka plan
    love.graphics.setColor(0.1, 0.1, 0.2)
    love.graphics.rectangle("fill", 0, 0, 1280, 720)
    
    -- Başlık
    love.graphics.setColor(1, 1, 1)
    love.graphics.print("LUA ÖZGÜR MOBA", 400, 100, 0, 2, 2)
    love.graphics.print("League of Legends Benzeri Oyun", 450, 150, 0, 1, 1)
    
    -- Butonları çiz
    for _, button in ipairs(self.buttons) do
        self:drawButton(button)
    end
    
    -- Karakter kategorileri bilgisi
    love.graphics.setColor(1, 1, 1)
    love.graphics.print("20 Farklı Karakter - 5 Kategori:", 50, 600)
    love.graphics.print("Büyücü, Savaşçı, Nişancı, Destek, Tank", 50, 620)
end

function Menu:drawCharacterSelect()
    -- Arka plan
    love.graphics.setColor(0.1, 0.1, 0.2)
    love.graphics.rectangle("fill", 0, 0, 1280, 720)
    
    -- Başlık
    love.graphics.setColor(1, 1, 1)
    love.graphics.print("Karakter Seçimi", 500, 30, 0, 2, 2)
    
    -- Kategori başlıkları
    love.graphics.setColor(1, 0.3, 0.3)
    love.graphics.print("BÜYÜCÜLER", 50, 70)
    love.graphics.setColor(0.8, 0.4, 0.2)
    love.graphics.print("SAVAŞÇILAR", 250, 70)
    love.graphics.setColor(0.2, 0.8, 0.4)
    love.graphics.print("NİŞANCILAR", 450, 70)
    love.graphics.setColor(0.2, 1, 0.2)
    love.graphics.print("DESTEKLER", 650, 70)
    love.graphics.setColor(0.5, 0.5, 0.5)
    love.graphics.print("TANKLAR", 850, 70)
    
    -- Karakter butonlarını çiz
    for _, button in ipairs(self.characterButtons) do
        self:drawCharacterButton(button)
    end
    
    -- Seçili karakter bilgisi
    if self.selectedCharacter then
        local charData = Characters.DATA[self.selectedCharacter]
        love.graphics.setColor(1, 1, 1)
        love.graphics.print("Seçili Karakter: " .. charData.name, 50, 470)
        love.graphics.print("Kategori: " .. charData.category, 50, 490)
        love.graphics.print("Can: " .. charData.health .. " | Saldırı: " .. charData.attack .. " | Hız: " .. charData.speed, 50, 510)
    end
    
    -- Takım seçim butonları
    love.graphics.setColor(1, 1, 1)
    love.graphics.print("Takım Seçin:", 400, 470)
    
    for _, button in ipairs(self.teamButtons) do
        self:drawTeamButton(button)
    end
    
    -- Geri butonu
    local backButton = {text = "Geri", x = 50, y = 650, width = 100, height = 40, action = "back"}
    self:drawButton(backButton)
    
    -- Başla butonu
    local startButton = {text = "Oyunu Başlat", x = 1100, y = 650, width = 150, height = 40, action = "startGame"}
    self:drawButton(startButton)
end

function Menu:drawHelp()
    -- Arka plan
    love.graphics.setColor(0.1, 0.1, 0.2)
    love.graphics.rectangle("fill", 0, 0, 1280, 720)
    
    -- Başlık
    love.graphics.setColor(1, 1, 1)
    love.graphics.print("YARDIM", 550, 50, 0, 2, 2)
    
    -- Kontroller
    love.graphics.print("KONTROLLER:", 50, 150)
    love.graphics.print("Sol Tık: Karakter seç / Hareket et", 50, 180)
    love.graphics.print("ESC: Menüye dön", 50, 200)
    love.graphics.print("ENTER: Oyunu başlat", 50, 220)
    
    -- Oyun Kuralları
    love.graphics.print("OYUN KURALLARI:", 50, 280)
    love.graphics.print("• Düşman kulelerini yıkarak üslerine ulaşın", 50, 310)
    love.graphics.print("• 3 şerit: Üst, Orta, Alt", 50, 330)
    love.graphics.print("• Her 30 saniyede minionlar spawn olur", 50, 350)
    love.graphics.print("• Karakterleriniz otomatik olarak düşmanlara saldırır", 50, 370)
    love.graphics.print("• Tüm düşman kulelerini yıkan takım kazanır", 50, 390)
    
    -- Karakter Kategorileri
    love.graphics.print("KARAKTER KATEGORİLERİ:", 50, 450)
    love.graphics.print("• Büyücü: Yüksek hasar, düşük can", 50, 480)
    love.graphics.print("• Savaşçı: Dengeli hasar ve can", 50, 500)
    love.graphics.print("• Nişancı: Uzun mesafe, yüksek hasar", 50, 520)
    love.graphics.print("• Destek: Düşük hasar, yardımcı yetenekler", 50, 540)
    love.graphics.print("• Tank: Düşük hasar, yüksek can ve savunma", 50, 560)
    
    -- Geri butonu
    local backButton = {text = "Geri", x = 50, y = 650, width = 100, height = 40, action = "back"}
    self:drawButton(backButton)
end

function Menu:drawButton(button)
    -- Buton arka planı
    love.graphics.setColor(0.3, 0.3, 0.5)
    love.graphics.rectangle("fill", button.x, button.y, button.width, button.height)
    
    -- Buton kenarlığı
    love.graphics.setColor(0.5, 0.5, 0.7)
    love.graphics.rectangle("line", button.x, button.y, button.width, button.height)
    
    -- Buton metni
    love.graphics.setColor(1, 1, 1)
    local textWidth = love.graphics.getFont():getWidth(button.text)
    local textHeight = love.graphics.getFont():getHeight()
    local textX = button.x + (button.width - textWidth) / 2
    local textY = button.y + (button.height - textHeight) / 2
    love.graphics.print(button.text, textX, textY)
end

function Menu:drawCharacterButton(button)
    -- Seçili karakter vurgusu
    if self.selectedCharacter == button.charIndex then
        love.graphics.setColor(1, 1, 0, 0.5)
        love.graphics.rectangle("fill", button.x - 5, button.y - 5, button.width + 10, button.height + 10)
    end
    
    -- Karakter rengi ile arka plan
    love.graphics.setColor(button.color[1] * 0.3, button.color[2] * 0.3, button.color[3] * 0.3)
    love.graphics.rectangle("fill", button.x, button.y, button.width, button.height)
    
    -- Karakter rengi ile kenarlık
    love.graphics.setColor(button.color[1], button.color[2], button.color[3])
    love.graphics.rectangle("line", button.x, button.y, button.width, button.height)
    
    -- Karakter adı
    love.graphics.setColor(1, 1, 1)
    love.graphics.print(button.text, button.x + 10, button.y + 10)
    
    -- Kategori
    love.graphics.setColor(0.8, 0.8, 0.8)
    love.graphics.print(button.category, button.x + 10, button.y + 30)
    
    -- Karakter özellikleri
    local charData = Characters.DATA[button.charIndex]
    love.graphics.print("Can: " .. charData.health, button.x + 10, button.y + 50)
    love.graphics.print("Saldırı: " .. charData.attack, button.x + 100, button.y + 50)
    
    -- Seçili işareti
    if self.selectedCharacter == button.charIndex then
        love.graphics.setColor(1, 1, 0)
        love.graphics.circle("fill", button.x + button.width - 15, button.y + 15, 8)
    end
end

function Menu:drawTeamButton(button)
    -- Takım rengi ile arka plan
    love.graphics.setColor(button.color[1] * 0.3, button.color[2] * 0.3, button.color[3] * 0.3)
    love.graphics.rectangle("fill", button.x, button.y, button.width, button.height)
    
    -- Takım rengi ile kenarlık
    love.graphics.setColor(button.color[1], button.color[2], button.color[3])
    love.graphics.rectangle("line", button.x, button.y, button.width, button.height)
    
    -- Takım adı
    love.graphics.setColor(1, 1, 1)
    local textWidth = love.graphics.getFont():getWidth(button.text)
    local textHeight = love.graphics.getFont():getHeight()
    local textX = button.x + (button.width - textWidth) / 2
    local textY = button.y + (button.height - textHeight) / 2
    love.graphics.print(button.text, textX, textY)
    
    -- Seçili takım işareti
    if self.selectedTeam == button.team then
        love.graphics.setColor(1, 1, 0)
        love.graphics.circle("fill", button.x + button.width - 15, button.y + button.height/2, 8)
    end
end

function Menu:mousepressed(x, y, button)
    if button == 1 then -- Sol tık
        if self.state == "main" then
            return self:handleMainMenuClick(x, y)
        elseif self.state == "characterSelect" then
            return self:handleCharacterSelectClick(x, y)
        elseif self.state == "help" then
            return self:handleHelpClick(x, y)
        end
    end
    return nil
end

function Menu:handleMainMenuClick(x, y)
    for _, button in ipairs(self.buttons) do
        if x >= button.x and x <= button.x + button.width and
           y >= button.y and y <= button.y + button.height then
            if button.action == "start" then
                -- Oyunu başlat
                return "startGame"
            elseif button.action == "characterSelect" then
                self.state = "characterSelect"
            elseif button.action == "help" then
                self.state = "help"
            elseif button.action == "exit" then
                love.event.quit()
            end
        end
    end
end

function Menu:handleCharacterSelectClick(x, y)
    -- Karakter butonları
    for _, charButton in ipairs(self.characterButtons) do
        if x >= charButton.x and x <= charButton.x + charButton.width and
           y >= charButton.y and y <= charButton.y + charButton.height then
            self.selectedCharacter = charButton.charIndex
            return
        end
    end
    
    -- Takım butonları
    for _, teamButton in ipairs(self.teamButtons) do
        if x >= teamButton.x and x <= teamButton.x + teamButton.width and
           y >= teamButton.y and y <= teamButton.y + teamButton.height then
            self.selectedTeam = teamButton.team
            return
        end
    end
    
    -- Geri butonu
    if x >= 50 and x <= 150 and y >= 650 and y <= 690 then
        self.state = "main"
        return
    end
    
    -- Başla butonu
    if x >= 1100 and x <= 1250 and y >= 650 and y <= 690 then
        return "startGame"
    end
end

function Menu:handleHelpClick(x, y)
    -- Geri butonu
    if x >= 50 and x <= 150 and y >= 650 and y <= 690 then
        self.state = "main"
    end
end

return Menu 