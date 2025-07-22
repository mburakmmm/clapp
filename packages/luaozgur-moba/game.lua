-- Ana oyun sınıfı
local Game = {}
Game.__index = Game

local Characters = require('characters')
local Map = require('map')

function Game:new()
    local game = {
        map = Map.GameMap:new(),
        blueTeam = {},
        redTeam = {},
        selectedCharacter = nil,
        mouseX = 0,
        mouseY = 0,
        gameTime = 0,
        gameState = "playing", -- playing, paused, gameOver
        winner = nil,
        effects = {},
        minions = {blue = {}, red = {}},
        minionSpawnTimer = 0
    }
    
    setmetatable(game, self)
    return game
end

function Game:startNewGame()
    -- Takımları oluştur
    self:createTeams()
    
    -- Oyun durumunu sıfırla
    self.gameTime = 0
    self.gameState = "playing"
    self.winner = nil
    self.effects = {}
    self.minions = {blue = {}, red = {}}
    self.minionSpawnTimer = 0
end

function Game:createTeams()
    self.blueTeam = {}
    self.redTeam = {}
    
    -- Her takım için 5 karakter seç (rastgele)
    local characterIndices = {}
    for i = 1, #Characters.DATA do
        table.insert(characterIndices, i)
    end
    
    -- Karıştır
    for i = #characterIndices, 2, -1 do
        local j = math.random(i)
        characterIndices[i], characterIndices[j] = characterIndices[j], characterIndices[i]
    end
    
    -- Mavi takım (ilk 5)
    for i = 1, 5 do
        local charData = Characters.DATA[characterIndices[i]]
        local spawnX, spawnY = self.map:getSpawnPoint(1)
        local char = Characters.Character:new(charData, spawnX, spawnY, 1)
        table.insert(self.blueTeam, char)
    end
    
    -- Kırmızı takım (sonraki 5)
    for i = 6, 10 do
        local charData = Characters.DATA[characterIndices[i]]
        local spawnX, spawnY = self.map:getSpawnPoint(2)
        local char = Characters.Character:new(charData, spawnX, spawnY, 2)
        table.insert(self.redTeam, char)
    end
end

function Game:update(dt)
    if self.gameState ~= "playing" then return end
    
    self.gameTime = self.gameTime + dt
    
    -- Karakterleri güncelle
    for _, char in ipairs(self.blueTeam) do
        if not char:isDead() then
            char:update(dt)
        end
    end
    
    for _, char in ipairs(self.redTeam) do
        if not char:isDead() then
            char:update(dt)
        end
    end
    
    -- Haritayı güncelle
    self.map:update(dt, self.blueTeam, self.redTeam)
    
    -- Minion spawn sistemi
    self.minionSpawnTimer = self.minionSpawnTimer + dt
    if self.minionSpawnTimer >= 30 then -- 30 saniyede bir minion
        self:spawnMinions()
        self.minionSpawnTimer = 0
    end
    
    -- Minionları güncelle
    self:updateMinions(dt)
    
    -- Efektleri güncelle
    self:updateEffects(dt)
    
    -- Savaş sistemi
    self:updateCombat(dt)
    
    -- Oyun sonu kontrolü
    self:checkGameEnd()
end

function Game:spawnMinions()
    -- Her şerit için minion spawn et
    local lanes = {"top", "mid", "bot"}
    
    for _, lane in ipairs(lanes) do
        local laneY = self.map:getLaneY(lane)
        
        -- Mavi minionlar
        for i = 1, 3 do
            local minion = {
                x = 150 + (i-1) * 30,
                y = laneY + math.random(-10, 10),
                team = 1,
                health = 300,
                maxHealth = 300,
                attack = 40,
                speed = 0.8,
                target = nil,
                isMoving = false
            }
            table.insert(self.minions.blue, minion)
        end
        
        -- Kırmızı minionlar
        for i = 1, 3 do
            local minion = {
                x = 1130 - (i-1) * 30,
                y = laneY + math.random(-10, 10),
                team = 2,
                health = 300,
                maxHealth = 300,
                attack = 40,
                speed = 0.8,
                target = nil,
                isMoving = false
            }
            table.insert(self.minions.red, minion)
        end
    end
end

function Game:updateMinions(dt)
    -- Mavi minionları güncelle
    for i = #self.minions.blue, 1, -1 do
        local minion = self.minions.blue[i]
        if minion.health <= 0 then
            table.remove(self.minions.blue, i)
        else
            self:updateMinion(minion, dt, self.minions.red, self.redTeam)
        end
    end
    
    -- Kırmızı minionları güncelle
    for i = #self.minions.red, 1, -1 do
        local minion = self.minions.red[i]
        if minion.health <= 0 then
            table.remove(self.minions.red, i)
        else
            self:updateMinion(minion, dt, self.minions.blue, self.blueTeam)
        end
    end
end

function Game:updateMinion(minion, dt, enemyMinions, enemyTeam)
    -- En yakın düşmanı bul
    local closestEnemy = nil
    local closestDistance = 1000
    
    -- Düşman minionları kontrol et
    for _, enemy in ipairs(enemyMinions) do
        if enemy.health > 0 then
            local dx = enemy.x - minion.x
            local dy = enemy.y - minion.y
            local distance = math.sqrt(dx * dx + dy * dy)
            
            if distance < closestDistance then
                closestEnemy = enemy
                closestDistance = distance
            end
        end
    end
    
    -- Düşman karakterleri kontrol et
    for _, enemy in ipairs(enemyTeam) do
        if not enemy:isDead() then
            local dx = enemy.x - minion.x
            local dy = enemy.y - minion.y
            local distance = math.sqrt(dx * dx + dy * dy)
            
            if distance < closestDistance then
                closestEnemy = enemy
                closestDistance = distance
            end
        end
    end
    
    -- Hedef varsa saldır veya yaklaş
    if closestEnemy and closestDistance < 50 then
        -- Saldır
        if closestEnemy.health then
            closestEnemy.health = math.max(0, closestEnemy.health - minion.attack * dt)
        end
    elseif closestEnemy then
        -- Yaklaş
        local dx = closestEnemy.x - minion.x
        local dy = closestEnemy.y - minion.y
        local distance = math.sqrt(dx * dx + dy * dy)
        
        if distance > 5 then
            local moveSpeed = 50 * minion.speed
            local moveX = (dx / distance) * moveSpeed * dt
            local moveY = (dy / distance) * moveSpeed * dt
            minion.x = minion.x + moveX
            minion.y = minion.y + moveY
        end
    else
        -- Hedef yoksa ileri git
        if minion.team == 1 then
            minion.x = minion.x + 30 * dt
        else
            minion.x = minion.x - 30 * dt
        end
    end
end

function Game:updateCombat(dt)
    -- Karakterler arası savaş
    for _, blueChar in ipairs(self.blueTeam) do
        if not blueChar:isDead() then
            for _, redChar in ipairs(self.redTeam) do
                if not redChar:isDead() then
                    local dx = redChar.x - blueChar.x
                    local dy = redChar.y - blueChar.y
                    local distance = math.sqrt(dx * dx + dy * dy)
                    
                    if distance <= blueChar.range then
                        local damage = blueChar:attack(redChar)
                        if damage > 0 then
                            self:addEffect("damage", redChar.x, redChar.y, damage)
                        end
                    end
                end
            end
        end
    end
end

function Game:updateEffects(dt)
    for i = #self.effects, 1, -1 do
        local effect = self.effects[i]
        effect.life = effect.life - dt
        
        if effect.life <= 0 then
            table.remove(self.effects, i)
        end
    end
end

function Game:addEffect(type, x, y, value)
    local effect = {
        type = type,
        x = x,
        y = y,
        value = value,
        life = 1.0,
        maxLife = 1.0
    }
    table.insert(self.effects, effect)
end

function Game:checkGameEnd()
    -- Tüm kuleler yıkıldı mı kontrol et
    local blueTowersDestroyed = 0
    local redTowersDestroyed = 0
    
    for _, tower in ipairs(self.map.towers) do
        if tower:isDestroyed() then
            if tower.team == 1 then
                blueTowersDestroyed = blueTowersDestroyed + 1
            else
                redTowersDestroyed = redTowersDestroyed + 1
            end
        end
    end
    
    -- Üs yıkıldı mı kontrol et (basit kontrol)
    if blueTowersDestroyed >= 9 then -- Tüm kuleler yıkıldı
        self.gameState = "gameOver"
        self.winner = 2 -- Kırmızı kazandı
    elseif redTowersDestroyed >= 9 then
        self.gameState = "gameOver"
        self.winner = 1 -- Mavi kazandı
    end
end

function Game:draw()
    -- Haritayı çiz
    self.map:draw()
    
    -- Minionları çiz
    self:drawMinions()
    
    -- Karakterleri çiz
    for _, char in ipairs(self.blueTeam) do
        if not char:isDead() then
            char:draw()
        end
    end
    
    for _, char in ipairs(self.redTeam) do
        if not char:isDead() then
            char:draw()
        end
    end
    
    -- Efektleri çiz
    self:drawEffects()
    
    -- UI çiz
    self:drawUI()
    
    -- Oyun sonu ekranı
    if self.gameState == "gameOver" then
        self:drawGameOver()
    end
end

function Game:drawMinions()
    -- Mavi minionlar
    love.graphics.setColor(0, 0, 1, 0.7)
    for _, minion in ipairs(self.minions.blue) do
        if minion.health > 0 then
            love.graphics.circle("fill", minion.x, minion.y, 8)
            
            -- Can barı
            local healthPercent = minion.health / minion.maxHealth
            love.graphics.setColor(1 - healthPercent, healthPercent, 0)
            love.graphics.rectangle("fill", minion.x - 10, minion.y - 15, 20 * healthPercent, 3)
        end
    end
    
    -- Kırmızı minionlar
    love.graphics.setColor(1, 0, 0, 0.7)
    for _, minion in ipairs(self.minions.red) do
        if minion.health > 0 then
            love.graphics.circle("fill", minion.x, minion.y, 8)
            
            -- Can barı
            local healthPercent = minion.health / minion.maxHealth
            love.graphics.setColor(1 - healthPercent, healthPercent, 0)
            love.graphics.rectangle("fill", minion.x - 10, minion.y - 15, 20 * healthPercent, 3)
        end
    end
end

function Game:drawEffects()
    for _, effect in ipairs(self.effects) do
        if effect.type == "damage" then
            local alpha = effect.life / effect.maxLife
            love.graphics.setColor(1, 0, 0, alpha)
            love.graphics.print("-" .. effect.value, effect.x, effect.y - alpha * 20)
        end
    end
end

function Game:drawUI()
    -- Oyun bilgileri
    love.graphics.setColor(1, 1, 1)
    love.graphics.print("Süre: " .. math.floor(self.gameTime), 10, 650)
    love.graphics.print("Mavi Takım: " .. #self.blueTeam, 10, 670)
    love.graphics.print("Kırmızı Takım: " .. #self.redTeam, 10, 690)
    
    -- Seçili karakter bilgileri
    if self.selectedCharacter then
        local char = self.selectedCharacter
        love.graphics.print("Seçili: " .. char.name, 1100, 650)
        love.graphics.print("Can: " .. math.floor(char.health) .. "/" .. char.maxHealth, 1100, 670)
        love.graphics.print("Saldırı: " .. char.attack, 1100, 690)
    end
end

function Game:drawGameOver()
    love.graphics.setColor(0, 0, 0, 0.8)
    love.graphics.rectangle("fill", 0, 0, 1280, 720)
    
    love.graphics.setColor(1, 1, 1)
    if self.winner == 1 then
        love.graphics.print("MAVİ TAKIM KAZANDI!", 500, 300)
    else
        love.graphics.print("KIRMIZI TAKIM KAZANDI!", 500, 300)
    end
    
    love.graphics.print("Tekrar başlamak için ENTER'a basın", 450, 350)
end

function Game:mousepressed(x, y, button)
    if button == 1 then -- Sol tık
        -- Karakter seçimi
        for _, char in ipairs(self.blueTeam) do
            if not char:isDead() then
                local dx = x - char.x
                local dy = y - char.y
                local distance = math.sqrt(dx * dx + dy * dy)
                
                if distance <= 25 then
                    self.selectedCharacter = char
                    return
                end
            end
        end
        
        -- Hareket komutu
        if self.selectedCharacter and not self.selectedCharacter:isDead() then
            self.selectedCharacter:moveTo(x, y)
        end
    end
end

function Game:mousemoved(x, y)
    self.mouseX = x
    self.mouseY = y
end

return Game 