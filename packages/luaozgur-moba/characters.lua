-- Karakter sınıfları ve özellikleri
local Characters = {}

-- Karakter kategorileri
Characters.CATEGORIES = {
    MAGE = "büyücü",
    WARRIOR = "savaşçı", 
    MARKSMAN = "nişancı",
    SUPPORT = "destek",
    TANK = "tank"
}

-- Karakter verileri
Characters.DATA = {
    -- BÜYÜCÜLER (MAGE)
    {
        name = "Ateş Büyücüsü",
        category = Characters.CATEGORIES.MAGE,
        health = 500,
        mana = 800,
        attack = 60,
        defense = 30,
        speed = 1.2,
        range = 150,
        abilities = {"Ateş Topu", "Lav Patlaması", "Güneş Işını"},
        color = {1, 0.3, 0.3}
    },
    {
        name = "Buz Büyücüsü", 
        category = Characters.CATEGORIES.MAGE,
        health = 450,
        mana = 900,
        attack = 55,
        defense = 25,
        speed = 1.1,
        range = 160,
        abilities = {"Buz Mızrağı", "Donma", "Kar Fırtınası"},
        color = {0.3, 0.7, 1}
    },
    {
        name = "Şimşek Büyücüsü",
        category = Characters.CATEGORIES.MAGE,
        health = 480,
        mana = 850,
        attack = 70,
        defense = 20,
        speed = 1.3,
        range = 140,
        abilities = {"Şimşek", "Elektrik Ağı", "Gök Gürültüsü"},
        color = {1, 1, 0.3}
    },
    {
        name = "Karanlık Büyücü",
        category = Characters.CATEGORIES.MAGE,
        health = 520,
        mana = 750,
        attack = 65,
        defense = 35,
        speed = 1.0,
        range = 145,
        abilities = {"Gölge Saldırısı", "Karanlık Halka", "Ölüm Dokunuşu"},
        color = {0.5, 0.2, 0.8}
    },

    -- SAVAŞÇILAR (WARRIOR)
    {
        name = "Kılıç Ustası",
        category = Characters.CATEGORIES.WARRIOR,
        health = 700,
        mana = 300,
        attack = 85,
        defense = 60,
        speed = 1.4,
        range = 80,
        abilities = {"Keskin Vuruş", "Dönen Kılıç", "Ölümcül Saldırı"},
        color = {0.8, 0.4, 0.2}
    },
    {
        name = "Çift Kılıçlı",
        category = Characters.CATEGORIES.WARRIOR,
        health = 650,
        mana = 250,
        attack = 90,
        defense = 45,
        speed = 1.6,
        range = 70,
        abilities = {"Çifte Saldırı", "Hızlı Kesme", "Ölüm Dansı"},
        color = {0.6, 0.3, 0.8}
    },
    {
        name = "Balta Savaşçısı",
        category = Characters.CATEGORIES.WARRIOR,
        health = 750,
        mana = 200,
        attack = 95,
        defense = 55,
        speed = 1.1,
        range = 85,
        abilities = {"Balta Fırlatma", "Güçlü Vuruş", "Savaş Çığlığı"},
        color = {0.7, 0.5, 0.2}
    },
    {
        name = "Mızrak Savaşçısı",
        category = Characters.CATEGORIES.WARRIOR,
        health = 680,
        mana = 280,
        attack = 80,
        defense = 65,
        speed = 1.3,
        range = 120,
        abilities = {"Mızrak Atışı", "Savunma Duruşu", "Saldırı Hücumu"},
        color = {0.4, 0.6, 0.8}
    },

    -- NİŞANCILAR (MARKSMAN)
    {
        name = "Okçu",
        category = Characters.CATEGORIES.MARKSMAN,
        health = 450,
        mana = 400,
        attack = 75,
        defense = 25,
        speed = 1.2,
        range = 200,
        abilities = {"Hızlı Ok", "Çoklu Atış", "Keskin Nişan"},
        color = {0.2, 0.8, 0.4}
    },
    {
        name = "Keskin Nişancı",
        category = Characters.CATEGORIES.MARKSMAN,
        health = 400,
        mana = 350,
        attack = 90,
        defense = 20,
        speed = 1.0,
        range = 250,
        abilities = {"Uzun Mesafe", "Kritik Vuruş", "Sessiz Avcı"},
        color = {0.3, 0.7, 0.5}
    },
    {
        name = "Çapraz Yay",
        category = Characters.CATEGORIES.MARKSMAN,
        health = 480,
        mana = 380,
        attack = 70,
        defense = 30,
        speed = 1.4,
        range = 180,
        abilities = {"Çapraz Atış", "Hızlı Tekrar", "Mobil Avcı"},
        color = {0.5, 0.8, 0.3}
    },
    {
        name = "Tüfekçi",
        category = Characters.CATEGORIES.MARKSMAN,
        health = 420,
        mana = 420,
        attack = 85,
        defense = 22,
        speed = 1.1,
        range = 220,
        abilities = {"Hızlı Ateş", "Mermi Yağmuru", "Taktik Geri Çekilme"},
        color = {0.6, 0.4, 0.6}
    },

    -- DESTEKLER (SUPPORT)
    {
        name = "Şifa Büyücüsü",
        category = Characters.CATEGORIES.SUPPORT,
        health = 550,
        mana = 1000,
        attack = 40,
        defense = 40,
        speed = 1.1,
        range = 130,
        abilities = {"Şifa", "Koruyucu Kalkan", "Toplu İyileştirme"},
        color = {0.2, 1, 0.2}
    },
    {
        name = "Koruyucu",
        category = Characters.CATEGORIES.SUPPORT,
        health = 600,
        mana = 800,
        attack = 45,
        defense = 50,
        speed = 1.0,
        range = 140,
        abilities = {"Koruma Kalkanı", "Güçlendirme", "Kutsal Işık"},
        color = {1, 1, 0.8}
    },
    {
        name = "Kontrol Büyücüsü",
        category = Characters.CATEGORIES.SUPPORT,
        health = 500,
        mana = 900,
        attack = 50,
        defense = 35,
        speed = 1.2,
        range = 150,
        abilities = {"Yavaşlatma", "Köleleştirme", "Zaman Durdurma"},
        color = {0.8, 0.2, 1}
    },
    {
        name = "Taktik Uzmanı",
        category = Characters.CATEGORIES.SUPPORT,
        health = 520,
        mana = 850,
        attack = 55,
        defense = 45,
        speed = 1.3,
        range = 125,
        abilities = {"Taktik İşaret", "Grup Koordinasyonu", "Strateji Planı"},
        color = {0.4, 0.8, 1}
    },

    -- TANKLAR (TANK)
    {
        name = "Demir Dev",
        category = Characters.CATEGORIES.TANK,
        health = 1200,
        mana = 200,
        attack = 60,
        defense = 120,
        speed = 0.8,
        range = 90,
        abilities = {"Demir Yumruk", "Kalkan Duvarı", "Yıkıcı Saldırı"},
        color = {0.5, 0.5, 0.5}
    },
    {
        name = "Kaya Savaşçısı",
        category = Characters.CATEGORIES.TANK,
        health = 1100,
        mana = 250,
        attack = 65,
        defense = 110,
        speed = 0.9,
        range = 85,
        abilities = {"Kaya Fırlatma", "Sertleşme", "Deprem"},
        color = {0.6, 0.4, 0.2}
    },
    {
        name = "Zırh Savaşçısı",
        category = Characters.CATEGORIES.TANK,
        health = 1000,
        mana = 300,
        attack = 70,
        defense = 100,
        speed = 1.0,
        range = 95,
        abilities = {"Zırh Saldırısı", "Savunma Modu", "Ağır Darbe"},
        color = {0.7, 0.7, 0.8}
    },
    {
        name = "Golem",
        category = Characters.CATEGORIES.TANK,
        health = 1300,
        mana = 150,
        attack = 55,
        defense = 130,
        speed = 0.7,
        range = 80,
        abilities = {"Golem Yumruğu", "Taşlaşma", "Yıkım"},
        color = {0.3, 0.3, 0.3}
    }
}

-- Karakter sınıfı
local Character = {}
Character.__index = Character

function Character:new(data, x, y, team)
    local char = {
        name = data.name,
        category = data.category,
        health = data.health,
        maxHealth = data.health,
        mana = data.mana,
        maxMana = data.mana,
        attack = data.attack,
        defense = data.defense,
        speed = data.speed,
        range = data.range,
        abilities = data.abilities,
        color = data.color,
        x = x or 100,
        y = y or 100,
        team = team or 1, -- 1: mavi, 2: kırmızı
        targetX = x or 100,
        targetY = y or 100,
        isMoving = false,
        isAttacking = false,
        attackCooldown = 0,
        level = 1,
        experience = 0,
        gold = 0
    }
    setmetatable(char, self)
    return char
end

function Character:update(dt)
    -- Hareket güncelleme
    if self.isMoving then
        local dx = self.targetX - self.x
        local dy = self.targetY - self.y
        local distance = math.sqrt(dx * dx + dy * dy)
        
        if distance > 5 then
            local moveSpeed = 100 * self.speed
            local moveX = (dx / distance) * moveSpeed * dt
            local moveY = (dy / distance) * moveSpeed * dt
            self.x = self.x + moveX
            self.y = self.y + moveY
        else
            self.isMoving = false
        end
    end
    
    -- Saldırı cooldown güncelleme
    if self.attackCooldown > 0 then
        self.attackCooldown = self.attackCooldown - dt
    end
end

function Character:draw()
    -- Karakter çemberi
    love.graphics.setColor(self.color[1], self.color[2], self.color[3])
    love.graphics.circle("fill", self.x, self.y, 20)
    
    -- Takım rengi
    if self.team == 1 then
        love.graphics.setColor(0, 0, 1, 0.5)
    else
        love.graphics.setColor(1, 0, 0, 0.5)
    end
    love.graphics.circle("line", self.x, self.y, 25)
    
    -- Can barı
    local barWidth = 40
    local barHeight = 4
    local healthPercent = self.health / self.maxHealth
    
    love.graphics.setColor(0.2, 0.2, 0.2, 0.8)
    love.graphics.rectangle("fill", self.x - barWidth/2, self.y - 35, barWidth, barHeight)
    
    love.graphics.setColor(1 - healthPercent, healthPercent, 0)
    love.graphics.rectangle("fill", self.x - barWidth/2, self.y - 35, barWidth * healthPercent, barHeight)
    
    -- İsim
    love.graphics.setColor(1, 1, 1)
    love.graphics.print(self.name, self.x - 30, self.y - 50)
end

function Character:moveTo(x, y)
    self.targetX = x
    self.targetY = y
    self.isMoving = true
end

function Character:attack(target)
    if self.attackCooldown <= 0 then
        local damage = self.attack - target.defense * 0.5
        damage = math.max(damage, 10) -- Minimum hasar
        target.health = math.max(0, target.health - damage)
        self.attackCooldown = 1.0 -- 1 saniye cooldown
        return damage
    end
    return 0
end

function Character:isDead()
    return self.health <= 0
end

Characters.Character = Character
return Characters 