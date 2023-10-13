local socket = require("socket")

local ip = "2.0.0.1"
local port = 8000

local c = assert(socket.connect(ip, port))
c:settimeout(0)

local last_msg = nil
local index = 0

print("Connected!")
while true do
    index = index + 1
    if index < 3 then
        c:send('tag1,tag2,tag3\njml,150,80\n')
    else
        c:send('tag1,tag2,tag3,tag4\njml,150,80,1\n')
    end
    local s, status, partial = c:receive()
    socket.sleep(1)
    print(s)
    if status == "closed" then
        c:send('quit')
        break
    end
    if index > 5 then
        c:send('quit')
        break
    end
end
c:close()
print("Client shut down!")