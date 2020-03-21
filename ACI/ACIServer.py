import websockets
import asyncio
import json
from ACI.database import Database


class Server:
    def __init__(self, loop, ip="localhost", port=8765):
        self.ip = ip
        self.port = port
        self.dbs = {}
        self.clients = []

        self.dbs["db1"] = Database("db1")
        self.dbs["db2"] = Database("db2")
        self.dbs["db1"].set("val", 15)

        asyncio.set_event_loop(loop)
        print("Starting Server")
        self.load_config()
        start_server = websockets.serve(self.connection_handler, self.ip, self.port)
        print("Opening Websocket Server on " + str(self.ip) + ":" + str(self.port))

        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()

    async def connection_handler(self, websocket, path):
        self.clients.append(websocket)

        print("Receiving Connection")
        while True:
            raw_cmd = await websocket.recv()
            cmd = json.loads(raw_cmd)
            response = ""

            if cmd["cmdType"] == "get_val":
                response = self.get_response_packet(cmd["key"], cmd["db_key"])
                await websocket.send(response)
            
            if cmd["cmdType"] == "set_val":
                self.dbs[cmd["db_key"]].set(cmd["key"], cmd["val"])
                response = json.dumps({"cmdType": "setResp", "msg": "Value Set."})
                await websocket.send(response)

            if cmd["cmdType"] == "wtd":
                self.write_to_disk(cmd["db_key"])

            if cmd["cmdType"] == "rfd":
                self.read_from_disk(cmd["db_key"])

            if cmd["cmdType"] == "list_databases":
                print("Database List Request")
                response = json.dumps({"cmdType":"ldResp", "msg":json.dumps(list(self.dbs[cmd["db_key"]].data.keys()))})
                await websocket.send(response)

            if response != "":
                print(response)

    def get_response_packet(self, key, db_key):
        return json.dumps({"cmdType": "getResp", "key": key, "val": self.dbs[db_key].get(key), "db_key": db_key})

    def write_to_disk(self, db_key):
        if db_key != "":
            self.dbs[db_key].write_to_disk()
        else:
            for db in self.dbs:
                self.dbs[db].write_to_disk()
    
    def read_from_disk(self, db_key):
        print("Reading Database %s from Disk" % db_key)
        self.dbs[db_key] = Database(db_key, read=True)

    def load_config(self):
        print("Reading Server.conf")
        try:
            file = open("./server.conf")
            config = json.loads(file.read())
            file.close()
            print("-Config Read Successfully")
            self.port = config["port"]
            self.ip = config["ip"]
            for db in config["dbs"]:
                self.read_from_disk(db)
        except Exception:
            print("Unable to read config. Please initialize databases manually.")
