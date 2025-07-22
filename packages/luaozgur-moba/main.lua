-- LÖVE2D MOBA Oyunu - Lua Özgür
-- Ana oyun dosyası

local Game = require('game')
local Menu = require('menu')
local gameState = "menu" -- menu, playing, paused
local game
local menu

function love.load()
    love.window.setTitle("Lua Özgür MOBA")
    love.window.setMode(1280, 720)
    
    -- Oyun nesnelerini yükle
    game = Game:new()
    menu = Menu:new()
    
    -- Font yükle
    love.graphics.setFont(love.graphics.newFont(14))
end

function love.update(dt)
    if gameState == "menu" then
        menu:update(dt)
    elseif gameState == "playing" then
        game:update(dt)
    end
end

function love.draw()
    if gameState == "menu" then
        menu:draw()
    elseif gameState == "playing" then
        game:draw()
    end
end

function love.keypressed(key)
    if key == "escape" then
        if gameState == "playing" then
            gameState = "menu"
        elseif gameState == "menu" then
            love.event.quit()
        end
    elseif key == "return" and gameState == "menu" then
        gameState = "playing"
        game:startNewGame()
    end
end

function love.mousepressed(x, y, button)
    if gameState == "menu" then
        local result = menu:mousepressed(x, y, button)
        if result == "startGame" then
            gameState = "playing"
            game:startNewGame()
        end
    elseif gameState == "playing" then
        game:mousepressed(x, y, button)
    end
end

function love.mousemoved(x, y)
    if gameState == "playing" then
        game:mousemoved(x, y)
    end
end 