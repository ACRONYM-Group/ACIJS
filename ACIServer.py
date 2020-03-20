import websockets
import threading
import asyncio
import json
import time
from database import database
from database import item

class server:
    def __init__(self, loop, ip="localhost", port=8765):
        self.ip = ip
        self.port = port
        self.dbs = {}
        self.clients = []

        self.dbs["db1"] = database()
        self.dbs["db1"].set("val", 15)

        asyncio.set_event_loop(loop)
        print("Starting Server")
        start_server = websockets.serve(self.connectionHandler, self.ip, self.port)

        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()


    async def connectionHandler(self, websocket, path):
        self.clients.append(websocket)


        print("Receiving Connection")
        while True:
            rawCmd = await websocket.recv()
            cmd = json.loads(rawCmd)
            response = ""

            if cmd["cmdType"] == "get":
                response = self.getResponsePacket(cmd["key"], cmd["dbKey"])
                await websocket.send(response)
            
            if cmd["cmdType"] == "set":
                self.dbs[cmd["dbKey"]].set(cmd["key"], cmd["val"])
                response = json.dumps({"cmdType":"setResp", "msg":"Value Set."})
                await websocket.send(response)
            if (response != ""):
                print(response)

    def getResponsePacket(self, key, database):
        return json.dumps({"cmdType":"getResp", "key":key, "val":self.dbs[database].get(key), "dbKey":database})

    