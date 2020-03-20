import asyncio
import websockets


class Node:
    """
        ACI Node
    """
    def __init__(self, ip, port, node_type):
        self.conncetion_type = "websocket"
        self.is_public = True
        self.ip = ip
        self.port = port
        self.node_type = node_type
        asyncio.get_event_loop().run_until_complete(self.connect(self.ip))

    def send(self, data):
        if self.conncetion_type == "websocket":
            self.websocket.send(data)

    async def connect(self, ip):
        async with websockets.connect(ip) as websocket:
            self.websocket = websocket

    async def receive(self):
        print(await self.websocket.recv())
        self.receive()
