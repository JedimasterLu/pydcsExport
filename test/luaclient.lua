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
    c:send('test\n')
    local s, status, partial = c:receive()
    socket.sleep(1)
    print("Server: ",s)
    if status == "closed" then
        c:send('quit\n')
        break
    end
    if index > 5 then
        c:send('quit\n')
        break
    end
end
c:close()
print("Client shut down!")