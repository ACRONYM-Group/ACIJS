import asyncio
import websockets
import json
import ACI
import time

ACI.init("server", 8765)

while True:
    time.sleep(1)