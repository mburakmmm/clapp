-- Harita ve kule sistemi
local Map = {}

-- Kule sınıfı
local Tower = {}
Tower.__index = Tower

function Tower:new(x, y, team, lane)
    local tower = {
        x = x,
        y = y,
        team = team, -- 1: mavi, 2: kırmızı
        lane = lane, -- "top", "mid", "bot"
        health = 2000,
        maxHealth = 2000,
        attack = 150,
        range = 200,
        attackCooldown = 0,
        target = nil,
        level = 1
    }
    setmetatable(tower, self)
    return tower
end

function Tower:update(dt, enemies)
    -- Saldırı cooldown güncelleme
    if self.attackCooldown > 0 then
        self.attackCooldown = self.attackCooldown - dt
    end
    
    -- Hedef bulma ve saldırma
    if self.attackCooldown <= 0 then
        local closestEnemy = nil
        local closestDistance = self.range
        
        for _, enemy in ipairs(enemies) do
            -- Karakter kontrolü
            if enemy.isDead then
                if not enemy:isDead() then
                    local dx = enemy.x - self.x
                    local dy = enemy.y - self.y
                    local distance = math.sqrt(dx * dx + dy * dy)
                    
                    if distance <= self.range and distance < closestDistance then
                        closestEnemy = enemy
                        closestDistance = distance
                    end
                end
            else
                -- Minion kontrolü (health özelliği varsa)
                if enemy.health and enemy.health > 0 then
                    local dx = enemy.x - self.x
                    local dy = enemy.y - self.y
                    local distance = math.sqrt(dx * dx + dy * dy)
                    
                    if distance <= self.range and distance < closestDistance then
                        closestEnemy = enemy
                        closestDistance = distance
                    end
                end
            end
        end
        
        if closestEnemy then
            self:attack(closestEnemy)
        end
    end
end

function Tower:attack(target)
    target.health = math.max(0, target.health - self.attack)
    self.attackCooldown = 1.5 -- 1.5 saniye cooldown
end

function Tower:draw()
    -- Kule çizimi
    if self.team == 1 then
        love.graphics.setColor(0, 0, 1, 0.8)
    else
        love.graphics.setColor(1, 0, 0, 0.8)
    end
    
    love.graphics.rectangle("fill", self.x - 15, self.y - 25, 30, 50)
    
    -- Kule üstü
    love.graphics.setColor(0.5, 0.5, 0.5)
    love.graphics.rectangle("fill", self.x - 20, self.y - 30, 40, 10)
    
    -- Can barı
    local barWidth = 50
    local barHeight = 6
    local healthPercent = self.health / self.maxHealth
    
    love.graphics.setColor(0.2, 0.2, 0.2, 0.8)
    love.graphics.rectangle("fill", self.x - barWidth/2, self.y - 40, barWidth, barHeight)
    
    love.graphics.setColor(1 - healthPercent, healthPercent, 0)
    love.graphics.rectangle("fill", self.x - barWidth/2, self.y - 40, barWidth * healthPercent, barHeight)
    
    -- Kule seviyesi
    love.graphics.setColor(1, 1, 1)
    love.graphics.print("T" .. self.level, self.x - 5, self.y - 5)
end

function Tower:isDestroyed()
    return self.health <= 0
end

-- Harita sınıfı
local GameMap = {}
GameMap.__index = GameMap

function GameMap:new()
    local map = {
        width = 1280,
        height = 720,
        towers = {},
        lanes = {
            top = {y = 150},
            mid = {y = 360},
            bot = {y = 570}
        },
        baseRadius = 80,
        spawnPoints = {
            blue = {x = 100, y = 360},
            red = {x = 1180, y = 360}
        }
    }
    
    -- Kuleleri yerleştir
    self:setupTowers(map)
    
    setmetatable(map, self)
    return map
end

function GameMap:setupTowers(map)
    -- Üst şerit kuleleri
    table.insert(map.towers, Tower:new(200, map.lanes.top.y, 1, "top"))
    table.insert(map.towers, Tower:new(400, map.lanes.top.y, 1, "top"))
    table.insert(map.towers, Tower:new(600, map.lanes.top.y, 1, "top"))
    table.insert(map.towers, Tower:new(800, map.lanes.top.y, 2, "top"))
    table.insert(map.towers, Tower:new(1000, map.lanes.top.y, 2, "top"))
    table.insert(map.towers, Tower:new(1080, map.lanes.top.y, 2, "top"))
    
    -- Orta şerit kuleleri
    table.insert(map.towers, Tower:new(200, map.lanes.mid.y, 1, "mid"))
    table.insert(map.towers, Tower:new(400, map.lanes.mid.y, 1, "mid"))
    table.insert(map.towers, Tower:new(600, map.lanes.mid.y, 1, "mid"))
    table.insert(map.towers, Tower:new(800, map.lanes.mid.y, 2, "mid"))
    table.insert(map.towers, Tower:new(1000, map.lanes.mid.y, 2, "mid"))
    table.insert(map.towers, Tower:new(1080, map.lanes.mid.y, 2, "mid"))
    
    -- Alt şerit kuleleri
    table.insert(map.towers, Tower:new(200, map.lanes.bot.y, 1, "bot"))
    table.insert(map.towers, Tower:new(400, map.lanes.bot.y, 1, "bot"))
    table.insert(map.towers, Tower:new(600, map.lanes.bot.y, 1, "bot"))
    table.insert(map.towers, Tower:new(800, map.lanes.bot.y, 2, "bot"))
    table.insert(map.towers, Tower:new(1000, map.lanes.bot.y, 2, "bot"))
    table.insert(map.towers, Tower:new(1080, map.lanes.bot.y, 2, "bot"))
end

function GameMap:update(dt, blueTeam, redTeam)
    -- Kuleleri güncelle
    for _, tower in ipairs(self.towers) do
        if not tower:isDestroyed() then
            local enemies = (tower.team == 1) and redTeam or blueTeam
            tower:update(dt, enemies)
        end
    end
end

function GameMap:draw()
    -- Arka plan
    love.graphics.setColor(0.1, 0.3, 0.1)
    love.graphics.rectangle("fill", 0, 0, self.width, self.height)
    
    -- Şerit çizgileri
    love.graphics.setColor(0.2, 0.4, 0.2)
    love.graphics.rectangle("fill", 0, self.lanes.top.y - 2, self.width, 4)
    love.graphics.rectangle("fill", 0, self.lanes.mid.y - 2, self.width, 4)
    love.graphics.rectangle("fill", 0, self.lanes.bot.y - 2, self.width, 4)
    
    -- Orta çizgi
    love.graphics.setColor(0.3, 0.5, 0.3)
    love.graphics.rectangle("fill", self.width/2 - 2, 0, 4, self.height)
    
    -- Üsler
    -- Mavi üs
    love.graphics.setColor(0, 0, 1, 0.3)
    love.graphics.circle("fill", self.spawnPoints.blue.x, self.spawnPoints.blue.y, self.baseRadius)
    love.graphics.setColor(0, 0, 1, 0.8)
    love.graphics.circle("line", self.spawnPoints.blue.x, self.spawnPoints.blue.y, self.baseRadius)
    
    -- Kırmızı üs
    love.graphics.setColor(1, 0, 0, 0.3)
    love.graphics.circle("fill", self.spawnPoints.red.x, self.spawnPoints.red.y, self.baseRadius)
    love.graphics.setColor(1, 0, 0, 0.8)
    love.graphics.circle("line", self.spawnPoints.red.x, self.spawnPoints.red.y, self.baseRadius)
    
    -- Kuleleri çiz
    for _, tower in ipairs(self.towers) do
        if not tower:isDestroyed() then
            tower:draw()
        end
    end
    
    -- Harita bilgileri
    love.graphics.setColor(1, 1, 1)
    love.graphics.print("Üst Şerit", 10, 10)
    love.graphics.print("Orta Şerit", 10, 220)
    love.graphics.print("Alt Şerit", 10, 430)
end

function GameMap:getSpawnPoint(team)
    if team == 1 then
        return self.spawnPoints.blue.x, self.spawnPoints.blue.y
    else
        return self.spawnPoints.red.x, self.spawnPoints.red.y
    end
end

function GameMap:getLaneY(lane)
    return self.lanes[lane].y
end

function GameMap:isInBase(x, y, team)
    local spawnX, spawnY = self:getSpawnPoint(team)
    local dx = x - spawnX
    local dy = y - spawnY
    local distance = math.sqrt(dx * dx + dy * dy)
    return distance <= self.baseRadius
end

Map.GameMap = GameMap
Map.Tower = Tower
return Map 