#!/usr/bin/env lua
--[[
Hello Lua - clapp Örnek Uygulaması

Bu uygulama clapp için Lua uygulaması geliştirme örneğidir.
--]]

local function print_separator()
    print("=" .. string.rep("=", 49))
end

local function print_header()
    print_separator()
    print("🚀 Hello Lua - clapp Örnek Uygulaması")
    print_separator()
end

local function get_current_time()
    local time = os.date("*t")
    return string.format("%04d-%02d-%02d %02d:%02d:%02d", 
        time.year, time.month, time.day, time.hour, time.min, time.sec)
end

local function main()
    -- Başlık
    print_header()
    
    -- Temel bilgiler
    print("📅 Tarih: " .. get_current_time())
    print("📁 Çalışma Dizini: " .. io.popen("pwd"):read("*l"))
    
    -- Kullanıcı etkileşimi
    io.write("\n👋 Adınızı girin: ")
    local name = io.read("*l")
    
    if name and name:match("%S") then
        print("Merhaba " .. name .. "! clapp'e hoş geldiniz!")
    else
        print("Merhaba! clapp'e hoş geldiniz!")
    end
    
    -- Örnek işlemler
    print("\n🔢 Basit Hesaplama Örneği:")
    io.write("Birinci sayıyı girin: ")
    local a = tonumber(io.read("*l"))
    
    io.write("İkinci sayıyı girin: ")
    local b = tonumber(io.read("*l"))
    
    if a and b then
        print("Toplam: " .. (a + b))
        print("Çarpım: " .. (a * b))
        
        if b ~= 0 then
            print("Bölüm: " .. (a / b))
        else
            print("Bölüm: Tanımsız (sıfıra bölme)")
        end
    else
        print("❌ Geçersiz sayı girişi!")
    end
    
    -- Lua özellikleri gösterimi
    print("\n🔧 Lua Özellikleri:")
    print("Lua sürümü: " .. _VERSION)
    
    -- Tablo örneği
    local colors = {"kırmızı", "yeşil", "mavi"}
    print("Renkler: " .. table.concat(colors, ", "))
    
    -- Fonksiyon örneği
    local function factorial(n)
        if n <= 1 then
            return 1
        else
            return n * factorial(n - 1)
        end
    end
    
    print("5! = " .. factorial(5))
    
    print("\n✅ Uygulama başarıyla tamamlandı!")
    print_separator()
end

-- Ana program
local success, err = pcall(main)
if not success then
    print("❌ Hata: " .. tostring(err))
    os.exit(1)
end 