---@diagnostic disable: undefined-global

lfs = require('lfs')

lastAircraftsTable = {}
lastModelTime = 0

function LuaExportStart()
    package.path  = package.path..";"..lfs.currentdir().."/LuaSocket/?.lua"
    package.cpath = package.cpath..";"..lfs.currentdir().."/LuaSocket/?.dll"
    socket = require("socket")
    host = '2.0.0.1'
    port = 8080
    c = assert(socket.connect(host, port)) -- connect to the listener socket
    targf = 1.0 -- G-Force (normal acceleration)
    tarrrt = 0 -- Roll Rate
    taracc = 0 -- Tangential accleration
    rollInput = 0 -- roll
    pitchInput = 0 -- pitch
    throttleInput = 0 -- throttle
    framcnt = 0
    preError = {
        roll = 0,
        pitch = 0,
        throttle = 0
    }
    integral = {
        roll = 0,
        pitch = 0,
        throttle = 0
    }
end


function LuaExportStop()
    c:send("Quit\n")
    c:close()
end


function LuaExportBeforeNextFrame()

    LoSetCommand(2001,pitchInput)
    LoSetCommand(2002,rollInput)
    LoSetCommand(2004,throttleInput)

    local curdata = GetMizDataString()
    c:send(curdata)

    local s, status, partial = c:receive()
    if s ~= nil then
        s = Split(s,' ')
        for i = 1,#s do
            s[i] = tonumber(s[i])
        end
        if s[1] == nil then
            s[1] = 1.0
        end
        if s[2] == nil then
            s[2] = 0
        end
        if s[3] == nil then
            s[3] = 0
        end

        targf = s[1]
        tarrrt = s[2]
        taracc = s[3]
    end
end

function LuaExportAfterNextFrame()

    local gf = 1
    local acc = 0
    local rrt = 0
    if LoIsObjectExportAllowed() then
        gf = LoGetAccelerationUnits().y
        acc = LoGetAccelerationUnits().x
        rrt = LoGetAngularVelocity().x
    end

    local dt = 0.2

    if framcnt == math.floor(60 * dt) then
        local curError = {
            roll = tarrrt - rrt,
            pitch = targf - gf,
            throttle = taracc - acc
        }
        for index,value in pairs(integral) do
            integral[index] = value + curError[index] * dt
        end
        local derivative = {
            pitch = (curError.pitch - preError.pitch) / dt,
            roll = (curError.roll - preError.roll) / dt,
            throttle = (curError.throttle - preError.throttle) / dt
        }
        -- The parameters for PID control
        local pK = {
            p = 0.80,
            i = 0.12,
            d = -0.11
        }
        local rK = {
            p = 1.6,
            i = 0.5,
            d = -0.3
        }
        local tK = {
            p = 7,
            i = 1.3,
            d = -0.8
        }
        local output = {
            pitch = pK.p * curError.pitch + pK.i * integral.pitch + pK.d * derivative.pitch,
            roll = rK.p * curError.roll + rK.i * integral.roll + rK.d * derivative.roll,
            throttle = tK.p * curError.throttle + tK.i * integral.throttle + tK.d * derivative.throttle
        }
        pitchInput = output.pitch
        rollInput = output.roll
        throttleInput = -output.throttle
        framcnt = 0
    else
        framcnt = framcnt + 1
    end

end


function Split(str,split)
    local lcSubStrTab = {}
    while true do
        local lcPos = string.find(str,split)
        if not lcPos then
            lcSubStrTab[#lcSubStrTab+1] =  str
            break
        end
        local lcSubStr  = string.sub(str,1,lcPos-1)
        lcSubStrTab[#lcSubStrTab+1] = lcSubStr
        str = string.sub(str,lcPos+1,#str)
    end
    return lcSubStrTab
end


function GetDataString()
    local acc = LoGetAccelerationUnits()
    local rrt = LoGetAngularVelocity()
    rrt = rrt.x
    return acc.x..' '..acc.y..' '..rrt..'\n'
end


function GetMizDataString()
    -- The message that is going to be sent to the server.
    local msgstr = ""
    -- Get the objects' data into a table.
    local objectsTable = LoGetWorldObjects("units")
    if not objectsTable then
        return "Export.lua: [ERROR] unitsTable is nil"
    end
    --[[
    if not lastAircraftsTable then
        lastAircraftsTable = objectsTable
    end
    ]]--
    local modelTime = LoGetModelTime()
    local missionStartTime = LoGetMissionStartTime()
    --[[
    if lastModelTime == 0 then
        lastModelTime = modelTime
    end
    ]]--
    for index,aircraftData in pairs(objectsTable) do
        --[[
        local lastAircraftData = lastAircraftsTable[index]
        local deltatime = modelTime - lastModelTime
        local vx,vy,vz
        if deltatime == 0 then
            vx = 0
            vy = 0
            vz = 0
        else
            vx = (aircraftData.Position.x-lastAircraftData.Position.x) / deltatime
            vy = (aircraftData.Position.z-lastAircraftData.Position.z) / deltatime
            vz = (aircraftData.LatLongAlt.Alt-lastAircraftData.LatLongAlt.Alt) / deltatime
        end
        ]]--
        local name = aircraftData.Name
        local x = aircraftData.Position.x
        if not x then x = 0 end
        local y = aircraftData.Position.z
        if not y then y = 0 end
        local altitude = aircraftData.LatLongAlt.Alt
        if not altitude then altitude = 0 end
        local heading = aircraftData.Heading
        if not heading then heading = 0 end
        local pitch = aircraftData.Pitch
        if not pitch then pitch = 0 end
        local bank = aircraftData.Bank
        if not bank then bank = 0 end
        local unitName = aircraftData.UnitName
        msgstr = msgstr..name.." "..unitName.." "..x.." "..y.." "..altitude.." "..heading.." "..pitch.." "..bank.." "..vx.." "..vy.." "..vz..'\n'
    end
    lastAircraftsTable = objectsTable
    lastModelTime = modelTime
    return msgstr
end