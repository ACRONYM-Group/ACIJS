import websockets
import asyncio
import json

from database import Database


class Server:
    """
        ACI Server
    """
    def __init__(self, loop, ip="localhost", port=8765):
        self.ip = ip
        self.port = port
        self.dbs = {}
        self.clients = []

        self.dbs["db1"] = Database()
        self.dbs["db1"].set_val("val", 15)

        asyncio.set_event_loop(loop)
        print("Starting Server")
        start_server = websockets.serve(self.connection_handler, self.ip,
                                        self.port)

        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()

    async def connection_handler(self, websocket, path):
        """
            Connection Handler
        """
        self.clients.append(websocket)

        print("Receiving Connection")
        while True:
            rawCmd = await websocket.recv()
            cmd = json.loads(rawCmd)
            response = ""

            if cmd["cmdType"] == "get":
                response = self.get_responce_packet(cmd["key"], cmd["dbKey"])
                await websocket.send(response)

            if cmd["cmdType"] == "set":
                self.dbs[cmd["dbKey"]].set_val(cmd["key"], cmd["val"])
                response = json.dumps({"cmdType": "setResp",
                                       "msg": "Value Set."})
                await websocket.send(response)

            if response != "":
                print(response)

    def get_responce_packet(self, key, database):
        return json.dumps({"cmdType": "getResp", "key": key,
                           "val": self.dbs[database].get_val(key),
                           "dbKey": database})
