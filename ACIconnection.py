import asyncio
import threading
import websockets
import json
import time
from queue import SimpleQueue

class connection:
    def __init__(self, ip, port, loop):
        self.ip = ip
        self.port = port
        self.ws = 0
        self.responses = SimpleQueue()


        newThread = threading.Thread(target=self.create, args=(port, ip, loop, self.responses), daemon=True)
        newThread.start()


    def create(self, port, ip, loop, responses):
        print("Starting Client")
        print("---------------")
        print(" ")
        asyncio.set_event_loop(loop)
        asyncio.get_event_loop().run_until_complete(self.handler(loop, responses, ip, port))
        asyncio.get_event_loop().run_forever()


    async def handler(self, loop, responses, ip="127.0.0.1", port=8765):
        asyncio.set_event_loop(loop)
        uri = "ws://" + str(ip) + ":" + str(port)
        async with websockets.connect(uri) as websocket:
            self.ws = websocket
            while True:
                consumer_task = asyncio.ensure_future(self.recvHandler(self.ws, uri, responses))

                done, pending = await asyncio.wait(
                    [consumer_task],
                    return_when=asyncio.FIRST_COMPLETED,
                )

                for task in pending:
                    task.cancel()


    async def recvHandler(self, websocket, path, responses):

        cmd = json.loads(await websocket.recv())

        if cmd["cmdType"] == "getResp":
            value = json.dumps(["get", cmd["key"], cmd["dbKey"], cmd["val"]])
            responses.put(value)
        
        if cmd["cmdType"] == "setResp":
            value = json.dumps(["set"])
            responses.put(value)


    async def getValue(self, key, dbKey):
        await self.ws.send(json.dumps({"cmdType":"get", "key":key, "dbKey":dbKey}))
        return await self.waitForResponse("get", key, dbKey)


    async def setValue(self, key, dbKey, val):
        await self.ws.send(json.dumps({"cmdType":"set", "key":key, "dbKey":dbKey, "val": val}))


    async def waitForResponse(self, type, key, dbKey):
        hasReturned = False
        while hasReturned == False:
            if self.responses.empty() == False:
                value = self.responses.get_nowait()
                cmd = json.loads(value)
                if cmd[0] == type and cmd[1] == key and cmd[2] == dbKey:
                    hasReturned = True
                    return cmd[3]