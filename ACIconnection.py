import asyncio
import threading
import websockets
import json
from queue import SimpleQueue


class Connection:
    """
        ACI Connection
    """
    def __init__(self, ip, port, loop):
        self.ip = ip
        self.port = port
        self.ws = 0
        self.responses = SimpleQueue()

        threading.Thread(target=self.create,
                         args=(port, ip, loop, self.responses),
                         daemon=True).start()

    def create(self, port, ip, loop, responses):
        """
            Create and start the client
        """
        print("Starting Client")
        print("---------------")
        print(" ")
        asyncio.set_event_loop(loop)
        asyncio.get_event_loop().run_until_complete(self.handler(loop,
                                                                 responses,
                                                                 ip, port))
        asyncio.get_event_loop().run_forever()

    async def handler(self, loop, responses, ip="127.0.0.1", port=8765):
        """
            Websocket Handler
        """
        asyncio.set_event_loop(loop)
        uri = "ws://" + str(ip) + ":" + str(port)
        async with websockets.connect(uri) as websocket:
            self.ws = websocket
            while True:
                consumer_task = asyncio.ensure_future(
                    self.recieve_handler(self.ws, uri, responses))

                done, pending = await asyncio.wait(
                    [consumer_task], return_when=asyncio.FIRST_COMPLETED)

                for task in pending:
                    task.cancel()

    async def recieve_handler(self, websocket, path, responses):
        """
            Recieve Handler
        """
        cmd = json.loads(await websocket.recv())

        if cmd["cmdType"] == "getResp":
            responses.put(json.dumps(["get", cmd["key"], cmd["dbKey"],
                                      cmd["val"]]))

        if cmd["cmdType"] == "setResp":
            responses.put(json.dumps(["set"]))

    async def get_value(self, key, db_key):
        await self.ws.send(json.dumps({"cmdType": "get", "key": key,
                                       "dbKey": db_key}))
        return await self.wait_for_response("get", key, db_key)

    async def set_value(self, key, db_key, val):
        await self.ws.send(json.dumps({"cmdType": "set", "key": key,
                                       "dbKey": db_key, "val": val}))

    async def wait_for_response(self, cmd_type, key, db_key):
        while True:
            if not self.responses.empty():
                value = self.responses.get_nowait()
                cmd = json.loads(value)
                if tuple(cmd[0]) == (cmd_type, key, db_key):
                    return cmd[3]
