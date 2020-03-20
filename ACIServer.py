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

        self.dbs["db1"] = database("db1")
        self.dbs["db2"] = database("db2")
        self.dbs["db1"].set("val", 15)

        asyncio.set_event_loop(loop)
        print("Starting Server")
        self.loadConfig()
        start_server = websockets.serve(self.connectionHandler, self.ip, self.port)
        print("Opening Websocket Server on " + str(self.ip) + ":" + str(self.port))

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

            if cmd["cmdType"] == "wtd":
                self.writeToDisk(cmd["dbKey"])

            if cmd["cmdType"] == "rfd":
                self.readFromDisk(cmd["dbKey"]) 

            if cmd["cmdType"] == "listDatabase":
                print("Database List Request")
                response = json.dumps({"cmdType":"ldResp", "msg":json.dumps(list(self.dbs[cmd["dbKey"]].data.keys()))})
                await websocket.send(response)

            if (response != ""):
                print(response)

    def getResponsePacket(self, key, database):
        return json.dumps({"cmdType":"getResp", "key":key, "val":self.dbs[database].get(key), "dbKey":database})

    def writeToDisk(self, dbKey):
        if dbKey != "":
            self.dbs[dbKey].writeToDisk()
        else:
            for db in self.dbs:
                self.dbs[db].writeToDisk()
    
    def readFromDisk(self, dbKey):
        print("Reading Database " + str(dbKey) + " from Disk")
        self.dbs[dbKey] = database(dbKey, read=True)

    def loadConfig(self):
        print("Reading server.conf")
        try:
            file = open("./server.conf")
            config = json.loads(file.read())
            file.close()
            print("-Config Read Successfully")
            self.port = config["port"]
            self.ip = config["ip"]
            for db in config["dbs"]:
                self.readFromDisk(db)
        except:
            print("Unable to read config. please initilize databases manually.")

    