import asyncio 
import websockets

class node:
    def __init__(self, ip, port, type):
        global network
        self.connectionType = "websocket"
        self.isPublic = True
        self.ip = ip
        self.port = port
        self.nodeType = type
        asyncio.get_event_loop().run_until_complete(self.connect(self.ip))
    
    def send(self, data):
        if self.connectionType == "websocket":
            self.websocket.send(data)

    async def connect(self, ip):
        async with websockets.connect(ip) as websocket:
            self.websocket = websocket
            i = 0

    async def receive(self):
        print(await websocket.recv())
        self.receive()

