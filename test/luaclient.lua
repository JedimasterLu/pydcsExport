local socket = require("socket")

local ip = "2.0.0.1"
local port = 8000

local c = assert(socket.connect(ip, port))
c:settimeout(0)

local last_msg = nil

print("Connected!")
while 1 do
    c:send('test')
    local s, status, partial = c:receive()
    if s ~= last_msg then
        print("Server: ",s)
        last_msg = s
    end
    if status == "closed" then
        break
    end
end
c:close()
print("Client shut down!")